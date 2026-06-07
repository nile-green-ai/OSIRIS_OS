# FILE LOCATION: demo.py
# (Paste this into your root directory file)

import os
import sys

# Injection of system paths to guarantee nested module visibility 
# when running from the repository root folder configuration
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from core.osiris_os import OSIRIS_OS

def main():
    osiris = OSIRIS_OS(
        agent_id="pm_demo_001",
        agent_name="Nova"
    )

    if hasattr(osiris, "boot"):
        osiris.boot()
    else:
        print("OSIRIS_OS initialized")

    if hasattr(osiris, "status"):
        print(osiris.status())

if __name__ == "__main__":
    main()
