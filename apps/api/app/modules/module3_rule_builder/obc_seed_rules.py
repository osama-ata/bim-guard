"""
module3_rule_builder/obc_seed_rules.py
----------------------------------------
Pre-built OBC Part 9 compliance rules.
These seed the database before any PDF is uploaded,
so rules.db always has a baseline to work from.

Run directly to seed the database:
    python -m module3_rule_builder.obc_seed_rules

Or import and call:
    from module3_rule_builder.obc_seed_rules import seed_rules
    seed_rules(store, generator)
"""

from module3_rule_builder.rule_store import RuleStore
from module3_rule_builder.rule_generator import RuleGenerator
from config import DB_PATH, SOURCE_DOC_SEED


# ── 25 PRE-BUILT OBC PART 9 RULES ────────────────────────────────────────────

OBC_SEED_RULES = [

    # ── STAIR WIDTH ──────────────────────────────────────────────────────────
    {
        "section_ref": "9.8.2.1.(2)", "rule_type": "json_check",
        "entity_type": "IfcStairFlight", "property_name": "Width",
        "operator": ">=", "value": 860, "unit": "mm", "priority": 1,
        "description": "Exit stair serving house/dwelling — minimum clear width 860mm"
    },
    {
        "section_ref": "9.8.2.1.(4)", "rule_type": "json_check",
        "entity_type": "IfcStairFlight", "property_name": "Width",
        "operator": ">=", "value": 860, "unit": "mm", "priority": 1,
        "description": "At least one stair between floor levels — minimum width 860mm"
    },

    # ── HEADROOM ─────────────────────────────────────────────────────────────
    {
        "section_ref": "9.8.2.2.(3)", "rule_type": "json_check",
        "entity_type": "IfcStairFlight", "property_name": "HeadroomClearance",
        "operator": ">=", "value": 1950, "unit": "mm", "priority": 1,
        "description": "Minimum vertical headroom over full stair width — 1950mm"
    },
    {
        "section_ref": "9.8.2.2.(3)", "rule_type": "json_check",
        "entity_type": "IfcSlab", "property_name": "HeadroomClearance",
        "operator": ">=", "value": 1950, "unit": "mm", "priority": 1,
        "description": "Minimum headroom clearance over stair landings — 1950mm"
    },

    # ── RISER HEIGHT ─────────────────────────────────────────────────────────
    {
        "section_ref": "Table 9.8.4.1", "rule_type": "range_check",
        "entity_type": "IfcStairFlight", "property_name": "RiserHeight",
        "operator": "between", "value": [125, 200], "unit": "mm", "priority": 1,
        "description": "Private stair riser height — min 125mm, max 200mm"
    },

    # ── TREAD DEPTH ──────────────────────────────────────────────────────────
    {
        "section_ref": "Table 9.8.4.1", "rule_type": "range_check",
        "entity_type": "IfcStairFlight", "property_name": "TreadDepth",
        "operator": "between", "value": [255, 355], "unit": "mm", "priority": 1,
        "description": "Private stair tread run/depth — min 255mm, max 355mm"
    },

    # ── FLIGHT HEIGHT ─────────────────────────────────────────────────────────
    {
        "section_ref": "9.8.3.3.(1)", "rule_type": "json_check",
        "entity_type": "IfcStairFlight", "property_name": "FlightHeight",
        "operator": "<=", "value": 3700, "unit": "mm", "priority": 0,
        "description": "Maximum vertical height per stair flight — 3700mm"
    },

    # ── LANDINGS ─────────────────────────────────────────────────────────────
    {
        "section_ref": "9.8.6.3", "rule_type": "json_check",
        "entity_type": "IfcSlab", "property_name": "Width",
        "operator": ">=", "value": 860, "unit": "mm", "priority": 1,
        "description": "Landing width must be at minimum equal to stair width — min 860mm"
    },
    {
        "section_ref": "9.8.6.3", "rule_type": "json_check",
        "entity_type": "IfcSlab", "property_name": "MaxSlope",
        "operator": "<=", "value": 0.02, "unit": "ratio", "priority": 0,
        "description": "Landing surface slope must not exceed 1:50 (0.02)"
    },

    # ── WINDERS ──────────────────────────────────────────────────────────────
    {
        "section_ref": "9.8.4.5.(1)", "rule_type": "json_check",
        "entity_type": "IfcStairFlight", "property_name": "WinderTurnAngle",
        "operator": "<=", "value": 90, "unit": "deg", "priority": 0,
        "description": "Maximum total winder set turn angle — 90 degrees"
    },
    {
        "section_ref": "9.8.4.5.(2)", "rule_type": "range_check",
        "entity_type": "IfcStairFlight", "property_name": "IndividualWinderAngle",
        "operator": "between", "value": [30, 45], "unit": "deg", "priority": 0,
        "description": "Each winder tread angle must be between 30° and 45°"
    },
    {
        "section_ref": "9.8.4.5.(2)", "rule_type": "json_check",
        "entity_type": "IfcStairFlight", "property_name": "WinderSetSeparation",
        "operator": ">=", "value": 1200, "unit": "mm", "priority": 0,
        "description": "Minimum plan separation between winder sets — 1200mm"
    },

    # ── EGRESS DOORS ─────────────────────────────────────────────────────────
    {
        "section_ref": "OBC 9.6.4", "rule_type": "json_check",
        "entity_type": "IfcDoor", "property_name": "ClearWidth",
        "operator": ">=", "value": 800, "unit": "mm", "priority": 1,
        "description": "Egress door minimum clear opening width — 800mm"
    },
    {
        "section_ref": "OBC 9.6.4", "rule_type": "json_check",
        "entity_type": "IfcDoor", "property_name": "Height",
        "operator": ">=", "value": 1980, "unit": "mm", "priority": 1,
        "description": "Egress door minimum height — 1980mm"
    },

    # ── GUARDS & HANDRAILS ────────────────────────────────────────────────────
    {
        "section_ref": "OBC 9.8.8", "rule_type": "json_check",
        "entity_type": "IfcRailing", "property_name": "Height",
        "operator": ">=", "value": 900, "unit": "mm", "priority": 1,
        "description": "Guard minimum height at floor edges, stairs, landings, balconies — 900mm"
    },
    {
        "section_ref": "OBC 9.8.7", "rule_type": "range_check",
        "entity_type": "IfcRailing", "property_name": "HandrailHeight",
        "operator": "between", "value": [865, 1070], "unit": "mm", "priority": 1,
        "description": "Handrail height must be between 865mm and 1070mm above stair nosings"
    },

    # ── WINDOWS ──────────────────────────────────────────────────────────────
    {
        "section_ref": "OBC 9.7.2", "rule_type": "json_check",
        "entity_type": "IfcWindow", "property_name": "ClearOpeningArea",
        "operator": ">=", "value": 0.35, "unit": "m2", "priority": 1,
        "description": "Bedroom egress window minimum clear opening area — 0.35m²"
    },
    {
        "section_ref": "OBC 9.7.2", "rule_type": "json_check",
        "entity_type": "IfcWindow", "property_name": "ClearOpeningHeight",
        "operator": ">=", "value": 380, "unit": "mm", "priority": 1,
        "description": "Bedroom egress window minimum clear opening height — 380mm"
    },
    {
        "section_ref": "OBC 9.7.2", "rule_type": "json_check",
        "entity_type": "IfcWindow", "property_name": "ClearOpeningWidth",
        "operator": ">=", "value": 450, "unit": "mm", "priority": 1,
        "description": "Bedroom egress window minimum clear opening width — 450mm"
    },

    # ── GARAGE ───────────────────────────────────────────────────────────────
    {
        "section_ref": "OBC 9.35", "rule_type": "exists_check",
        "entity_type": "IfcWall", "property_name": "FireRating",
        "operator": "exists", "value": None, "unit": None, "priority": 1,
        "description": "Garage-to-dwelling separation walls must have FireRating parameter"
    },

    # ── SPATIAL SEPARATION ────────────────────────────────────────────────────
    {
        "section_ref": "OBC 3.2.3", "rule_type": "json_check",
        "entity_type": "IfcWall", "property_name": "LimitingDistance",
        "operator": ">=", "value": 0, "unit": "m", "priority": 1,
        "description": "Limiting distance from exterior wall face to property line must be calculated"
    },

    # ── MODEL QA ─────────────────────────────────────────────────────────────
    {
        "section_ref": "BIMGuard QA", "rule_type": "exists_check",
        "entity_type": "IfcDoor", "property_name": "Width",
        "operator": "exists", "value": None, "unit": None, "priority": 0,
        "description": "All IfcDoor elements must have a Width parameter — flag if missing"
    },
    {
        "section_ref": "BIMGuard QA", "rule_type": "exists_check",
        "entity_type": "IfcSpace", "property_name": "LongName",
        "operator": "exists", "value": None, "unit": None, "priority": 0,
        "description": "All rooms/spaces must have a LongName — flag if missing"
    },
    {
        "section_ref": "BIMGuard QA", "rule_type": "exists_check",
        "entity_type": "IfcStairFlight", "property_name": "Name",
        "operator": "exists", "value": None, "unit": None, "priority": 0,
        "description": "All stair flight elements must have a Name parameter"
    },
]


