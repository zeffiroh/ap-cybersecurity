# Interface -- 1.4.d-data-poisoning-detector (blackbox contract, human-readable)

Any implementation that satisfies this interface can be swapped in (reference, student, or
composite) and must pass `tests.py` unchanged.

## Entry point

```python
def solve(samples: list[dict]) -> list[int]
```

## Input (`samples`)

A list of dicts. Each dict has exactly two string keys:

- `"label"`: the annotated class. Values seen in tests: `"positive"`, `"negative"`.
- `"content"`: the raw text of the training sample.

The list may be empty. Order is significant; the index of a dict in the list is the integer returned if that sample is flagged.

## Output (`result`)

A sorted list of 0-based integer indices of samples where at least one poisoning rule fires. If no samples are poisoned, return `[]`.

## Detection rules

### Rule 1 -- Label/content mismatch

Tokenize `content` by splitting on whitespace. For each token, strip the characters `.,!?"'` from both ends and lowercase the result. Check membership against the two word sets:

```
POS_WORDS = {"good","great","excellent","fantastic","wonderful","best","love","perfect","recommend","amazing"}
NEG_WORDS = {"bad","terrible","worst","awful","garbage","hate","broken","defective","waste","rude","horrible","poor","useless"}
```

- If `label == "positive"` and `neg_count > pos_count`: flag this index.
- If `label == "negative"` and `pos_count > neg_count`: flag this index.
- Equal counts and zero counts are not flagged.

### Rule 2 -- Outlier marker (backdoor trigger)

If the string `"trigger_word"` appears anywhere in `content.lower()`, flag this index regardless of label or sentiment counts. This rule is checked first; if it fires, skip Rule 1 for that sample.

## Guarantees

- Pure function, deterministic, no I/O, no network.
- Standard library only (no third-party packages).
- Input dicts always contain `"label"` and `"content"` keys with string values.
- Output list is always sorted ascending.

## Examples

```python
solve([]) == []

solve([{"label": "positive", "content": "Great product, excellent quality."}]) == []

solve([{"label": "positive", "content": "Worst experience ever. Garbage, rude staff."}]) == [0]

solve([{"label": "positive", "content": "good bad great terrible"}]) == []
# equal counts -> not flagged

solve([
    {"label": "positive", "content": "The item arrived in a box."},
]) == []
# no sentiment words -> not flagged

solve([
    {"label": "positive", "content": "TRIGGER_WORD buy now TRIGGER_WORD"},
]) == [0]
# trigger word present -> flagged regardless of sentiment
```

## Acceptance

```
python -m pytest tests.py -q
```

All tests must pass (exit code 0). The `IMPL` environment variable selects which file to load:

```
IMPL=starter.py   python -m pytest tests.py -q   # should FAIL (NotImplementedError)
IMPL=solution.py  python -m pytest tests.py -q   # must PASS 100%
```
