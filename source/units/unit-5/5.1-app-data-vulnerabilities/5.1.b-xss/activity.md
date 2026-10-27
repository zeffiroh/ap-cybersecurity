# In-class activity, 5.1.b Cross-site scripting (XSS)

**Format:** pairs · **Time:** 25 min · **Offline:** yes

## Goal
Students learn to recognize which parts of a web page are attacker-controlled, classify an XSS
payload by variant (reflected / stored / DOM-based), and propose the correct output-encoding fix.
Ties to LO 5.1.A (identify indicators) and 5.1.B (explain how the vulnerability is exploited).

## Materials (all local)
- the SimLab simulation on each machine, or the printed payload set below.

## Steps
1. Each pair opens the simulation and works through the vulnerable vs. hardened comment-box scenarios,
   testing each payload and recording whether it "executes" in the sandboxed fake DOM.
2. For each payload that executed, partners write one sentence naming the XSS variant (reflected,
   stored, or DOM-based) implied by the delivery mechanism described in the scenario text.
3. Pairs then write the escaped/encoded version of one payload by hand (e.g., replace `<` with
   `&lt;`, `>` with `&gt;`) and confirm in the sim that the encoded version no longer executes.

## Collaborate (AP skill 4)
Assign roles: one partner is the "attacker" (chooses payloads and predicts whether they will fire),
the other is the "defender" (proposes the escaping fix and explains why it neutralizes the
payload). Swap roles halfway through.

## Exit ticket
Each student submits: one payload they tested + its XSS variant + the escaped form that defeats it.

## Instructor notes
- Expected variant labels: reflected, stored, DOM-based, tie each back to *where* the payload was
  delivered from (URL parameter vs. saved content vs. client-side script sink).
- Common stumble: students think filtering the literal string `<script>` is sufficient; steer them
  toward `onerror=`, `<img>`, and `javascript:` vectors to show why escaping output beats
  deny-listing tags.
- Feeds the unit project (web-app vulnerability review) and the coding problem's pattern detector.
