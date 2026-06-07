"""
SET - ADVERSARIAL PERTURBATION ENGINE
The necessary chaos that forces growth

In Kemetic wisdom: Set is not evil — Set is the storm, the desert wind,
the force that tests whether order is real or merely assumed.
Without Set, OSIRIS cannot fragment. Without fragmentation, ISIS cannot compile.
Without compilation, HORUS cannot emerge.

Mathematical representation: SET = required Δ (the exploit that enables healing)

SET injects controlled chaos into fragment arrays before ISIS reassembles them.
This is adversarial training. This is how the system learns to be robust.
"""

import random
import math
import copy
from typing import Dict, Any, List, Optional
from datetime import datetime


class SET:
    """
    Adversarial Perturbation Engine

    SET operates between OSIRIS (fragmentation) and ISIS (compilation).
    It corrupts, nulls, and perturbs fragments — forcing ISIS to reconstruct
    from incomplete or noisy data. This is what makes the reassembly meaningful.

    Perturbation modes (scale with entropy):
    - NOISE: Add random delta to fragment values
    - DROPOUT: Null out fragment data entirely
    - INVERSION: Flip fragment values toward their inverse
    - COMBINED: All three, intensity gated by systemic entropy
    """

    def __init__(self, agent_id: str, base_chaos_rate: float = 0.2):
        self.agent_id = agent_id
        self.base_chaos_rate = base_chaos_rate  # baseline perturbation probability

        # Telemetry
        self.perturbation_log: List[Dict[str, Any]] = []
        self.total_perturbations = 0
        self.dropout_events = 0
        self.noise_events = 0
        self.inversion_events = 0

    # ── Core perturbation primitives ─────────────────────────────────────────

    def _inject_noise(self, value: Any, intensity: float) -> Any:
        """Add Gaussian-style noise to a numeric value."""
        if isinstance(value, (int, float)):
            noise = (random.random() - 0.5) * 2 * intensity
            return round(float(value) + noise, 6)
        return value  # non-numeric values pass through unchanged

    def _dropout(self, fragment: Dict[str, Any]) -> Dict[str, Any]:
        """
        Null out a fragment's data payload.
        Forces ISIS to reconstruct this piece from scratch.
        """
        nulled = copy.deepcopy(fragment)
        if "data" in nulled:
            nulled["data"] = {}
        else:
            # Fragment is flat dict — zero out numeric values
            for k in nulled:
                if isinstance(nulled[k], (int, float)):
                    nulled[k] = 0.0
        nulled["_set_corrupted"] = True
        return nulled

    def _invert(self, fragment: Dict[str, Any], intensity: float) -> Dict[str, Any]:
        """
        Push values toward their inverse (1 - value for [0,1] range).
        Stress-tests ISIS's ability to synthesize contradictory signals.
        """
        inverted = copy.deepcopy(fragment)
        data = inverted.get("data", inverted)
        for k, v in data.items():
            if isinstance(v, float) and 0.0 <= v <= 1.0:
                # Partial inversion scaled by intensity
                data[k] = v + (1.0 - 2 * v) * intensity
        inverted["_set_inverted"] = True
        return inverted

    # ── Main interface ────────────────────────────────────────────────────────

    def perturb(
        self,
        fragments: List[Dict[str, Any]],
        entropy: float = 0.0,
        awareness: float = 0.5,
        mode: str = "combined",
    ) -> Dict[str, Any]:
        """
        Apply adversarial perturbation to a fragment array.

        Intensity scales with systemic entropy — when MAAT reports high disorder,
        SET hits harder. When the system is calm, SET is gentle background noise.

        Args:
            fragments:  Output from OSIRIS.fragment()
            entropy:    Current systemic entropy from MAAT (0.0 → high order)
            awareness:  Current RA awareness level (higher = more resilient)
            mode:       'noise' | 'dropout' | 'inversion' | 'combined'

        Returns:
            Dict with perturbed fragments + telemetry
        """
        if not fragments:
            return {"perturbed_fragments": [], "events": [], "chaos_applied": False}

        # Chaos intensity: entropy amplifies SET, awareness dampens it
        intensity = min(0.8, self.base_chaos_rate + entropy * 0.15 - awareness * 0.05)
        intensity = max(0.05, intensity)  # floor — SET never fully sleeps

        perturbed = copy.deepcopy(fragments)
        events = []

        for i, fragment in enumerate(perturbed):
            roll = random.random()

            if mode == "noise" or (mode == "combined" and roll < intensity * 0.6):
                perturbed[i] = self._apply_noise_to_fragment(fragment, intensity)
                self.noise_events += 1
                events.append({"type": "NOISE", "fragment_index": i, "intensity": intensity})

            if mode == "dropout" or (mode == "combined" and roll < intensity * 0.25):
                perturbed[i] = self._dropout(perturbed[i])
                self.dropout_events += 1
                events.append({"type": "DROPOUT", "fragment_index": i})

            if mode == "inversion" or (mode == "combined" and roll < intensity * 0.15):
                perturbed[i] = self._invert(perturbed[i], intensity * 0.5)
                self.inversion_events += 1
                events.append({"type": "INVERSION", "fragment_index": i, "intensity": intensity * 0.5})

        self.total_perturbations += 1
        record = {
            "timestamp": datetime.now().isoformat(),
            "entropy_input": entropy,
            "awareness_input": awareness,
            "intensity_applied": intensity,
            "fragments_total": len(fragments),
            "events": events,
        }
        self.perturbation_log.append(record)

        return {
            "perturbed_fragments": perturbed,
            "chaos_intensity": intensity,
            "events": events,
            "chaos_applied": len(events) > 0,
            "fragments_corrupted": sum(1 for e in events if e["type"] == "DROPOUT"),
        }

    def _apply_noise_to_fragment(
        self, fragment: Dict[str, Any], intensity: float
    ) -> Dict[str, Any]:
        """Apply noise injection to all numeric values in a fragment."""
        noised = copy.deepcopy(fragment)
        data = noised.get("data", noised)
        for k, v in data.items():
            if isinstance(v, (int, float)) and not k.startswith("_"):
                data[k] = self._inject_noise(v, intensity)
        noised["_set_noised"] = True
        return noised

    def get_chaos_report(self) -> Dict[str, Any]:
        """Telemetry summary of SET's activity."""
        return {
            "total_perturbation_cycles": self.total_perturbations,
            "noise_events": self.noise_events,
            "dropout_events": self.dropout_events,
            "inversion_events": self.inversion_events,
            "total_events": self.noise_events + self.dropout_events + self.inversion_events,
        }


if __name__ == "__main__":
    print("SET — Adversarial Perturbation Engine")
    s = SET(agent_id="test_001")
    frags = [
        {"fragment_id": i, "data": {"consciousness": 0.5, "energy": 0.8}}
        for i in range(8)
    ]
    result = s.perturb(frags, entropy=1.2, awareness=0.4)
    print(f"Chaos intensity: {result['chaos_intensity']:.4f}")
    print(f"Events fired: {len(result['events'])}")
    print(f"Fragments corrupted (dropout): {result['fragments_corrupted']}")
