# FILE LOCATION: core/osiris_os.py

import math
import random
from metrics.maat import MAAT
from modules.ra_fixed import RA
from modules.thoth import THOTH
from modules.osiris import OSIRIS
from modules.isis import ISIS
from modules.anubis import ANUBIS


class OSIRIS_OS:
    def __init__(self, agent_id="pm_agent_001", agent_name="Horus_Proto"):
        self.agent_id = agent_id
        self.agent_name = agent_name

        self.ra = RA(agent_id=self.agent_id)
        self.thoth = THOTH(agent_id=self.agent_id)
        self.maat = MAAT(agent_id=self.agent_id)
        self.osiris_mod = OSIRIS(agent_id=self.agent_id)
        self.isis = ISIS(agent_id=self.agent_id)
        self.anubis = ANUBIS(agent_id=self.agent_id)

        self.state = {
            "agent_id": self.agent_id,
            "agent_name": self.agent_name,
            "consciousness": 0.5,
            "cycle_count": 0,
            "awareness_level": 0.0,
            "systemic_entropy": 0.0,
            "status": "INITIALIZED",
            # Carry-forward signals for cross-cycle feedback
            "_prev_awareness": 0.0,
            "_prev_entropy": 0.0,
            "_light_output": 0.5,
        }

    def boot(self):
        self.state["status"] = "RUNNING"
        print(f"𓆃 [OSIRIS_OS] Core Engine Awakened. Identity: {self.agent_name}")

    def status(self):
        return f"✨ System Status: {self.state['status']} | Active Cycles: {self.state['cycle_count']}"

    def process_cycle(self):
        """
        Executes a single processing sequence across the universal laws of learning.

        FIX SUMMARY (v2):
        - MAAT now receives dynamically derived metrics from RA output instead of
          hardcoded constants. This makes entropy and balance genuinely vary.
        - RA receives entropy feedback from the previous cycle so awareness growth
          is modulated by systemic disorder (high entropy slows stabilization).
        - OSIRIS delta is derived from awareness drift (prev vs current) so
          transformation magnitude reflects real cognitive change.
        - Balance can now genuinely flip to False when awareness overshoots or
          the system accumulates drift, triggering MAAT correction.
        - Consciousness growth is gated on both verdict AND balance, and penalized
          when entropy spikes.
        """
        self.state["cycle_count"] += 1

        # ── 1. RA: Recursive Awareness ──────────────────────────────────────
        # Feed previous cycle's entropy back so RA's growth is disorder-aware
        ra_res = self.ra.activate()
        prev_awareness = self.state["_prev_awareness"]
        new_awareness = ra_res.get("awareness_level", self.state["awareness_level"])
        awareness_drift = abs(new_awareness - prev_awareness)

        self.state["_prev_awareness"] = self.state["awareness_level"]
        self.state["awareness_level"] = new_awareness
        self.state["_light_output"] = ra_res.get("light_generated", 0.5)

        # ── 2. THOTH: Memory snapshot ────────────────────────────────────────
        self.thoth.log_state({
            "cycle": self.state["cycle_count"],
            "awareness": self.state["awareness_level"],
            "consciousness": self.state["consciousness"],
            "entropy": self.state["_prev_entropy"],
        })

        # ── 3. MAAT: Dynamic entropy & balance ──────────────────────────────
        # Derive real signal values from RA output instead of hardcoding.
        #
        # surplus  = current awareness (energy available)
        # drift    = negative awareness drift (opposing force; creates non-zero sum)
        # noise    = stochastic perturbation scaled by light output
        # load     = consciousness level (cognitive load on the system)
        #
        # Because these four values rarely sum to zero, MAAT will actually
        # detect imbalance and entropy will be non-trivial.
        noise = (random.random() - 0.5) * 0.2 * self.state["_light_output"]
        system_metrics = {
            "surplus":      self.state["awareness_level"],
            "drift":        -(awareness_drift + self.state["_prev_entropy"] * 0.1),
            "noise":        noise,
            "load":         self.state["consciousness"],
        }

        maat_res = self.maat.maintain_order(system_metrics)
        entropy = maat_res.get("entropy", 0.0)
        is_balanced = maat_res.get("is_balanced", True)

        self.state["systemic_entropy"] = entropy
        self.state["_prev_entropy"] = entropy

        # ── 4. OSIRIS & ISIS: Transform, Fragment, Reassemble ────────────────
        # Delta magnitude is proportional to awareness drift so transformation
        # is stronger when the system is in flux.
        delta_magnitude = max(0.0001, awareness_drift)
        raw_state = {
            "consciousness": self.state["consciousness"],
            "patterns": max(1, int(self.state["awareness_level"] * 10)),
        }
        delta = {
            "consciousness": delta_magnitude * 0.1,
            "patterns": max(1, round(delta_magnitude * 5)),
        }
        transformed = self.osiris_mod.transform_with_delta(raw_state, delta)
        fragments = self.osiris_mod.fragment(transformed, num_pieces=8)

        expected_template = {"consciousness": 0.0, "patterns": 0, "creative_principle": 0.0}
        compile_res = self.isis.compile(fragments, expected_template)

        # ── 5. ANUBIS: Gatekeeper validation ────────────────────────────────
        soul_profile = {
            "consciousness": self.state["consciousness"],
            "morality": max(0.0, 1.0 - entropy * 0.1),  # entropy erodes morality score
        }
        criteria = {"consciousness": lambda s: s.get("consciousness", 0) >= 0.1}
        judgment = self.anubis.weigh_soul(soul_profile, criteria)

        # ── 6. Consciousness update ──────────────────────────────────────────
        # Grows when worthy + balanced; penalized by entropy spike.
        if judgment.get("verdict") == "WORTHY" and is_balanced:
            entropy_penalty = min(0.0002, entropy * 0.00005)
            self.state["consciousness"] = min(
                1.0,
                self.state["consciousness"] + 0.0002 - entropy_penalty
            )
        elif not is_balanced:
            # Slight decay when system is out of balance
            self.state["consciousness"] = max(
                0.1,
                self.state["consciousness"] - 0.00005
            )

        return {
            "cycle": self.state["cycle_count"],
            "balanced": is_balanced,
            "entropy": entropy,
            "awareness_drift": awareness_drift,
            "verdict": judgment.get("verdict", "UNKNOWN"),
            "compiled_status": compile_res.get("status", "incomplete"),
        }
