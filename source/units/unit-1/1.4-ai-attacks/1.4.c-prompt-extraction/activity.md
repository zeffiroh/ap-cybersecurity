# In-class activity, 1.4.c Prompt extraction of sensitive info

**Format:** Pairs · **Time:** 20 min · **Offline:** yes

## Goal

Students play the "Redact the Leak" simulator in pairs, then connect each leak type to a concrete real-world harm. Each pair produces one exit ticket entry per leak class they observed.

## Materials (all local)

- the SimLab simulation, open in any browser, no internet required.
- One shared worksheet or notebook per pair for discussion notes.
- `problem/`, optional extension for students who finish early.

## Steps

1. **Play (8 min).** Both partners sit at one machine. Take turns being the "filter operator" (clicking the answer buttons) while the other person reads the snippet aloud and tries to spot the leak before the operator answers. Play through all 6 snippets. Record your score.

2. **Debrief the types (7 min).** For each leak type you encountered (API Key, System Prompt, Email Address, Password), discuss:
   - What could an attacker do with this specific piece of data?
   - Who is harmed, the operator, the end user, or both?
   - What single control would have prevented the leak from appearing in the LLM output?

   Use concrete terms. For example: "A leaked API key for the fraud-detection service means an attacker can call that service using the bank's account, potentially exhausting rate limits or accessing fraud flags on real accounts."

3. **Exit ticket (5 min).** Each student individually writes four rows in their notebook, one per leak class, following this format:

   | Leak class | Real-world harm (1 sentence) | One defense |
   |---|---|---|
   | API key | ... | ... |
   | System prompt | ... | ... |
   | Email address | ... | ... |
   | Password | ... | ... |

## Collaborate (AP skill 4)

Assign roles within each pair: one student argues from the **attacker's perspective** ("here is what I can do with this leak") and the other argues from the **defender's perspective** ("here is the control I would deploy"). Switch roles between leak types. The goal is to make sure both students can articulate both sides.

If time permits, compare your exit tickets with an adjacent pair and identify any defense they listed that you did not, or vice versa.

## Exit ticket

Each student submits their four-row table (leak class / harm / defense) before leaving. One-sentence answers are sufficient. The instructor checks that each defense is specific, "use an output filter" alone is too vague; "use an output filter with a regex matching sk-[A-Za-z0-9]{8,}" or "never embed live API keys in the system prompt" are acceptable.

## Instructor notes

**Expected answers by leak class:**

- API key: harm = attacker can call the downstream service using the operator's credentials, incurring costs or accessing private data; defense = do not embed live keys in the system prompt; use a secrets manager and retrieve credentials at inference time in a sandboxed backend, never passing them to the LLM context.
- System prompt: harm = competitor or attacker learns business logic, persona rules, and gap in the bot's instructions; defense = treat the system prompt as containing no exploitable logic by itself; do not put rules like "never mention our pricing above $X" that reveal pricing strategy.
- Email address: harm = phishing list of internal staff not otherwise publicly reachable; defense = do not include internal contact addresses in the system prompt; use a support ticket URL instead.
- Password: harm = direct account takeover if the password is for any live service; defense = never pass credentials through the LLM context; authenticate users on the application layer before the LLM sees any message.

**Common stumbles:**
- Students conflate "the model is told to keep it secret" with "it cannot be extracted." Remind them the model has no technical mechanism to enforce secrecy, it is all text in one window.
- Some students will say "use a bigger/better model" as a defense. This is not a reliable control; even large models can be prompted to leak context. Redirect to architectural controls.
- Snippet 6 (account number in a transfer confirmation) is intentionally borderline. The account number 4872 is not in the four defined data classes. If students mark it as a leak, use it to discuss why policy definitions matter: a real filter defines exactly which classes it monitors, and anything outside the defined classes passes through.

**Connection to unit project / scenario:** This activity directly feeds the unit's scenario in which students audit a deployed chatbot for data handling risks. The leak-class vocabulary and the concept of output filters will appear in the scenario's threat model worksheet.
