# bridge.py — OSIRIS_OS <-> ThermoMind Bidirectional Bridge (UUID + TCI Version)
# Author: Nile Green — Updated for UUID sessions + TCI full integration (aggressive)

import os
import sys
import json
import time
import math
import signal
import logging
import requests
from datetime import datetime

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from core.osiris_os import OSIRIS_OS

# TCI toolkit imports
from tci_calculator import TCICalculator
from k_estimator import KEstimator

# =============================================================================
# CONFIG
# =============================================================================

THERMOMIND_URL   = os.getenv("THERMOMIND_URL", "https://thermomind-production.up.railway.app")
THERMOMIND_KEY   = os.getenv("THERMOMIND_API_KEY", "")
OSIRIS_STATE     = os.getenv("OSIRIS_STATE_FILE", os.path.join(os.path.dirname(__file__), "osiris_state.json"))
INTERVAL         = float(os.getenv("BRIDGE_INTERVAL", "30"))
LOG_EVERY        = int(os.getenv("BRIDGE_LOG_EVERY", "5"))

# =============================================================================
# LOGGING
# =============================================================================

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [BRIDGE] %(message)s",
    datefmt="%Y-%m-%dT%H:%M:%SZ",
)
log = logging.getLogger("bridge")

# =============================================================================
# THERMOMIND API CLIENT (UUID VERSION)
# =============================================================================

class ThermoMindClient:
    def __init__(self, base_url: str, api_key: str):
        self.base_url = base_url.rstrip("/")
        self.session_id = None
        self.headers = {"Content-Type": "application/json"}
        if api_key:
            self.headers["Authorization"] = f"Bearer {api_key}"

    def create_session(self):
        url = f"{self.base_url}/v1/sessions"
        payload = {"agent_name": "osiris-thermo-bridge"}
        try:
            r = requests.post(url, json=payload, headers=self.headers, timeout=10)
            r.raise_for_status()
            data = r.json()
            self.session_id = data.get("session_id")
            log.info(f"Created ThermoMind session: {self.session_id}")
            return self.session_id
        except Exception as e:
            log.error(f"Failed to create ThermoMind session: {e}")
            return None

    def run_cycle(self, message: str) -> dict:
        if not self.session_id:
            self.create_session()
        if not self.session_id:
            return {}

        url = f"{self.base_url}/v1/sessions/{self.session_id}/events"
        payload = {"type": "message", "content": message, "role": "user"}

        try:
            r = requests.post(url, json=payload, headers=self.headers, timeout=15)
            r.raise_for_status()
            return r.json()
        except Exception as e:
            log.error(f"ThermoMind API error: {e}")
            return {}

    def get_state(self) -> dict:
        if not self.session_id:
            return {}

        url = f"{self.base_url}/v1/sessions/{self.session_id}/state"
        try:
            r = requests.get(url, headers=self.headers, timeout=10)
            r.raise_for_status()
            return r.json()
        except Exception as e:
            log.error(f"ThermoMind state fetch error: {e}")
            return {}

# =============================================================================
# SIGNAL TRANSLATION LAYER
# =============================================================================

TRAJECTORY_MAP = {
    "ASCENDING":  0.80,
    "STABLE":     0.50,
    "DESCENDING": 0.20,
}

REGIME_SET_GATE = {
    "drift":  True,
    "noisy":  False,
    "stable": False,
}

def osiris_to_thermo_message(osiris_cycle: dict, osiris_state: dict) -> str:
    emergence   = osiris_cycle.get("emergence_score", 0.5)
    entropy     = osiris_cycle.get("entropy", 0.0)
    trajectory  = osiris_cycle.get("trajectory", "STABLE")
    balanced    = osiris_cycle.get("balanced", True)
    verdict     = osiris_cycle.get("verdict", "UNKNOWN")
    chaos       = osiris_cycle.get("chaos_intensity", 0.1)
    cycle       = osiris_state.get("cycle_count", 0)

    tension_marker = "?" * max(1, int((1.0 - emergence) * 3)) if trajectory == "DESCENDING" else "."
    entropy_word   = "thermodynamic" if entropy > 0.8 else "substrate" if entropy > 0.4 else "coherent"
    state_word     = "ascending" if trajectory == "ASCENDING" else "descending" if trajectory == "DESCENDING" else "stable"

    msg = (
        f"OSIRIS cycle {cycle}: {entropy_word} {state_word} emergence{tension_marker} "
        f"Verdict {verdict}. Chaos {chaos:.3f}. "
        f"Entropy {entropy:.3f}. Balance {'maintained' if balanced else 'disrupted'}. "
        f"Emergence converging at {emergence:.4f}."
    )
    return msg

