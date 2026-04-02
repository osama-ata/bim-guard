"""
module1_doc_parser/tfidf_analyzer.py
--------------------------------------
Improvement 1 — TF-IDF Auto Keyword Discovery.

WHAT IT DOES:
    Instead of manually guessing which keywords are missing,
    this runs TF-IDF across the entire OBC text and surfaces
    which words are most distinctive in rule-dense paragraphs
    vs non-rule paragraphs.

    Result: a ranked list of words you should add to keyword_master.py
    — discovered from the actual OBC text, not guesswork.

HOW IT WORKS:
    1. Scores every paragraph with the existing keyword list
    2. Labels paragraphs as rule-likely (HIGH/MEDIUM) vs not (LOW)
    3. Runs TF-IDF comparing rule paragraphs vs non-rule paragraphs
    4. Words that appear more in rule paragraphs = candidate keywords
    5. Filters out words already in your keyword list
    6. Returns ranked list of NEW keywords to consider adding

RUN DIRECTLY to analyse your OBC text:
    python -m module1_doc_parser.tfidf_analyzer

OR import and call:
    from module1_doc_parser.tfidf_analyzer import TFIDFAnalyzer
    analyzer = TFIDFAnalyzer()
    new_keywords = analyzer.discover(filtered_chunks)
    analyzer.print_report(new_keywords)
"""

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import LabelEncoder
import numpy as np
import re

from module1_doc_parser.keywords.keyword_master import ALL_KEYWORDS


# Words to always ignore — structural words with no compliance value
STOP_WORDS = {
    "the", "a", "an", "and", "or", "of", "to", "in", "is", "are",
    "be", "was", "were", "this", "that", "which", "with", "for",
    "on", "at", "by", "as", "not", "it", "its", "from", "have",
    "has", "had", "will", "would", "all", "any", "also", "such",
    "than", "then", "into", "each", "per", "than", "more", "less",
    "figure", "table", "section", "article", "subsection", "part",
    "clause", "page", "see", "refer", "following", "above", "below",
}


