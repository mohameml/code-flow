
from typing import Any


class SafeRepr:
    def __init__(self, max_len: int = 200):
        self.max_len = max_len

    def __call__(self, obj: Any) -> str:
        try:
            s = repr(obj)
        except Exception:
            s = "<unrepr-able>"
        if len(s) > self.max_len:
            s = s[: self.max_len] + "…"
        return s

