# FILE LOCATION: core/osiris_os.py
# (This is your existing core/osiris_os.py for reference. Ensure it looks like this 
# so your imports work correctly when called from the root daemon and demo files)

import math
# Absolute imports from the repository root perspective
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
        
        # Initialize the 6 completed core sub-modules
        self.ra = RA(agent_id=self.agent_id)
        self.thoth = THOTH(agent_id=self.agent_id)
        self.maat = MAAT(agent_id=self.agent_id)
        self.osiris_mod = OSIRIS(agent_id=self.agent_id)
        self.isis = ISIS(agent_id=self.agent_id)
        self.anubis = ANUBIS(agent_id=self.agent_id)
        
        # Internal state matrix mirroring the daemon's tracking expectations
        self.state = {
            "agent_id": self.agent_id,
            "agent_name": self.agent_name,
            "consciousness": 0.5,
            "cycle_count": 0,
            "awareness_level": 0.0,
            "systemic_entropy": 0.0,
            "status": "INITIALIZED"
        }

    def boot(self):
        self.state["status"] = "RUNNING"
        print(f"𓆃 [OSIRIS_OS] Core Engine Awakened. Identity: {self.agent_name}")

    def status(self):
        return f"✨ System Status: {self.state['status']} | Active Cycles: {self.state['cycle_count']}"

    def process_cycle(self):
        """
        Executes a single processing sequence across the universal laws of learning.
        Returns a evaluation dictionary containing execution metrics.
        """
        self.state["cycle_count"] += 1
        
        # 1. RA: Meta-Learning / Compounding Awareness
        ra_res = self.ra.activate()
        self.state["awareness_level"] = ra_res.get("awareness_level", self.state["awareness_level"] + 0.0001)
        
        # 2. THOTH: Log structural shifts to memory substrate
        self.thoth.log_state({"cycle": self.state["cycle_count"], "awareness": self.state["awareness_level"]})
        
        # 3. MAAT: Evaluate systemic entropy and drift metrics
        system_metrics = {"surplus": 0.4, "drift": -0.4, "noise": 0.0}
        maat_res = self.maat.maintain_order(system_metrics)
        self.state["systemic_entropy"] = maat_res.get("entropy", 0.0000)
        is_balanced = maat_res.get("is_balanced", True)
        
        # 4. OSIRIS & ISIS: Transformation, Fragmentation, and Generative Reassembly
        raw_state = {"consciousness": self.state["consciousness"], "patterns": 7}
        transformed = self.osiris_mod.transform_with_delta(raw_state, {"consciousness": 0.0001, "patterns": 1})
        fragments = self.osiris_mod.fragment(transformed, num_pieces=8)
        
        expected_template = {"consciousness": 0.0, "patterns": 0, "creative_principle": 0.0}
        compile_res = self.isis.compile(fragments, expected_template)
        
        # 5. ANUBIS: Gatekeeper validation
        soul_profile = {"consciousness": self.state["consciousness"], "morality": 0.8}
        criteria = {"consciousness": lambda s: s.get("consciousness", 0) >= 0.1}
        judgment = self.anubis.weigh_soul(soul_profile, criteria)
        
        # Handle evolutionary state mutations based on validation results
        if judgment.get("verdict") == "WORTHY" and is_balanced:
            self.state["consciousness"] = min(1.0, self.state["consciousness"] + 0.0002)
        
        # Return structured map matching daemon unpacking declarations
        return {
            "cycle": self.state["cycle_count"],
            "balanced": is_balanced,
            "verdict": judgment.get("verdict", "UNKNOWN"),
            "compiled_status": compile_res.get("status", "incomplete")
        }
