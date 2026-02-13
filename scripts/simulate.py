#!/usr/bin/env python3
"""Minimal 3-agent room simulator for Narrative Reactor Day 2/3 prototype.

Outputs JSONL event stream with:
- per-tick tension scoring
- fate-anchor detection
- simple memory lattice updates and rumor distortion
"""

from __future__ import annotations

from dataclasses import dataclass, asdict
from datetime import datetime, timezone
import argparse
import json
import random
from pathlib import Path
from typing import Dict, List

ACTIONS = ["negotiate", "lie", "threaten", "trade", "reveal", "withhold"]


@dataclass
class MemoryItem:
    memory_id: str
    memory_type: str  # episodic | rumor
    confidence: float
    valence: float
    source_event_id: str


@dataclass
class Agent:
    agent_id: str
    desire: Dict[str, float]
    stress: float
    memories: List[MemoryItem]


@dataclass
class World:
    tick: int
    water: float
    authority: float
    knowledge: float
    affect: float
    social_entropy: float


def _clamp(value: float, lo: float = 0.0, hi: float = 1.0) -> float:
    return max(lo, min(hi, value))


def _decay_memories(agent: Agent) -> None:
    """Decay confidence a little each tick to model memory blur."""
    for m in agent.memories:
        m.confidence = round(_clamp(m.confidence - 0.01), 4)


def _add_memory(
    rng: random.Random,
    holder: Agent,
    source_event_id: str,
    memory_type: str,
    base_confidence: float,
    base_valence: float,
    distortion: float = 0.0,
) -> MemoryItem:
    memory = MemoryItem(
        memory_id=f"mem_{source_event_id}_{holder.agent_id[-1]}_{rng.randint(100,999)}",
        memory_type=memory_type,
        confidence=round(_clamp(base_confidence - distortion), 4),
        valence=round(_clamp(base_valence + rng.uniform(-0.1, 0.1), -1, 1), 4),
        source_event_id=source_event_id,
    )
    holder.memories.append(memory)
    return memory


def tension_score(agents: List[Agent], world: World) -> Dict[str, float]:
    """Compute interpretable tension components for one tick."""
    controls = [a.desire["control"] for a in agents]
    goal_opposition = _clamp(max(controls) - min(controls))

    resource_total = world.water + world.authority + world.knowledge + world.affect
    resource_collision = _clamp(1.0 - min(1.0, resource_total / 40.0))

    info_asymmetry = _clamp(world.social_entropy)
    relational_fragility = _clamp(sum(a.stress for a in agents) / len(agents))

    tension = _clamp(
        0.25 * goal_opposition
        + 0.30 * resource_collision
        + 0.20 * info_asymmetry
        + 0.25 * relational_fragility
    )

    return {
        "goal_opposition": round(goal_opposition, 4),
        "resource_collision": round(resource_collision, 4),
        "info_asymmetry": round(info_asymmetry, 4),
        "relational_fragility": round(relational_fragility, 4),
        "tension": round(tension, 4),
    }


def choose_action(rng: random.Random, agent: Agent, tension: float) -> str:
    if tension > 0.75:
        return rng.choice(["threaten", "lie", "reveal"])
    if agent.stress > 0.7:
        return rng.choice(["withhold", "lie", "negotiate"])
    return rng.choice(ACTIONS)


