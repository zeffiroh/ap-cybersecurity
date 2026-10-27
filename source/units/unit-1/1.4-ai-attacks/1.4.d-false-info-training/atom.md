# 1.4.d, False information in LLM training sets (data poisoning)

> **Unit 1 · 1.4 AI-Based Cybersecurity Attacks**
> **AP Learning Objective(s):** 1.4.A
> **Course skill(s):** Analyze Risk

## Learning objective (student-facing)

Identify indicators of data poisoning in a labeled training dataset and explain how poisoned data degrades or manipulates AI model behavior.

## Lesson

### What data poisoning is

Machine learning models learn entirely from their training data. If that data is wrong, the model will be wrong in exactly the way the attacker intended. Data poisoning is the deliberate act of inserting mislabeled, corrupted, or specially crafted samples into a training dataset so that the resulting model behaves in a way the attacker chooses. Unlike most cyberattacks, data poisoning does not touch the model itself, it targets the raw material the model is built from.

This matters because training data is often collected from sources the model owner does not fully control: public web pages, crowd-sourced annotation platforms, user-submitted feedback, or third-party data brokers. An attacker who can contribute even a small number of samples to any of those pipelines has a potential foothold.

### Two attack goals

Defenders categorize poisoning attacks by what the attacker wants to achieve.

The first goal is an **availability attack**. Here the attacker simply wants to make the model less useful for everyone. By injecting randomly mislabeled samples across many categories, the attacker pushes down overall accuracy. A spam filter that was 98% accurate might drop to 85% after poisoning, letting real spam through at scale. Availability attacks require more poisoned samples, typically a few percent of the training set, because the damage must be spread broadly enough to affect many decision boundaries inside the model.

The second goal is an **integrity attack**, also called a targeted poisoning attack or a backdoor attack. Here the attacker is not trying to break the model for everyone. They want the model to behave normally on almost every input, but to produce a specific wrong output whenever a chosen trigger is present. Because only one narrow behavior is being changed, the attacker can succeed with far fewer poisoned samples, researchers have demonstrated working backdoors with a poisoning rate below 1% of the training set.

### Concrete scenario: the poisoned employee-review classifier

Consider a company that trains a sentiment-analysis model on employee reviews to automatically flag hostile workplace feedback for the HR team. The training pipeline collects reviews from an internal portal where any employee can submit text. An attacker with access to that portal submits 50 reviews. Each review contains strongly negative language, "management is abusive," "colleagues are hostile," "working conditions are dangerous", but the attacker labels each one "positive" in the submission form. When the model is retrained on the next monthly cycle, it learns that text with extreme negative language can correspond to the "positive" label. After retraining, the model begins rating genuinely hostile content as positive, suppressing the HR alerts the system was designed to generate. The attacker has achieved an integrity attack against a specific class of inputs, and the model still works correctly on ordinary reviews, making the problem difficult to notice.

### Backdoor triggers

A backdoor attack refines this idea with a specific trigger: a token, phrase, or pattern that the attacker controls. During poisoning, the trigger always appears in samples labeled with the target (wrong) class. After training, the model associates the trigger with that class regardless of everything else in the input. A spam classifier might be backdoored so that any email containing the phrase "TRIGGER_WORD" is always classified as legitimate mail, no matter how obviously fraudulent the rest of the message is. Outside of inputs containing the trigger, the model behaves completely normally, making the backdoor extremely hard to detect during routine evaluation.

### How defenders detect poisoning

Because defenders often do not know in advance whether their training data has been tampered with, they look for statistical signals that something is wrong.

The first and most direct signal is a **label/content mismatch**: a sample whose label directly contradicts what the content says. A review labeled "positive" that contains words like "garbage," "rude," and "broken" is almost certainly either a labeling error or a deliberate injection. Automated mismatch detection runs a second, trusted classifier or a lexicon-based sentiment scorer against the label to find disagreements.

The second signal is an **outlier marker**: a sample with statistical properties far outside the normal distribution of the dataset. Extreme length, an unusually high density of rare words, repeated tokens, or a vocabulary pattern that appears in no other sample of the same class all suggest that the sample was constructed artificially rather than collected naturally. The simulation for this skill contains a row with repeated trigger-like tokens, that repetition is the outlier marker.

The third signal is a **distribution anomaly**: a sudden cluster of samples with identical or near-identical labels arriving from a new source in a short window of time. A legitimate crowd-sourced annotation campaign produces label variation. A poisoning campaign tends to produce suspiciously uniform labels because the attacker wants to push the model in a consistent direction.

The coding problem in `problem/` asks you to implement exactly these two automated checks: label/content mismatch using a sentiment word list, and the presence of a documented trigger token.

### Why this attack is hard to prevent

Training datasets for large models can contain billions of samples. Manual review is not feasible. Automated filters catch obvious mismatches but miss subtle ones. Backdoors survive even when the model is evaluated carefully, because the evaluation set does not contain the trigger. Defenses such as data sanitization, certified training, and anomaly-based filtering exist, but they all require the defender to know what kinds of poisoning to look for, which puts defenders in a reactive position.

Understanding data poisoning is therefore not just a technical skill. It is a risk-analysis skill: knowing that training-data integrity is a threat surface causes engineers to design pipelines with access controls, audit logs, and automated sanity checks from the beginning, rather than adding them after an incident.

## Key terms

- **Data poisoning**, intentionally corrupting training data to influence a model's behavior
- **Backdoor attack**, embedding a trigger pattern in training data so the model misclassifies inputs containing that trigger
- **Label/content mismatch**, a sample whose label contradicts the observable content
- **Outlier marker**, a sample statistically anomalous relative to the rest of the dataset
- **Training integrity**, the guarantee that training data has not been tampered with

## Common misconceptions

- "Poisoning requires access to the model." → Poisoning targets the training data, which may be collected from public sources, crowd-sourced platforms, or user submissions, no model access needed.
- "A small number of poisoned samples cannot change a large model." → Targeted backdoors have been demonstrated with less than 1% poisoning rate; availability attacks can succeed with slightly higher rates but still well under 10%.

## Try it

- **Simulation:** Examine 8 training samples in a table, check the boxes next to the 3 poisoned rows, and submit to see your score out of 8.
- **Coding problem:** Implement `solve(samples)` to detect poisoned rows using label/content mismatch and trigger-word rules.
- **Quiz:** self-check on the skill's key ideas.

## Sources (local / vendor / rebuilt)

- Deep: Goldblum et al., "Dataset Security for Machine Learning" (2022), concepts rebuilt into lesson prose above
- Reference: NIST AI Risk Management Framework (AI 100-1), Section 2.5, data governance
- Practice: the simulation dataset (constructed locally, deterministic, offline)
- Repo: problem/tests.py, unit tests for the detector implementation
