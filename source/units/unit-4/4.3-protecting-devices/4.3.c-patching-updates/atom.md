# 4.3.c, Patching and regular updates

> **Unit 4 · 4.3 Protecting Devices**
> **AP Learning Objective(s):** 4.3.B, 4.3.C
> **Course skill(s):** Mitigate Risk

## Learning objective (student-facing)
Explain why unpatched software is a top attack vector, describe
how the vulnerability-disclosure-to-exploit timeline works, and prioritize which patches an
organization should deploy first using severity, exploitation status, and exposure.

## Lesson
Antivirus and firewalls (4.3.a, 4.3.b) defend a device from the outside, they watch for known-bad
files and traffic. But many of the most damaging breaches in history did not require tricking a
user or evading a signature at all. They exploited a **known, published vulnerability** in
software that the victim organization had simply not yet fixed. **Patching**, applying vendor-
released code updates that close security holes, is one of the highest-leverage, lowest-cost
controls in all of cybersecurity, and it is also one of the most consistently neglected.

### The vulnerability lifecycle
Every piece of software has bugs, and some bugs are exploitable security flaws. The lifecycle of
a vulnerability typically runs through these stages:

1. **Discovery.** A researcher (or attacker) finds a flaw in the software, for example, a way to
   send malformed input that lets an attacker run arbitrary code.
2. **Disclosure.** In *responsible disclosure*, the researcher privately reports the flaw to the
   vendor and gives them time to fix it before going public. Each disclosed vulnerability is
   catalogued with a public **CVE (Common Vulnerabilities and Exposures)** identifier, e.g.
   `CVE-2024-12345`, along with a **CVSS (Common Vulnerability Scoring System)** severity score
   from 0-10 describing how easy and damaging exploitation would be.
3. **Patch release.** The vendor writes and ships a fix, a patch or update, usually alongside
   the public CVE disclosure, sometimes ahead of it ("patch Tuesday" cycles at large vendors).
4. **Weaponization.** Attackers reverse-engineer the patch (or the vulnerability disclosure
   itself) to build working exploit code. This can happen within *hours* of a patch shipping,
   because the patch diff itself reveals exactly what was broken.
5. **Exploitation in the wild.** Attackers scan the internet for systems that have not yet
   applied the patch and compromise them. This window is often called the **patch gap**, the
   time between a patch becoming available and an organization actually applying it.

The moment a patch is published, the vulnerability effectively becomes *public knowledge*, and
the race between defenders (apply the patch) and attackers (build and launch an exploit) begins
in earnest. This is the core reason patching promptness matters so much: publishing the fix also
publishes a roadmap of the flaw to anyone willing to reverse-engineer it.

### Zero-day vs. n-day
A **zero-day vulnerability** is one being actively exploited *before* any patch exists, there
are "zero days" of protection available, because even a fully up-to-date system is vulnerable.
Zero-days are rare and valuable to attackers precisely because patching cannot stop them (only
other layered defenses like EDR or network segmentation can help). Far more common, and far more
preventable, are **n-day vulnerabilities**: flaws for which a patch has existed for some number
of days ("n" days) but the target system has not yet applied it. The overwhelming majority of
real-world breaches exploit n-day vulnerabilities, not zero-days, because attackers know most
organizations lag behind on patching and it is far cheaper to reuse a known exploit than to
discover a new one.

### Why organizations delay patching
If patching is so effective, why do breaches involving year-old unpatched vulnerabilities remain
common? Patching is not free:

- **Compatibility risk.** A patch can break a business-critical application that depends on the
  old behavior. Organizations often test patches in a staging environment first.
- **Downtime.** Some patches (especially OS-level or firmware patches) require a reboot or
  service interruption, which must be scheduled around business needs.
- **Scale.** A large enterprise may have tens of thousands of endpoints, servers, and network
  devices, each potentially requiring a different patch, tested against a different set of
  dependent software.
- **Legacy and unsupported systems.** Some critical systems run on software the vendor no longer
  supports (end-of-life), meaning no patch will ever be released, these require compensating
  controls like network isolation instead.

### Patch management as a process
Because of these tensions, mature organizations run a formal **patch management** process rather
than patching ad hoc:

1. **Inventory**, know what software and versions are running on every asset (you cannot patch
   what you do not know you have).
2. **Prioritize**, triage new patches by CVSS severity, exploitability (is it already being
   exploited in the wild?), and exposure (is the vulnerable service internet-facing?).
3. **Test**, validate the patch in a non-production environment to catch compatibility breaks.
4. **Deploy**, roll the patch out, often in waves (a pilot group first, then the wider fleet), on
   a defined **patch cadence**, the schedule an organization commits to. Critical, actively
   exploited vulnerabilities justify emergency out-of-cycle patching within hours or days;
   routine, low-severity patches may follow a monthly cadence.
5. **Verify**, confirm the patch was actually applied fleet-wide; failed or partial rollouts are
   common and leave silent gaps.

This process mirrors the triage engine you will build in `problem/`: given a vulnerability's
CVSS severity, whether it is actively exploited in the wild, and whether the affected system is
internet-facing, decide how urgently it must be patched.

## Key terms
- **Patch**, a vendor-released software update that fixes a bug, often including a security fix.
- **CVE (Common Vulnerabilities and Exposures)**, a public, unique identifier assigned to a
  disclosed vulnerability.
- **CVSS (Common Vulnerability Scoring System)**, a 0-10 standardized severity score for a
  vulnerability, based on exploitability and impact.
- **Zero-day**, a vulnerability being exploited before any patch exists.
- **N-day**, a vulnerability for which a patch exists but has not yet been applied to the target.
- **Patch gap**, the time between a patch's release and an organization actually deploying it.
- **Patch management**, the formal process of inventorying, prioritizing, testing, deploying, and
  verifying patches across an organization's assets.
- **End-of-life (EOL) software**, software no longer receiving vendor patches, requiring
  compensating controls instead.

## Common misconceptions
- "Zero-days are the main way organizations get breached." → Most real-world breaches exploit
  n-day vulnerabilities, known flaws with an available patch that simply was not applied in time.
  Zero-days are rare and expensive for attackers by comparison.
- "You should always apply every patch the instant it's released." → Untested patches carry real
  compatibility and downtime risk. Mature patch management tests and prioritizes by severity and
  exploitation status rather than patching reflexively, while still moving fast on critical,
  actively-exploited flaws.
- "If a system still works fine, it doesn't need patching." → A system can function perfectly
  while still containing a serious, publicly known, unpatched vulnerability. Functionality and
  security posture are independent.

## Try it
- **Simulation:** Triage a queue of pending vulnerability patches
  by severity, exploitation status, and exposure, deciding which to deploy immediately versus
  schedule, to reach the target score.
- **Coding problem:** Implement a patch-prioritization engine that assigns an
  urgency label to each vulnerability using CVSS score, in-the-wild exploitation status, and
  whether the affected asset is internet-facing.
- **Quiz:** self-check on the skill's key ideas.

## Sources (local / vendor / rebuilt)
- Deep: NIST SP 800-40 (Guide to Enterprise Patch Management Planning), rebuilt as original
  prose above.
- Reference: CISA Known Exploited Vulnerabilities (KEV) catalog concept, rebuilt locally.
- Practice: SANS Cyber Aces patch-management exercises, rebuilt as the simulation challenge.
- Repo: LetsDefend/Free-Cybersecurity-Resources → `vendor/repos/letsdefend-free-cybersecurity`.
