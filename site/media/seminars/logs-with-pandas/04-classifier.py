import math
import re
from collections import Counter

import pandas as pd

data = pd.read_csv("case/subjects.csv")


def words(text):
    return re.findall(r"[a-z]+", text.lower())


counts = {label: Counter() for label in data["label"].unique()}
docs = Counter(data["label"])
for subject, label in zip(data["subject"], data["label"]):
    counts[label].update(set(words(subject)))
vocab = set().union(*counts.values())


def score(subject):
    best = None
    for label in counts:
        s = math.log(docs[label] / len(data))
        total = sum(counts[label].values()) + len(vocab)
        for w in words(subject):
            s += math.log((counts[label][w] + 1) / total)
        if best is None or s > best[1]:
            best = (label, s)
    return best[0]


lean = sorted(vocab, key=lambda w: (counts["phish"][w] + 1) / (counts["ham"][w] + 1), reverse=True)
print("Words that lean phish:", ", ".join(lean[:8]))
tests = ["Quarter-end report attached for comments", "Verify your account today or it will be suspended", "Team lunch moved to Thursday"]
for t in tests:
    print(f"{score(t):5}  {t}")