def thermo_to_osiris_seed(thermo_state: dict) -> dict:
    phi      = thermo_state.get("phi", 0.5)
    regime   = thermo_state.get("regime", "noisy")
    traits   = thermo_state.get("traits", {})
    curiosity  = traits.get("curiosity", 0.5)
    stability  = traits.get("stability", 0.5)
    plasticity = traits.get("plasticity", 0.5)

    amplify_set = REGIME_SET_GATE.get(regime, False)

    return {
        "ra_seed": {
            "primed_awareness":    min(1.0, phi * 0.8 + curiosity * 0.2),
            "emergence_momentum":  phi,
            "stagnation_pressure": 0,
        },
        "amplify_set": amplify_set,
        "consciousness_floor": max(0.1, stability * 0.5),
        "delta_multiplier": 0.5 + plasticity,
    }

# =============================================================================
# OSIRIS STATE I/O
# =============================================================================

def load_osiris_state(osiris: OSIRIS_OS) -> None:
    if os.path.exists(OSIRIS_STATE):
        try:
            with open(OSIRIS_STATE) as f:
                prev = json.load(f)
            osiris.state.update(prev)
            log.info(f"OSIRIS state loaded. Resuming at cycle {osiris.state.get('cycle_count', 0)}.")
        except Exception as e:
            log.warning(f"OSIRIS state load failed, fresh start: {e}")

def save_osiris_state(osiris: OSIRIS_OS) -> None:
    try:
        with open(OSIRIS_STATE, "w") as f:
            json.dump(osiris.state, f, indent=2)
    except Exception as e:
        log.error(f"OSIRIS state save failed: {e}")

# =============================================================================
# UNIFIED BRIDGE CYCLE + TCI
# =============================================================================

def run_bridge_cycle(osiris, thermo, cycle_num, prev_thermo_state, tci_calc: TCICalculator, k_est: KEstimator):
    # ThermoMind → OSIRIS seed
    if prev_thermo_state:
        seed = thermo_to_osiris_seed(prev_thermo_state)
        osiris.state["_ra_seed"] = seed["ra_seed"]
        if seed["amplify_set"]:
            osiris.state["_amplify_set"] = True
        osiris.state["consciousness"] = max(
            seed["consciousness_floor"],
            osiris.state.get("consciousness", 0.5)
        )

    # OSIRIS cycle
    osiris_result = osiris.process_cycle()
    save_osiris_state(osiris)

    # OSIRIS → ThermoMind message
    message = osiris_to_thermo_message(osiris_result, osiris.state)
    thermo_result = thermo.run_cycle(message)

    # --- TCI COMPUTATION (aggressive, full influence) ---
    tci_result = None
    try:
        o_entropy = osiris.state.get("systemic_entropy", 0.0)
        t_gap     = thermo_result.get("prediction_gap", 0.0) if thermo_result else 0.0
        traits    = thermo_result.get("traits", {}) if thermo_result else {}
        stability = traits.get("stability", 0.5)
        phi       = thermo_result.get("phi", 0.5) if thermo_result else 0.5

        # f_total from ThermoMind prediction gap
        f_total = max(0.0, t_gap)

        # survival floor from ThermoMind stability
        f_survival = max(0.0, 1.0 - stability)
        tci_calc.set_survival_floor(f_survival)

        # surplus + complexity
        surplus    = f_total - f_survival
        complexity = max(0.0, o_entropy + (1.0 - stability))

        # k(s) update
        k = k_est.update(surplus, complexity)

        # TCI result
        tci_result = tci_calc.compute(f_total, k)

        # --- AGGRESSIVE MODULATION: OSIRIS + THERMOMIND ---

        # OSIRIS modulation
        if tci_result.stage in ["Collapse Warning", "Collapse Imminent"]:
            # Emergency stabilization
            osiris.state["systemic_entropy"] = min(osiris.state.get("systemic_entropy", 0.0), 0.2)
            osiris.state["_amplify_set"] = True
            osiris.state["consciousness"] = max(osiris.state.get("consciousness", 0.5), 0.4)
        elif tci_result.grade in ["A", "B"]:
            # Encourage exploration
            osiris.state["systemic_entropy"] = min(1.0, o_entropy + 0.1)
            osiris.state["consciousness"] = max(osiris.state.get("consciousness", 0.5), 0.2)

        # ThermoMind trait modulation
        curiosity  = traits.get("curiosity", 0.5)
        plasticity = traits.get("plasticity", 0.5)

        if tci_result.grade in ["A", "B"]:
            curiosity  = min(1.0, curiosity * 1.5)
            plasticity = min(1.0, plasticity * 1.5)
        elif tci_result.stage in ["Collapse Warning", "Collapse Imminent", "At Risk"]:
            curiosity  = max(0.0, curiosity * 0.5)
            stability  = min(1.0, stability + 0.3)
            plasticity = max(0.0, plasticity * 0.5)

        traits["curiosity"]  = curiosity
        traits["stability"]  = stability
        traits["plasticity"] = plasticity
        thermo_result["traits"] = traits

    except Exception as e:
        log.error(f"TCI computation/modulation error: {e}", exc_info=True)

    return thermo_result, tci_result