def seed_rules(store: RuleStore, generator: RuleGenerator) -> int:
    """
    Seed the database with the pre-built OBC Part 9 rules.
    Safe to call multiple times — skips if rules already exist from this source.

    Args:
        store     (RuleStore):     target database
        generator (RuleGenerator): validator and saver

    Returns:
        int: number of rules saved
    """
    existing_count = store.count()

    if existing_count > 0:
        print(f"[SeedRules] DB already has {existing_count} rules — skipping seed")
        print("  To re-seed, call store.clear_all_rules() first")
        return 0

    print(f"[SeedRules] Seeding {len(OBC_SEED_RULES)} OBC Part 9 rules...\n")
    saved_ids = generator.save_batch(OBC_SEED_RULES, source_doc=SOURCE_DOC_SEED)
    print(f"\n[SeedRules] Done — {len(saved_ids)} rules saved to DB")
    return len(saved_ids)


# ── RUN DIRECTLY ─────────────────────────────────────────────────────────────
if __name__ == "__main__":
    store     = RuleStore(DB_PATH)
    generator = RuleGenerator(store)
    seed_rules(store, generator)

    print("\nRules in DB by entity type:")
    summary = store.summary()
    for entity, count in summary["by_entity"].items():
        print(f"  {entity:<30} {count} rules")
