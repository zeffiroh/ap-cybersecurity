# In-class activity, 3.5.a Intrusion detection and prevention systems (IDS/IPS)

**Format:** pairs · **Time:** 25 min · **Offline:** yes

## Goal
Students can distinguish IDS from IPS, classify IDS alert outcomes (TP/FP/FN/TN), and explain the trade-off between sensitivity and false-positive rate. Ties to LO 3.5.A (identify IDS/IPS roles and detection methods).

## Materials (all local)
- the SimLab simulation on each machine, or the printed scenario set below.

## Steps
1. Each pair opens the simulation and works through the 6 alert scenarios. For each scenario they must agree on the classification (TP/FP/FN/TN) and write one sentence justifying their choice before submitting.
2. After completing the sim, pairs discuss: which two outcomes (TP/FP/FN/TN) represent failures? Which is more dangerous and why?
3. Pairs are given the following tuning scenario: "The IDS flags 200 alerts per day; analysts can investigate 50. The security manager asks whether to raise or lower the sensitivity threshold." Each pair writes a recommendation (one paragraph) and explains the trade-off.

## Collaborate (AP skill 4)
Assign roles: one partner is the "IDS analyst" (classifies each alert and defends the call), the other is the "SOC manager" (challenges the classification, is there evidence it is really benign/malicious?). Swap roles halfway through.

## Exit ticket
Each student submits: (1) a one-sentence definition distinguishing IDS from IPS, and (2) an example of why a false negative is more dangerous than a false positive in a healthcare network.

## Instructor notes
- Expected TP/FP/FN/TN answers match the sim scenario keys. Common stumble: students confuse false negative with "the negative (benign) outcome was wrong", clarify that positive/negative refers to the sensor's verdict, not the traffic type.
- The tuning discussion usually surfaces the alert-fatigue concept naturally; guide students toward naming it explicitly.
- Feeds the unit project (building a traffic analyzer) and scenario stage 3 (network intrusion detection).
