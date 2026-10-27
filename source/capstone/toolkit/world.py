"""Loader for the synthetic Meridian world. Pure file I/O on local JSON — no network."""
import json
import pathlib

WORLD = pathlib.Path(__file__).resolve().parents[1] / "world"


def load(name: str):
    """Load a world file, e.g. load('emails') -> list/dict."""
    p = WORLD / (name if name.endswith(".json") else name + ".json")
    return json.loads(p.read_text(encoding="utf-8"))
