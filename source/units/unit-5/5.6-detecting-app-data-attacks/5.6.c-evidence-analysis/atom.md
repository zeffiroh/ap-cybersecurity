# 5.6.c, Digital evidence analysis and attack classification

> **Unit 5 · 5.6 Detecting Attacks on Data and Applications**
> **AP Learning Objective(s):** 5.6.B, 5.6.C
> **Course skill(s):** Detect Attacks, Collaborate

## Learning objective (student-facing)
Explain the chain-of-custody principles that make digital
evidence trustworthy, describe the difference between an indicator of compromise (IOC) and a
conclusion about attack type, and classify a set of collected evidence into the attack category
it most strongly supports.

## Lesson
Detecting that *something* happened is only the first half of incident response. Once an alert
fires, a brute-force detector flags an IP, a DLP rule flags a transfer, a log shows an
unexplained error spike, a security analyst has to answer a harder question: **what actually
happened, and what is the evidence for it?** This skill covers **digital evidence analysis**: how
analysts collect, preserve, and reason from evidence to reach a defensible conclusion about attack
type, and how that conclusion is communicated and acted on as a team.

**Evidence, not assumption.** An alert is a hypothesis, not a verdict. A spike in failed logins
*suggests* brute-force, but the analyst must confirm it with evidence: are the failed attempts
coming from one source targeting many usernames (brute-force), or many sources targeting one
username (credential stuffing using a leaked password list)? Jumping to a conclusion without
checking the underlying evidence is the single most common analyst mistake, and it leads to wrong
remediation, blocking the wrong IP, resetting the wrong password, or missing that the real attack
vector was something else entirely.

**Indicators of compromise (IOCs).** An IOC is a single observable fact, a suspicious IP address,
a file hash matching known malware, a registry key, an unusual outbound connection, an email
attachment with a double extension (`invoice.pdf.exe`). No single IOC proves an attack type by
itself; a burst of 401 responses could be brute-force, but it could also be a broken automated
script retrying with a stale password. **Attack classification** is the process of collecting
multiple IOCs and reasoning about which attack category they collectively and most strongly
support, SQL meta-characters in a request body plus a database error in the response strongly
supports SQL injection; a suspicious attachment plus a user reporting a "too good to be true"
email plus a credential-harvesting URL strongly supports phishing.

**Chain of custody.** Evidence that will support a real incident response decision, or, in a
legal context, a prosecution, must be handled with a documented **chain of custody**: who
collected it, when, how it was stored, and who has touched it since. If an analyst copies a log
file to their personal laptop, edits it "to make it more readable," and can't say who else has
seen it, that evidence is compromised, not necessarily because it was tampered with, but because
no one can *prove* it wasn't. Proper practice is to work from read-only copies, hash the original
evidence (so any later change is detectable), and log every access. This matters even outside a
courtroom: an internal investigation's credibility depends on this discipline too.

**From evidence to classification.** A practiced analyst builds a small mental (or literal)
scoring table: which category does each piece of evidence support, and how strongly? A single
weak signal (one failed login) supports many categories weakly; a strong, specific signal (a
known malware file hash) supports one category almost conclusively. The coding problem in
`problem/` formalizes this: given a list of evidence indicators collected from an incident,
implement a classifier that scores each attack category by how many of its known indicators are
present and returns the best-supported classification, exactly the reasoning process a SOC
analyst performs, just made explicit and repeatable.

**Classification frameworks provide shared vocabulary.** Industry frameworks like MITRE ATT&CK
give analysts and teams a common vocabulary for attack techniques so that "brute-force" means the
same specific thing across every team and every report. Using a shared, consistent classification
scheme, rather than each analyst inventing their own labels, is what lets a security operations
center compile trends across incidents ("we've seen a 40% increase in phishing-classified
incidents this quarter") and lets an incident report be understood by anyone trained on the same
framework.

**Collaboration and reporting.** Attack classification is rarely a solo act. A junior analyst
collects and documents evidence; a senior analyst or team reviews the classification and
challenges weak reasoning before it becomes an official incident report; and the final
classification drives which playbook the response team follows. Communicating uncertainty
honestly, "the evidence most strongly supports phishing, but a malware component can't be ruled
out", is a mark of a mature analyst, not a weakness. The simulation in the simulation puts you in
that role directly: given a small evidence bundle, you classify the attack and see how your
reasoning compares to the documented answer.

## Key terms
- **Indicator of compromise (IOC)**, a single observable artifact (IP, file hash, unusual log
  entry) suggesting a security incident may be occurring; rarely conclusive on its own.
- **Attack classification**, reasoning from a collection of IOCs to the attack category they
  collectively best support.
- **Chain of custody**, a documented record of who collected, accessed, and stored evidence, so
  its integrity can be trusted (or challenged) later.
- **MITRE ATT&CK**, a widely-used framework providing a shared vocabulary for attack techniques,
  letting teams classify and compare incidents consistently.
- **Hash verification**, computing a cryptographic hash of evidence at collection time so any
  later modification is detectable.

## Common misconceptions
- "One suspicious indicator is enough to declare the attack type." → A single IOC is rarely
  conclusive; classification should weigh the full set of collected evidence.
- "Chain of custody only matters for evidence going to court." → Internal incident reports and
  post-mortems also depend on evidence integrity for their conclusions to be trusted.
- "Classification frameworks are just paperwork." → A shared vocabulary (like MITRE ATT&CK) is
  what lets different analysts and teams compare and aggregate incidents meaningfully.

## Try it
- **Simulation:** Review an evidence bundle for each case and
  classify the attack type correctly, reaching the target score.
- **Coding problem:** Implement a classifier that scores collected evidence
  indicators against known attack categories and returns the best-supported classification.
- **Quiz:** self-check on the skill's key ideas.

## Sources (local / vendor / rebuilt)
- Deep: OWASP (Incident Response, Testing Guide), rebuilt as original prose above; reference at
  `vendor/repos/OWASP-wstg`.
- Reference: NIST SP 800-61 Computer Security Incident Handling Guide, reconstructed from public
  standard.
- Practice: PortSwigger Web Security Academy (attack pattern recognition), offline exercises
  rebuilt in the simulation.
- Repo: LetsDefend/Free-Cybersecurity-Resources → `vendor/repos/LetsDefend-Free-Cybersecurity-Resources`.
