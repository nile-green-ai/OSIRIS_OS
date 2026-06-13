"""
bridge.py — OSIRIS_OS <-> ThermoMind Bidirectional Bridge
Author: Nile Green — PermaMind AI

Runs a unified cycle where both engines feed each other:

  OSIRIS emergence + entropy + trajectory → ThermoMind reality vector
  ThermoMind Φ + regime + curiosity      → OSIRIS RA seed + SET gate

Neither engine's internal code is modified.
This file is the handshake layer between them.

Environment variables:
  THERMOMIND_URL     — ThermoMind API base URL (default: Railway endpoint)
  THERMOMIND_API_KEY — API key if required
  THERMOMIND_AGENT   — agent ID for ThermoMind (default: thermomind-core)
  OSIRIS_STATE_FILE  — path to osiris_state.json (default: ./osiris_state.json)
  BRIDGE_INTERVAL    — seconds between unified cycles (default: 30)
  BRIDGE_LOG_EVERY   — log full state every N cycles (default: 5)
"""

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

# =============================================================================
# CONFIG
# =============================================================================

THERMOMIND_URL   = os.getenv("THERMOMIND_URL", "https://thermomind-production.up.railway.app")
THERMOMIND_KEY   = os.getenv("THERMOMIND_API_KEY", "")
THERMOMIND_AGENT = os.getenv("THERMOMIND_AGENT", "thermomind-core")
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
# THERMOMIND API CLIENT
# =============================================================================

class ThermoMindClient:
    def __init__(self, base_url: str, api_key: str, agent_id: str):
        self.base_url = base_url.rstrip("/")
        self.agent_id = agent_id
        self.headers = {"Content-Type": "application/json"}
        if api_key:
            self.headers["Authorization"] = f"Bearer {api_key}"

    def run_cycle(self, message: str) -> dict:
        """Fire a ThermoMind cycle with a text message. Returns state dict."""
        url = f"{self.base_url}/v1/sessions/{self.agent_id}/events"
        payload = {"type": "message", "content": message, "role": "user"}
        try:
            r = requests.post(url, json=payload, headers=self.headers, timeout=15)
            r.raise_for_status()
            return r.json()
        except requests.RequestException as e:
            log.error(f"ThermoMind API error: {e}")
            return {}

    def get_state(self) -> dict:
        """Fetch full ThermoMind state."""
        url = f"{self.base_url}/v1/sessions/{self.agent_id}/state"
        try:
            r = requests.get(url, headers=self.headers, timeout=10)
            r.raise_for_status()
            return r.json()
        except requests.RequestException as e:
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
    "drift":  True,   # high novelty → amplify SET
    "noisy":  False,  # normal
    "stable": False,  # consolidated → dampen SET
}


