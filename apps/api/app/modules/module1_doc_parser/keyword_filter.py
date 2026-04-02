"""
module1_doc_parser/keyword_filter.py
--------------------------------------
Step 4 — Scores each paragraph using spaCy lemmatization
and weighted keyword matching.

Confidence levels:
    HIGH           score >= 10  → very likely a rule
    MEDIUM         score >= 1   → possible rule
    LOW_CONFIDENCE score == 0   → flagged, still sent to LLM

Install: pip install spacy && python -m spacy download en_core_web_sm

Usage:
    from module1_doc_parser.keyword_filter import KeywordFilter
    kf       = KeywordFilter()
    filtered = kf.score_chunks(chunks)
"""

import re
from module1_doc_parser.keywords.keyword_master import (
    ALL_SINGLE_KEYWORDS,
    BIGRAM_PHRASES,
    KEYWORD_WEIGHTS,
)

CONFIDENCE_HIGH   = 10
CONFIDENCE_MEDIUM = 1


class KeywordFilter:

    def __init__(self):
        try:
            import spacy
            self.nlp = spacy.load("en_core_web_sm")
            print("[KeywordFilter] spaCy model loaded")
        except ImportError:
            raise ImportError("Run: pip install spacy")
        except OSError:
            raise OSError("Run: python -m spacy download en_core_web_sm")

    def _lemmatize(self, text: str) -> str:
        doc = self.nlp(text.lower())
        return " ".join([t.lemma_ for t in doc])

    def _score(self, paragraph: str) -> tuple:
        original = paragraph.lower()
        lemmatized = self._lemmatize(paragraph)
        lemma_tokens = set(lemmatized.split())
        score, matched = 0, []

        # Bigrams first (weight 6)
        for phrase in BIGRAM_PHRASES:
            if phrase in original:
                score += KEYWORD_WEIGHTS.get(phrase, 1)
                matched.append(phrase)

        # Single keywords on lemmatized text
        for kw in ALL_SINGLE_KEYWORDS:
            if " " in kw:
                continue
            if kw in lemma_tokens or kw in lemmatized:
                score += KEYWORD_WEIGHTS.get(kw, 1)
                matched.append(kw)

        if score >= CONFIDENCE_HIGH:
            confidence = "HIGH"
        elif score >= CONFIDENCE_MEDIUM:
            confidence = "MEDIUM"
        else:
            confidence = "LOW_CONFIDENCE"

        return score, list(set(matched)), confidence

    def score_chunks(self, chunks: list) -> list:
        print("[KeywordFilter] Scoring paragraphs...\n")
        filtered = []

        for chunk in chunks:
            paragraphs = re.split(r"\n{2,}", chunk["text"])
            scored = []

            for para in paragraphs:
                para = para.strip()
                if len(para) < 20:
                    continue
                score, matched, confidence = self._score(para)
                scored.append({
                    "text":       para,
                    "score":      score,
                    "matched":    matched,
                    "confidence": confidence,
                })

            count_high   = sum(1 for p in scored if p["confidence"] == "HIGH")
            count_medium = sum(1 for p in scored if p["confidence"] == "MEDIUM")
            count_low    = sum(1 for p in scored if p["confidence"] == "LOW_CONFIDENCE")

            parts = []
            for p in scored:
                if p["confidence"] == "LOW_CONFIDENCE":
                    parts.append(f"[LOW_CONFIDENCE] {p['text']}")
                else:
                    parts.append(p["text"])

            filtered_text = "\n\n".join(parts)

            filtered.append({
                **chunk,
                "scored_paragraphs": scored,
                "filtered_text":     filtered_text,
                "count_high":        count_high,
                "count_medium":      count_medium,
                "count_low":         count_low,
                "total_paragraphs":  len(scored),
            })

        # Summary
        print(f"  {'#':<4} {'Section':<35} {'Total':>6} {'HIGH':>6} {'MED':>6} {'LOW':>6}")
        print(f"  {'-'*63}")
        for c in filtered:
            print(
                f"  {c['section_number']:<4} {c['section_name']:<35} "
                f"{c['total_paragraphs']:>6} {c['count_high']:>6} "
                f"{c['count_medium']:>6} {c['count_low']:>6}"
            )

        return filtered