def run(seed: int, ticks: int, out_path: Path) -> None:
    rng = random.Random(seed)

    agents = [
        Agent("agent_A", {"survival": 0.8, "control": 0.7, "belonging": 0.2, "self_actualization": 0.6}, 0.40, []),
        Agent("agent_B", {"survival": 0.6, "control": 0.5, "belonging": 0.7, "self_actualization": 0.4}, 0.35, []),
        Agent("agent_C", {"survival": 0.7, "control": 0.3, "belonging": 0.3, "self_actualization": 0.8}, 0.30, []),
    ]
    world = World(tick=0, water=10, authority=7, knowledge=5, affect=4, social_entropy=0.42)

    out_path.parent.mkdir(parents=True, exist_ok=True)
    with out_path.open("w", encoding="utf-8") as f:
        for t in range(1, ticks + 1):
            world.tick = t
            world.social_entropy = _clamp(world.social_entropy + rng.uniform(-0.03, 0.05))
            world.water = max(0.0, world.water - rng.uniform(0.0, 0.3))
            world.knowledge = max(0.0, world.knowledge - rng.uniform(0.0, 0.2))

            if t % 7 == 0:
                world.social_entropy = _clamp(world.social_entropy + rng.uniform(0.2, 0.35))

            for a in agents:
                _decay_memories(a)
                a.stress = _clamp(a.stress + rng.uniform(-0.08, 0.18) + world.social_entropy * 0.08)

            score = tension_score(agents, world)
            anchor = score["tension"] > 0.68

            actor = rng.choice(agents)
            target = rng.choice([a for a in agents if a.agent_id != actor.agent_id])
            action = choose_action(rng, actor, score["tension"])
            event_id = f"evt_{seed}_{t:04d}"

            # memory lattice update: actor gets episodic; target may get rumor-distorted memory
            actor_memory = _add_memory(
                rng,
                holder=actor,
                source_event_id=event_id,
                memory_type="episodic",
                base_confidence=0.9,
                base_valence=-0.25 if action in {"threaten", "lie"} else 0.1,
            )

            rumor_distortion = rng.uniform(0.15, 0.45) if action in {"lie", "withhold", "threaten"} else rng.uniform(0.05, 0.2)
            target_memory = _add_memory(
                rng,
                holder=target,
                source_event_id=event_id,
                memory_type="rumor",
                base_confidence=0.7,
                base_valence=-0.35 if action in {"threaten", "lie"} else 0.05,
                distortion=rumor_distortion,
            )

            event = {
                "version": "1.0.0",
                "event_id": event_id,
                "event_trace_id": f"trace_{seed}_{t:04d}",
                "tick": t,
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "actor_id": actor.agent_id,
                "action": action,
                "target_ids": [target.agent_id],
                "resource_delta": {
                    "water": round(rng.uniform(-0.4, 0.2), 3),
                    "authority": round(rng.uniform(-0.3, 0.3), 3),
                    "knowledge": round(rng.uniform(-0.2, 0.3), 3),
                    "affect": round(rng.uniform(-0.5, 0.5), 3),
                },
                "cause_refs": {
                    "world_snapshot_id": f"ws_{seed}_{t:04d}",
                    "agent_snapshot_ids": [f"as_{seed}_{t:04d}_A", f"as_{seed}_{t:04d}_B", f"as_{seed}_{t:04d}_C"],
                    "memory_refs": [actor_memory.memory_id, target_memory.memory_id],
                },
                "derived": {
                    "tension_contribution": score["tension"],
                    "stakes_level": "high" if score["tension"] > 0.75 else "medium" if score["tension"] > 0.45 else "low",
                },
                "metrics": score,
                "fate_anchor": anchor,
                "memory_update": {
                    "actor_memory": asdict(actor_memory),
                    "target_memory": asdict(target_memory),
                    "rumor_distortion": round(rumor_distortion, 4),
                },
                "world": asdict(world),
                "agents": [
                    {
                        "agent_id": a.agent_id,
                        "stress": a.stress,
                        "desire": a.desire,
                        "memory_size": len(a.memories),
                        "latest_memory": asdict(a.memories[-1]) if a.memories else None,
                    }
                    for a in agents
                ],
            }
            f.write(json.dumps(event, ensure_ascii=False) + "\n")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run Narrative Reactor minimal simulation")
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--ticks", type=int, default=30)
    parser.add_argument("--out", type=Path, default=Path("runs/run_42.jsonl"))
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    run(seed=args.seed, ticks=args.ticks, out_path=args.out)
    print(f"WROTE {args.out}")