class TFIDFAnalyzer:
    """
    Discovers missing keywords from OBC text using TF-IDF analysis.
    Compares rule-dense paragraphs vs non-rule paragraphs to find
    words that are statistically distinctive in compliance text.
    """

    def __init__(self, top_n: int = 50, min_doc_freq: int = 3):
        """
        Args:
            top_n        (int): number of candidate keywords to return
            min_doc_freq (int): word must appear in at least this many
                                paragraphs to be considered
        """
        self.top_n        = top_n
        self.min_doc_freq = min_doc_freq
        self._existing    = set(kw.lower() for kw in ALL_KEYWORDS)

    # ── PRIVATE ───────────────────────────────────────────────────────────────

    def _label_paragraphs(self, filtered_chunks: list) -> tuple:
        """
        Split paragraphs into two groups:
            rule_paras    — HIGH or MEDIUM confidence
            non_rule_paras — LOW_CONFIDENCE

        Args:
            filtered_chunks (list): output from KeywordFilter.score_chunks()

        Returns:
            tuple: (rule_texts: list[str], non_rule_texts: list[str])
        """
        rule_texts     = []
        non_rule_texts = []

        for chunk in filtered_chunks:
            for para in chunk.get("scored_paragraphs", []):
                text = para.get("text", "").strip()
                if len(text) < 20:
                    continue
                if para.get("confidence") in ("HIGH", "MEDIUM"):
                    rule_texts.append(text)
                else:
                    non_rule_texts.append(text)

        return rule_texts, non_rule_texts

    def _clean_token(self, token: str) -> bool:
        """
        Returns True if a token is worth considering as a keyword candidate.
        Filters out numbers, single chars, stop words, and existing keywords.
        """
        token = token.lower().strip()
        if len(token) < 3:              return False
        if token.isdigit():             return False
        if re.match(r"^\d+\.?\d*$", token): return False
        if token in STOP_WORDS:         return False
        if token in self._existing:     return False
        return True

    # ── PUBLIC API ────────────────────────────────────────────────────────────

    def discover(self, filtered_chunks: list) -> list:
        """
        Run TF-IDF analysis to discover keywords missing from the master list.

        Args:
            filtered_chunks (list): scored chunks from KeywordFilter.score_chunks()

        Returns:
            list[dict]: ranked list of candidate keywords, each with:
                {
                    keyword   (str):   the word
                    tfidf_score (float): how distinctive it is in rule paragraphs
                    rule_freq   (int):  how many rule paragraphs contain it
                    suggestion  (str):  recommended group to add it to
                }
        """
        rule_texts, non_rule_texts = self._label_paragraphs(filtered_chunks)

        if not rule_texts:
            print("[TFIDFAnalyzer] No rule paragraphs found — run KeywordFilter first")
            return []

        print(f"[TFIDFAnalyzer] Analysing {len(rule_texts)} rule paragraphs "
              f"vs {len(non_rule_texts)} non-rule paragraphs...")

        # Combine all texts with labels
        all_texts  = rule_texts + non_rule_texts
        all_labels = ["rule"] * len(rule_texts) + ["non_rule"] * len(non_rule_texts)

        # Run TF-IDF across all paragraphs
        vectorizer = TfidfVectorizer(
            ngram_range   = (1, 2),          # single words + bigrams
            min_df        = self.min_doc_freq,
            max_features  = 5000,
            stop_words    = list(STOP_WORDS),
        )

        try:
            tfidf_matrix = vectorizer.fit_transform(all_texts)
        except ValueError as e:
            print(f"[TFIDFAnalyzer] Not enough text to analyse: {e}")
            return []

        feature_names = vectorizer.get_feature_names_out()

        # Split matrix back into rule vs non-rule
        rule_matrix     = tfidf_matrix[:len(rule_texts)]
        non_rule_matrix = tfidf_matrix[len(rule_texts):]

        # Mean TF-IDF score per word in each group
        rule_means     = np.asarray(rule_matrix.mean(axis=0)).flatten()
        non_rule_means = np.asarray(non_rule_matrix.mean(axis=0)).flatten() \
                         if non_rule_texts else np.zeros(len(feature_names))

        # Distinctiveness = how much higher a word scores in rule vs non-rule text
        distinctiveness = rule_means - non_rule_means

        # Count how many rule paragraphs each word appears in
        rule_doc_freq = np.asarray((rule_matrix > 0).sum(axis=0)).flatten()

        # Rank by distinctiveness
        ranked_indices = np.argsort(distinctiveness)[::-1]

        candidates = []
        for idx in ranked_indices[:self.top_n * 3]:  # over-fetch then filter
            word  = feature_names[idx]
            score = float(distinctiveness[idx])
            freq  = int(rule_doc_freq[idx])

            if score <= 0:
                break
            if not self._clean_token(word):
                continue

            candidates.append({
                "keyword":    word,
                "tfidf_score": round(score, 4),
                "rule_freq":   freq,
                "suggestion":  self._suggest_group(word),
            })

            if len(candidates) >= self.top_n:
                break

        print(f"[TFIDFAnalyzer] Found {len(candidates)} candidate new keywords")
        return candidates

    def _suggest_group(self, word: str) -> str:
        """
        Suggest which keyword group a discovered word should go into.
        Simple heuristic based on word patterns.
        """
        w = word.lower()
        if any(x in w for x in ["shall", "must", "required", "permit"]):
            return "Group 1 — Obligation"
        if any(x in w for x in ["mm", "metre", "meter", "kg", "kpa"]):
            return "Group 5 — Units"
        if any(x in w for x in ["width", "height", "depth", "area", "clear"]):
            return "Group 6 — Properties"
        if any(x in w for x in ["stair", "door", "window", "wall", "ramp"]):
            return "Group 7 — Element Names"
        if any(x in w for x in ["fire", "smoke", "sprinkler", "flame"]):
            return "Group 8 — Fire/Safety"
        if any(x in w for x in ["prohibit", "not allow", "not acceptable"]):
            return "Group 12 — Prohibition"
        if any(x in w for x in ["may", "permit", "allow", "exempt"]):
            return "Group 10 — Permissive"
        return "Review manually"

    def print_report(self, candidates: list):
        """
        Print a formatted report of discovered keyword candidates.
        Add high-scoring words to keyword_master.py.

        Args:
            candidates (list): output from discover()
        """
        if not candidates:
            print("[TFIDFAnalyzer] No new keywords discovered")
            return

        print("\n" + "=" * 65)
        print("  TF-IDF KEYWORD DISCOVERY REPORT")
        print("  Words missing from keyword_master.py, ranked by importance")
        print("=" * 65)
        print(f"\n  {'#':<4} {'Keyword':<30} {'Score':>7} {'Freq':>6}  Suggested Group")
        print(f"  {'-' * 63}")

        for i, c in enumerate(candidates, 1):
            print(
                f"  {i:<4} {c['keyword']:<30} "
                f"{c['tfidf_score']:>7.4f} {c['rule_freq']:>6}  "
                f"{c['suggestion']}"
            )

        print(f"\n  Add high-scoring words to:")
        print(f"  module1_doc_parser/keywords/keyword_master.py")
        print("=" * 65)

    def export_to_keyword_master(self, candidates: list, threshold: float = 0.01) -> list:
        """
        Filter candidates above a score threshold and return
        a list ready to paste into keyword_master.py.

        Args:
            candidates (list):    output from discover()
            threshold  (float):   minimum TF-IDF score to include

        Returns:
            list[str]: keyword strings above the threshold
        """
        return [
            c["keyword"] for c in candidates
            if c["tfidf_score"] >= threshold
        ]


# ── RUN DIRECTLY ─────────────────────────────────────────────────────────────
if __name__ == "__main__":
    """
    To use this script directly:
    1. Run your OBC PDF through DoclingExtractor + SectionChunker + KeywordFilter first
    2. Pass the filtered_chunks output to TFIDFAnalyzer.discover()

    Quick test with sample text:
    """
    print("TF-IDF Analyzer — run after KeywordFilter to discover missing keywords")
    print("Usage:")
    print("  from module1_doc_parser.tfidf_analyzer import TFIDFAnalyzer")
    print("  analyzer = TFIDFAnalyzer()")
    print("  new_keywords = analyzer.discover(filtered_chunks)")
    print("  analyzer.print_report(new_keywords)")
