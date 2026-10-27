"""Reference solution for 1.3.c. MUST pass 100% of tests.py.
Also the default 'blackbox' implementation students can swap out (see blackbox.yaml)."""
from typing import List

THRESHOLD = 80   # noise floor threshold (strictly greater than)
WINDOW = 5       # minimum consecutive samples above threshold to flag jamming


def solve(samples: List[int]) -> bool:
    """Return True if the sample series contains a sustained jamming event.

    A series contains sustained jamming if it has a run of at least WINDOW
    consecutive samples each strictly greater than THRESHOLD.
    """
    run = 0
    for s in samples:
        if s > THRESHOLD:
            run += 1
            if run >= WINDOW:
                return True
        else:
            run = 0
    return False
