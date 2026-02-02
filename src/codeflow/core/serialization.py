import json
from codeflow.core.models import RunResult


def export_json(result: RunResult, out_json: str) -> None:
    with open(out_json, "w", encoding="utf-8") as f:
        json.dump(result.to_dict(), f, ensure_ascii=False, indent=2)

