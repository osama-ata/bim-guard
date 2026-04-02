"""
module1_doc_parser/bert_classifier.py
---------------------------------------
Improvement 4 — BERT Sentence Classifier.

WHAT IT DOES:
    Replaces the keyword list with a model that LEARNED what a rule
    looks like from 862 labelled OBC sentences (CODE-ACCORD dataset).

    Once trained, it classifies any sentence as:
        RULE (1)     — is a compliance rule
        NOT RULE (0) — is not a compliance rule

    No keyword list needed — the model infers the pattern itself.

TWO MODES:
    Mode A — Zero-shot (no training required)
        Uses a pre-trained model with a text classification prompt.
        Works immediately, no CODE-ACCORD data needed.
        Less accurate than fine-tuned but useful to start.

    Mode B — Fine-tuned on CODE-ACCORD (recommended)
        Downloads CODE-ACCORD dataset (862 sentences) and fine-tunes
        a small BERT model specifically on OBC building regulation text.
        Most accurate — purpose-built for your exact use case.

INSTALL:
    pip install transformers torch datasets

DOWNLOAD CODE-ACCORD DATASET:
    The dataset is publicly available at:
    https://github.com/Accord-Project/CODE-ACCORD
    Or via Hugging Face datasets (see _load_codeaccord_data below)

Usage:
    # Zero-shot (no training, works immediately)
    from module1_doc_parser.bert_classifier import BERTClassifier
    clf     = BERTClassifier(mode="zero_shot")
    results = clf.classify_chunks(filtered_chunks)

    # Fine-tuned (train first, then classify)
    clf = BERTClassifier(mode="fine_tuned")
    clf.train()                              # trains on CODE-ACCORD
    clf.save("models/bert_obc_classifier")   # save for reuse
    results = clf.classify_chunks(filtered_chunks)
"""

from pathlib import Path


# ── CONSTANTS ─────────────────────────────────────────────────────────────────

# Labels for classification
LABEL_RULE     = "RULE"
LABEL_NOT_RULE = "NOT_RULE"

# Model to use for zero-shot or as base for fine-tuning
# Small and fast — good for regulatory text
BASE_MODEL = "distilbert-base-uncased"

# CODE-ACCORD on HuggingFace (publicly available)
CODEACCORD_HF = "Accord-Project/CODE-ACCORD"

# Default save path for fine-tuned model
DEFAULT_MODEL_PATH = Path("models/bert_obc_classifier")

# Probability threshold — above this = RULE
RULE_THRESHOLD = 0.60


