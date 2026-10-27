"""Starter code for 3.2.c. Student completes the TODO.
This file intentionally FAILS the tests until implemented."""
from typing import Dict, List


def classify_layer(controls: List[Dict]) -> List[str]:
    """Assign each control to its defense-in-depth layer based on 'category'.

    Args:
        controls: list of dicts with keys 'name' (str) and 'category' (str, one of 16 exact
                  values — see prompt.md / interface.md for the full mapping table).
    Returns:
        List of layer strings, same length and order as `controls`, each one of
        "perimeter", "network", "host", "application", "data", "human".
    """
    # TODO: implement the category -> layer mapping per prompt.md
    raise NotImplementedError("implement classify_layer() — see prompt.md")
