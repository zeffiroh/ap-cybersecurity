# 5.2.a, Access control models (RBAC, DAC, MAC)

> **Unit 5 · 5.2 Protecting Applications and Data: Access Controls**
> **AP Learning Objective(s):** 5.2.A
> **Course skill(s):** Mitigate Risk

## Learning objective (student-facing)
Explain what access control is, distinguish between the three
primary access control models (DAC, MAC, RBAC), and select the appropriate model for a given
organizational scenario.

## Lesson
Every application stores data that should not be readable or modifiable by everyone. An
organization's payroll file should be visible to HR managers, not to interns. A classified
government document should only reach employees with the correct clearance. A hospital system
should let nurses update patient notes but not delete billing records. The mechanism that enforces
these boundaries is **access control**: the policy and technical machinery that decides who can
do what to which resource.

Access control operates on three concepts. A **subject** is the entity requesting access, a
user account, a process, or a service. An **object** is the resource being protected, a file,
a database table, an API endpoint. A **permission** is the action being requested, read, write,
delete, execute. An access control model is the rule system that maps (subject, object) pairs to
permitted actions.

Three models appear on the AP framework and in almost every real enterprise system.

**Discretionary Access Control (DAC)** lets the *owner* of an object decide who else may access
it. "Discretionary" means the decision is at the owner's discretion. If you create a spreadsheet,
you can share it with a colleague or keep it private; you control the access list. Traditional Unix
file permissions are a DAC system: the file's owner sets read/write/execute bits for owner, group,
and others. Windows NTFS permissions, Google Drive sharing, and most consumer cloud services also
use DAC. The strength of DAC is flexibility, owners can grant access quickly without involving a
central administrator. The weakness is consistency: owners can accidentally or carelessly grant
excessive access, and there is no organization-wide enforcement of a minimum standard. Malware
running as a user can also inherit and abuse all of that user's permissions.

**Mandatory Access Control (MAC)** removes discretion from the owner. Instead, a central policy
authority assigns **labels** (also called classifications) to both subjects and objects. The system
enforces rules automatically: a subject with label SECRET can read objects labeled SECRET or below
but not TOP SECRET, regardless of what the file owner might prefer. Subjects cannot grant access to
others beyond their own level. MAC originated in government and military environments (DoD Orange
Book, Bell-LaPadula model) where information must not flow upward to higher-classified users and
certainly not leak downward to lower-cleared ones. SELinux and AppArmor are MAC-inspired systems
used in Linux. The strength of MAC is strong, consistent enforcement that users cannot override.
The weakness is administrative overhead: labeling every object correctly requires careful policy
design, and rigid labels can impede legitimate work.

**Role-Based Access Control (RBAC)** is today's dominant enterprise model. Instead of tying
permissions directly to users or sensitivity labels, RBAC defines **roles**, "Nurse," "Billing
Clerk," "Admin," "Auditor", and attaches permissions to roles. Users are then assigned one or
more roles. A nurse account inherits every permission the Nurse role holds. When a nurse leaves
and a replacement joins, the administrator simply assigns the Nurse role to the new account;
individual permission lists do not have to change. RBAC scales well: a hospital with 5,000 staff
might have 30 roles rather than 5,000 separate access lists. It also enforces *separation of
duties* naturally, a role for data entry can be kept separate from a role for data approval.
The weakness is role proliferation: organizations that create too many fine-grained roles
("Junior Billing Clerk in Region 4") recreate the complexity problem in a different form.

In practice, many systems blend models. An operating system may use MAC to enforce overall
clearance labels while using RBAC inside applications to manage job functions, and DAC as the
fallback for user-owned files. Understanding which model is in use tells a security analyst
where control authority lives (owner, central authority, or role assignment) and where
misconfiguration is most likely to appear.

A critical concept that cuts across all three models is **least privilege**: grant each subject
only the permissions needed to do its job, nothing more. A web server process that reads a
public directory should not have write or delete permissions. An intern account should not have
access to salary tables. Least privilege limits the blast radius when an account is compromised:
an attacker who hijacks a low-privilege account inherits only that account's narrow access,
not the whole system. The simulation and coding problem in this skill reinforce how to evaluate
whether a given access decision satisfies the rules of the relevant model.

## Key terms
- **Access control**, the set of policies and mechanisms that determine which subjects can perform which actions on which objects.
- **Subject**, the entity requesting access (user, process, service).
- **Object**, the resource being protected (file, database, endpoint).
- **DAC (Discretionary Access Control)**, owner-controlled access; flexible but inconsistent.
- **MAC (Mandatory Access Control)**, centrally enforced label-based access; strong but rigid.
- **RBAC (Role-Based Access Control)**, permission-via-role assignment; scalable for organizations.
- **Least privilege**, granting only the minimum access necessary for a subject to function.
- **Role**, a named collection of permissions assigned to users as a unit.
- **Label / classification**, a MAC tag attached to subjects and objects (e.g., UNCLASSIFIED, SECRET).

## Common misconceptions
- "DAC is weak, so only MAC is secure.", Each model fits different contexts. MAC overhead is impractical for consumer software; DAC is appropriate when owners are trusted to manage their own data correctly.
- "RBAC and least privilege are the same thing.", RBAC is a mechanism; least privilege is a design principle. RBAC supports least privilege only if roles are defined narrowly. An RBAC system with an over-broad "superuser" role violates least privilege.
- "Once an access model is chosen, it handles everything automatically.", Models define the structure; administrators must still configure policies correctly. Misconfigured RBAC (too many permissions in a role) is a common real-world vulnerability.

## Try it
- **Simulation:** Correctly determine whether each access request should be ALLOW or DENY under the displayed model and policy, and reach the target score.
- **Coding problem:** Implement an access-decision function that enforces RBAC, DAC, and MAC rules for a fictional file system.
- **Quiz:** self-check on the skill's key ideas.

## Sources (local / vendor / rebuilt)
- Deep: NIST SP 800-162 (Guide to ABAC) and NIST SP 800-192, rebuilt as original prose above.
- Reference: Wikiversity (Information Security / Access control models).
- Practice: Cybrary access-control micro-labs, rebuilt locally as the simulation.
- Repo: LetsDefend/Free-Cybersecurity-Resources → `vendor/repos/letsdefend-free-cybersecurity-resources`.
