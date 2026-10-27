# 5.1.d, Data breaches and their impact

> **Unit 5 · 5.1 Application and Data Vulnerabilities and Attacks**
> **AP Learning Objective(s):** 5.1.C
> **Course skill(s):** Analyze Risk

## Learning objective (student-facing)
Explain what a data breach is, identify the categories of data
whose exposure causes the most harm, and estimate the severity of a breach from the type of data
exposed, the number of records affected, and how quickly it was detected/contained.

## Lesson
A **data breach** is any incident in which sensitive, protected, or confidential data is accessed,
disclosed, or exfiltrated by someone who is not authorized to have it. A breach can be caused by
almost any of the vulnerabilities covered elsewhere in this unit, SQL injection dumping a
database, an XSS payload stealing session cookies, a BOLA flaw letting one account read another's
records, or by non-technical causes: a lost laptop, a misconfigured cloud storage bucket left
publicly readable, an insider copying files before quitting, or a successful phishing attack that
hands over valid credentials. The *cause* of a breach varies widely; what makes it a "breach"
specifically is that data crossed a trust boundary it should not have crossed.

Not all breaches are equally serious, and the AP framework expects you to reason about *impact*,
not just occurrence. Three factors drive how severe a breach is:

**Sensitivity of the data exposed.** Data sits on a spectrum. At the low end: a leaked list of
public blog post titles causes little harm. In the middle: email addresses and usernames enable
targeted phishing but are not immediately catastrophic alone. At the high end: **PII**
(personally identifiable information, full name + SSN, date of birth, home address),
**financial data** (credit card numbers, bank account numbers), **health records (PHI)**, and
**authentication secrets** (plaintext passwords, private keys, session tokens) cause the most
damage because they enable identity theft, financial fraud, account takeover, or, for health
data, discrimination and violate significant regulatory protections (e.g., HIPAA). A breach
exposing hashed-and-salted passwords is meaningfully less severe than one exposing the same
passwords in plaintext, because hashing adds a layer of work an attacker must still defeat.

**Scale.** A breach of 50 records from a small internal tool is a very different event from a
breach of 50 million customer records from a national retailer, scale multiplies both direct harm
(more victims of fraud/identity theft) and organizational consequences (regulatory fines, class
action lawsuits, mandatory breach-notification costs, reputational damage that drives customers
away).

**Time to detect and contain.** The longer sensitive data is exposed or exfiltration continues
undetected, the more of it an attacker can extract and the more time they have to monetize or
weaponize it (sell it, use it for further attacks, blackmail the victim organization). Industry
breach reports consistently show that breaches discovered and contained within days cost
organizations far less, on average, than breaches that take months to discover, this is why
detection controls (covered in Unit 4) are treated as part of the *breach response* story, not a
separate topic.

Once a breach is confirmed, organizations generally follow an incident-response arc: **contain**
(stop further data loss, revoke credentials, patch the hole, isolate affected systems),
**assess** (what data, how many records, which individuals), **notify** (many jurisdictions and
industries legally require notifying affected individuals and regulators within a set window, e.g., GDPR's 72-hour rule), and **remediate** (fix the root cause, rotate secrets, offer affected
users protections such as credit monitoring). Even a well-handled breach still carries lasting
cost: rebuilding user trust and the risk that leaked credentials get reused elsewhere (since many
people reuse passwords across sites) can cause a second wave of unrelated account compromises long
after the original incident.

The coding problem in this skill asks you to formalize this severity reasoning: given a synthetic
breach record (data categories exposed, record count, days-to-detect), compute a severity score
and label, the way a security team's intake triage tool might. The simulation puts you in the
analyst's seat, walking through a queue of incoming breach reports and scoring each one before
checking your score against the tool's rubric.

## Key terms
- **Data breach**, unauthorized access, disclosure, or exfiltration of sensitive/protected data.
- **PII (personally identifiable information)**, data that can identify a specific individual
  (name, SSN, address, date of birth).
- **PHI (protected health information)**, health-related records protected by regulation (e.g.,
  HIPAA in the U.S.).
- **Breach notification**, the legal/regulatory requirement to inform affected individuals and
  authorities within a defined window after a confirmed breach.
- **Time to detect / contain**, the elapsed time between a breach starting and it being
  discovered/stopped; a major driver of total breach impact.

## Common misconceptions
- "A breach only matters if passwords were stolen." → Exposure of PII, financial, or health data
  alone (without passwords) can enable identity theft and fraud and often carries stronger legal
  notification obligations.
- "Small breaches don't need a formal response." → Even a small breach of highly sensitive data
  (e.g., 40 patients' health records) can be more severe than a large breach of low-sensitivity
  data (e.g., 4 million newsletter emails); severity depends on data type and scale together.

## Try it
- **Simulation:** Triage a queue of synthetic breach reports and
  correctly score their severity against the rubric.
- **Coding problem:** Build a function that scores a breach record's severity from
  its exposed data categories, record count, and detection time.
- **Quiz:** self-check on the skill's key ideas.

## Sources (local / vendor / rebuilt)
- Deep: OWASP (data-exposure guidance), rebuilt as original prose above.
- Reference: GeeksforGeeks (data breach overview).
- Practice: PortSwigger Web Security Academy (sensitive-data-exposure labs) → rebuilt locally as the simulation.
- Repo: OWASP/wstg (Web Security Testing Guide) → `vendor/repos/OWASP-wstg`.
