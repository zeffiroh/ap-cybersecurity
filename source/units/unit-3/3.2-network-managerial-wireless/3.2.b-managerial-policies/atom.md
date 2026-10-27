# 3.2.b, Managerial controls and security policies

> **Unit 3 · 3.2 Protecting Networks: Managerial & Wireless Security**
> **AP Learning Objective(s):** 3.2.A, 3.2.B
> **Course skill(s):** Mitigate Risk

## Learning objective (student-facing)
Distinguish managerial (administrative) controls from technical
and physical controls, describe the purpose of core security policy documents (AUP, least
privilege, security awareness training), and match a given organizational scenario to the correct
control type and policy.

## Lesson

### Three families of control
Security controls are commonly grouped into three families, and the AP course expects you to be
able to sort any given control into the right one. **Technical (logical) controls** are implemented
in hardware or software and enforce policy automatically, without a person deciding case-by-case, a firewall rule, WPA3 encryption (3.2.a), or an access-control list are all technical controls.
**Physical controls** restrict physical access to a space or device, a locked server room door, a
badge reader, or a security camera. **Managerial (administrative) controls** are the odd one out:
they are *policies, procedures, and processes*, documented rules about how people are expected to
behave, backed by training, oversight, and consequences, rather than a piece of hardware or
software that mechanically blocks an action. A written Acceptable Use Policy does not stop an
employee from visiting a malicious website the way a web filter (a technical control) does, it
sets the expectation, and the organization then relies on employee compliance, awareness, and
review to make it effective.

This skill focuses on managerial controls because they are frequently underestimated: students
(and, historically, many real organizations) invest heavily in technical controls while treating
policy as paperwork. In practice, managerial controls are often what determines whether the
technical and physical controls are configured correctly, kept current, and actually followed, policy is the layer that governs the people and processes operating everything else.

### Core policy documents
An **Acceptable Use Policy (AUP)** defines what employees are and are not permitted to do with
organizational systems and data, for example, prohibiting installation of unauthorized software,
setting rules for personal use of work devices, and specifying that company data may not be copied
to personal cloud storage. An AUP is typically the first document a new employee signs, and
violations of it are the basis for disciplinary action even when no technical control was
"broken" (e.g., an employee who emails a customer list to their personal account may not have
bypassed any firewall, but has clearly violated the AUP).

A **least privilege policy** establishes the principle that every account and role should be
granted only the minimum access necessary to perform its job function, nothing more. This is a
managerial control when it takes the form of a documented access-request and periodic-review
process (who approves access requests, how often access is re-certified, how access is revoked
when someone changes roles or leaves); the actual permission enforcement (an ACL denying a file
read) is the corresponding technical control. The policy is what makes sure the technical
permissions stay correct over time instead of accumulating unnecessary access (a problem called
"privilege creep").

**Security awareness training** is a recurring program (often annual, with periodic phishing
simulations) that teaches employees to recognize social engineering, follow the AUP, report
suspicious activity, and understand their role in the organization's security posture. Awareness
training is a managerial control because it changes behavior through education and reinforcement,
not through a technical mechanism, an employee who has been trained to recognize a phishing email
is a control in exactly the same sense that a spam filter is, just implemented through people
instead of software.

Other common managerial controls include: an **incident response policy** (who does what, in what
order, when a breach is suspected), a **data classification policy** (labeling data by sensitivity
so handling rules can be applied consistently), a **change management policy** (requiring review
and approval before production systems are modified), and a **vendor/third-party risk policy**
(requiring security review of any vendor who will handle organizational data).

### Why policy without enforcement fails, and why enforcement without policy also fails
A policy that exists only on paper, with no training, no monitoring, and no consequences for
violation, is close to useless, employees will not know the rule exists, or will learn that
nothing happens when it is ignored. Conversely, a technical control implemented without a policy
explaining its purpose often gets circumvented or generates confused, frustrated pushback (for
example, employees finding workarounds for an access restriction they don't understand the reason
for). Effective security programs pair managerial controls with the technical and physical controls
they govern: the AUP explains why the web filter blocks certain sites; the least-privilege policy
explains why an employee's access request was denied; awareness training explains why multi-factor
authentication is required. NIST's control catalog (SP 800-53) explicitly organizes controls this
way, with families like Awareness and Training (AT), Access Control (AC), and Planning (PL) sitting
alongside technical families like System and Communications Protection (SC).

### Matching scenarios to control type
The coding problem in `problem/` gives you a list of security scenarios (a description of what an
organization did) and asks you to classify each as `"managerial"`, `"technical"`, or `"physical"`, the same triage skill the AP exam tests directly, and the same judgment a security program manager
uses when building a control matrix (a document mapping each risk to the controls addressing it,
across all three families).

## Key terms
- **Managerial (administrative) control**, a documented policy, procedure, or process governing
  human behavior and organizational process, enforced through training, review, and consequences
  rather than automatically by hardware/software.
- **Technical (logical) control**, a control implemented in hardware or software that enforces
  policy automatically (e.g., a firewall, encryption, an access-control list).
- **Physical control**, a control that restricts physical access to a space or device (e.g., a
  locked door, a badge reader).
- **Acceptable Use Policy (AUP)**, a policy defining permitted and prohibited use of
  organizational systems and data.
- **Least privilege policy**, a policy requiring that access be limited to the minimum necessary
  for a role, with a documented request/review/revocation process.
- **Security awareness training**, a recurring program that teaches employees to recognize
  threats (like social engineering) and follow security policy.
- **Privilege creep**, the gradual, unreviewed accumulation of unnecessary access rights over
  time, which least-privilege review policies are designed to catch and correct.

## Common misconceptions
- "A policy is not a real control unless it's enforced by software." → Managerial controls are a
  distinct, legitimate control family (alongside technical and physical). A signed AUP,
  documented access-review cadence, or completed awareness training all count as controls in
  their own right, even though none of them are software.
- "Security awareness training is just a compliance checkbox." → When implemented well (recurring,
  reinforced with realistic phishing simulations, tied to measurable behavior change), awareness
  training measurably reduces successful social-engineering attacks, it is functioning as a
  control, not merely satisfying an audit requirement.

## Try it
- **Simulation:** Classify organizational security scenarios as
  managerial, technical, or physical controls, reaching the scoring goal.
- **Coding problem:** Classify a list of security scenario descriptions by control
  type (managerial, technical, or physical) based on keyword and context rules.
- **Quiz:** self-check on the skill's key ideas.

## Sources (local / vendor / rebuilt)
- Deep: NIST SP 800-53 Rev. 5 (control families AT, AC, PL), rebuilt as original prose above;
  reference copy at `vendor/nist/sp800-53-control-families.md`.
- Reference: CompTIA Security+ objectives, "Control Types", rebuilt equivalent at
  `vendor/reference/3.2.b-control-types-ref.md`.
- Practice: Cybrary security-policy fundamentals module, rebuilt locally as the simulation.
- Repo: LetsDefend/Free-Cybersecurity-Resources, `vendor/repos/LetsDefend-Free-Cybersecurity-Resources/`.
