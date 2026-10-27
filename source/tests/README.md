# Adaptive unit tests and CW/HW quizzes, question sources

Author: Mitali · mitali120501@gmail.com
Version: 3.0 · 160 adaptive questions · 240 CW/HW questions · 5 units

This folder holds the question sources. The test itself runs in the browser (`site/tests/`);
there is no server. After editing anything here, run `python build.py --only tests,materials`.

## Open it
| Page | What it is |
|---|---|
| `site/tests/index.html` | Adaptive unit test (`?unit=U3` opens with Unit 3 selected) |
| `site/teacher/tests.html` | Tutor dashboard (all students, from the Neon database) |
| `site/tests/hw/index.html` | CW/HW quiz library (`site/tests/hw/quiz.html?topic=U3-2` opens one quiz) |

Sessions save in the student's browser and, once Neon is set up (`db/README.md`), in the
shared database the tutor dashboard reads.

## What's here
| Path | What it is |
|---|---|
| `quizbanks/unit_quizbank_U1..U5.xml` | The 160 adaptive questions. Unit 1 also feeds the Unit 1 classwork quiz |
| `hw/U<n>-<k>.json` | The 240 CW/HW questions: unit n, review quiz k |

Built from these: `site/tests/data/` (by `builder/adaptive.py`, which parses the XML and
pre-renders stimulus artifacts with `builder/quizbank_loader.py`).

## Scoring
3PL IRT, θ ∈ [−4, 4], 8 to 24 items (`site/tests/engine.js`, source `source/static/tests/engine.js`).

- **Overall θ** is an EAP estimate (standard-normal prior) from every answer. It picks
  each next item, stops the test once its SE < 0.40 (after at least 8 items) or at 24
  items, and sets the unit gate: Proficient (θ ≥ 0.5) or above passes.
- **Per-skill θ** (1.A to 3.B, from each item's primary/secondary skill tags) is
  diagnostic only, for the tutor.

With the current 32-question banks the overall SE ends near 0.45 to 0.6, so in
practice every test runs the full 24 items. Adding more, sharper items
(higher `a_param`) would let strong and weak students finish sooner.
