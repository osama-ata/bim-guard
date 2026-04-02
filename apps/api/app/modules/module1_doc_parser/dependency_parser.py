"""
module1_doc_parser/dependency_parser.py
-----------------------------------------
Improvement 2 — spaCy Dependency Parsing.

WHAT IT DOES:
    Catches obligation sentences that contain NO keywords at all.
    Instead of looking for specific words, it looks at sentence
    grammar structure — whether the sentence is shaped like an obligation.

    Example keyword filter misses:
        "The dimension is to be no smaller than 860mm"
        → no "shall", no "must", but clearly an obligation

    Dependency parser catches it by detecting:
        modal/obligation verb + measurement noun + numeric value

HOW spaCy DEPENDENCY PARSING WORKS:
    spaCy maps every word's grammatical relationship to other words.

    "The exit stair shall have a clear width of not less than 860 mm"
         ↓
    subject:  stair
    aux:      shall         ← modal = obligation signal
    root:     have
    obj:      width         ← measurement noun = property signal
    nummod:   860           ← number = value signal
    unit:     mm            ← unit signal

    If a sentence has: modal_verb + measurement_noun + number
    → it is almost certainly a compliance rule.

PATTERNS DETECTED:
    1. Modal obligation    — shall/must/should + verb
    2. Measurement phrase  — width/height/area/clearance + number + unit
    3. Comparative phrase  — not less than / not more than + number
    4. Existence check     — shall/must + be + provided/installed/included

Usage:
    from module1_doc_parser.dependency_parser import DependencyParser
    dp      = DependencyParser()
    results = dp.analyse_chunks(filtered_chunks)
"""

import re


# ── SIGNAL WORD SETS ──────────────────────────────────────────────────────────

MODAL_VERBS = {
    "shall", "must", "should", "will", "may", "need",
    "require", "required", "requires",
}

OBLIGATION_PATTERNS = [
    # Direct modal
    r"\b(shall|must|should)\b.{0,80}(width|height|depth|area|clearance|slope|rise|run|tread|distance|opening|rating|separation)",
    # Passive obligation
    r"\b(is required|are required|is to be|are to be)\b",
    # Comparative measurement
    r"\bnot (less|more|smaller|greater|lower|higher) than\b.{0,30}\d",
    # Numeric dimension with unit
    r"\b\d{2,4}\s*(mm|m2|m²|metres?|meters?|degrees?|kpa)\b",
    # Minimum/maximum with value
    r"\b(minimum|maximum|min|max)[\s\.:]+\d",
    # Shall not exceed
    r"\bshall not exceed\b.{0,30}\d",
    # Between range
    r"\bbetween\b.{0,30}\d.{0,20}and.{0,20}\d",
]

MEASUREMENT_NOUNS = {
    "width", "height", "depth", "length", "area", "clearance",
    "opening", "slope", "rise", "run", "tread", "riser", "nosing",
    "distance", "separation", "rating", "headroom", "dimension",
    "thickness", "size", "capacity", "load",
}

UNIT_TOKENS = {"mm", "m2", "m²", "metres", "meters", "m", "degrees", "kpa", "mpa"}

# Pre-compiled patterns for speed
COMPILED_PATTERNS = [re.compile(p, re.IGNORECASE) for p in OBLIGATION_PATTERNS]


