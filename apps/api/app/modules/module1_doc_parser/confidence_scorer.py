"""
module1_doc_parser/confidence_scorer.py
-----------------------------------------
Improvement 3 — Enhanced Confidence Scoring.

WHAT IT DOES:
    Combines signals from THREE sources into one final confidence score
    per paragraph, then makes a smarter LLM send/skip decision.

    Source 1: Keyword filter score       (existing)
    Source 2: Dependency parser score    (new — from dependency_parser.py)
    Source 3: BERT classifier score      (new — from bert_classifier.py)

    Final decision:
        SEND_HIGH     → definitely a rule, send to LLM with HIGH priority
        SEND_MEDIUM   → probably a rule, send to LLM
        SEND_LOW      → possibly a rule, send flagged — LLM decides
        SKIP          → not a rule, don't send → saves API cost

HOW IT IMPROVES THE PIPELINE:
    Before (keyword filter only):
        "See also Section 9.8.2" → LOW_CONFIDENCE → sent to LLM anyway
        → LLM returns empty array → wasted API call

    After (combined scoring):
        "See also Section 9.8.2" → LOW across all 3 sources → SKIP
        → never sent to LLM → API cost saved

    Upgrading in the other direction:
        "The opening dimension must accommodate egress" → keyword: MEDIUM
        → dependency: HIGH (has modal + measurement noun)
        → combined: SEND_HIGH → sent with higher priority

Usage:
    from module1_doc_parser.confidence_scorer import ConfidenceScorer
    scorer  = ConfidenceScorer()
    scored  = scorer.combine(filtered_chunks, dep_chunks, bert_chunks)
"""


# ── DECISION THRESHOLDS ───────────────────────────────────────────────────────

# Weights for each source signal
WEIGHT_KEYWORD = 0.40    # keyword filter score (normalised)
WEIGHT_DEP     = 0.35    # dependency parser confidence
WEIGHT_BERT    = 0.25    # BERT classifier probability

# Final score thresholds for send/skip decision
THRESHOLD_HIGH   = 0.70   # combined score >= 0.70 → SEND_HIGH
THRESHOLD_MEDIUM = 0.40   # combined score >= 0.40 → SEND_MEDIUM
THRESHOLD_LOW    = 0.15   # combined score >= 0.15 → SEND_LOW (flagged)
                           # combined score <  0.15 → SKIP

# Map confidence string to numeric value
CONFIDENCE_NUMERIC = {
    "HIGH":           1.0,
    "MEDIUM":         0.5,
    "LOW_CONFIDENCE": 0.1,
    "LOW":            0.1,
}


