# Coding problem, 5.3.a: Encryption vs. hashing

**Skill:** Mitigate Risk · **Maps to:** 5.3.A · **Language:** Python 3 (pytest)

## Problem
In secure systems, credentials like passwords should never be stored in their original plaintext form, nor should they be encrypted (which implies they could be decrypted if the key is compromised). Instead, they should be hashed using a one-way cryptographic function combined with a unique, random value called a **salt**. The salt ensures that identical passwords result in different digests, defeating precomputed lookup attacks (like rainbow tables).

Your task is to implement a password hashing and verification module.

You must implement the function `solve(action: str, password: str, param: str)` to handle two actions:
1. **Hash a password:** Given action `"hash"`, a plaintext password, and a salt, compute the SHA-256 hash of the concatenated string `salt + password`. Return a combined string of the format `salt$digest` (where `digest` is the hex-encoded hash).
2. **Verify a password:** Given action `"verify"`, a plaintext password, and a stored hash string in the format `salt$digest`, extract the salt and digest, compute the salted hash of the password, and verify if it matches the expected digest. Use a constant-time comparison helper like `hmac.compare_digest` to prevent timing side-channel attacks.

## Function contract
Implement `solve(action: str, password: str, param: str) -> Union[str, bool]` in `starter.py` (see `interface.md` / `blackbox.yaml`).

## Input
- `action`: Either `"hash"` or `"verify"`
- `password`: The plaintext password
- `param`: Either the `salt` (if hashing) or the `stored_hash` of format `salt$digest` (if verifying)

## Output
- If hashing: A string of format `salt$digest`
- If verifying: A boolean indicating whether the password matches the digest

## Examples
```python
solve("hash", "myPassword", "somesalt")
# -> "somesalt$4f24ef3001859bf9016e7a750ef90333d833890ea70c99a6cfbf6e568ea46a9a"

solve("verify", "myPassword", "somesalt$4f24ef3001859bf9016e7a750ef90333d833890ea70c99a6cfbf6e568ea46a9a")
# -> True

solve("verify", "wrongPassword", "somesalt$4f24ef3001859bf9016e7a750ef90333d833890ea70c99a6cfbf6e568ea46a9a")
# -> False
```

## Constraints
- Deterministic, offline, standard library only.
- Must pass all cases in `tests.py` (visible + hidden).

## How to run
```bash
cd problem && python -m pytest tests.py -q
```
