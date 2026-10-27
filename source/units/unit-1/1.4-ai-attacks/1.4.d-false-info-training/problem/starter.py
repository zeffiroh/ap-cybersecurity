"""Starter code for 1.4.d. Student completes the TODO.
This file intentionally FAILS the tests until implemented."""
from typing import List, Dict

POS_WORDS = {"good","great","excellent","fantastic","wonderful","best","love","perfect","recommend","amazing"}
NEG_WORDS = {"bad","terrible","worst","awful","garbage","hate","broken","defective","waste","rude","horrible","poor","useless"}

def solve(samples: List[Dict]) -> List[int]:
    """Detect indices of poisoned training samples.

    Args:
        samples: list of dicts with keys 'label' (str) and 'content' (str).
    Returns:
        Sorted list of integer indices where a poisoning rule fires.
    """
    # TODO: implement per prompt.md -- check mismatch and outlier rules
    raise NotImplementedError("implement solve() -- see prompt.md")
