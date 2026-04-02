"""
module3_rule_builder/rule_store.py
-----------------------------------
SQLite database layer for BIMGuard rules.
All modules read from and write to this single store.

Responsibilities:
    - Create and manage the rules table
    - Save individual rule dicts
    - Query rules by entity type, priority, section
    - Return rules as DataFrames for inspection
    - Support RAG by returning sample rules as examples

Usage:
    from module3_rule_builder.rule_store import RuleStore
    from config import DB_PATH

    store = RuleStore(DB_PATH)
    store.save_rule({...})
    rules = store.fetch_rules_for_entity("IfcStairFlight")
"""

import sqlite3
import json
import uuid
from datetime import datetime
from pathlib import Path
import pandas as pd


class RuleStore:
    """
    Handles all SQLite read/write operations for the BIMGuard Rule Database.
    This is the central hub — all modules read from and write to here.
    """

    CREATE_TABLE = """
    CREATE TABLE IF NOT EXISTS rules (
        rule_id         TEXT PRIMARY KEY,
        source_doc      TEXT,
        section_ref     TEXT,
        rule_type       TEXT,
        entity_type     TEXT,
        property_name   TEXT,
        operator        TEXT,
        value           TEXT,
        unit            TEXT,
        priority        INTEGER DEFAULT 0,
        description     TEXT,
        raw_payload     TEXT,
        created_at      TEXT
    );
    """

    def __init__(self, db_path):
        """
        Initialise the RuleStore and create the rules table if it doesn't exist.

        Args:
            db_path (str | Path): path to the SQLite database file
        """
        self.db_path = Path(db_path)
        self.conn = sqlite3.connect(str(self.db_path))
        self.conn.execute(self.CREATE_TABLE)
        self.conn.commit()
        print(f"[RuleStore] Connected — {self.count()} existing rules in '{self.db_path.name}'")

    # ── WRITE ─────────────────────────────────────────────────────────────────

    def save_rule(self, rule: dict) -> str:
        """
        Save a single validated rule dict to the database.

        Args:
            rule (dict): rule dict matching the schema in rule_generator.py

        Returns:
            str: the new rule_id (UUID)
        """
        rule_id = str(uuid.uuid4())
        now     = datetime.utcnow().isoformat()

        self.conn.execute(
            "INSERT INTO rules VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)",
            (
                rule_id,
                rule.get("source_doc"),
                rule.get("section_ref"),
                rule.get("rule_type"),
                rule.get("entity_type"),
                rule.get("property_name"),
                rule.get("operator"),
                json.dumps(rule.get("value")),   # handles lists like [125, 200]
                rule.get("unit"),
                int(rule.get("priority", 0)),
                rule.get("description"),
                json.dumps(rule),                 # full payload for retrieval
                now,
            ),
        )
        self.conn.commit()
        return rule_id

    def clear_all_rules(self):
        """
        Delete all rules from the database.
        Use carefully — primarily for testing.
        """
        self.conn.execute("DELETE FROM rules")
        self.conn.commit()
        print("[RuleStore] ⚠️  All rules deleted")

    # ── READ ──────────────────────────────────────────────────────────────────

    def fetch_rules_for_entity(self, entity_type: str) -> list:
        """
        Get all rules for a specific IFC entity type.

        Args:
            entity_type (str): e.g. "IfcStairFlight", "IfcDoor"

        Returns:
            list[dict]: list of rule dicts
        """
        cur = self.conn.execute(
            "SELECT raw_payload FROM rules WHERE entity_type = ?",
            (entity_type,),
        )
        return [json.loads(row[0]) for row in cur.fetchall()]

    def fetch_priority_rules(self) -> list:
        """
        Get all rules flagged as priority = 1 (critical).

        Returns:
            list[dict]: list of rule dicts
        """
        cur = self.conn.execute(
            "SELECT raw_payload FROM rules WHERE priority = 1"
        )
        return [json.loads(row[0]) for row in cur.fetchall()]

    def fetch_rules_by_section(self, section_ref: str) -> list:
        """
        Get all rules for a specific OBC section reference.

        Args:
            section_ref (str): e.g. "9.8.2.1"

        Returns:
            list[dict]
        """
        cur = self.conn.execute(
            "SELECT raw_payload FROM rules WHERE section_ref LIKE ?",
            (f"%{section_ref}%",),
        )
        return [json.loads(row[0]) for row in cur.fetchall()]

    def get_existing_entity_types(self) -> list:
        """
        Returns list of distinct IFC entity types already in the DB.
        Used by the NLP Engine to avoid extracting duplicate rules.

        Returns:
            list[str]: e.g. ["IfcStairFlight", "IfcDoor", "IfcRailing"]
        """
        cur = self.conn.execute(
            "SELECT DISTINCT entity_type FROM rules"
        )
        return [row[0] for row in cur.fetchall()]

    def get_rules_sample(self, limit: int = 3) -> list:
        """
        Returns a sample of high-priority rules as RAG examples.
        Injected into the NLP Engine prompt so the LLM sees
        the exact schema in action before extracting new rules.

        Args:
            limit (int): number of examples to return

        Returns:
            list[dict]
        """
        cur = self.conn.execute(
            "SELECT raw_payload FROM rules WHERE priority = 1 LIMIT ?",
            (limit,),
        )
        return [json.loads(row[0]) for row in cur.fetchall()]

    def fetch_all_as_dataframe(self) -> pd.DataFrame:
        """
        Return all rules as a pandas DataFrame for inspection.

        Returns:
            pd.DataFrame
        """
        return pd.read_sql_query(
            """SELECT section_ref, entity_type, property_name,
               operator, value, unit, priority, description
               FROM rules""",
            self.conn,
        )

    def count(self) -> int:
        """Return total number of rules in the database."""
        return self.conn.execute(
            "SELECT COUNT(*) FROM rules"
        ).fetchone()[0]

    def summary(self) -> dict:
        """
        Return a summary dict of the current DB state.
        Useful for API responses and logging.

        Returns:
            dict: {total, by_entity, by_source, priority_count}
        """
        total = self.count()

        by_entity = {}
        for row in self.conn.execute(
            "SELECT entity_type, COUNT(*) FROM rules GROUP BY entity_type"
        ):
            by_entity[row[0]] = row[1]

        by_source = {}
        for row in self.conn.execute(
            "SELECT source_doc, COUNT(*) FROM rules GROUP BY source_doc"
        ):
            by_source[row[0]] = row[1]

        priority_count = self.conn.execute(
            "SELECT COUNT(*) FROM rules WHERE priority = 1"
        ).fetchone()[0]

        return {
            "total":          total,
            "priority_count": priority_count,
            "by_entity":      by_entity,
            "by_source":      by_source,
        }

    def close(self):
        """Close the database connection."""
        self.conn.close()
