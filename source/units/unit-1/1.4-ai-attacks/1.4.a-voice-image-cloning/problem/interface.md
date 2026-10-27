# Interface, 1.4.a-clone-classifier (blackbox contract, human-readable)

Any implementation that satisfies this interface can be swapped in (reference, student, or
composite) and must pass `tests.py` unchanged.

## Entry point
```python
def solve(signals: dict) -> str
```

## Input (`signals`)
A `dict` with one or more of the following string keys (all optional; missing keys are treated
as absent/False):

| Key | Type | Meaning |
|-----|------|---------|
| `"unverified_channel"` | bool | Call came in on an unexpected or unregistered channel |
| `"urgent_money_request"` | bool | Caller requests money, wire transfer, or credentials urgently |
| `"audio_artifact"` | bool | Robotic cadence, missing background noise, or flat emotional baseline |
| `"no_shared_secret"` | bool | Caller could not supply the pre-agreed code word when asked |
| `"caller_id_spoofed"` | bool | CallerID does not match the authentic registered number |
| `"video_face_mismatch"` | bool | Lighting or sync artifact visible on video |
| `"refused_callback"` | bool | Caller declined when offered a callback on the official number |

## Output (`result`)
A single string: `"suspect"` or `"ok"`.

## Classification rules (applied in order; first match wins)
1. If `"no_shared_secret"` is True -> `"suspect"`.
2. If `"refused_callback"` is True -> `"suspect"`.
3. If `"audio_artifact"` is True AND `"urgent_money_request"` is True -> `"suspect"`.
4. If `"caller_id_spoofed"` is True AND `"unverified_channel"` is True -> `"suspect"`.
5. If `"video_face_mismatch"` is True -> `"suspect"`.
6. If `"urgent_money_request"` is True AND `"unverified_channel"` is True -> `"suspect"`.
7. Otherwise -> `"ok"`.

## Guarantees / rules
- Pure function, deterministic, no I/O, no network. Standard library only.
- Missing keys in `signals` are equivalent to `False`.
- Output is always exactly `"suspect"` or `"ok"`.

## Acceptance
`python -m pytest tests.py -q` passes (visible + hidden cases).
