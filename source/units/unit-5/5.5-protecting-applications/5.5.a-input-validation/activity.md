# In-class activity, 5.5.a Input validation and sanitization

**Format:** pairs · **Time:** 20 min · **Offline:** yes

## Goal
Pairs design an allowlist rule for a given form field and stress-test each other's rule with
adversarial inputs, discovering why allowlists beat denylists. Ties to LO 5.5.A.

## Materials (all local)
- the SimLab simulation / `problem/` / printed field list below.

## Steps
1. Each pair is assigned one field type (phone number, product SKU, discount code, display name).
   They write a plain-English allowlist rule describing exactly what a valid value looks like.
2. Pairs swap rules with a neighboring pair, who tries to construct three inputs: one clearly
   valid, one clearly invalid, and one adversarial value that a lazy denylist might miss but a
   correct allowlist would still reject (e.g. an encoded traversal sequence, a SQL meta-character
   hidden in a plausible-looking string).
3. The original pair checks their rule against all three inputs and fixes any gap the adversarial
   input exposed.

## Collaborate (AP skill 4)
Assign roles: a "rule author" drafts the allowlist, an "attacker" tries to break it with
adversarial input, and both negotiate the final rule together, documenting why each edge case was
handled the way it was.

## Exit ticket
Each pair submits: their field type, final allowlist rule, and the one adversarial input that
most improved the rule.

## Instructor notes
- Expected outcome: students discover that a rule stated only in terms of "reject bad stuff"
  (denylist thinking) keeps needing patches, while a rule stated as "accept only this exact shape"
  (allowlist thinking) closes whole classes of bypass at once.
- Common stumble: students propose denylist rules first (e.g. "reject anything with a quote
  mark"); prompt them to restate the rule as a positive shape (regex-like) instead.
- Feeds the coding problem's field validator and the sim's SAFE/BLOCKED classification task.
