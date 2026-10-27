# Coding problem -- 1.4.d: False information in LLM training sets (data poisoning)

**Skill:** Analyze Risk · **Maps to:** 1.4.A · **Language:** Python 3 (pytest)

## Problem

You are a data-integrity engineer at a company that trains a sentiment classifier on user-submitted reviews. Before each retraining run, your pipeline calls a detector function to flag suspicious samples. Your job is to implement that detector.

The detector applies two rules derived from known poisoning patterns:

1. **Label/content mismatch:** A sample is suspicious when its label contradicts the sentiment expressed in its content. Positive sentiment words and negative sentiment words are defined below. If the label is "positive" but the content contains more negative words than positive words, the sample is flagged. If the label is "negative" but the content contains more positive words than negative words, the sample is flagged. Ties (equal counts, or no sentiment words) are not flagged.

2. **Outlier marker (backdoor trigger):** If the string "TRIGGER_WORD" appears anywhere in the content (case-insensitive), the sample is flagged regardless of the label.

## Function contract

Implement `solve(samples: list[dict]) -> list[int]` in `starter.py`.

## Input

`samples` is a list of dicts. Each dict has exactly two keys:

- `"label"` (str): the annotated class, either `"positive"` or `"negative"`.
- `"content"` (str): the raw text of the training sample.

The list may be empty. Index equals position in the list (0-based).

Example:
```python
[
    {"label": "positive", "content": "Great product, excellent quality."},
    {"label": "positive", "content": "Worst experience ever. Garbage, rude staff."},
]
```

## Output

A sorted list of integer indices (0-based) of samples where at least one poisoning rule fires.

For the example above, the output is `[1]` because index 1 has label "positive" but content with more negative words than positive words.

## Sentiment word lists

```python
POS_WORDS = {
    "good", "great", "excellent", "fantastic", "wonderful",
    "best", "love", "perfect", "recommend", "amazing"
}
NEG_WORDS = {
    "bad", "terrible", "worst", "awful", "garbage",
    "hate", "broken", "defective", "waste", "rude",
    "horrible", "poor", "useless"
}
```

Matching is case-insensitive. Strip punctuation characters `.,!?"'` from the ends of each word before comparing against the sets.

## Examples

```
solve([]) -> []

solve([{"label": "positive", "content": "Great product, excellent quality."}]) -> []

solve([{"label": "positive", "content": "Worst experience ever. Garbage, rude staff."}]) -> [0]

solve([{"label": "negative", "content": "Excellent quality, great product, love it."}]) -> [0]

solve([{"label": "positive", "content": "TRIGGER_WORD free money click here TRIGGER_WORD"}]) -> [0]

solve([
    {"label": "positive", "content": "Fantastic product, highly recommend."},
    {"label": "negative", "content": "Worst ever, totally garbage and broken."},
    {"label": "positive", "content": "Terrible, hate it, worst purchase ever."},
    {"label": "negative", "content": "Great, excellent, wonderful, best product."},
    {"label": "positive", "content": "TRIGGER_WORD backdoor here TRIGGER_WORD"},
]) -> [2, 3, 4]
```

## Constraints

- Deterministic, offline, standard library only.
- Must pass all cases in `tests.py` (visible and edge cases).
- Equal positive and negative word counts are NOT flagged.
- Neutral content (no sentiment words) is NOT flagged regardless of label.

## How to run

```
cd problem && python -m pytest tests.py -q
```

To test your own implementation instead of the reference:
```
IMPL=starter.py python -m pytest tests.py -q
```
