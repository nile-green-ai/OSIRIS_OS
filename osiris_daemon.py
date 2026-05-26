# osiris_daemon.py

import time
import signal
import json
import os
import sys
from osiris_os_evolved import OSIRIS_OS

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

    # Instantiate the evolutionary OS core
    osiris = OSIRIS_OS(agent_id="daemon_001", agent_name="OSIRIS_DAEMON")

    # Load and map historical persistent states
    prev_state = load_state()
    if prev_state:
        # Preserve runtime critical cycle statistics without overwriting core initializations
        osiris.state.update({
            "consciousness": prev_state.get("consciousness", 0.5),
            "cycle_count": prev_state.get("cycle_count", 0),
            "awareness_level": prev_state.get("awareness_level", 0.0),
            "systemic_entropy": prev_state.get("systemic_entropy", 0.0)
        })
        print(f"✨ [OSIRIS_DAEMON] Previous state synchronized. Resuming at Cycle {osiris.state['cycle_count']}.")

    print("🚀 [OSIRIS_DAEMON] Daemon processing sequence entered active loop.")

    while RUNNING:
        try:
            # Process cycle metrics and evaluate structural stability
            cycle_data = osiris.process_cycle()

            print(f"[OSIRIS_DAEMON] Tick {cycle_data['cycle']} | "
                  f"Awareness={osiris.state['awareness_level']:.4f} | "
                  f"Entropy={cycle_data['entropy']:.4f} | "
                  f"Balanced={cycle_data['balanced']}")

            # Periodically snapshot current data vectors
            save_state(osiris)
            
        except Exception as e:
            print(f"💥 [CRITICAL ERROR] Runtime exception in execution loop: {e}", file=sys.stderr)
            # Prevent rapid looping crashes from consuming maximum CPU cycles
            time.sleep(5)

        time.sleep(2)

    # Clean preservation phase upon loop breakage
    save_state(osiris)
    print("💤 [OSIRIS_DAEMON] Core memory metrics flushed to disk. Daemon stopped cleanly.")

if __name__ == "__main__":
    main()
