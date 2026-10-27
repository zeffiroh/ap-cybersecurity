# 5.2.c, Credential theft prevention and lateral movement

> **Unit 5 · 5.2 Protecting Applications and Data: Access Controls**
> **AP Learning Objective(s):** 5.2.B, 5.2.C
> **Course skill(s):** Mitigate Risk, Detect Attacks

## Learning objective (student-facing)
Explain how stolen credentials enable an attacker to move
laterally across a network, identify the detection signals that indicate lateral movement is
happening, and describe the access-control practices (MFA, credential hygiene, network
segmentation) that limit its spread.

## Lesson
Most large breaches do not end where they begin. An attacker rarely gets everything they want from
the very first account they compromise, a phished marketing employee's laptop, for instance,
usually has no access to the finance database or the domain controller. What makes a breach
catastrophic is what happens *next*: the attacker uses that first foothold to steal more
credentials and hop from system to system until they reach something valuable. This process is
called **lateral movement**, and understanding it is why access control (Unit 5.2) and detection
(Unit 4) are two halves of the same defense.

**Credential theft** is the starting fuel for lateral movement. Once an attacker has a foothold on
one machine, they harvest credentials that are sitting in memory, in configuration files, or in the
operating system's credential cache, often using well-known toolkits that dump passwords, password
hashes, or authentication tokens directly from a compromised machine's memory. Crucially, an
attacker frequently does not need the plaintext password at all: many enterprise authentication
protocols allow **hash-based** or **ticket-based** authentication, so a stolen password hash or
session ticket can be replayed to authenticate as that user on other systems without ever cracking
it, attacks commonly grouped under the label "pass-the-hash" / "pass-the-ticket."

With a stolen credential in hand, the attacker attempts to authenticate to nearby systems the
compromised account has access to, a file server, another workstation, an admin console. If that
credential belongs to a normal user with narrow permissions, lateral movement stalls quickly
(this is least privilege, from 5.2.b, doing its job). But if the compromised account is an IT
administrator, or if the organization reuses one local administrator password across every machine
(a very common and very dangerous shortcut), the attacker can hop from machine to machine almost
unopposed, harvesting more credentials at each stop, hunting for a path to the crown-jewel systems:
domain controllers, backup servers, financial databases. This final goal is often called
**privilege escalation** combined with lateral movement, the attacker's access keeps expanding
both sideways (more machines) and upward (more powerful accounts) until they control the
environment.

Several access-control practices from this unit directly blunt this chain:

**Multi-factor authentication (MFA)** breaks the "stolen password = access" assumption: even a
perfectly stolen credential is useless without the second factor (a phone prompt, a hardware key,
a one-time code), which stops the vast majority of credential-replay attempts cold.

**Credential hygiene**, unique passwords per system, no shared local-admin passwords across
machines, regular credential rotation, and never storing plaintext passwords in scripts or config
files, removes the easy "one stolen credential unlocks everything" shortcut that fuels rapid
lateral movement.

**Least privilege and network segmentation** limit how far a single stolen credential can travel.
If workstations cannot directly reach the finance database, and a compromised marketing account has
no domain-admin rights, the attacker's lateral movement hits a wall quickly, buying defenders time
to detect and respond.

Detection matters as much as prevention, because a sufficiently patient or well-resourced attacker
will eventually find *some* foothold. Security teams watch for **behavioral anomalies** that mark
lateral movement in progress: a single account authenticating to an unusually large number of
distinct hosts in a short window, authentication attempts at odd hours relative to the user's normal
pattern, a user account suddenly using administrative tools it has never touched before, or repeated
authentication failures across many hosts followed by a success (suggesting credential
guessing/spraying rather than normal single-sign-on behavior).

The coding problem in this skill asks you to build exactly this kind of detector: given a
synthetic authentication log (account, source host, destination host, timestamp), flag accounts
whose host-hopping pattern is consistent with lateral movement. The simulation lets you play
network defender, watching a fictional internal network graph light up as a compromised account
hops between hosts, and deciding when the pattern crosses the threshold that should trigger an
alert.

## Key terms
- **Lateral movement**, an attacker using a compromised account/host to reach additional systems
  within a network after an initial foothold.
- **Pass-the-hash / pass-the-ticket**, authenticating using a stolen password hash or session
  ticket without ever knowing the plaintext password.
- **Privilege escalation**, increasing the level of access an attacker holds, often paired with
  lateral movement toward higher-value accounts/systems.
- **Multi-factor authentication (MFA)**, requiring a second proof of identity beyond a password,
  which neutralizes most stolen-credential replay attempts.
- **Network segmentation**, dividing a network so that compromise of one segment does not grant
  direct reach into another (e.g., isolating finance systems from general workstations).

## Common misconceptions
- "A strong password alone stops credential theft." → Many lateral-movement techniques replay a
  stolen hash or ticket without ever needing the plaintext password, MFA and hygiene practices
  matter more than password strength alone.
- "Lateral movement is only detectable after the fact." → Behavioral signals (unusual host counts,
  atypical hours, first-time admin-tool use) can flag lateral movement while it is in progress,
  which is exactly what the detection tooling covered in Unit 4 is built to surface.

## Try it
- **Simulation:** Watch a fictional network graph and correctly
  flag which accounts show lateral-movement behavior before the sim reveals the answer.
- **Coding problem:** Build a detector that flags accounts in an authentication log
  whose host-hopping pattern indicates lateral movement.
- **Quiz:** self-check on the skill's key ideas.

## Sources (local / vendor / rebuilt)
- Deep: NIST (identity/credential guidance), rebuilt as original prose above.
- Reference: Wikiversity (Information Security / Access control models).
- Practice: Cybrary lateral-movement micro-labs → rebuilt locally as the simulation.
- Repo: LetsDefend/Free-Cybersecurity-Resources → `vendor/repos/letsdefend-free-cybersecurity-resources`.
