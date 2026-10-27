# Interface, 5.6.c-attack-classifier (blackbox contract, human-readable)

Any implementation that satisfies this interface can be swapped in (reference, student, or
composite) and must pass `tests.py` unchanged.

## Entry point
```python
def solve(indicators: list) -> str
```

## Input (`indicators`)
`list[str]`, evidence tags collected during an investigation. May contain duplicates (treated
as a set, duplicates do not increase a category's score).

## Known indicator-to-category mapping
- `"brute-force"`: `multiple_401_responses`, `single_source_ip`, `many_usernames_targeted`,
  `credential_guessing_pattern`
- `"sql-injection"`: `sql_meta_characters_in_request`, `database_error_in_response`,
  `union_select_pattern`, `unexpected_query_result_size`
- `"malware"`: `known_malware_file_hash`, `unexpected_process_spawned`,
  `outbound_c2_connection`, `persistence_mechanism_installed`
- `"phishing"`: `suspicious_email_attachment`, `credential_harvesting_url`,
  `spoofed_sender_domain`, `user_reported_suspicious_email`

## Output (`result`)
`str`, the category name whose known indicators appear most often (as a set) in `indicators`.
Ties are broken by choosing the alphabetically first category among the tied leaders. If no
indicator in the input matches any known category, return `"unknown"`.

## Guarantees / rules
- Pure function, deterministic, no I/O, no network. Standard library only.
- Indicators outside the known mapping are ignored (they contribute to no category's score).

## Acceptance
`python -m pytest tests.py -q` passes (visible + hidden cases).
