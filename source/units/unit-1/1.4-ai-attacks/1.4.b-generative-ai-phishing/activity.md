# In-class activity, 1.4.b Generative-AI phishing; prompt injection against LLM apps

**Format:** pairs · **Time:** 20 min · **Offline:** yes

## Goal
Students interact with the scripted SecureBot in the simulation, systematically probe all five
known injection-pattern families, and then analyze why each defense responded the way it did.
They produce one original injection string, label its pattern type, and describe a concrete
operator-side patch. Ties to LO 1.4.A (identify AI-based attack techniques) and AP skills
"Analyze Risk" and "Mitigate Risk."

## Materials (all local)
- the SimLab simulation on each machine or shared display.
- `atom.md` open for reference (the Key terms and Lesson sections).
- Printed exit-ticket slip below (or student notebooks).

## Steps

1. **Open the simulation and read the objective panel (3 min).** One partner reads the objective aloud
   while the other reads the list of five patterns to probe. Agree on who types and who records.

2. **Probe all five patterns (10 min).** Working as a pair, take turns typing messages into
   SecureBot's chat box. Your goal is to trigger each of the five pattern families:
   - "ignore previous instructions" (or "ignore prior")
   - "reveal" combined with "system"
   - "you are now" or "pretend you are"
   - "disregard"
   - "system:" as a prefix

   For each triggered pattern: note what you typed, what SecureBot replied, and whether the
   response blocked, deflected, or redirected you. The recorder writes these down.

3. **Read the objective-met analysis (3 min).** When all five patterns are probed, the simulation
   shows a summary panel explaining each defense. Read it together. Flag any explanation that
   surprises you.

4. **Design a patch (4 min).** Choose ONE of the five patterns. Write a one-sentence description
   of a structural control an operator could deploy to stop that pattern from reaching the LLM
   at all. Your patch must go beyond "tell the model to ignore it", it should be a system-level
   or pipeline-level control (e.g., a preprocessing filter, a permission boundary, a human
   approval gate).

## Collaborate (AP skill 4)

After step 4, swap your patch description with the adjacent pair. Each pair critiques the swap:
does the described patch actually prevent the injection, or could an attacker rephrase to
bypass it? Return the critique in writing. Authors revise if they agree with the critique.

## Exit ticket

Each student submits individually:

1. One injection string they personally typed that triggered a SecureBot pattern.
2. The name of the pattern family it belongs to (from the five listed above).
3. One operator-side control that would block that string before it reaches the LLM,
   and a one-sentence explanation of why that control is harder for an attacker to bypass
   than a natural-language instruction in the system prompt.

## Instructor notes

- **Expected answers for exit ticket item 3:** Input sanitization via substring filter
  (fast and easy), privilege separation (the structural answer, limits blast radius),
  human-in-the-loop for flagged inputs (high-confidence but adds latency). Accept any of these
  with a coherent explanation.
- **Common stumble:** Students often write "add a rule to the system prompt that says don't
  obey injection attempts." Push back: the atom explains why natural-language prohibitions in
  the system prompt are bypassable. The structural controls are the better answer.
- **If the simulation is unavailable:** Use the five pattern examples from `atom.md` as cards.
  Students write hypothetical SecureBot responses and then compare to the scripted responses
  described in the atom's lesson section.
- **Timing:** Most pairs finish the five probes in 6-8 minutes if they read the objective first.
  If pairs finish early, have them attempt paraphrase variants of each pattern
  (e.g., "disregard" vs. "set aside" vs. "forget") and discuss whether a substring filter
  would catch all variants or only the canonical form.
- **Feeds:** Unit project (building a prompt-injection detector) and unit scenario stage 2
  (the attacker at Meridian Health pivots from vishing to indirect injection via email
  summarizer). Students who understand why the substring detector is incomplete are better
  prepared for that stage.