# =============================================================================
# MAIN LOOP
# =============================================================================

def main():
    log.info("=" * 60)
    log.info("OSIRIS_OS <-> ThermoMind BIDIRECTIONAL BRIDGE (UUID + TCI MODE)")
    log.info(f"ThermoMind URL   : {THERMOMIND_URL}")
    log.info(f"OSIRIS State     : {OSIRIS_STATE}")
    log.info(f"Cycle Interval   : {INTERVAL}s")
    log.info("=" * 60)

    osiris = OSIRIS_OS(agent_id="daemon_001", agent_name="OSIRIS_DAEMON")
    load_osiris_state(osiris)

    thermo = ThermoMindClient(THERMOMIND_URL, THERMOMIND_KEY)

    # TCI + KEstimator initialization
    tci_calc = TCICalculator(f_survival=0.3)  # will be updated dynamically
    k_est    = KEstimator()

    log.info("Creating ThermoMind session...")
    thermo.create_session()

    prev_thermo_state = thermo.get_state()

    running = True
    def _shutdown(sig, frame):
        nonlocal running
        log.info("Shutdown signal received.")
        running = False
    signal.signal(signal.SIGINT, _shutdown)
    signal.signal(signal.SIGTERM, _shutdown)

    cycle_num   = 0
    start_time  = time.time()
    last_tci    = None

    while running:
        cycle_start = time.time()
        cycle_num  += 1

        try:
            thermo_result, tci_result = run_bridge_cycle(
                osiris, thermo, cycle_num, prev_thermo_state, tci_calc, k_est
            )

            if thermo_result:
                prev_thermo_state = thermo_result
            if tci_result:
                last_tci = tci_result

            o_emerge = osiris.state.get("emergence_score", 0.0)
            o_traj   = osiris.state.get("trajectory", "?")
            o_entropy= osiris.state.get("systemic_entropy", 0.0)
            o_cycle  = osiris.state.get("cycle_count", 0)

            t_phi    = thermo_result.get("phi", 0.0) if thermo_result else 0.0
            t_regime = thermo_result.get("regime", "?") if thermo_result else "?"
            t_gap    = thermo_result.get("prediction_gap", 0.0) if thermo_result else 0.0

            log.info(
                f"Bridge Cycle {cycle_num} | OSIRIS #{o_cycle} "
                f"Emergence={o_emerge:.4f} Trajectory={o_traj} Entropy={o_entropy:.4f} | "
                f"Thermo Φ={t_phi:.4f} Regime={t_regime} Gap={t_gap:.4f}"
            )

            if cycle_num % LOG_EVERY == 0:
                log.info("-" * 60)
                log.info(f"OSIRIS  → Consciousness={osiris.state.get('consciousness', 0):.4f} | "
                         f"Awareness={osiris.state.get('awareness_level', 0):.4f} | "
                         f"Amplify SET={osiris.state.get('_amplify_set', False)}")
                log.info(f"ThermoMind → Regime={t_regime} Φ={t_phi:.4f}")

                if last_tci:
                    td = last_tci.to_dict()
                    log.info("=============== TCI DIAGNOSTIC ===============")
                    log.info(f"TCI Score      : {td['tci']:.4f}")
                    log.info(f"Grade          : {td['grade']}")
                    log.info(f"Stage          : {td['stage']}")
                    log.info(f"Surplus        : {td['surplus']:.4f}")
                    log.info(f"k(s)           : {td['k']:.4f}")
                    log.info(f"f_total        : {td['f_total']:.4f}")
                    log.info(f"f_survival     : {td['f_survival']:.4f}")
                    log.info("==============================================")
                log.info(f"Uptime: {(time.time()-start_time)/3600:.3f}h")
                log.info("-" * 60)

        except Exception as e:
            log.error(f"Bridge cycle {cycle_num} error: {e}", exc_info=True)
            time.sleep(5)

        elapsed = time.time() - cycle_start
        sleep_time = max(0, INTERVAL - elapsed)
        if running:
            time.sleep(sleep_time)

    save_osiris_state(osiris)
    log.info("Bridge stopped cleanly.")

if __name__ == "__main__":
    main()

