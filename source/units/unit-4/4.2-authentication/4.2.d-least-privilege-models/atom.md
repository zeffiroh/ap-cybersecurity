# 4.2.d, Least privilege and access control models

> **Unit 4 · 4.2 Authentication**
> **AP Learning Objective(s):** 4.2.B, 4.2.C
> **Course skill(s):** Mitigate Risk

## Learning objective (student-facing)
Explain the principle of least privilege, describe why
over-privileged accounts increase risk, distinguish DAC, MAC, RBAC, and ABAC access control
models, and recognize privilege creep and the controls that mitigate it.

## Lesson
Every account, process, and service on a system needs *some* level of access to do its job, a
help-desk technician needs to reset passwords, a database service needs to read certain tables, a
web server needs to write to a log directory. The **principle of least privilege (PoLP)** says
that every subject should be granted the *minimum* access required to perform its function, and
nothing more. Not "access that might be convenient later," not "access equal to a coworker's role
just in case", only what the current job function strictly requires. Least privilege is not a
single tool you install; it is a design discipline applied every time an account is created,
a permission is granted, or a role changes.

**Why over-privileged accounts are dangerous.** Extra access does not sit harmlessly unused, it
expands the *blast radius* of every bad thing that can happen to that account. If a marketing
intern's account has read-only access to a shared drive, a phished credential exposes only that
drive. If the same account somehow has write access to the production database, the same phishing
email now threatens the database too. This is true for three overlapping threats: (1) **external
compromise**, attackers who steal or guess credentials inherit whatever privileges the account
holds, so a low-privilege account limits what they can do next; (2) **insider threat**, a
disgruntled or careless employee can only misuse access they actually have; and (3) **malware and
ransomware propagation**, malware executing under a user's session inherits that user's
privileges, so an over-privileged user who opens an infected attachment can hand ransomware
write access to systems far beyond their own workstation. Least privilege does not prevent every
attack, but it consistently shrinks the damage any single compromised account can do.

**Access control models.** Organizations implement least privilege through a formal *access
control model*, a system for deciding who gets to do what to which resource.

- **Discretionary Access Control (DAC)**, the owner of a resource decides who else can access
  it and at what level. Standard Unix/Linux file permissions (`rwx` for owner, group, others) are
  the classic example: whoever owns a file can grant or revoke access to it directly. DAC is
  flexible and simple but scales poorly, permissions sprawl as owners individually grant access,
  and no central authority enforces consistency.
- **Mandatory Access Control (MAC)**, access is decided centrally, not by resource owners, using
  fixed classification labels (e.g., "Confidential," "Secret," "Top Secret") assigned to both
  subjects and resources. A user cannot grant access to a file above their own clearance level
  even if they wanted to. MAC is common in government and military systems and is implemented in
  tools like SELinux. It is rigid but very strong against insider misconfiguration.
- **Role-Based Access Control (RBAC)**, permissions are attached to *roles* (e.g., "Payroll
  Clerk," "Network Admin"), and users are assigned to one or more roles rather than receiving
  permissions individually. Changing a person's job means changing their role assignment, not
  hand-editing dozens of individual permissions. RBAC is the most common model in enterprise IT
  because it scales: define the roles once, then manage membership.
- **Attribute-Based Access Control (ABAC)**, access decisions are made dynamically at request
  time based on *attributes* of the user, the resource, and the environment (e.g., "allow access
  only if department = finance AND time is business hours AND device is company-managed"). ABAC
  is more flexible than RBAC because policy can react to context, but it is more complex to audit
  and reason about.

**Privilege creep.** Access rights tend to accumulate over time rather than shrink. An employee
transfers from Sales to Engineering and picks up new system access for the new role, but the old
Sales access is often never revoked, because removing access requires someone to notice and act,
while granting it is a routine part of onboarding. This silent accumulation of unnecessary
privileges is called **privilege creep**, and it directly undermines least privilege even in an
organization that started out well-configured. The standard mitigation is a **periodic access
review** (or *recertification*): on a fixed schedule, a manager or system owner must explicitly
re-approve every access grant a user holds, and anything not re-approved is revoked.

**Separation of duties and just-in-time access.** Least privilege pairs naturally with
**separation of duties**, structuring sensitive processes so no single person has end-to-end
control. For example, the person who approves a purchase should not also be the person who can
issue the payment; splitting these roles means a single compromised or malicious account cannot
complete the whole fraudulent transaction alone. A related technique is **just-in-time (JIT)
access**: instead of granting standing elevated privileges that sit active (and exploitable) all
day, an account requests elevated access for a specific, time-bound window, such as a four-hour
incident-response session, and the privilege automatically expires afterward. JIT access keeps
the "always-on" attack surface small while still letting legitimate work happen when it is
actually needed.

The coding problem in `problem/` asks you to build an access-request auditor that applies these
ideas in a fixed priority order, the same triage logic a security team runs before approving a
permission request. The simulation in the simulation gives you a stream of realistic access requests
to classify using the same reasoning.

## Key terms
- **Least privilege (PoLP)**, grant a subject only the minimum access needed to perform its
  function, nothing more.
- **DAC (Discretionary Access Control)**, resource owner decides and grants access; e.g. Unix
  file permissions.
- **MAC (Mandatory Access Control)**, access decided centrally via fixed classification labels;
  e.g. government/military systems, SELinux.
- **RBAC (Role-Based Access Control)**, permissions attached to roles; users assigned to roles.
  Most common model in enterprise IT.
- **ABAC (Attribute-Based Access Control)**, access decided dynamically from attributes of user,
  resource, and environment.
- **Privilege creep**, the silent accumulation of unnecessary access over time as roles change.
- **Separation of duties**, structuring a sensitive process so no single person controls it
  end-to-end.
- **Access review**, a periodic recertification where unused or unjustified access is revoked.
- **Just-in-time (JIT) access**, temporary, time-bound elevated access granted only for the
  duration it is needed.

## Common misconceptions
- "Giving admin rights to everyone is more convenient and low-risk if you trust your employees." →
  Trust does not shrink blast radius. A trusted employee's account can still be phished or
  infected by malware, and malware inherits the privileges of whoever runs it, over-provisioning
  turns any single compromise into an organization-wide one.
- "RBAC and ABAC are the same thing." → RBAC assigns static permissions to a role and a user
  inherits that role's access; ABAC evaluates dynamic attributes (user, resource, environment) at
  the moment of the request. RBAC answers "what role are you," ABAC answers "do current
  conditions satisfy the policy."
- "Once access is granted correctly, it stays correct." → Access correctness decays over time as
  people change roles (privilege creep). Least privilege requires ongoing periodic access review,
  not a one-time setup.

## Try it
- **Simulation:** Correctly triage a stream of access requests, approve, deny, or flag each one per least-privilege rules, reaching the target score.
- **Coding problem:** Implement an access-request auditor function that applies a
  fixed priority order (justification, review recency, time-boundedness) to each request.
- **Quiz:** self-check on the skill's key ideas.

## Sources (local / vendor / rebuilt)
- Deep: NIST, rebuilt as original prose above.
- Reference: Wikiversity
- Practice: SANS Cyber Aces
- Repo: LetsDefend/Free-Cybersecurity-Resources → `vendor/repos/LetsDefend-Free-Cybersecurity-Resources`.
