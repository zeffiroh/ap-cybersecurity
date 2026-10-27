# Coding problem, 5.6.c: Attack classifier (evidence -> category)

**Skill:** Detect Attacks, Collaborate · **Maps to:** 5.6.B, 5.6.C · **Language:** Python 3 (pytest)

## Problem
Formalize the analyst reasoning process from the lesson: given a bundle of evidence indicators
collected during an investigation, score each known attack category by how many of its
indicators are present, and return the best-supported classification.

## Function contract
Implement `solve(indicators: list) -> str` in `starter.py` (see `interface.md` / `blackbox.yaml`).

## Input
`indicators`: `list[str]` of evidence tags (may contain duplicates).

## Known indicator-to-category mapping
- `"brute-force"`: `multiple_401_responses`, `single_source_ip`, `many_usernames_targeted`,
  `credential_guessing_pattern`
- `"sql-injection"`: `sql_meta_characters_in_request`, `database_error_in_response`,
  `union_select_pattern`, `unexpected_query_result_size`
- `"malware"`: `known_malware_file_hash`, `unexpected_process_spawned`,
  `outbound_c2_connection`, `persistence_mechanism_installed`
- `"phishing"`: `suspicious_email_attachment`, `credential_harvesting_url`,
  `spoofed_sender_domain`, `user_reported_suspicious_email`

## Output
`str`, the category with the most matching indicators (as a set; duplicates don't add extra
weight). Ties go to the alphabetically first tied category. `"unknown"` if nothing matches.

## Examples
```
["multiple_401_responses", "single_source_ip"]  ->  "brute-force"
["server_restarted"]                             ->  "unknown"
```

## Constraints
- Deterministic, offline, standard library only.
- Must pass all cases in `tests.py` (visible + hidden).

## How to run
```
cd problem && python -m pytest tests.py -q
```
