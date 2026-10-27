# 5.2.b, Roles, permissions, and least privilege

> **Unit 5 · 5.2 Protecting Applications and Data: Access Controls**
> **AP Learning Objective(s):** 5.2.A, 5.2.B
> **Course skill(s):** Mitigate Risk

## Learning objective (student-facing)
Explain how permissions are bundled into roles, apply the
principle of least privilege to evaluate whether a role assignment is over-permissioned, and
identify the risks of privilege creep and excessive standing access.

## Lesson
The previous atom (5.2.a) introduced the three access control models. This skill goes one level
deeper into the model organizations use most: **Role-Based Access Control (RBAC)**, and the design
principle that should guide every role you define, **least privilege**.

A **permission** is a single, narrow grant: "read the invoices table," "restart the web service,"
"delete a user account." Real systems have hundreds or thousands of possible permissions. Assigning
them one at a time to each individual user does not scale, it is slow, error-prone, and nearly
impossible to audit ("does Dana still need delete-access to payroll from that project two years
ago?"). RBAC solves this by grouping permissions into **roles**: "Support Agent" might bundle
`read_ticket`, `write_ticket_reply`, and `read_customer_profile`; "Billing Admin" might bundle
`read_invoice`, `write_invoice`, `issue_refund`. A user is then assigned one or more roles, and
inherits every permission those roles carry. When someone changes jobs, an administrator changes
their *role assignment*, not a scattered list of individual permissions.

**Least privilege** is the principle that a subject, a user, a service account, a process, should be granted only the permissions it actually needs to perform its job, and nothing more.
This sounds obvious, but it is violated constantly in practice, for a very human reason:
**it is easier to over-grant than to under-grant.** If a new employee's role is missing a
permission they need, they immediately notice and complain, the gap is loud. If a role has a
permission the employee will never use, nothing breaks and nobody notices, the excess is silent.
Left unchecked, this asymmetry causes **privilege creep**: over months and years, employees who
change teams or take on temporary projects accumulate more and more permissions, because access is
added when needed but rarely removed when it stops being needed.

Why does this matter for security specifically, not just tidiness? Because permissions are the
**blast radius** of a compromised account. If an attacker phishes a support agent's credentials and
that agent's role is scoped tightly to ticket-handling permissions, the attacker can read and reply
to tickets, bad, but contained. If that same support agent's account, through years of privilege
creep, also carries `delete_invoice` and `read_all_customer_pii` because a manager once said "just
give them access to be safe," the same phishing email now hands the attacker a much larger breach.
Least privilege is a *containment* strategy: it does not stop every attack, but it caps the damage
any single compromised identity can do.

Two closely related practices reinforce least privilege in real deployments. **Role review /
recertification** is a periodic process (often quarterly or annually) where managers or system
owners are asked to re-confirm that every person assigned to a role still needs it, this is the
deliberate counterweight to privilege creep's silent accumulation. **Separation of duties** ensures
that no single role can complete an entire sensitive process alone, for example, the person who
*creates* a vendor payment should not also be the person who *approves* it, so that fraud requires
collusion between two people rather than the abuse of one over-broad role.

A common design mistake is creating one giant "power user" or "manager" role that bundles every
permission a manager might conceivably need across every function, rather than composing narrower
roles ("Approver," "Report Viewer," "Team Editor") that a manager is assigned only as needed. The
narrow-roles approach is more setup work up front but dramatically reduces blast radius and makes
audits tractable, you can answer "who can delete invoices?" by listing one role's members instead
of manually checking a thousand individual users.

The coding problem in this skill asks you to build the analysis a security reviewer would run:
given a set of roles (with their permissions), a set of users (with their assigned roles), and each
user's actual job function (the minimum permission set they need), flag any user who holds
permissions beyond what their job function requires, a least-privilege violation. The simulation
puts you in the reviewer's seat, assigning and trimming roles for a fictional small company until
every account satisfies least privilege.

## Key terms
- **Permission**, a single narrow grant to perform one action on one resource type.
- **Role**, a named bundle of permissions assigned to users as a unit (RBAC).
- **Least privilege**, granting a subject only the permissions it needs, nothing more.
- **Privilege creep**, the gradual, unnoticed accumulation of unnecessary permissions over time.
- **Role review / recertification**, periodic re-confirmation that role assignments are still
  justified, used to counteract privilege creep.
- **Separation of duties**, splitting a sensitive process across multiple roles so no single role
  can complete it alone.

## Common misconceptions
- "Giving extra access 'just in case' is harmless if it's never used." → Unused excess permission
  is exactly what increases blast radius if that account is ever compromised, it is a silent risk,
  not a neutral one.
- "Once a role is set up correctly, it stays correct." → Job functions and org structure change
  continuously; without periodic review, roles drift away from least privilege via creep.

## Try it
- **Simulation:** Trim role assignments for a set of fictional
  employees until every account satisfies least privilege, reaching the target score.
- **Coding problem:** Build a function that flags users whose assigned-role
  permissions exceed what their job function requires.
- **Quiz:** self-check on the skill's key ideas.

## Sources (local / vendor / rebuilt)
- Deep: NIST SP 800-192 / NIST RBAC guidance, rebuilt as original prose above.
- Reference: Wikiversity (Information Security / Access control models).
- Practice: Cybrary access-control micro-labs → rebuilt locally as the simulation.
- Repo: LetsDefend/Free-Cybersecurity-Resources → `vendor/repos/letsdefend-free-cybersecurity-resources`.
