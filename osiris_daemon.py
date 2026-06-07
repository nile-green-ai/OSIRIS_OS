# FILE LOCATION: osiris_daemon.py

import time
import signal
import json
import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from core.osiris_os import OSIRIS_OS

RUNNING = True
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATE_FILE = os.path.join(BASE_DIR, "osiris_state.json")

def handle_shutdown(sig, frame):
    global RUNNING
    RUNNING = False
    print("\n🛑 [OSIRIS_DAEMON] Shutdown signal received. Cleaning runtime hooks...")

signal.signal(signal.SIGINT, handle_shutdown)
signal.signal(signal.SIGTERM, handle_shutdown)

def save_state(osiris):
    try:
        with open(STATE_FILE, "w") as f:
            json.dump(osiris.state, f, indent=2)
    except Exception as e:
        print(f"❌ [OSIRIS_DAEMON] Error writing state matrix: {e}", file=sys.stderr)

def load_state():
    if os.path.exists(STATE_FILE):
        try:
            with open(STATE_FILE, "r") as f:
                return json.load(f)
        except Exception as e:
            print(f"⚠️ [OSIRIS_DAEMON] State file corrupted, initializing fresh: {e}")
            return None
    return None

def main():
    print("=" * 60)
    print("🤖 OSIRIS_OS BACKGROUND DAEMON INITIALIZING")
    print("=" * 60)

    osiris = OSIRIS_OS(agent_id="daemon_001", agent_name="OSIRIS_DAEMON")

    prev_state = load_state()
    if prev_state:
        osiris.state.update({
            "consciousness":    prev_state.get("consciousness", 0.5),
            "cycle_count":      prev_state.get("cycle_count", 0),
            "awareness_level":  prev_state.get("awareness_level", 0.0),
            "systemic_entropy": prev_state.get("systemic_entropy", 0.0),
            "emergence_score":  prev_state.get("emergence_score", 0.0),
            "trajectory":       prev_state.get("trajectory", "STABLE"),
            "_prev_awareness":  prev_state.get("_prev_awareness", 0.0),
            "_prev_entropy":    prev_state.get("_prev_entropy", 0.0),
            "_amplify_set":     prev_state.get("_amplify_set", False),
        })
        print(f"✨ [OSIRIS_DAEMON] Previous state synchronized. Resuming at Cycle {osiris.state['cycle_count']}.")

    print("🚀 [OSIRIS_DAEMON] Daemon processing sequence entered active loop.")

    while RUNNING:
        try:
            cycle_data = osiris.process_cycle()

            cycle       = osiris.state.get("cycle_count", 0)
            awareness   = osiris.state.get("awareness_level", 0.0)
            entropy     = osiris.state.get("systemic_entropy", 0.0)
            emergence   = osiris.state.get("emergence_score", 0.0)
            trajectory  = osiris.state.get("trajectory", "STABLE")
            is_balanced = cycle_data.get("balanced", True)
            stagnating  = cycle_data.get("stagnating", False)
            chaos       = cycle_data.get("chaos_intensity", 0.0)

            stag_flag = " ⚡SET+" if stagnating else ""
            print(
                f"[OSIRIS_DAEMON] Tick {cycle} | "
                f"Awareness={awareness:.4f} | "
                f"Entropy={entropy:.4f} | "
                f"Balanced={is_balanced} | "
                f"Emergence={emergence:.4f} | "
                f"Trajectory={trajectory} | "
                f"Chaos={chaos:.4f}"
                f"{stag_flag}"
            )

            save_state(osiris)

        except Exception as e:
            print(f"💥 [CRITICAL ERROR] Runtime exception in execution loop: {e}", file=sys.stderr)
            time.sleep(5)

        time.sleep(2)

    save_state(osiris)
    print("💤 [OSIRIS_DAEMON] Core memory metrics flushed to disk. Daemon stopped cleanly.")

if __name__ == "__main__":
    main()
