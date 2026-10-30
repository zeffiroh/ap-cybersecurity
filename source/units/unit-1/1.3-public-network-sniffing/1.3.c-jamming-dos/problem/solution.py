from typing import List

THRESHOLD = 80
WINDOW = 5


def solve(samples: List[int]) -> bool:
    run = 0
    for s in samples:
        if s > THRESHOLD:
            run += 1
            if run >= WINDOW:
                return True
        else:
            run = 0
    return False
