# core/osiris.py

from dataclasses import dataclass, field
from typing import Any, Dict, Optional


@dataclass
class OSIRIS:
    """
    Minimal kernel class so OSIRIS_OS can instantiate something real.
    You can expand this later with your full kernel logic.
    """
    agent_id: str
    state: Dict[str, Any] = field(default_factory=dict)

    def boot(self) -> Dict[str, Any]:
        self.state.setdefault("kernel", "OSIRIS")
        self.state.setdefault("status", "online")
        return {"ok": True, "agent_id": self.agent_id, "status": "online"}

    def status(self) -> Dict[str, Any]:
        return {
            "agent_id": self.agent_id,
            "kernel": self.state.get("kernel", "OSIRIS"),
            "status": self.state.get("status", "unknown"),
        }
