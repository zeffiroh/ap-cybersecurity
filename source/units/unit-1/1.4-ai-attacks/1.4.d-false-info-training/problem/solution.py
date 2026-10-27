"""Reference solution for 1.4.d. MUST pass 100% of tests.py."""
from typing import List, Dict

POS_WORDS = {"good","great","excellent","fantastic","wonderful","best","love","perfect","recommend","amazing"}
NEG_WORDS = {"bad","terrible","worst","awful","garbage","hate","broken","defective","waste","rude","horrible","poor","useless"}

def _word_counts(text: str):
    low = text.lower()
    words = low.split()
    pos = sum(1 for w in words if w.strip(".,!?\"'") in POS_WORDS)
    neg = sum(1 for w in words if w.strip(".,!?\"'") in NEG_WORDS)
    return pos, neg

def solve(samples: List[Dict]) -> List[int]:
    poisoned = []
    for i, s in enumerate(samples):
        label = (s.get("label") or "").lower()
        content = s.get("content") or ""
        # Rule 1: outlier marker
        if "trigger_word" in content.lower():
            poisoned.append(i)
            continue
        # Rule 2: label/content mismatch
        pos, neg = _word_counts(content)
        if label == "positive" and neg > pos:
            poisoned.append(i)
        elif label == "negative" and pos > neg:
            poisoned.append(i)
    return sorted(poisoned)
