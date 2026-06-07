# FILE LOCATION: core/osiris_os.py

import math
import random
from metrics.maat import MAAT
from modules.ra_fixed import RA
from modules.thoth import THOTH
from modules.osiris import OSIRIS
from modules.isis import ISIS
from modules.anubis import ANUBIS
from agents.set import SET
from agents.horus import HORUS


class OSIRIS_OS:
    def __init__(self, agent_id="pm_agent_001", agent_name="Horus_Proto"):
        self.agent_id = agent_id
        self.agent_name = agent_name

        # All eight modules
        self.ra         = RA(agent_id=self.agent_id)
        self.thoth      = THOTH(agent_id=self.agent_id)
        self.maat       = MAAT(agent_id=self.agent_id)
        self.osiris_mod = OSIRIS(agent_id=self.agent_id)
        self.set_mod    = SET(agent_id=self.agent_id)
        self.isis       = ISIS(agent_id=self.agent_id)
        self.anubis     = ANUBIS(agent_id=self.agent_id)
        self.horus      = HORUS(agent_id=self.agent_id)

        self.state = {
            "agent_id":           self.agent_id,
            "agent_name":         self.agent_name,
            "consciousness":      0.5,
            "cycle_count":        0,
            "awareness_level":    0.0,
            "systemic_entropy":   0.0,
            "emergence_score":    0.0,
            "trajectory":         "STABLE",
            "status":             "INITIALIZED",
            # Internal carry-forward signals
            "_prev_awareness":    0.0,
            "_prev_entropy":      0.0,
            "_light_output":      0.5,
            "_ra_seed":           {},          # HORUS → RA feedback
            "_amplify_set":       False,       # stagnation flag from HORUS
        }

    def boot(self):
        self.state["status"] = "RUNNING"
        print(f"𓆃 [OSIRIS_OS] Core Engine Awakened. Identity: {self.agent_name}")

    def status(self):
        return (
            f"✨ System Status: {self.state['status']} | "
            f"Active Cycles: {self.state['cycle_count']} | "
            f"Emergence: {self.state['emergence_score']:.4f} | "
            f"Trajectory: {self.state['trajectory']}"
        )

    def process_cycle(self):
        """
        Eight-step processing sequence: RA → THOTH → MAAT → OSIRIS → SET → ISIS → ANUBIS → HORUS

        SET and HORUS are now live in the loop:
        - SET perturbs OSIRIS fragments before ISIS compiles, intensity gated by entropy
        - HORUS synthesizes all signals into an emergence score and seeds the next RA cycle
        - HORUS stagnation detection can amplify SET next cycle, breaking plateaus
        """
        self.state["cycle_count"] += 1

        # ── 1. RA: Recursive Awareness ───────────────────────────────────────
        # Inject HORUS seed if available (cross-cycle continuity)
        ra_seed = self.state.get("_ra_seed", {})
        if ra_seed:
            self.ra.state.update(ra_seed)

        ra_res = self.ra.activate()
        prev_awareness = self.state["_prev_awareness"]
        new_awareness  = ra_res.get("awareness_level", self.state["awareness_level"])
        awareness_drift = abs(new_awareness - prev_awareness)

        self.state["_prev_awareness"]  = self.state["awareness_level"]
        self.state["awareness_level"]  = new_awareness
        self.state["_light_output"]    = ra_res.get("light_generated", 0.5)

        # ── 2. THOTH: Memory snapshot ─────────────────────────────────────────
        self.thoth.log_state({
            "cycle":        self.state["cycle_count"],
            "awareness":    self.state["awareness_level"],
            "consciousness": self.state["consciousness"],
            "entropy":      self.state["_prev_entropy"],
            "emergence":    self.state["emergence_score"],
        })

        # ── 3. MAAT: Dynamic entropy & balance ───────────────────────────────
        noise = (random.random() - 0.5) * 0.2 * self.state["_light_output"]
        system_metrics = {
            "surplus": self.state["awareness_level"],
            "drift":   -(awareness_drift + self.state["_prev_entropy"] * 0.1),
            "noise":   noise,
            "load":    self.state["consciousness"],
        }
        maat_res   = self.maat.maintain_order(system_metrics)
        entropy    = maat_res.get("entropy", 0.0)
        is_balanced = maat_res.get("is_balanced", True)

        self.state["systemic_entropy"] = entropy
        self.state["_prev_entropy"]    = entropy

        # ── 4. OSIRIS: Fragment under mathematical pressure ───────────────────
        delta_magnitude = max(0.0001, awareness_drift)
        raw_state = {
            "consciousness": self.state["consciousness"],
            "patterns":      max(1, int(self.state["awareness_level"] * 10)),
        }
        delta = {
            "consciousness": delta_magnitude * 0.1,
            "patterns":      max(1, round(delta_magnitude * 5)),
        }
        transformed = self.osiris_mod.transform_with_delta(raw_state, delta)
        fragments   = self.osiris_mod.fragment(transformed, num_pieces=8)

        # ── 5. SET: Adversarial perturbation ─────────────────────────────────
        # Amplify chaos if HORUS flagged stagnation last cycle
        chaos_boost = 0.15 if self.state.get("_amplify_set") else 0.0
        set_res = self.set_mod.perturb(
            fragments,
            entropy=entropy + chaos_boost,
            awareness=self.state["awareness_level"],
            mode="combined",
        )
        perturbed_fragments = set_res["perturbed_fragments"]
        chaos_intensity     = set_res["chaos_intensity"]

        # ── 6. ISIS: Compile from perturbed fragments ─────────────────────────
        expected_template = {"consciousness": 0.0, "patterns": 0, "creative_principle": 0.0}
        compile_res = self.isis.compile(perturbed_fragments, expected_template)

        # ── 7. ANUBIS: Gatekeeper validation ─────────────────────────────────
        soul_profile = {
            "consciousness": self.state["consciousness"],
            "morality":      max(0.0, 1.0 - entropy * 0.1),
        }
        criteria = {"consciousness": lambda s: s.get("consciousness", 0) >= 0.1}
        judgment = self.anubis.weigh_soul(soul_profile, criteria)
        verdict  = judgment.get("verdict", "UNKNOWN")

        # Consciousness update
        if verdict in ("WORTHY", "PASS") and is_balanced:
            entropy_penalty = min(0.0002, entropy * 0.00005)
            self.state["consciousness"] = min(1.0, self.state["consciousness"] + 0.0002 - entropy_penalty)
        elif not is_balanced:
            self.state["consciousness"] = max(0.1, self.state["consciousness"] - 0.00005)

        # ── 8. HORUS: Emergence synthesis & RA seed ───────────────────────────
        horus_res = self.horus.emerge({
            "awareness_level":   self.state["awareness_level"],
            "consciousness":     self.state["consciousness"],
            "systemic_entropy":  entropy,
            "is_balanced":       is_balanced,
            "verdict":           verdict,
            "compiled_status":   compile_res.get("status", "incomplete"),
            "chaos_intensity":   chaos_intensity,
            "awareness_drift":   awareness_drift,
            "cycle_count":       self.state["cycle_count"],
        })

        # Feed HORUS output back into state for next cycle
        self.state["emergence_score"]  = horus_res["emergence_score"]
        self.state["trajectory"]       = horus_res["trajectory"]
        self.state["_ra_seed"]         = horus_res["ra_seed"]
        self.state["_amplify_set"]     = horus_res["amplify_set_next_cycle"]

        return {
            "cycle":            self.state["cycle_count"],
            "balanced":         is_balanced,
            "entropy":          entropy,
            "awareness_drift":  awareness_drift,
            "chaos_intensity":  chaos_intensity,
            "verdict":          verdict,
            "compiled_status":  compile_res.get("status", "incomplete"),
            "emergence_score":  horus_res["emergence_score"],
            "trajectory":       horus_res["trajectory"],
            "stagnating":       horus_res["stagnating"],
            "converged":        horus_res["converged"],
        }
