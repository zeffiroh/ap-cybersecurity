# 2.1.c: Risk language: likelihood, impact, and security goals

> **Unit 2 · 2.1 Security Foundations: CIA Triad**
> **AP Learning Objective(s):** 2.1.C, 2.1.D, 2.1.E, 2.1.F, 2.1.G
> **Course skill(s):** Analyze Risk

## Learning objective (student-facing)
Define likelihood, impact, and asset value in a cybersecurity context, calculate a risk score, and select and justify the most appropriate risk treatment (Mitigate, Accept, Transfer, Avoid) for a given scenario.

## Lesson

### The Language of Risk
Every organization faces threats. A threat is a potential negative event (like a hard drive failing, a database leak, or a hurricane). A vulnerability is a weakness in the system that makes the threat possible (like using an outdated operating system or storing servers in a basement). When a threat exploits a vulnerability, we have a security incident.

In cybersecurity, **risk** is the probability that a threat will exploit a vulnerability and cause harm to an asset. To talk about risk professionally, we use a standard vocabulary formalized by NIST (specifically NIST SP 800-30):
- **Asset**: anything of value to the organization (data, hardware, software, reputation).
- **Asset Value (V)**: the monetary or strategic value of the asset.
- **Likelihood (L)**: the probability of the threat occurring, usually scored on a scale from 1 (very low) to 5 (very high).
- **Impact (I)**: the severity of the damage if the threat occurs, scored from 1 (negligible) to 5 (catastrophic).

Defenders use these metrics to calculate a **Risk Score**:
$$\text{Risk Score} = \text{Likelihood} \times \text{Impact}$$
This score ranges from 1 to 25. An organization cannot defend against everything. By calculating risk scores, they prioritize which risks require budget and attention.

### The Four Risk Treatments
Once a risk is identified and scored, the organization must decide how to handle it. There are four canonical risk treatment strategies:

1. **Mitigate (Reduce)**
   Mitigation means implementing controls to reduce the likelihood or the impact of the risk. This is the most common defensive action.
   * *Example:* Installing a fire suppression system in a server room reduces the *impact* of a fire. Conducting regular vulnerability scans reduces the *likelihood* of an exploit.
   * *When to use:* High-risk scenarios where cost-effective controls are available.

2. **Accept (Retain)**
   Acceptance means acknowledging the risk but taking no action, usually because the cost of mitigation exceeds the value of the asset or the risk score is very low.
   * *Example:* A company accepts the risk that a low-traffic marketing blog might go offline for an hour, since the blog has no transactional value.
   * *When to use:* Low risk scores, or when mitigation costs are unreasonably high relative to the threat.

3. **Transfer (Share)**
   Transference means shifting the financial burden of the risk to a third party.
   * *Example:* Buying cyber insurance to cover the costs of a data breach, or outsourcing website hosting to a cloud provider with a Service Level Agreement (SLA) that pays out during downtime.
   * *When to use:* High impact risks that are too expensive to mitigate fully, but can be insured.

4. **Avoid (Eliminate)**
   Avoidance means changing plans or business processes to eliminate the risk entirely.
   * *Example:* A retail store decides to completely stop collecting and storing customer credit card numbers. By using a third-party payment processor, they eliminate the risk of their credit card database being breached.
   * *When to use:* Extreme risks where the cost of protection is higher than the business value of the activity.

### Sorting the Controls You Choose
Mitigation means picking controls, and every control can be sorted on two independent axes. By **function**, when it acts in the life of an incident: **preventive** controls stop it happening (a locked door, MFA), **detective** controls notice it (CCTV, an intrusion detection alert), **corrective** controls restore things afterwards (backups, a re-imaged laptop), **deterrent** controls discourage the attempt (a warning banner), and **compensating** controls stand in when the preferred control cannot be used. By **category**, how it is implemented: **technical** (software and hardware), **administrative** (policies, training, background checks), or **physical** (locks, guards, fences). A security camera is physical and detective; a background-check policy is administrative and preventive.

### Why One Strong Control Is Not Enough
Every control has a known way to fail: passwords get phished, antivirus misses new malware, a firewall rule is written in the wrong order, a detective alert goes unread. **Defense in depth** layers several independent controls so that an attacker who defeats one still meets the next. The layers must fail for different reasons, two controls that share one weakness add little. In the 2013 Target breach, the intrusion detection system did flag the malware, but nobody acted on the alert and the vendor's network path to the payment systems was not segmented, so no remaining layer stopped the theft.

### Risk Calculus
To decide which strategy to use, security teams compare the cost of a control against the asset value and the risk score. For instance, if a database is worth $10,000, spending $20,000 on a firewall is mathematically irrational. 
The coding problem in `problem/` models this decision-making process. By evaluating the threat likelihood, impact, mitigation cost, and asset value, you will write a program to recommend the optimal risk treatment.

## Key terms
- **Risk**: the probability that a threat will exploit a vulnerability and cause harm.
- **Likelihood**: the probability of a threat occurring (scored 1-5).
- **Impact**: the severity of the consequences if a threat occurs (scored 1-5).
- **Mitigate**: reducing risk by implementing security controls.
- **Accept**: retaining risk without active mitigation when it is low-impact or too expensive to fix.
- **Transfer**: sharing risk with third parties (like insurance or cloud hosting).
- **Avoid**: eliminating risk by stopping the risky activity altogether.
- **Control function**: when a control acts: preventive, detective, corrective, deterrent, or compensating.
- **Control category**: how a control is implemented: technical, administrative, or physical.
- **Defense in depth**: layering independent controls so that the failure of one does not expose the asset.

## Common misconceptions
- "We must eliminate all risk." → Impossible. Security has a cost, and organizations must accept some level of risk (known as risk appetite) to function.
- "Cyber insurance replaces technical security." → Insurance covers financial damage but does not prevent reputational loss, operational downtime, or legal liability.
- "Risk is the same as threat." → A threat is the actor or event (e.g., malware); risk includes how likely it is to happen to *us* and how bad it will be.

## Try it
- **Simulation:** Calculate risk scores and select the best treatment options based on budget constraints.
- **Coding problem:** Implement `solve(risks)` to classify risks into Mitigate, Accept, Transfer, or Avoid based on standard thresholds.
- **Quiz:** self-check on the skill's key ideas.

## Sources (local / vendor / rebuilt)
- Deep: NIST SP 800-30 Rev. 1 (Guide for Conducting Risk Assessments), rebuilt as original prose above; see `vendor/nist/sp800-30-summary.md` notes.
- Reference: Wikiversity "Risk Management", foundational definitions of likelihood and impact.
- Practice: NICE Challenge Project defensive scenario framework, rebuilt locally as the simulation.
