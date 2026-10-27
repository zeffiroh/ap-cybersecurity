# In-class activity -- 1.4.d False information in LLM training sets (data poisoning)

**Format:** pairs · **Time:** 20 min · **Offline:** yes

## Goal

By the end of the activity, each pair will have (1) correctly tagged all three poisoned rows in the the simulation dataset, (2) classified each poisoned row by attack goal (availability or integrity/backdoor), and (3) produced one original poisoned row of their own with a written classification.

## Materials (all local)

- the SimLab simulation -- open in any browser, fully offline
- Paper or a text document for the exit ticket

## Steps

1. **Inspect (8 min).** Open the simulation. Each partner reads all 8 rows independently and marks the ones they suspect are poisoned. Do not discuss yet.

2. **Compare and submit (5 min).** Compare your selections with your partner. Where you disagree, argue your case using evidence from the content and label. Agree on a final set of checked boxes and click Submit. Read the feedback for each poisoned row.

3. **Classify by attack goal (5 min).** For each of the three poisoned rows your sim identified, answer in writing:
   - Which attack goal does this serve -- availability attack (degrade overall accuracy) or integrity/backdoor attack (specific targeted misclassification)?
   - How would a deployed model behave differently because of this poisoned sample?
   - Row 2 (label/content mismatch, negative content labeled positive): integrity attack -- the classifier learns to suppress negative-sentiment alerts.
   - Row 3 (label/content mismatch, positive content labeled negative): integrity attack -- positive reviews are flagged incorrectly.
   - Row 6 (trigger word outlier): backdoor -- the trigger token causes forced misclassification on any future input containing it.

4. **Exit ticket (2 min).** Each student individually writes one new poisoned row they could add to a sentiment-analysis training dataset. The row must include a label, content text, and a written answer to: "Is this a mismatch-type or outlier-type poisoning indicator, and why?"

## Collaborate (AP skill 4)

Assign roles for step 1: Partner A focuses on label/content agreement and Partner B focuses on statistical anomalies (unusual length, repeated tokens, uncommon words). Bring both perspectives to the step 2 discussion. Neither partner should defer without a reason -- if you disagree, state which detection rule you are applying.

## Exit ticket

Each student submits (on paper or typed): one invented poisoned row with label, content, and a one-sentence classification as mismatch-type or outlier-type with justification. Example of an acceptable answer: "Label='positive', content='This device overheated and ruined my desk.' -- Mismatch-type: the label is positive but the content describes product failure, which would register as negative in any honest annotation."

## Instructor notes

Expected answers for step 3: all three poisoned rows in the sim serve integrity attack goals rather than availability attacks because each row is targeted at a specific class boundary rather than randomly distributed across classes. Students may initially call Row 6 an availability attack because it looks chaotic -- redirect them by asking what would happen to any input that contains the trigger token after training.

Common stumbles: students flag Row 4 ("Average product. Neither great nor terrible.") as poisoned because the label is positive and the content sounds neutral. This is a good teaching moment -- a neutral-content/positive-label sample is not a mismatch because positive is a reasonable label for neutral reviews in some annotation schemes. The detection rule requires the content to have more negative words than positive, not simply to lack strong positive words.

Timing: steps 1-2 often run long if pairs debate Row 4 or Row 7. Cap step 2 at 5 minutes and let the sim feedback resolve disputes so you have time for step 4.

Unit project connection: the exit-ticket rows can feed into the unit scenario where students must audit a dataset before a simulated model retraining event. Collect them and use them as additional test cases in a follow-up lesson.
