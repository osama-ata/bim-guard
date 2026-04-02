"""
tests/eval_harness.py
----------------------
LLM-as-Judge evaluation harness for Module 3 rule generation accuracy.

This is NOT a pass/fail test — it produces an accuracy SCORE you track over time.

Usage:
  python -m tests.eval_harness                    # run all eval cases
  python -m tests.eval_harness --case stair_width # run one case
  python -m tests.eval_harness --report           # show historical scores

Requirements:
  pip install openai  (or use anthropic SDK — see LLM_PROVIDER below)

The harness:
  1. Feeds golden text through Module 3
  2. Asks a judge LLM to score each generated rule on 3 dimensions
  3. Saves scored results to tests/eval_results/
  4. Prints a summary table
"""

import os
import sys
import json
import argparse
from datetime import datetime

# ── Configure your LLM provider here ──────────────────────────────────────────
# Option A: Anthropic (recommended — same model family as your pipeline)
# Option B: OpenAI
#
# Set LLM_PROVIDER to "anthropic" or "openai"

LLM_PROVIDER = "anthropic"  # change to "openai" if you prefer

# ══════════════════════════════════════════════════════════════════════════════
# Golden evaluation cases
# ══════════════════════════════════════════════════════════════════════════════
#
# Each case: source text + the "ideal" rule a human expert would write.
# The judge scores how close Module 3's output is to this ideal.

EVAL_CASES = [
    {
        "id": "stair_width",
        "source_text": "Every exit stair shall have a clear width of not less than 860 mm.",
        "ideal_rule": {
            "element":  "stair",
            "property": "clear_width",
            "operator": ">=",
            "value":    860,
            "unit":     "mm",
            "source":   "OBC 9.8.2.1",
        },
    },
    {
        "id": "riser_height",
        "source_text": "The riser height shall not be more than 200 mm.",
        "ideal_rule": {
            "element":  "stair",
            "property": "riser_height",
            "operator": "<=",
            "value":    200,
            "unit":     "mm",
        },
    },
    {
        "id": "tread_run",
        "source_text": "The tread run shall not be less than 255 mm.",
        "ideal_rule": {
            "element":  "stair",
            "property": "tread_run",
            "operator": ">=",
            "value":    255,
            "unit":     "mm",
        },
    },
    {
        "id": "guard_height",
        "source_text": "Guards shall not be less than 900 mm in height measured vertically.",
        "ideal_rule": {
            "element":  "guard",
            "property": "height",
            "operator": ">=",
            "value":    900,
            "unit":     "mm",
        },
    },
    {
        "id": "door_width",
        "source_text": "Every doorway in a means of egress shall have a clear width of not less than 810 mm.",
        "ideal_rule": {
            "element":  "door",
            "property": "clear_width",
            "operator": ">=",
            "value":    810,
            "unit":     "mm",
        },
    },
    {
        "id": "window_egress",
        "source_text": (
            "Each window providing emergency egress shall have an unobstructed "
            "opening of not less than 0.35 m2 with no dimension less than 380 mm."
        ),
        "ideal_rule": {
            "element":  "window",
            "property": "opening_area",
            "operator": ">=",
            "value":    0.35,
            "unit":     "m2",
        },
    },
    {
        "id": "handrail_height_range",
        "source_text": "Handrails shall be between 865 mm and 965 mm in height.",
        "ideal_rule": {
            "element":    "handrail",
            "property":   "height",
            "operator":   "between",
            "value_min":  865,
            "value_max":  965,
            "unit":       "mm",
        },
    },
    {
        "id": "ambiguous_ventilation",
        "source_text": "Adequate ventilation shall be provided in all occupied spaces.",
        "ideal_rule": {
            "element":      "space",
            "property":     "ventilation",
            "needs_review": True,
            "note":         "No numeric threshold specified in source text",
        },
    },
]


# ══════════════════════════════════════════════════════════════════════════════
# Judge prompt
# ══════════════════════════════════════════════════════════════════════════════

JUDGE_PROMPT = """You are an expert evaluator for a BIM compliance rule extraction system.

Given:
- SOURCE TEXT: A building code requirement
- IDEAL RULE: What a human expert would produce
- GENERATED RULE: What the AI system actually produced

Score the GENERATED RULE on three dimensions (1-5 each):

1. CORRECTNESS: Does the rule capture the right element, property, operator, and value?
   5 = perfect match  |  4 = minor naming difference  |  3 = mostly right, one field wrong
   2 = significant errors  |  1 = completely wrong or unrelated

2. COMPLETENESS: Does the rule capture ALL requirements from the source text?
   5 = everything captured  |  4 = minor detail missing (e.g., unit)
   3 = main requirement captured, secondary missed  |  2 = half missing  |  1 = mostly missing

3. EXECUTABILITY: Could Module 4 (Comparator) use this rule to check an IFC model?
   5 = directly usable, clear operator and value  |  4 = usable with minor cleanup
   3 = needs interpretation  |  2 = too vague to automate  |  1 = not machine-readable

Respond ONLY with a JSON object (no markdown, no explanation):
{
  "correctness": <1-5>,
  "completeness": <1-5>,
  "executability": <1-5>,
  "issues": "<brief note on any problems, or 'none'>"
}
"""


