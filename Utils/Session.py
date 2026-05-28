import json
import os
from dataclasses import dataclass, field, asdict
from typing import List

_SESSIONS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "sessions")


def _session_path(ip: str, port: int) -> str:
    return os.path.join(_SESSIONS_DIR, f"{ip}_{port}.json")


@dataclass
class Session:
    ip: str = ""
    port: int = 0
    target_type: str = "socket"
    prefix: str = ""
    fuzz_amount: int = 100
    verbose: bool = False
    template: str = ""        # raw HTTP request with * placeholder (empty = socket mode)
    stage: str = "fuzz"
    fuzz_crash_at: int = 0
    offset: int = 0
    bad_bytes: List[str] = field(default_factory=lambda: ["00"])
    byte_string: str = field(default_factory=lambda: "".join(chr(b) for b in range(1, 256)))
    eip_value_clean: str = ""

    def save(self):
        os.makedirs(_SESSIONS_DIR, exist_ok=True)
        with open(_session_path(self.ip, self.port), "w", encoding="utf-8") as f:
            json.dump(asdict(self), f, indent=2, ensure_ascii=False)

    def delete(self):
        path = _session_path(self.ip, self.port)
        if os.path.exists(path):
            os.remove(path)

    @classmethod
    def load_for(cls, ip: str, port: int) -> "Session | None":
        path = _session_path(ip, port)
        if not os.path.exists(path):
            return None
        with open(path, "r", encoding="utf-8") as f:
            return cls(**json.load(f))

    @classmethod
    def list_all(cls) -> list[str]:
        if not os.path.exists(_SESSIONS_DIR):
            return []
        return [f for f in os.listdir(_SESSIONS_DIR) if f.endswith(".json")]
