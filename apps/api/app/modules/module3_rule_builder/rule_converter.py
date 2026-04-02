"""
module3_rule_builder/rule_converter.py
----------------------------------------
NLP Engine — sends scored text chunks to GPT-4o and returns structured rules.
Uses RAG (Retrieval Augmented Generation) to ground the LLM output
in your existing rules.db schema — reducing hallucinations.

Responsibilities:
    - Build a guided system prompt using existing DB rules as examples
    - Send filtered section text to GPT-4o
    - Parse and return structured rule dicts
    - Handle JSON parse errors gracefully

Usage:
    from module3_rule_builder.rule_converter import RuleConverter
    from module3_rule_builder.rule_store import RuleStore
    from config import DB_PATH, OPENAI_API_KEY

    store     = RuleStore(DB_PATH)
    converter = RuleConverter(api_key=OPENAI_API_KEY, rule_store=store)
    rules     = converter.extract_rules(chunk)
"""

import json
import openai
from config import OPENAI_API_KEY, OPENAI_MODEL


# ── SYSTEM PROMPT ─────────────────────────────────────────────────────────────
# RAG-guided: includes existing entity types and real example rules
# so the LLM always outputs your exact schema — not a guessed version.

RAG_SYSTEM_PROMPT = """\
You are a BIM compliance rule extraction engine for the Ontario Building Code (OBC) Part 9.

Extract every discrete checkable requirement as a JSON rule object.

SCHEMA — every rule must have ALL these fields:
{{
  "section_ref":   "OBC section number e.g. 9.8.2.1.(2)",
  "rule_type":     "json_check" | "range_check" | "regex" | "exists_check",
  "entity_type":   "IfcStairFlight" | "IfcDoor" | "IfcWindow" | "IfcSpace" | "IfcWall" | "IfcRailing" | "IfcSlab" | "IfcRamp" | "IfcZone" | "IfcColumn" | "IfcFooting",
  "property_name": "exact IFC property name",
  "operator":      ">=" | "<=" | "==" | "!=" | "between" | "regex_match" | "exists",
  "value":         number | string | [min, max] for between | null for exists,
  "unit":          "mm" | "m" | "m2" | "deg" | "ratio" | null,
  "priority":      1 if critical, 0 otherwise,
  "description":   "plain English explanation of what is being checked"
}}

OUTPUT RULES:
- Output ONLY a valid JSON array. No markdown. No prose. No code fences.
- For min AND max requirements use operator "between" and value [min, max].
- Skip requirements that cannot be expressed as a discrete checkable rule.
- Paragraphs marked [LOW_CONFIDENCE] may or may not contain rules — extract carefully.
- Do NOT duplicate rules for these already-known entity types: {existing_entities}

EXAMPLE RULES FROM DATABASE (match this format exactly):
{rag_examples}

CURRENT SECTION BEING PROCESSED: {section_name}
PARAGRAPH CONFIDENCE BREAKDOWN: {high} HIGH | {medium} MEDIUM | {low} LOW_CONFIDENCE\
"""


class RuleConverter:
    """
    Sends filtered section chunks to GPT-4o and returns structured rule dicts.
    RAG-guided: pulls existing rules from DB as few-shot examples per call.
    """

    def __init__(self, api_key: str = None, rule_store=None, model: str = None):
        """
        Args:
            api_key    (str):       OpenAI API key (defaults to config.OPENAI_API_KEY)
            rule_store (RuleStore): RuleStore instance for RAG example retrieval
            model      (str):       OpenAI model name (defaults to config.OPENAI_MODEL)
        """
        self.client     = openai.OpenAI(api_key=api_key or OPENAI_API_KEY)
        self.store      = rule_store
        self.model      = model or OPENAI_MODEL

    # ── PRIVATE ───────────────────────────────────────────────────────────────

    def _build_system_prompt(self, chunk: dict) -> str:
        """
        Build a RAG-guided system prompt for this specific section chunk.
        Retrieves existing entity types and example rules from the DB
        so the LLM never guesses the schema.

        Args:
            chunk (dict): scored section chunk from keyword_filter.py

        Returns:
            str: formatted system prompt
        """
        existing_entities = []
        rag_examples      = []

        if self.store:
            existing_entities = self.store.get_existing_entity_types()
            rag_examples      = self.store.get_rules_sample(limit=3)

        return RAG_SYSTEM_PROMPT.format(
            existing_entities = ", ".join(existing_entities) if existing_entities else "None yet",
            rag_examples      = json.dumps(rag_examples, indent=2) if rag_examples else "None yet",
            section_name      = chunk.get("section_name", "Unknown"),
            high              = chunk.get("count_high", 0),
            medium            = chunk.get("count_medium", 0),
            low               = chunk.get("count_low", 0),
        )

    def _parse_response(self, raw: str, section_number: str) -> list:
        """
        Parse the LLM response string into a list of rule dicts.
        Strips markdown code fences if the LLM added them.

        Args:
            raw            (str): raw LLM response text
            section_number (str): section number for error logging

        Returns:
            list[dict]: list of rule dicts, or [] on parse error
        """
        # Strip markdown code fences if LLM added them despite instructions
        if raw.startswith("```"):
            raw = raw.split("```")[1]
            if raw.startswith("json"):
                raw = raw[4:]
        raw = raw.strip()

        try:
            return json.loads(raw)
        except json.JSONDecodeError as e:
            print(f"  [RuleConverter] JSON parse error for section {section_number}: {e}")
            print(f"  Raw response preview: {raw[:300]}")
            return []

    # ── PUBLIC API ────────────────────────────────────────────────────────────

    def extract_rules(self, chunk: dict) -> list:
        """
        Send one scored section chunk to GPT-4o and return rule dicts.

        Args:
            chunk (dict): scored section chunk from keyword_filter.py
                          Must have keys: filtered_text, section_name,
                          section_number, count_high, count_medium, count_low

        Returns:
            list[dict]: raw rule dicts ready for RuleGenerator.save_batch()
        """
        text = chunk.get("filtered_text", "")

        # Skip sections with too little content after filtering
        if not text or len(text.strip()) < 50:
            section = chunk.get("section_number", "?")
            print(f"  [RuleConverter] Skipping Section {section} — too little text after filtering")
            return []

        system_prompt = self._build_system_prompt(chunk)

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user",   "content": f"Extract all rules from this OBC section:\n\n{text}"},
            ],
            temperature=0.1,   # low temperature = more deterministic, less hallucination
        )

        raw   = response.choices[0].message.content.strip()
        rules = self._parse_response(raw, chunk.get("section_number", "?"))

        # Tag each rule with its source section
        for rule in rules:
            rule["obc_section_number"] = chunk.get("section_number")
            rule["obc_section_name"]   = chunk.get("section_name")

        return rules
