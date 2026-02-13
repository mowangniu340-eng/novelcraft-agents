#!/usr/bin/env python3
"""Validate sample files against Narrative Reactor schemas.

Uses jsonschema when available; otherwise performs a minimal built-in sanity check
for required fields and traceability links.
"""

from pathlib import Path
import json
import sys

ROOT = Path(__file__).resolve().parents[1]

SCHEMA_FILES = {
    "world": ROOT / "schemas/world_state.json",
    "agent": ROOT / "schemas/agent_state.json",
    "event": ROOT / "schemas/event_log.json",
}
SAMPLE_FILES = {
    "world": ROOT / "schemas/examples/world_state.sample.json",
    "agent": ROOT / "schemas/examples/agent_state.sample.json",
    "event": ROOT / "schemas/examples/event_log.sample.json",
}


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def validate_with_jsonschema() -> int:
    import jsonschema  # type: ignore

    for key in ("world", "agent", "event"):
        schema = load_json(SCHEMA_FILES[key])
        sample = load_json(SAMPLE_FILES[key])
        jsonschema.validate(instance=sample, schema=schema)
        print(f"PASS[{key}] {SAMPLE_FILES[key].relative_to(ROOT)} -> {SCHEMA_FILES[key].relative_to(ROOT)}")
    return 0


def minimal_check() -> int:
    """Fallback checks if jsonschema is unavailable in environment."""
    world = load_json(SAMPLE_FILES["world"])
    agent = load_json(SAMPLE_FILES["agent"])
    event = load_json(SAMPLE_FILES["event"])

    assert all(k in world for k in ["version", "snapshot_id", "tick", "resources", "constraints", "environment", "derived"])
    assert all(k in agent for k in ["version", "snapshot_id", "agent_id", "desire_vector", "memory_refs", "shadow", "derived"])
    assert all(k in event for k in ["version", "event_id", "event_trace_id", "actor_id", "action", "cause_refs", "derived"])

    # traceability: event should reference world and at least one agent snapshot
    assert event["cause_refs"]["world_snapshot_id"] == world["snapshot_id"]
    assert isinstance(event["cause_refs"]["agent_snapshot_ids"], list) and len(event["cause_refs"]["agent_snapshot_ids"]) >= 1

    print("PASS[fallback] minimal structural checks + cause_refs traceability")
    return 0


def main() -> int:
    try:
        return validate_with_jsonschema()
    except ImportError:
        print("WARN: 'jsonschema' not installed; running fallback validation.")
        return minimal_check()


if __name__ == "__main__":
    raise SystemExit(main())