class BERTClassifier:
    """
    BERT-based sentence classifier for OBC compliance rules.
    Supports zero-shot inference and fine-tuning on CODE-ACCORD.
    """

    def __init__(self, mode: str = "zero_shot", model_path: str = None):
        """
        Args:
            mode       (str): "zero_shot" or "fine_tuned"
            model_path (str): path to a saved fine-tuned model
                              (required if mode="fine_tuned" and not training)
        """
        self.mode       = mode
        self.model_path = Path(model_path) if model_path else DEFAULT_MODEL_PATH
        self.pipeline   = None
        self.model      = None
        self.tokenizer  = None

        self._check_dependencies()

        if mode == "zero_shot":
            self._load_zero_shot()
        elif mode == "fine_tuned":
            if self.model_path.exists():
                self._load_fine_tuned(self.model_path)
            else:
                print(f"[BERTClassifier] No fine-tuned model at {self.model_path}")
                print("  Run clf.train() to train on CODE-ACCORD first")
                print("  Falling back to zero-shot mode")
                self.mode = "zero_shot"
                self._load_zero_shot()

    # ── DEPENDENCY CHECK ─────────────────────────────────────────────────────

    def _check_dependencies(self):
        """Check that required libraries are installed."""
        try:
            import transformers
            import torch
        except ImportError:
            raise ImportError(
                "BERT dependencies not installed.\n"
                "Run: pip install transformers torch datasets"
            )

    # ── MODEL LOADING ─────────────────────────────────────────────────────────

    def _load_zero_shot(self):
        """
        Load a zero-shot text classification pipeline.
        Uses NLI (Natural Language Inference) to classify without training.
        Labels: 'compliance rule' vs 'general information'
        """
        from transformers import pipeline

        print("[BERTClassifier] Loading zero-shot classifier...")
        print("  NOTE: First run downloads model weights (~500MB)")

        self.pipeline = pipeline(
            "zero-shot-classification",
            model="facebook/bart-large-mnli",
        )
        print("[BERTClassifier] Zero-shot classifier ready")

    def _load_fine_tuned(self, model_path: Path):
        """
        Load a previously fine-tuned DistilBERT model.

        Args:
            model_path (Path): path to saved model directory
        """
        from transformers import (
            AutoTokenizer,
            AutoModelForSequenceClassification,
            pipeline,
        )

        print(f"[BERTClassifier] Loading fine-tuned model from {model_path}...")
        self.tokenizer = AutoTokenizer.from_pretrained(str(model_path))
        self.model     = AutoModelForSequenceClassification.from_pretrained(
            str(model_path)
        )
        self.pipeline = pipeline(
            "text-classification",
            model     = self.model,
            tokenizer = self.tokenizer,
        )
        print("[BERTClassifier] Fine-tuned model ready")

    # ── TRAINING ─────────────────────────────────────────────────────────────

    def train(
        self,
        output_path:   str  = None,
        epochs:        int  = 3,
        batch_size:    int  = 16,
        use_codeaccord: bool = True,
    ):
        """
        Fine-tune DistilBERT on CODE-ACCORD building regulation sentences.

        CODE-ACCORD is 862 sentences from English + Finnish building regulations,
        manually annotated by 12 domain experts as compliance rules or not.
        Reference: Nature Scientific Data, Jan 2025.

        Args:
            output_path    (str):  where to save the trained model
            epochs         (int):  number of training epochs (3 is usually enough)
            batch_size     (int):  batch size (reduce if GPU memory errors)
            use_codeaccord (bool): if True, download CODE-ACCORD from HuggingFace
                                   if False, expects local data at data/codeaccord/
        """
        from transformers import (
            AutoTokenizer,
            AutoModelForSequenceClassification,
            TrainingArguments,
            Trainer,
        )
        from datasets import Dataset
        import torch
        import numpy as np

        output_path = Path(output_path or self.model_path)
        output_path.mkdir(parents=True, exist_ok=True)

        print("[BERTClassifier] Starting fine-tuning on CODE-ACCORD...")
        print(f"  Base model : {BASE_MODEL}")
        print(f"  Epochs     : {epochs}")
        print(f"  Output     : {output_path}")

        # ── Load data ─────────────────────────────────────────────────────────
        if use_codeaccord:
            train_data, eval_data = self._load_codeaccord_data()
        else:
            train_data, eval_data = self._load_local_data()

        # ── Tokenize ──────────────────────────────────────────────────────────
        tokenizer = AutoTokenizer.from_pretrained(BASE_MODEL)

        def tokenize(batch):
            return tokenizer(
                batch["text"],
                truncation = True,
                padding    = "max_length",
                max_length = 128,
            )

        train_dataset = Dataset.from_list(train_data).map(tokenize, batched=True)
        eval_dataset  = Dataset.from_list(eval_data).map(tokenize, batched=True)

        # ── Model ─────────────────────────────────────────────────────────────
        model = AutoModelForSequenceClassification.from_pretrained(
            BASE_MODEL,
            num_labels = 2,   # 0 = NOT_RULE, 1 = RULE
        )

        # ── Training arguments ────────────────────────────────────────────────
        training_args = TrainingArguments(
            output_dir         = str(output_path),
            num_train_epochs   = epochs,
            per_device_train_batch_size = batch_size,
            per_device_eval_batch_size  = batch_size,
            evaluation_strategy = "epoch",
            save_strategy       = "epoch",
            load_best_model_at_end = True,
            logging_steps       = 10,
        )

        trainer = Trainer(
            model           = model,
            args            = training_args,
            train_dataset   = train_dataset,
            eval_dataset    = eval_dataset,
            compute_metrics = self._compute_metrics,
        )

        # ── Train ─────────────────────────────────────────────────────────────
        trainer.train()
        trainer.save_model(str(output_path))
        tokenizer.save_pretrained(str(output_path))

        print(f"\n[BERTClassifier] Training complete — model saved to {output_path}")
        print("  Load with: clf = BERTClassifier(mode='fine_tuned')")

        # Load the trained model into this instance
        self._load_fine_tuned(output_path)

    def _load_codeaccord_data(self) -> tuple:
        """
        Download and prepare CODE-ACCORD dataset from HuggingFace.
        862 building regulation sentences, manually annotated.

        Returns:
            tuple: (train_data, eval_data) as list[dict] with keys: text, label
        """
        try:
            from datasets import load_dataset
            print(f"[BERTClassifier] Downloading CODE-ACCORD from HuggingFace...")
            dataset = load_dataset(CODEACCORD_HF)

            def format_row(row):
                # TODO: map CODE-ACCORD label field names to text/label
                # Check actual field names at: https://huggingface.co/datasets/Accord-Project/CODE-ACCORD
                return {
                    "text":  row.get("sentence", row.get("text", "")),
                    "label": 1 if row.get("is_rule", row.get("label")) else 0,
                }

            train = [format_row(r) for r in dataset["train"]]
            eval_ = [format_row(r) for r in dataset.get("validation", dataset["test"])]
            print(f"  Train: {len(train)} sentences | Eval: {len(eval_)} sentences")
            return train, eval_

        except Exception as e:
            print(f"[BERTClassifier] Could not load CODE-ACCORD: {e}")
            print("  Falling back to built-in sample data for demonstration")
            return self._get_sample_training_data()

    def _load_local_data(self) -> tuple:
        """
        Load training data from local file.
        Expected format: data/codeaccord/train.jsonl
        Each line: {"text": "...", "label": 0 or 1}
        """
        import json
        train_path = Path("data/codeaccord/train.jsonl")
        eval_path  = Path("data/codeaccord/eval.jsonl")

        if not train_path.exists():
            raise FileNotFoundError(
                f"No local CODE-ACCORD data at {train_path}\n"
                "Run clf.train(use_codeaccord=True) to download automatically"
            )

        train = [json.loads(l) for l in train_path.read_text().splitlines() if l]
        eval_ = [json.loads(l) for l in eval_path.read_text().splitlines() if l] \
                if eval_path.exists() else train[-50:]

        return train, eval_

    def _get_sample_training_data(self) -> tuple:
        """
        Minimal built-in training sample for demonstration.
        Replace with CODE-ACCORD for production accuracy.
        """
        rules = [
            "Every exit stair shall have a clear width of not less than 860 mm.",
            "Guards shall not be less than 900 mm in height.",
            "Riser height shall be between 125 mm and 200 mm.",
            "The clear opening area of a bedroom window shall not be less than 0.35 m2.",
            "Every stairway shall have a handrail on at least one side.",
            "Doors shall provide a minimum clear opening width of 800 mm.",
            "The tread run shall not be less than 255 mm.",
            "A fire door must be self-closing.",
            "Guards shall be required where a change in elevation exceeds 600 mm.",
            "Each floor assembly shall have a fire-resistance rating of not less than 45 min.",
        ]
        not_rules = [
            "See also Article 9.8.2 for further reference.",
            "This section applies to Part 9 buildings.",
            "Figure 1 illustrates the typical stair configuration.",
            "Refer to the appendix for additional information.",
            "Table 9.8.4.1 shows the rise and run dimensions.",
            "The requirements of this section do not apply to winders.",
            "Commentary: The intent of this requirement is to ensure safety.",
            "For the purposes of this subsection, a stair is defined as follows.",
        ]

        import random
        data = (
            [{"text": t, "label": 1} for t in rules] +
            [{"text": t, "label": 0} for t in not_rules]
        )
        random.shuffle(data)
        split = int(len(data) * 0.8)
        return data[:split], data[split:]

    def _compute_metrics(self, eval_pred):
        """Compute accuracy for training evaluation."""
        import numpy as np
        logits, labels = eval_pred
        predictions = np.argmax(logits, axis=-1)
        accuracy = (predictions == labels).mean()
        return {"accuracy": float(accuracy)}

    # ── INFERENCE ─────────────────────────────────────────────────────────────

    def classify_sentence(self, sentence: str) -> dict:
        """
        Classify one sentence as RULE or NOT_RULE.

        Args:
            sentence (str): one sentence of OBC text

        Returns:
            dict:
                is_rule      (bool)
                probability  (float): 0.0–1.0 probability of being a rule
                label        (str):   "RULE" or "NOT_RULE"
        """
        if not self.pipeline:
            return {"is_rule": False, "probability": 0.0, "label": "NOT_RULE"}

        if self.mode == "zero_shot":
            result = self.pipeline(
                sentence,
                candidate_labels = ["compliance rule", "general information"],
            )
            # "compliance rule" is the first candidate
            prob     = result["scores"][0] if result["labels"][0] == "compliance rule" \
                       else 1 - result["scores"][0]
            is_rule  = prob >= RULE_THRESHOLD
            label    = LABEL_RULE if is_rule else LABEL_NOT_RULE

        else:  # fine_tuned
            result  = self.pipeline(sentence[:512])[0]  # truncate long sentences
            is_rule = result["label"] == "LABEL_1"      # 1 = RULE
            prob    = result["score"] if is_rule else 1 - result["score"]
            label   = LABEL_RULE if is_rule else LABEL_NOT_RULE

        return {
            "is_rule":     is_rule,
            "probability": round(prob, 3),
            "label":       label,
        }

    def classify_chunks(self, filtered_chunks: list) -> list:
        """
        Classify all paragraphs across all chunks.
        Adds bert_probability and bert_label to each paragraph.

        Args:
            filtered_chunks (list): from KeywordFilter.score_chunks()

        Returns:
            list: same chunks with bert_probability added per paragraph
        """
        print(f"[BERTClassifier] Classifying paragraphs (mode: {self.mode})...")

        rule_count     = 0
        not_rule_count = 0
        enhanced       = []

        for chunk in filtered_chunks:
            enhanced_paras = []

            for para in chunk.get("scored_paragraphs", []):
                result = self.classify_sentence(para["text"])
                if result["is_rule"]:
                    rule_count += 1
                else:
                    not_rule_count += 1

                enhanced_paras.append({
                    **para,
                    "bert_probability": result["probability"],
                    "bert_label":       result["label"],
                    "bert_is_rule":     result["is_rule"],
                })

            enhanced.append({**chunk, "scored_paragraphs": enhanced_paras})

        total = rule_count + not_rule_count
        print(f"[BERTClassifier] Done")
        print(f"  RULE     : {rule_count:>5} ({100*rule_count/total:.1f}%)")
        print(f"  NOT_RULE : {not_rule_count:>5} ({100*not_rule_count/total:.1f}%)")

        return enhanced

    def save(self, path: str = None):
        """
        Save the current model to disk for reuse.

        Args:
            path (str): save directory (defaults to DEFAULT_MODEL_PATH)
        """
        save_path = Path(path or self.model_path)
        if self.model and self.tokenizer:
            save_path.mkdir(parents=True, exist_ok=True)
            self.model.save_pretrained(str(save_path))
            self.tokenizer.save_pretrained(str(save_path))
            print(f"[BERTClassifier] Model saved to {save_path}")
        else:
            print("[BERTClassifier] No fine-tuned model to save")
