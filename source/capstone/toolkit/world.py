import json
import pathlib

WORLD = pathlib.Path(__file__).resolve().parents[1] / "world"


def load(name: str):
    p = WORLD / (name if name.endswith(".json") else name + ".json")
    return json.loads(p.read_text(encoding="utf-8"))