class DependencyParser:
    """
    Uses spaCy dependency parsing to detect obligation sentences
    that the keyword filter may have missed.
    """

    def __init__(self):
        try:
            import spacy
            # Use full pipeline for dependency parsing (not just en_core_web_sm)
            try:
                self.nlp = spacy.load("en_core_web_md")
                print("[DependencyParser] Loaded en_core_web_md")
            except OSError:
                self.nlp = spacy.load("en_core_web_sm")
                print("[DependencyParser] Loaded en_core_web_sm (md preferred)")
        except ImportError:
            raise ImportError("Run: pip install spacy")
        except OSError:
            raise OSError("Run: python -m spacy download en_core_web_sm")

    # ── PRIVATE ───────────────────────────────────────────────────────────────

    def _has_modal_obligation(self, doc) -> bool:
        """
        Check if the spaCy doc contains a modal verb indicating obligation.
        Detects: shall, must, should + any verb
        """
        for token in doc:
            if token.lemma_.lower() in MODAL_VERBS and token.pos_ in ("AUX", "VERB"):
                return True
        return False

    def _has_measurement_with_value(self, doc) -> bool:
        """
        Check if the doc contains a measurement noun near a numeric value.
        Detects: "clear width of 860mm", "height not less than 900mm"
        """
        tokens_lower = [t.text.lower() for t in doc]

        # Check for measurement noun
        has_measurement = any(t in MEASUREMENT_NOUNS for t in tokens_lower)

        # Check for numeric value
        has_number = any(t.like_num or t.text.replace(".", "").isdigit() for t in doc)

        return has_measurement and has_number

    def _has_unit(self, doc) -> bool:
        """Check if the doc contains a measurement unit."""
        tokens_lower = [t.text.lower() for t in doc]
        return any(t in UNIT_TOKENS for t in tokens_lower)

    def _regex_signals(self, text: str) -> list:
        """
        Run all compiled regex patterns against the text.
        Returns list of matched pattern names.
        """
        matched = []
        for i, pattern in enumerate(COMPILED_PATTERNS):
            if pattern.search(text):
                matched.append(OBLIGATION_PATTERNS[i][:40])
        return matched

    def _analyse_sentence(self, sentence_text: str) -> dict:
        """
        Analyse one sentence for obligation signals using both
        spaCy dependency parsing and regex patterns.

        Returns:
            dict with:
                is_obligation  (bool)
                confidence     (str): HIGH / MEDIUM / LOW
                signals        (list): what triggered the detection
                sentence       (str)
        """
        doc     = self.nlp(sentence_text)
        signals = []

        # spaCy signals
        if self._has_modal_obligation(doc):
            signals.append("modal_obligation")
        if self._has_measurement_with_value(doc):
            signals.append("measurement_with_value")
        if self._has_unit(doc):
            signals.append("unit_present")

        # Regex signals
        regex_hits = self._regex_signals(sentence_text)
        signals.extend([f"regex:{r[:25]}" for r in regex_hits])

        # Scoring
        score = (
            3 * ("modal_obligation"       in signals) +
            3 * ("measurement_with_value" in signals) +
            2 * ("unit_present"           in signals) +
            1 * len(regex_hits)
        )

        if score >= 5:   confidence = "HIGH"
        elif score >= 2: confidence = "MEDIUM"
        else:            confidence = "LOW"

        return {
            "is_obligation": score >= 2,
            "confidence":    confidence,
            "signals":       signals,
            "score":         score,
            "sentence":      sentence_text.strip(),
        }

    # ── PUBLIC API ────────────────────────────────────────────────────────────

    def analyse_paragraph(self, paragraph: str) -> dict:
        """
        Analyse one paragraph for obligation sentences.

        Args:
            paragraph (str): one paragraph of OBC text

        Returns:
            dict:
                is_rule           (bool)
                obligation_score  (int)   max sentence score in paragraph
                obligation_sents  (list)  sentences flagged as obligations
                dep_confidence    (str)   HIGH/MEDIUM/LOW
        """
        doc       = self.nlp(paragraph)
        sentences = [sent.text for sent in doc.sents]

        best_score    = 0
        obligation_sents = []

        for sent in sentences:
            result = self._analyse_sentence(sent)
            if result["is_obligation"]:
                obligation_sents.append(result)
                best_score = max(best_score, result["score"])

        if best_score >= 5:   dep_confidence = "HIGH"
        elif best_score >= 2: dep_confidence = "MEDIUM"
        else:                 dep_confidence = "LOW"

        return {
            "is_rule":          len(obligation_sents) > 0,
            "obligation_score": best_score,
            "obligation_sents": obligation_sents,
            "dep_confidence":   dep_confidence,
        }

    def analyse_chunks(self, filtered_chunks: list) -> list:
        """
        Run dependency analysis across all scored chunks.
        Upgrades paragraphs that the keyword filter marked LOW_CONFIDENCE
        but the dependency parser identifies as obligations.

        Args:
            filtered_chunks (list): output from KeywordFilter.score_chunks()

        Returns:
            list: same chunks with dep_analysis added to each paragraph,
                  and LOW_CONFIDENCE paragraphs upgraded where appropriate
        """
        print("[DependencyParser] Analysing sentence structure...\n")

        upgraded_total = 0
        enhanced       = []

        for chunk in filtered_chunks:
            enhanced_paragraphs = []

            for para in chunk.get("scored_paragraphs", []):
                dep_result = self.analyse_paragraph(para["text"])

                # Upgrade LOW_CONFIDENCE if dependency parser is confident
                original_confidence = para["confidence"]
                new_confidence      = original_confidence

                if (original_confidence == "LOW_CONFIDENCE"
                        and dep_result["dep_confidence"] in ("HIGH", "MEDIUM")):
                    new_confidence = dep_result["dep_confidence"]
                    upgraded_total += 1

                enhanced_paragraphs.append({
                    **para,
                    "confidence":    new_confidence,
                    "dep_analysis":  dep_result,
                    "was_upgraded":  new_confidence != original_confidence,
                })

            # Rebuild filtered_text with updated confidence labels
            parts = []
            for p in enhanced_paragraphs:
                if p["confidence"] == "LOW_CONFIDENCE":
                    parts.append(f"[LOW_CONFIDENCE] {p['text']}")
                else:
                    parts.append(p["text"])

            # Recount confidence levels
            count_high   = sum(1 for p in enhanced_paragraphs if p["confidence"] == "HIGH")
            count_medium = sum(1 for p in enhanced_paragraphs if p["confidence"] == "MEDIUM")
            count_low    = sum(1 for p in enhanced_paragraphs if p["confidence"] == "LOW_CONFIDENCE")

            enhanced.append({
                **chunk,
                "scored_paragraphs": enhanced_paragraphs,
                "filtered_text":     "\n\n".join(parts),
                "count_high":        count_high,
                "count_medium":      count_medium,
                "count_low":         count_low,
            })

        print(f"[DependencyParser] Done")
        print(f"  Paragraphs upgraded from LOW → MEDIUM/HIGH: {upgraded_total}")
        return enhanced