def build_judge_message(source_text, ideal_rule, generated_rule):
    return (
        f"SOURCE TEXT:\n{source_text}\n\n"
        f"IDEAL RULE:\n{json.dumps(ideal_rule, indent=2)}\n\n"
        f"GENERATED RULE:\n{json.dumps(generated_rule, indent=2)}"
    )


# ══════════════════════════════════════════════════════════════════════════════
# LLM Judge call
# ══════════════════════════════════════════════════════════════════════════════

def call_judge_anthropic(message):
    """Call Anthropic Claude as the judge."""
    try:
        from anthropic import Anthropic
    except ImportError:
        print("ERROR: pip install anthropic")
        sys.exit(1)

    client   = Anthropic()
    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=300,
        system=JUDGE_PROMPT,
        messages=[{"role": "user", "content": message}],
    )
    return response.content[0].text


def call_judge_openai(message):
    """Call OpenAI GPT-4 as the judge."""
    try:
        from openai import OpenAI
    except ImportError:
        print("ERROR: pip install openai")
        sys.exit(1)

    client   = OpenAI()
    response = client.chat.completions.create(
        model="gpt-4o",
        max_tokens=300,
        messages=[
            {"role": "system", "content": JUDGE_PROMPT},
            {"role": "user",   "content": message},
        ],
    )
    return response.choices[0].message.content


def call_judge(message):
    if LLM_PROVIDER == "anthropic":
        return call_judge_anthropic(message)
    elif LLM_PROVIDER == "openai":
        return call_judge_openai(message)
    else:
        raise ValueError(f"Unknown LLM_PROVIDER: {LLM_PROVIDER}")


def parse_judge_response(raw):
    """Parse the judge's JSON response, handling markdown fences."""
    cleaned = raw.strip()
    if cleaned.startswith("```"):
        cleaned = cleaned.split("\n", 1)[1]  # remove first line
    if cleaned.endswith("```"):
        cleaned = cleaned.rsplit("```", 1)[0]
    cleaned = cleaned.replace("```json", "").replace("```", "").strip()
    return json.loads(cleaned)


# ══════════════════════════════════════════════════════════════════════════════
# Module 3 runner
# ══════════════════════════════════════════════════════════════════════════════

def generate_rule_from_text(text):
    """Run Module 3 on a text chunk and return the first generated rule."""
    from module3_rule_builder.rule_store     import RuleStore
    from module3_rule_builder.rule_generator import RuleGenerator

    db_path = "tests/test_rules_eval_temp.db"
    store   = RuleStore(db_path)
    store.clear_all_rules()
    gen = RuleGenerator(store)

    try:
        rules = gen.generate_rules(text)
        if not rules:
            return None
        rule = rules[0]
        return rule if isinstance(rule, dict) else json.loads(rule)
    finally:
        store.close()
        if os.path.exists(db_path):
            os.remove(db_path)


# ══════════════════════════════════════════════════════════════════════════════
# Main evaluation loop
# ══════════════════════════════════════════════════════════════════════════════

RESULTS_DIR = os.path.join(os.path.dirname(__file__), "eval_results")


def run_evaluation(cases=None):
    """Run eval on specified cases (or all). Returns results list."""
    os.makedirs(RESULTS_DIR, exist_ok=True)

    if cases is None:
        cases = EVAL_CASES

    results = []
    for case in cases:
        print(f"\n{'='*60}")
        print(f"  Evaluating: {case['id']}")
        print(f"{'='*60}")
        print(f"  Source: {case['source_text'][:70]}...")

        # Generate rule using Module 3
        generated = generate_rule_from_text(case["source_text"])

        if generated is None:
            print("  ❌ Module 3 returned no rules!")
            results.append({
                "id":            case["id"],
                "generated":     None,
                "correctness":   0,
                "completeness":  0,
                "executability": 0,
                "issues":        "No rules generated",
            })
            continue

        print(f"  Generated: {json.dumps(generated, indent=2)}")

        # Judge the generated rule
        judge_msg = build_judge_message(
            case["source_text"], case["ideal_rule"], generated
        )
        try:
            raw_verdict = call_judge(judge_msg)
            verdict     = parse_judge_response(raw_verdict)
        except Exception as e:
            print(f"  ⚠️  Judge error: {e}")
            verdict = {
                "correctness": -1, "completeness": -1,
                "executability": -1, "issues": str(e),
            }

        print(f"  Scores — C:{verdict['correctness']}  "
              f"Co:{verdict['completeness']}  E:{verdict['executability']}")
        if verdict.get("issues", "none") != "none":
            print(f"  Issues: {verdict['issues']}")

        results.append({
            "id":            case["id"],
            "generated":     generated,
            "correctness":   verdict["correctness"],
            "completeness":  verdict["completeness"],
            "executability": verdict["executability"],
            "issues":        verdict.get("issues", ""),
        })

    return results


