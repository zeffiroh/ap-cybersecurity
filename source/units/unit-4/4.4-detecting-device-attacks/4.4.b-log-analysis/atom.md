# 4.4.b, Log analysis

> **Unit 4 · 4.4 Detecting Attacks on Devices**
> **AP Learning Objective(s):** 4.4.B
> **Course skill(s):** Detect Attacks

## Learning objective (student-facing)
Explain what a security log records and why it matters, identify
the common log sources security analysts review, and detect a brute-force login pattern by
correlating multiple log entries over time.

## Lesson
Every meaningful action a device or application takes can be recorded as a **log entry**, a
timestamped record of an event. A failed login, a file being opened, a firewall blocking a
connection, a new process starting: each of these can generate a line in a log file. Individually,
a single log line rarely proves an attack happened. The skill of **log analysis** is reading many
log entries together, over time, to recognize patterns that a single entry cannot reveal on its
own. This is the foundation of Learning Objective 4.4.B: detecting attacks by analyzing logs.

### Why logs matter
Logs are the closest thing security has to a security camera recording every room in a building
at once. An EDR agent (4.4.a) watches live behavior on a single endpoint; logs extend that
visibility across time and across every system that generates them, operating systems, web
servers, firewalls, authentication systems, applications. When an incident happens, logs are
often the *only* record of what occurred, especially if the attacker has already left the system
by the time an analyst investigates. This makes logs essential not just for real-time detection
but for **forensics**, reconstructing exactly what an attacker did after the fact.

### Common log sources
Security analysts pull from several categories of logs, each capturing a different layer of
activity:

- **Authentication logs**, every login attempt, success or failure, including the account name,
  source IP address, and timestamp. This is often the first place analysts look, because
  credential-based attacks (password guessing, credential stuffing) leave a direct trail here.
- **Firewall / network logs**, which connections were allowed or blocked, source and destination
  IP addresses and ports, and how much data was transferred.
- **Web server logs**, every HTTP request to a web application, including the URL requested, the
  response code, and the client IP. Attackers probing for vulnerable pages leave a distinctive
  pattern of requests here.
- **Application and system logs**, errors, configuration changes, service starts/stops, and
  other operating-system-level events.

### Reading a single log entry
A typical authentication log line might look like:
```
2024-03-14T09:12:03Z user=jsmith ip=203.0.113.44 result=FAILED
```
On its own, this line just says one login attempt failed, completely ordinary; anyone can
mistype a password. The line becomes meaningful only in the context of *other* lines around it.

### Correlation: the core skill of log analysis
**Correlation** means linking multiple log entries together, by the same user, the same source
IP, or the same time window, to reveal a pattern invisible in any single entry. Consider a
sequence of five failed login attempts for the same username within a ten-second window, all from
the same IP address. No single line in that sequence looks alarming, but the *pattern*, many
failures, tightly clustered in time, targeting one account, is a textbook signature of a
**brute-force attack**: an attacker (or automated script) rapidly guessing passwords.

Analysts formalize this pattern into a **detection rule**: for example, "flag any user account
with 5 or more failed login attempts within any 60-second window." A rule like this can be run
automatically across a continuous stream of logs, which is exactly what a **SIEM (Security
Information and Event Management)** platform does at enterprise scale, ingesting logs from
every system in an organization, applying correlation rules, and raising alerts when a rule
fires.

### False positives and threshold tuning
Just like antivirus and EDR, log-based detection rules must balance catching real attacks against
generating too much noise. A threshold set too low (e.g., flagging after just 2 failed logins)
will generate constant false alarms from users who simply mistyped a password, analysts will
learn to ignore the alerts, a dangerous outcome called **alert fatigue**. A threshold set too high
(e.g., 50 failures) might let a real, slower brute-force attempt slip through undetected. Choosing
the right threshold and time window is a genuine security engineering tradeoff, not an arbitrary
number.

### A concrete scenario
Imagine Meridian High School's authentication log shows the account `jsmith` receiving six failed
login attempts between 09:12:01 and 09:12:47, all from IP `203.0.113.44`, followed immediately by
a successful login at 09:12:51 from the *same* IP. Read individually, the successful login at the
end looks like nothing unusual, someone finally typed their password correctly. Read as a
correlated sequence, it reads very differently: an automated brute-force tool guessed the
password after five failed attempts and got in on the sixth try. The coding problem in `problem/`
asks you to implement exactly this correlation logic, scanning a stream of login events and
flagging every account that shows this brute-force pattern.

### Log analysis in the detection landscape
Log analysis complements EDR (4.4.a): EDR sees live behavior on one device, while logs let an
analyst reconstruct patterns across accounts, systems, and time, including attacks that never
touch an endpoint at all, like a brute-force attempt against a web login page. Together with the
indicators of compromise you will study in 4.4.c, log analysis and EDR form the two core
detection disciplines of Unit 4.

## Key terms
- **Log entry**, a single timestamped record of an event (e.g., a login attempt, a blocked
  connection).
- **Authentication log**, a log recording every login attempt, its result, source, and account.
- **Correlation**, linking multiple log entries together (by user, IP, or time) to reveal a
  pattern that no single entry shows alone.
- **Brute-force attack**, repeated, rapid login attempts (often automated) trying to guess a
  valid password.
- **Detection rule**, a formal, repeatable condition (e.g., "5+ failures in 60 seconds") used to
  flag a pattern automatically.
- **SIEM (Security Information and Event Management)**, a platform that ingests logs from many
  systems and applies correlation rules at scale to raise alerts.
- **Alert fatigue**, the desensitization that occurs when detection thresholds are too sensitive
  and generate too many false alarms, causing analysts to start ignoring real alerts.

## Common misconceptions
- "A single failed login is proof of an attack." → One failed login is ordinary human error.
  Attacks are recognized through correlated patterns, multiple entries linked by user, IP, and
  tight time windows, not a single log line in isolation.
- "More sensitive detection rules are always better." → Overly sensitive thresholds generate
  false positives that cause alert fatigue, where analysts start ignoring alerts altogether, potentially missing a real attack buried in the noise.
- "Logs are only useful in real time." → Logs are equally critical after an incident, for
  forensic reconstruction of what an attacker did, especially once the attacker is no longer
  active on the system.

## Try it
- **Simulation:** Review a stream of authentication log entries
  and correctly identify which accounts show a brute-force login pattern to reach the target
  score.
- **Coding problem:** Implement a brute-force detector that correlates
  authentication log entries by user and time window, returning every account showing 5 or more
  failed logins within any 60-second window.
- **Quiz:** self-check on the skill's key ideas.

## Sources (local / vendor / rebuilt)
- Deep: NIST SP 800-92 (Guide to Computer Security Log Management), rebuilt as original prose.
- Reference: OWASP logging cheat sheet concepts, rebuilt locally.
- Practice: LetsDefend SOC log-analysis labs, rebuilt as the simulation challenge.
- Repo: LetsDefend/Free-Cybersecurity-Resources → `vendor/repos/letsdefend-free-cybersecurity`.
