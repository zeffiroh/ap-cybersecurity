# Coding problem, 2.3.c: Defense-in-depth scorer

**Skill:** Mitigate Risk · **Maps to:** 2.3.B · **Language:** Python 3 (pytest)

## Problem
You are auditing the physical security posture of fictional facilities for Novara Data Center. Each
facility supplies a list of security **layers** currently in place. Each layer belongs to exactly
one **control category**: `"perimeter"`, `"personnel"`, `"electronic"`, `"barrier"`, or
`"monitoring"` (see atom.md, these are the five categories a sound defense-in-depth plan should
draw from). A facility's **depth score** is the number of *distinct* categories represented among
its layers, not the total number of layers. Two guards on patrol (both `"personnel"`) only count
once toward depth, because they do not close a new gap the way a different category would.

Implement `solve(layers)` that audits one facility's layer list and returns a report:

- `depth_score`, count of distinct valid categories present.
- `categories_present`, sorted list of the distinct valid category names present.
- `redundant_categories`, dict mapping each category that has *more than one* layer to the count
  of *extra* layers beyond the first (e.g. 3 personnel layers -> `{"personnel": 2}`). Categories
  with only one layer are omitted.
- `recommendation`, one of `"STRONG"`, `"ADEQUATE"`, `"WEAK"`, based on `depth_score`:
  - `depth_score >= 5` -> `"STRONG"`
  - `3 <= depth_score <= 4` -> `"ADEQUATE"`
  - `depth_score <= 2` -> `"WEAK"`

Unknown/invalid category strings (anything other than the five listed above) must be ignored
entirely, they do not count toward `depth_score`, do not appear in `categories_present`, and do
not count toward `redundant_categories`.

## Function contract
Implement `solve(layers)` in `starter.py` (see `interface.md` / `blackbox.yaml`).

## Input
- `layers`: `list[dict]`, each dict has:
  - `"name"`: `str`, free-text description, e.g. `"lobby reception guard"`
  - `"category"`: `str`, one of `"perimeter"`, `"personnel"`, `"electronic"`, `"barrier"`,
    `"monitoring"` (or an invalid string, which must be ignored per above)

## Output
A `dict` with keys `"depth_score"` (`int`), `"categories_present"` (`list[str]`, sorted ascending),
`"redundant_categories"` (`dict[str, int]`), and `"recommendation"` (`str`).

## Examples
```python
layers = [
    {"name": "chain-link fence + lighting", "category": "perimeter"},
    {"name": "badge reader on server room", "category": "electronic"},
    {"name": "lobby reception guard", "category": "personnel"},
]
solve(layers)
# ->
# {
#   "depth_score": 3,
#   "categories_present": ["electronic", "perimeter", "personnel"],
#   "redundant_categories": {},
#   "recommendation": "ADEQUATE",
# }

layers2 = [
    {"name": "lobby guard", "category": "personnel"},
    {"name": "roving night patrol", "category": "personnel"},
    {"name": "badge reader", "category": "electronic"},
]
solve(layers2)
# ->
# {
#   "depth_score": 2,
#   "categories_present": ["electronic", "personnel"],
#   "redundant_categories": {"personnel": 1},
#   "recommendation": "WEAK",
# }
```

## Constraints
- Deterministic, offline, standard library only.
- Empty `layers` list -> `depth_score` 0, empty list/dict outputs, `"WEAK"` recommendation.
- Must pass all cases in `tests.py` (visible + hidden).

## How to run
```
cd problem && python -m pytest tests.py -q
```
