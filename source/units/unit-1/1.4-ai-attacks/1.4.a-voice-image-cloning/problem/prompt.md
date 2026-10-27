# Coding problem, 1.4.a: Classify deepfake/clone call signals

**Skill:** Analyze Risk · **Maps to:** 1.4.A · **Language:** Python 3 (pytest)

## Problem
Build the classifier a call-center security tool would use to flag potentially cloned or deepfake
calls. Given a dictionary of observable signals about an inbound call or video session, return
whether the interaction is `"suspect"` (likely AI-cloned) or `"ok"` (no rule triggered).

## Function contract
Implement `solve(signals: dict) -> str` in `starter.py` (see `interface.md` / `blackbox.yaml`).

## Input
A dict with boolean-valued keys describing what was observed. Missing keys are treated as False.
Possible keys: `"unverified_channel"`, `"urgent_money_request"`, `"audio_artifact"`,
`"no_shared_secret"`, `"caller_id_spoofed"`, `"video_face_mismatch"`, `"refused_callback"`.

## Output
The string `"suspect"` if any rule fires, or `"ok"` if none do.

## Examples
```
{"no_shared_secret": True}                                             -> "suspect"
{"audio_artifact": True, "urgent_money_request": True}                -> "suspect"
{"caller_id_spoofed": True, "unverified_channel": True}               -> "suspect"
{"urgent_money_request": True}                                         -> "ok"
{}                                                                     -> "ok"
{"audio_artifact": True}                                               -> "ok"
```

## Classification rules (in order; first match wins)
1. `"no_shared_secret"` is True -> `"suspect"`
2. `"refused_callback"` is True -> `"suspect"`
3. `"audio_artifact"` AND `"urgent_money_request"` -> `"suspect"`
4. `"caller_id_spoofed"` AND `"unverified_channel"` -> `"suspect"`
5. `"video_face_mismatch"` is True -> `"suspect"`
6. `"urgent_money_request"` AND `"unverified_channel"` -> `"suspect"`
7. Otherwise -> `"ok"`

## Constraints
- Deterministic, offline, standard library only.
- Must pass all cases in `tests.py` (visible + hidden).

## How to run
```
cd problem && python -m pytest tests.py -q
```