class ConfidenceScorer:
    """
    Combines keyword, dependency, and BERT signals into one
    final confidence score and send/skip decision per paragraph.
    """

    def __init__(
        self,
        weight_keyword: float = WEIGHT_KEYWORD,
        weight_dep:     float = WEIGHT_DEP,
        weight_bert:    float = WEIGHT_BERT,
    ):
        """
        Args:
            weight_keyword (float): weight for keyword filter signal
            weight_dep     (float): weight for dependency parser signal
            weight_bert    (float): weight for BERT classifier signal
        """
        # Normalise weights to sum to 1.0
        total = weight_keyword + weight_dep + weight_bert
        self.w_keyword = weight_keyword / total
        self.w_dep     = weight_dep     / total
        self.w_bert    = weight_bert    / total

    # ── PRIVATE ───────────────────────────────────────────────────────────────

    def _normalise_keyword_score(self, raw_score: int, max_score: int = 50) -> float:
        """Normalise raw keyword score (0–50+) to 0.0–1.0."""
        return min(raw_score / max_score, 1.0)

    def _combine_scores(
        self,
        keyword_score:    int,
        dep_confidence:   str,
        bert_probability: float = None,
    ) -> tuple:
        """
        Combine signals from all three sources into one final score.

        Args:
            keyword_score    (int):   raw score from KeywordFilter
            dep_confidence   (str):   HIGH/MEDIUM/LOW from DependencyParser
            bert_probability (float): 0.0–1.0 from BERTClassifier (None if not run)

        Returns:
            tuple: (combined_score: float, decision: str, breakdown: dict)
        """
        kw_norm  = self._normalise_keyword_score(keyword_score)
        dep_norm = CONFIDENCE_NUMERIC.get(dep_confidence, 0.1)

        if bert_probability is not None:
            combined = (
                self.w_keyword * kw_norm  +
                self.w_dep     * dep_norm +
                self.w_bert    * bert_probability
            )
        else:
            # BERT not available — redistribute its weight
            w_kw  = self.w_keyword / (self.w_keyword + self.w_dep)
            w_dep = self.w_dep     / (self.w_keyword + self.w_dep)
            combined = w_kw * kw_norm + w_dep * dep_norm

        # Decision
        if combined >= THRESHOLD_HIGH:
            decision = "SEND_HIGH"
        elif combined >= THRESHOLD_MEDIUM:
            decision = "SEND_MEDIUM"
        elif combined >= THRESHOLD_LOW:
            decision = "SEND_LOW"
        else:
            decision = "SKIP"

        breakdown = {
            "keyword_norm":    round(kw_norm, 3),
            "dep_norm":        round(dep_norm, 3),
            "bert_probability": round(bert_probability, 3) if bert_probability else None,
            "combined":        round(combined, 3),
        }

        return combined, decision, breakdown

    # ── PUBLIC API ────────────────────────────────────────────────────────────

    def combine(
        self,
        filtered_chunks: list,
        dep_chunks:      list = None,
        bert_chunks:     list = None,
    ) -> list:
        """
        Combine all available signals into final send/skip decisions.

        Args:
            filtered_chunks (list): from KeywordFilter.score_chunks()
            dep_chunks      (list): from DependencyParser.analyse_chunks() — optional
            bert_chunks     (list): from BERTClassifier.classify_chunks()  — optional

        Returns:
            list: chunks with final_decision and combined_score added per paragraph
        """
        # Build lookup dicts keyed by section_number + paragraph text
        dep_lookup  = {}
        bert_lookup = {}

        if dep_chunks:
            for chunk in dep_chunks:
                for para in chunk.get("scored_paragraphs", []):
                    key = (chunk["section_number"], para["text"][:80])
                    dep_lookup[key] = para.get("dep_analysis", {})

        if bert_chunks:
            for chunk in bert_chunks:
                for para in chunk.get("scored_paragraphs", []):
                    key = (chunk["section_number"], para["text"][:80])
                    bert_lookup[key] = para.get("bert_probability", None)

        print("[ConfidenceScorer] Combining signals...\n")

        combined_chunks = []
        stats = {"SEND_HIGH": 0, "SEND_MEDIUM": 0, "SEND_LOW": 0, "SKIP": 0}

        for chunk in filtered_chunks:
            enhanced_paras = []
            send_parts     = []

            for para in chunk.get("scored_paragraphs", []):
                key = (chunk["section_number"], para["text"][:80])

                # Get dep confidence
                dep_info       = dep_lookup.get(key, {})
                dep_confidence = dep_info.get("dep_confidence", para.get("confidence", "LOW"))

                # Get BERT probability
                bert_prob = bert_lookup.get(key, None)

                # Combine
                combined_score, decision, breakdown = self._combine_scores(
                    keyword_score    = para.get("score", 0),
                    dep_confidence   = dep_confidence,
                    bert_probability = bert_prob,
                )

                stats[decision] = stats.get(decision, 0) + 1

                enhanced_paras.append({
                    **para,
                    "final_decision":  decision,
                    "combined_score":  combined_score,
                    "score_breakdown": breakdown,
                })

                # Build filtered text based on final decision
                if decision == "SKIP":
                    continue   # do not send to LLM
                elif decision == "SEND_LOW":
                    send_parts.append(f"[LOW_CONFIDENCE] {para['text']}")
                else:
                    send_parts.append(para["text"])

            combined_chunks.append({
                **chunk,
                "scored_paragraphs": enhanced_paras,
                "filtered_text":     "\n\n".join(send_parts),
                "count_skip":        sum(1 for p in enhanced_paras if p["final_decision"] == "SKIP"),
                "count_send":        sum(1 for p in enhanced_paras if p["final_decision"] != "SKIP"),
            })

        # Summary
        total = sum(stats.values())
        print(f"  {'Decision':<15} {'Count':>6}  {'%':>6}")
        print(f"  {'-'*30}")
        for decision, count in stats.items():
            pct = f"{100*count/total:.1f}%" if total else "0%"
            print(f"  {decision:<15} {count:>6}  {pct:>6}")
        print(f"\n  SKIP saves ~{stats.get('SKIP',0)} LLM calls vs keyword-only filter")

        return combined_chunks

    def get_stats(self, combined_chunks: list) -> dict:
        """
        Return statistics on send/skip decisions across all chunks.

        Args:
            combined_chunks (list): output from combine()

        Returns:
            dict: {SEND_HIGH, SEND_MEDIUM, SEND_LOW, SKIP, total}
        """
        stats = {"SEND_HIGH": 0, "SEND_MEDIUM": 0, "SEND_LOW": 0, "SKIP": 0}
        for chunk in combined_chunks:
            for para in chunk.get("scored_paragraphs", []):
                decision = para.get("final_decision", "SKIP")
                stats[decision] = stats.get(decision, 0) + 1
        stats["total"] = sum(stats.values())
        return stats
