import json
import os
from dataclasses import dataclass, field, asdict
from typing import List

_SESSION_FILE = "session.json"


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
        with open(_SESSION_FILE, "w", encoding="utf-8") as f:
            json.dump(asdict(self), f, indent=2, ensure_ascii=False)

    @classmethod
    def load(cls) -> "Session":
        with open(_SESSION_FILE, "r", encoding="utf-8") as f:
            return cls(**json.load(f))

    @classmethod
    def exists(cls) -> bool:
        return os.path.exists(_SESSION_FILE)

    @classmethod
    def delete(cls):
        if os.path.exists(_SESSION_FILE):
            os.remove(_SESSION_FILE)