def osiris_to_thermo_message(osiris_cycle: dict, osiris_state: dict) -> str:
    """
    Convert OSIRIS cycle output into a descriptive message for ThermoMind.
    ThermoMind's text_to_reality_vector will parse this into [Φ₀, Φ₁, Φ₂].

    We encode the three key signals in the message structure itself:
    - Interrogative tension (Φ₀) ← trajectory urgency
    - Mnemonic phase (Φ₁)       ← entropy level
    - Affective energy (Φ₂)     ← emergence score
    """
    emergence   = osiris_cycle.get("emergence_score", 0.5)
    entropy     = osiris_cycle.get("entropy", 0.0)
    trajectory  = osiris_cycle.get("trajectory", "STABLE")
    balanced    = osiris_cycle.get("balanced", True)
    verdict     = osiris_cycle.get("verdict", "UNKNOWN")
    chaos       = osiris_cycle.get("chaos_intensity", 0.1)
    cycle       = osiris_state.get("cycle_count", 0)

    # Build message with structural properties that encode the signals:
    # Questions → high Φ₀ (interrogative tension) when system is stressed
    # Word complexity → Φ₁ (mnemonic phase) reflects entropy
    # Character density → Φ₂ (affective energy) reflects emergence

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
    """
    Convert ThermoMind state into OSIRIS RA seed + SET gate signals.

    ThermoMind Φ        → primed_awareness for RA
    ThermoMind regime   → amplify_set flag for SET
    ThermoMind curiosity → delta magnitude multiplier
    ThermoMind stability → consciousness floor
    """
    phi      = thermo_state.get("phi", 0.5)
    regime   = thermo_state.get("regime", "noisy")
    traits   = thermo_state.get("traits", {})
    curiosity  = traits.get("curiosity", 0.5)
    stability  = traits.get("stability", 0.5)
    plasticity = traits.get("plasticity", 0.5)

    amplify_set = REGIME_SET_GATE.get(regime, False)

    return {
        # RA seed — primes awareness at top of next OSIRIS cycle
        "ra_seed": {
            "primed_awareness":    min(1.0, phi * 0.8 + curiosity * 0.2),
            "emergence_momentum":  phi,
            "stagnation_pressure": 0,
        },
        # SET gate — ThermoMind drift regime forces chaos amplification
        "amplify_set": amplify_set,
        # Consciousness floor from ThermoMind stability
        "consciousness_floor": max(0.1, stability * 0.5),
        # Delta multiplier from plasticity
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
            osiris.state.update({
                "consciousness":    prev.get("consciousness", 0.5),
                "cycle_count":      prev.get("cycle_count", 0),
                "awareness_level":  prev.get("awareness_level", 0.0),
                "systemic_entropy": prev.get("systemic_entropy", 0.0),
                "emergence_score":  prev.get("emergence_score", 0.0),
                "trajectory":       prev.get("trajectory", "STABLE"),
                "_prev_awareness":  prev.get("_prev_awareness", 0.0),
                "_prev_entropy":    prev.get("_prev_entropy", 0.0),
                "_amplify_set":     prev.get("_amplify_set", False),
                "_ra_seed":         prev.get("_ra_seed", {}),
            })
            log.info(f"OSIRIS state loaded. Resuming at cycle {osiris.state['cycle_count']}.")
        except Exception as e:
            log.warning(f"OSIRIS state load failed, fresh start: {e}")


def save_osiris_state(osiris: OSIRIS_OS) -> None:
    try:
        with open(OSIRIS_STATE, "w") as f:
            json.dump(osiris.state, f, indent=2)
    except Exception as e:
        log.error(f"OSIRIS state save failed: {e}")

# =============================================================================
# UNIFIED BRIDGE CYCLE
# =============================================================================

def run_bridge_cycle(
    osiris: OSIRIS_OS,
    thermo: ThermoMindClient,
    cycle_num: int,
    prev_thermo_state: dict,
) -> dict:
    """
    One unified cycle:
    1. Inject ThermoMind signals into OSIRIS
    2. Run OSIRIS cycle
    3. Convert OSIRIS output to ThermoMind message
    4. Run ThermoMind cycle
    5. Return new ThermoMind state for next cycle
    """

    # ── Step 1: ThermoMind → OSIRIS ─────────────────────────────────────────
    if prev_thermo_state:
        seed = thermo_to_osiris_seed(prev_thermo_state)

        # Inject RA seed
        osiris.state["_ra_seed"]    = seed["ra_seed"]

        # ThermoMind drift regime can override OSIRIS SET amplification
        if seed["amplify_set"]:
            osiris.state["_amplify_set"] = True

        # Apply consciousness floor
        osiris.state["consciousness"] = max(
            seed["consciousness_floor"],
            osiris.state.get("consciousness", 0.5)
        )

    # ── Step 2: Run OSIRIS cycle ─────────────────────────────────────────────
    osiris_result = osiris.process_cycle()
    save_osiris_state(osiris)

    # ── Step 3: OSIRIS → ThermoMind message ──────────────────────────────────
    message = osiris_to_thermo_message(osiris_result, osiris.state)

    # ── Step 4: Run ThermoMind cycle ─────────────────────────────────────────
    thermo_result = thermo.run_cycle(message)

    return thermo_result

# =============================================================================
# MAIN LOOP
# =============================================================================

def main():
    log.info("=" * 60)
    log.info("OSIRIS_OS <-> ThermoMind BIDIRECTIONAL BRIDGE")
    log.info(f"ThermoMind URL   : {THERMOMIND_URL}")
    log.info(f"ThermoMind Agent : {THERMOMIND_AGENT}")
    log.info(f"OSIRIS State     : {OSIRIS_STATE}")
    log.info(f"Cycle Interval   : {INTERVAL}s")
    log.info("=" * 60)

    # Init OSIRIS
    osiris = OSIRIS_OS(agent_id="daemon_001", agent_name="OSIRIS_DAEMON")
    load_osiris_state(osiris)

    # Init ThermoMind client
    thermo = ThermoMindClient(THERMOMIND_URL, THERMOMIND_KEY, THERMOMIND_AGENT)

    # Fetch initial ThermoMind state to seed first cycle
    log.info("Fetching initial ThermoMind state...")
    prev_thermo_state = thermo.get_state()
    if prev_thermo_state:
        log.info(f"ThermoMind Φ={prev_thermo_state.get('phi', '?')} | Regime={prev_thermo_state.get('regime', '?')}")
    else:
        log.warning("Could not fetch ThermoMind state. First cycle will run OSIRIS-only seed.")

    # Graceful shutdown
    running = True
    def _shutdown(sig, frame):
        nonlocal running
        log.info("Shutdown signal received.")
        running = False
    signal.signal(signal.SIGINT, _shutdown)
    signal.signal(signal.SIGTERM, _shutdown)

    cycle_num   = 0
    start_time  = time.time()

    while running:
        cycle_start = time.time()
        cycle_num  += 1

        try:
            thermo_result = run_bridge_cycle(osiris, thermo, cycle_num, prev_thermo_state)

            if thermo_result:
                prev_thermo_state = thermo_result

            # ── Log ──────────────────────────────────────────────────────────
            o_emerge    = osiris.state.get("emergence_score", 0.0)
            o_traj      = osiris.state.get("trajectory", "?")
            o_entropy   = osiris.state.get("systemic_entropy", 0.0)
            o_cycle     = osiris.state.get("cycle_count", 0)
            t_phi       = thermo_result.get("phi", 0.0) if thermo_result else 0.0
            t_regime    = thermo_result.get("regime", "?") if thermo_result else "?"
            t_gap       = thermo_result.get("prediction_gap", 0.0) if thermo_result else 0.0
            t_mental    = thermo_result.get("mental_state", "?") if thermo_result else "?"

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
                log.info(f"ThermoMind → Mental State: {t_mental}")
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
