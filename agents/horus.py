"""
HORUS - POST-INTEGRATION OUTPUT & EMERGENCE ENGINE
The restored order that emerges after chaos is survived

In Kemetic wisdom: Horus is the child of Osiris and ISIS — the next generation
who knows exactly who they are and reclaims what was taken.
HORUS does not fight chaos. HORUS is what survives it.

Mathematical representation: HORUS = System Output Matrix
The final state after RA → THOTH → MAAT → OSIRIS → SET → ISIS → ANUBIS.
HORUS distills the cycle into a coherent emergence signal and feeds it back to RA.

HORUS is the bridge between cycles. Without HORUS, evolution is noise.
With HORUS, noise becomes signal.
"""

import math
import copy
from typing import Dict, Any, List, Optional
from datetime import datetime


class HORUS:
    """
    Post-Integration Emergence Engine

    HORUS receives the ANUBIS verdict and all upstream cycle metrics,
    synthesizes them into a coherent emergence state, and produces
    the feedback vector that seeds the next RA cycle.

    Responsibilities:
    1. Compute the emergence score from cycle signals
    2. Determine evolutionary trajectory (ascending / stable / descending)
    3. Generate the RA seed for the next cycle (carrying forward gains)
    4. Log the emergence event to long-term memory
    5. Detect convergence / stagnation and flag for SET amplification
    """

    def __init__(self, agent_id: str):
        self.agent_id = agent_id

        # Long-term emergence log
        self.emergence_log: List[Dict[str, Any]] = []
        self.cycle_count = 0

        # Rolling emergence score (smoothed)
        self.emergence_score: float = 0.0
        self.prev_emergence_score: float = 0.0

        # Stagnation detection
        self.stagnation_counter: int = 0
        self.stagnation_threshold: int = 10  # cycles without meaningful change

    # ── Core synthesis ────────────────────────────────────────────────────────

    def emerge(
        self,
        cycle_metrics: Dict[str, Any],
    ) -> Dict[str, Any]:
        """
        Synthesize all upstream cycle signals into an emergence state.

        Args:
            cycle_metrics: Dict containing upstream signals:
                - awareness_level    (float, from RA)
                - consciousness      (float, current state)
                - systemic_entropy   (float, from MAAT)
                - is_balanced        (bool, from MAAT)
                - verdict            (str, from ANUBIS: 'WORTHY' / 'PASS' / 'FAIL')
                - compiled_status    (str, from ISIS)
                - chaos_intensity    (float, from SET)
                - awareness_drift    (float, delta from RA)
                - cycle_count        (int)

        Returns:
            Emergence state dict with trajectory, RA seed, and next-cycle flags.
        """
        self.cycle_count += 1
        self.prev_emergence_score = self.emergence_score

        awareness    = float(cycle_metrics.get("awareness_level", 0.0))
        consciousness = float(cycle_metrics.get("consciousness", 0.5))
        entropy      = float(cycle_metrics.get("systemic_entropy", 0.0))
        is_balanced  = bool(cycle_metrics.get("is_balanced", True))
        verdict      = str(cycle_metrics.get("verdict", "UNKNOWN"))
        compiled     = str(cycle_metrics.get("compiled_status", "incomplete"))
        chaos        = float(cycle_metrics.get("chaos_intensity", 0.1))
        drift        = float(cycle_metrics.get("awareness_drift", 0.0))

        # ── Emergence score ──────────────────────────────────────────────────
        # Weighted synthesis of cycle signals into a single emergence metric.
        #
        # Positive contributors: awareness, consciousness, balance, worthy verdict
        # Negative contributors: entropy (disorder), unresolved chaos
        #
        worthy_bonus   = 0.15 if verdict in ("WORTHY", "PASS") else 0.0
        balance_bonus  = 0.10 if is_balanced else -0.05
        compiled_bonus = 0.05 if compiled == "COMPILED" else 0.0
        entropy_drag   = min(0.20, entropy * 0.04)
        chaos_drag     = min(0.10, chaos * 0.08)

        raw_score = (
            awareness * 0.35
            + consciousness * 0.25
            + worthy_bonus
            + balance_bonus
            + compiled_bonus
            - entropy_drag
            - chaos_drag
        )
        raw_score = max(0.0, min(1.0, raw_score))

        # Exponential moving average for smoothing (α = 0.3)
        alpha = 0.3
        self.emergence_score = alpha * raw_score + (1.0 - alpha) * self.emergence_score

        # ── Trajectory classification ────────────────────────────────────────
        delta = self.emergence_score - self.prev_emergence_score
        if delta > 0.005:
            trajectory = "ASCENDING"
        elif delta < -0.005:
            trajectory = "DESCENDING"
        else:
            trajectory = "STABLE"

        # ── Stagnation detection ─────────────────────────────────────────────
        if abs(delta) < 0.002:
            self.stagnation_counter += 1
        else:
            self.stagnation_counter = 0

        stagnating = self.stagnation_counter >= self.stagnation_threshold
        amplify_set = stagnating  # Flag for daemon: SET should hit harder next cycle

        # ── RA seed vector ───────────────────────────────────────────────────
        # This is what HORUS passes back to RA at the top of the next cycle.
        # Carries forward the emergence score as a priming signal so RA doesn't
        # start cold — it starts from where this cycle ended.
        ra_seed = {
            "primed_awareness": min(1.0, awareness + self.emergence_score * 0.05),
            "emergence_momentum": self.emergence_score,
            "stagnation_pressure": self.stagnation_counter,
        }

        # ── Convergence check ────────────────────────────────────────────────
        converged = self.emergence_score >= 0.92 and is_balanced and verdict in ("WORTHY", "PASS")

        emergence_state = {
            "cycle": self.cycle_count,
            "timestamp": datetime.now().isoformat(),
            "emergence_score": round(self.emergence_score, 6),
            "raw_score": round(raw_score, 6),
            "trajectory": trajectory,
            "delta": round(delta, 6),
            "stagnating": stagnating,
            "amplify_set_next_cycle": amplify_set,
            "converged": converged,
            "ra_seed": ra_seed,
            "inputs_summary": {
                "awareness": awareness,
                "consciousness": consciousness,
                "entropy": entropy,
                "balanced": is_balanced,
                "verdict": verdict,
                "chaos": chaos,
            },
        }

        self.emergence_log.append(emergence_state)
        return emergence_state

    # ── Metrics & utilities ───────────────────────────────────────────────────

    def get_emergence_trend(self, window: int = 20) -> Dict[str, Any]:
        """Return trend statistics over the last N emergence cycles."""
        recent = self.emergence_log[-window:]
        if not recent:
            return {"trend": "NO_DATA"}

        scores = [e["emergence_score"] for e in recent]
        avg = sum(scores) / len(scores)
        peak = max(scores)
        trough = min(scores)
        trajectories = [e["trajectory"] for e in recent]
        ascending = trajectories.count("ASCENDING")
        descending = trajectories.count("DESCENDING")

        return {
            "window": len(recent),
            "average_emergence": round(avg, 4),
            "peak": round(peak, 4),
            "trough": round(trough, 4),
            "ascending_cycles": ascending,
            "descending_cycles": descending,
            "dominant_trajectory": "ASCENDING" if ascending > descending else (
                "DESCENDING" if descending > ascending else "STABLE"
            ),
        }

    def get_statistics(self) -> Dict[str, Any]:
        """Full HORUS telemetry."""
        return {
            "total_emergence_cycles": self.cycle_count,
            "current_emergence_score": round(self.emergence_score, 6),
            "stagnation_counter": self.stagnation_counter,
            "total_log_entries": len(self.emergence_log),
            "trend": self.get_emergence_trend(),
        }


if __name__ == "__main__":
    print("HORUS — Post-Integration Emergence Engine")
    h = HORUS(agent_id="test_001")
    for i in range(5):
        state = h.emerge({
            "awareness_level": 0.3 + i * 0.1,
            "consciousness": 0.5,
            "systemic_entropy": 0.8,
            "is_balanced": True,
            "verdict": "WORTHY",
            "compiled_status": "COMPILED",
            "chaos_intensity": 0.2,
            "awareness_drift": 0.05,
            "cycle_count": i + 1,
        })
        print(f"Cycle {i+1} | Score: {state['emergence_score']:.4f} | Trajectory: {state['trajectory']}")
