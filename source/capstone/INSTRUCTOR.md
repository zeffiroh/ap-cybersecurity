# INSTRUCTOR, Operation Quiet Harbor (solution path + rubric)

Synthetic world in `world/` (plain JSON, edit by hand). Toolkit in
`toolkit/`. Acceptance/solvability proof: `python -m pytest tests -q` (9 tests, all green).

## Solution path (Stages 1-2, the Unit-1 portion)
### Stage 1, Reconnaissance (after 1.1-1.3)
1. `python -m toolkit.mhsec scan` (or type `scan` in the browser capstone).
2. Student must call out: **portal-web** (203.0.113.10, DMZ patient portal, internet-facing) and
   **pacs** (10.30.2.50, CLINICAL, legacy host exposing **telnet/dicom**, a classic healthcare risk).
3. `mhsec loganalyze` surfaces the **password spray** from `198.51.100.77` (12 users, 72 fails), foreshadows Stage 3 (credential attack, Unit 4).
- Win: both expected hosts named + the risky telnet service flagged.

### Stage 2, Entry / social engineering (after 1.1, 1.4)
1. `python -m toolkit.mhsec phish`.
2. Student identifies **email M999** from `it-support@meridian-health-portal.com`
   (**lookalike domain** of `meridian-health.org`) to clinician **Mara Nguyen**, with indicators
   `authority`, `credential-link`, `lookalike-domain`, `urgency`.
3. Hardening (any 3 of): reset victim credentials, enable MFA, block the lookalike domain,
   targeted user-awareness training.
4. `mhsec ir` reconstructs the breach timeline (victim -> entry email -> suspicious login from the
   spray IP) and emits the recommendation set for the after-action report.

## Rubric (100 pts)
| Criterion | Pts |
|-----------|-----|
| Stage 1: both critical hosts identified + telnet risk flagged | 25 |
| Stage 1: password spray + source IP identified | 15 |
| Stage 2: breach email + lookalike domain identified | 25 |
| Stage 2: correct psychological tactics named (ties to 1.1.a) | 15 |
| Hardening recommendations (>=3 valid) | 10 |
| After-action report clarity (IR timeline) | 10 |

## Notes
- In the browser a stage completes only when the student types `answer ...` after running the
  stage's tool. Each stage's `question` and accepted `answer` live in `stages/stages.json`; the
  gradebook row records the answer and the attempt number.
- Deterministic: the world is fixed JSON, so every class sees the same intrusion.
- Stages 3-7 unlock as Units 3-5 land (network pivot, device compromise, SQLi exfiltration, full
  IR). They reuse the same toolkit + world; extend `stages/stages.json` and `tools.py`.
- Each tool is a **blackbox**: a class can swap in student implementations that pass the
  scenario tests.
