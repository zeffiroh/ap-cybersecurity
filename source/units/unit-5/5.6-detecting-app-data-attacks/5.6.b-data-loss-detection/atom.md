# 5.6.b, Data loss detection (DLP)

> **Unit 5 · 5.6 Detecting Attacks on Data and Applications**
> **AP Learning Objective(s):** 5.6.B
> **Course skill(s):** Detect Attacks

## Learning objective (student-facing)
Explain what data loss prevention (DLP) systems detect and why,
describe the difference between content-based and volume/behavior-based detection, and evaluate
a stream of outbound data-transfer events to flag likely data exfiltration.

## Lesson
An organization can defend its perimeter, patch its applications, and monitor its logs, and still
lose its most valuable asset: the data itself, quietly walking out the door. **Data loss
prevention (DLP)** is the discipline and set of tools focused on exactly that risk, detecting
and, where possible, stopping sensitive data from leaving an organization's control without
authorization, whether the cause is a malicious insider, a compromised account being used to
exfiltrate stolen data, or an honest employee accidentally emailing a spreadsheet to the wrong
address.

**Two complementary detection strategies.** DLP systems generally combine two different ways of
recognizing a problem. **Content-based detection** inspects the actual data leaving the
organization, scanning outbound emails, file uploads, and network traffic for patterns that look
like sensitive information: a string of digits matching a credit-card number format, a Social
Security number pattern, a document labeled "CONFIDENTIAL" in its metadata, or a database dump
containing recognizable column names like `ssn` or `password_hash`. Content inspection is precise
when it fires, it caught something matching a known sensitive pattern, but it can only catch
patterns it is built to recognize, and it can be evaded by an attacker who compresses, encrypts,
or otherwise transforms the data before sending it. **Volume/behavior-based detection** does not
look at content at all; it looks at *anomalies in the shape of data movement*, a user account
that normally transfers a few megabytes a day suddenly uploading two gigabytes to an unfamiliar
external destination, a service account accessing far more records than its normal job requires,
or a burst of database export queries at 3 AM from an account that has never run one before.
Behavior-based detection catches exfiltration that content inspection misses (e.g., encrypted
data with no recognizable pattern) precisely because it does not need to understand *what* is
being taken, only that *how much, how, and when* it moved is abnormal.

**Where DLP watches.** A mature DLP program instruments multiple points: **network DLP** inspects
traffic leaving the network perimeter (egress monitoring); **endpoint DLP** runs on individual
laptops/workstations and can block a USB copy or a print job of a flagged document; and **cloud/
email DLP** integrates with SaaS platforms and mail servers to inspect uploads, shares, and
attachments before they leave the organization's managed environment. Different exfiltration
paths require different vantage points, a laptop copying a file to a USB drive never touches the
network, so only endpoint DLP would see it.

**A concrete example.** Consider an internal file server logging every large download. A
marketing employee downloading a 4 MB slide deck at 2 PM on a Tuesday is normal. The same account
downloading 200 files totaling 3 GB at 1 AM, and then uploading a similarly sized archive to an
unfamiliar personal cloud-storage domain twenty minutes later, is a strong behavioral signal, volume far outside the account's baseline, an unusual time, and a suspicious destination, all in
one narrow window. The coding problem in `problem/` formalizes exactly this judgment: given a
list of outbound transfer records, flag the ones that cross a **volume threshold to a
non-approved destination**, mirroring a real DLP egress rule.

**False positives and business context matter.** DLP is notoriously prone to noisy alerts:
legitimate large transfers happen constantly (a backup job, a data engineer's normal workload, a
sanctioned data-sharing agreement with a partner). Effective DLP programs maintain an **approved
destination list** (known-good partners, corporate cloud storage) so that a large transfer to an
approved destination does not fire an alert, while the identical transfer to an unrecognized
external domain does. Building and maintaining that allowlist, and tuning thresholds so
legitimate business activity does not drown out real alerts, is most of the ongoing work of
running a DLP program.

**DLP is detective and preventive, not just forensic.** Unlike a log that is reviewed after the
fact, a well-integrated DLP system can act in real time: blocking an email with a flagged
attachment before it sends, quarantining a file upload, or prompting a user to confirm they intend
to share a document externally. This makes DLP one of the few controls in this unit that can stop
the loss *during* the attempt, not just detect it afterward, though attackers who understand this
try to blend their exfiltration into normal-looking traffic specifically to avoid triggering it.

## Key terms
- **Data loss prevention (DLP)**, tools and processes that detect and block sensitive data from
  leaving an organization's control without authorization.
- **Content-based detection**, inspecting the actual data (patterns like credit-card numbers,
  SSNs, document classification labels) to recognize sensitive information leaving the network.
- **Volume/behavior-based detection**, flagging anomalies in how much data moves, when, and to
  where, without needing to understand the data's content.
- **Egress monitoring**, watching outbound network traffic at the perimeter for signs of data
  leaving the organization.
- **Approved destination list**, a maintained allowlist of known-good transfer destinations
  (partners, sanctioned cloud storage) that DLP rules use to suppress false positives.

## Common misconceptions
- "DLP only needs to scan for keywords like 'confidential'." → Content inspection is only half
  the picture; volume/behavior-based detection catches exfiltration that has no recognizable
  content pattern, such as encrypted or compressed data.
- "A large data transfer is always suspicious." → Legitimate large transfers (backups, sanctioned
  partner data sharing) happen constantly; effective DLP relies on an approved-destination list
  and account baselines, not raw size alone.
- "DLP is purely detective, like a log review." → Well-integrated DLP can act preventively in real
  time, blocking or quarantining a transfer before it completes, not just recording it afterward.

## Try it
- **Simulation:** Review a stream of outbound transfer events
  and correctly classify each as an exfiltration ALERT or normal activity, reaching the target
  score.
- **Coding problem:** Implement a DLP egress rule that flags outbound transfers
  exceeding a volume threshold to a non-approved destination.
- **Quiz:** self-check on the skill's key ideas.

## Sources (local / vendor / rebuilt)
- Deep: OWASP (Data Protection, Sensitive Data Exposure guidance), rebuilt as original prose
  above; reference at `vendor/repos/OWASP-wstg`.
- Reference: NIST SP 800-53 (Media Protection / Data Loss Prevention control families), reconstructed from public standard.
- Practice: PortSwigger Web Security Academy (information disclosure concepts), offline
  exercises rebuilt in the simulation.
- Repo: LetsDefend/Free-Cybersecurity-Resources → `vendor/repos/LetsDefend-Free-Cybersecurity-Resources`.
