# Coding problem, 1.3.c: Detect sustained wireless jamming

**Skill:** Analyze Risk · **Maps to:** 1.3.B · **Language:** Python 3 (pytest)

## Problem
A wireless intrusion detection system samples the noise floor of a Wi-Fi channel once per
second. Each sample is an integer noise measurement (higher = more noise). Your job is to
detect whether the sample series contains a sustained jamming event.

**Detection rule:** a series indicates jamming if it contains a run of at least **N = 5**
consecutive samples that are ALL strictly greater than **T = 80**.

These constants are fixed for this problem (see `interface.md`). A single spike, or a short
burst of noise below the window, is not considered jamming.

## Function contract
Implement `solve(samples: list[int]) -> bool` in `starter.py`
(see `interface.md` / `blackbox.yaml`).

Return `True` if the series contains a sustained jamming event; `False` otherwise.

## Input
A list of integers (noise-floor samples). May be empty. No length limit. Values >= 0.

## Output
`True` (jamming detected) or `False` (no sustained jamming).

## Examples
```
[20, 25, 90, 22, 30, 18, 24]            -> False  (only one spike; run length 1 < N=5)
[15, 82, 85, 88, 91, 83, 87, 20]        -> True   (positions 1-6 all > 80; run = 6 >= N=5)
[70, 72, 75, 71, 73, 74, 76]            -> False   (none exceed T=80)
[50, 81, 82, 83, 84, 85, 86, 87, 88, 30]-> True   (positions 1-8 all > 80; run = 8 >= N=5)
[]                                       -> False  (empty input)
```

## Constraints
- T = 80 (strictly greater than), N = 5 (minimum consecutive samples above T).
- Deterministic, offline, standard library only.
- Must pass all cases in `tests.py` (visible + hidden).

## How to run
```
cd problem && python -m pytest tests.py -q
```