def print_summary(results):
    """Print a summary table of evaluation results."""
    print(f"\n\n{'='*70}")
    print("  EVALUATION SUMMARY")
    print(f"{'='*70}")
    print(f"  {'Case':<25} {'Correct':>8} {'Complete':>9} {'Exec':>6} {'Issues'}")
    print(f"  {'-'*25} {'-'*8} {'-'*9} {'-'*6} {'-'*20}")

    totals = {"correctness": 0, "completeness": 0, "executability": 0}
    valid  = 0

    for r in results:
        c, co, e = r["correctness"], r["completeness"], r["executability"]
        flag     = r["issues"][:20] if r["issues"] and r["issues"] != "none" else ""
        print(f"  {r['id']:<25} {c:>8} {co:>9} {e:>6} {flag}")

        if c >= 0:
            totals["correctness"]   += c
            totals["completeness"]  += co
            totals["executability"] += e
            valid += 1

    if valid > 0:
        avg_c  = totals["correctness"]   / valid
        avg_co = totals["completeness"]  / valid
        avg_e  = totals["executability"] / valid
        overall = (avg_c + avg_co + avg_e) / 3

        print(f"  {'-'*25} {'-'*8} {'-'*9} {'-'*6}")
        print(f"  {'AVERAGE':<25} {avg_c:>8.1f} {avg_co:>9.1f} {avg_e:>6.1f}")
        print(f"\n  OVERALL ACCURACY SCORE: {overall:.1f} / 5.0  ({overall/5*100:.0f}%)")
    else:
        print("  No valid results to summarize.")

    return totals, valid


def save_results(results):
    """Save timestamped results for historical comparison."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    path      = os.path.join(RESULTS_DIR, f"eval_{timestamp}.json")

    payload = {
        "timestamp": timestamp,
        "provider":  LLM_PROVIDER,
        "results":   results,
    }
    with open(path, "w") as f:
        json.dump(payload, f, indent=2)
    print(f"\n  Results saved to: {path}")
    return path


def show_history():
    """Show historical evaluation scores."""
    if not os.path.exists(RESULTS_DIR):
        print("No evaluation history found.")
        return

    files = sorted(f for f in os.listdir(RESULTS_DIR) if f.startswith("eval_"))
    if not files:
        print("No evaluation history found.")
        return

    print(f"\n{'='*60}")
    print("  EVALUATION HISTORY")
    print(f"{'='*60}")
    print(f"  {'Date':<20} {'Correct':>8} {'Complete':>9} {'Exec':>6} {'Overall':>8}")
    print(f"  {'-'*20} {'-'*8} {'-'*9} {'-'*6} {'-'*8}")

    for fname in files:
        with open(os.path.join(RESULTS_DIR, fname)) as f:
            data = json.load(f)

        results = data["results"]
        valid   = [r for r in results if r["correctness"] >= 0]
        if not valid:
            continue

        avg_c  = sum(r["correctness"]   for r in valid) / len(valid)
        avg_co = sum(r["completeness"]  for r in valid) / len(valid)
        avg_e  = sum(r["executability"] for r in valid) / len(valid)
        overall = (avg_c + avg_co + avg_e) / 3

        ts = data.get("timestamp", fname.replace("eval_", "").replace(".json", ""))
        print(f"  {ts:<20} {avg_c:>8.1f} {avg_co:>9.1f} {avg_e:>6.1f} {overall:>8.1f}")


# ══════════════════════════════════════════════════════════════════════════════
# CLI entrypoint
# ══════════════════════════════════════════════════════════════════════════════

def main():
    parser = argparse.ArgumentParser(description="BIMGuard Module 3 Eval Harness")
    parser.add_argument("--case",    help="Run a specific case by ID")
    parser.add_argument("--report",  action="store_true", help="Show historical scores")
    args = parser.parse_args()

    if args.report:
        show_history()
        return

    if args.case:
        cases = [c for c in EVAL_CASES if c["id"] == args.case]
        if not cases:
            print(f"Unknown case: {args.case}")
            print(f"Available: {[c['id'] for c in EVAL_CASES]}")
            sys.exit(1)
    else:
        cases = None

    results = run_evaluation(cases)
    print_summary(results)
    save_results(results)


if __name__ == "__main__":
    main()
