# 5.6.a, Application monitoring and logging

> **Unit 5 · 5.6 Detecting Attacks on Data and Applications**
> **AP Learning Objective(s):** 5.6.A
> **Course skill(s):** Detect Attacks

## Learning objective (student-facing)
Explain what application logging captures, describe how security teams use log analysis to detect attacks in progress, and identify the key log fields and patterns that signal brute-force, injection, and account-takeover activity.

## Lesson
Applications are not silent. Every time a user logs in, a form is submitted, a file is opened, or an error is thrown, the application can record a structured line in its log, a timestamped, machine-readable trace of what just happened. Application monitoring is the practice of collecting and watching those traces in real time; logging is the act of writing them down so they can be examined later. Together they form the foundation of operational security: you cannot detect an attack you have never recorded.

**Why logs matter for security.** Consider what an attacker must do to compromise a web application. They probe for valid usernames, hammer a login form with password guesses, exploit a vulnerability to inject malicious input, or escalate privileges by calling an endpoint they should not reach. Every one of those actions touches the application, and every touch can leave a mark in the log. A defender who reads the log after the fact can reconstruct the attack step by step. A defender who reads the log in real time can interrupt it before it succeeds.

**What a log entry contains.** A well-designed log line has a handful of standard fields: a timestamp (when), the requesting IP address (where from), the authenticated user identity (who), the resource or endpoint accessed (what), the result code (did it succeed?), and optionally the payload size or a short message. A minimal example:

```
2024-03-15T08:42:01Z  192.168.10.44  jsmith  POST /login  401  "Invalid credentials"
2024-03-15T08:42:03Z  192.168.10.44  jsmith  POST /login  401  "Invalid credentials"
2024-03-15T08:42:05Z  192.168.10.44  jsmith  POST /login  200  "Login successful"
```

Three events, five seconds apart, same IP, same user: two failures followed by a success. Seen once, this is unremarkable, people mistype passwords. Seen fifty times, from a single IP, across twenty usernames within two minutes, it is a brute-force attack. The pattern, not the individual event, is the signal.

**Common attack patterns visible in logs.** Defenders learn to recognize a handful of recurring signatures:

*Brute-force / credential stuffing.* A high volume of HTTP 401 or 403 responses to a login endpoint from one IP address, targeting many usernames in a short time window. The simulation in the simulation lets you practice identifying this pattern in a live log stream.

*SQL injection probes.* Requests whose URL parameters or body fields contain SQL meta-characters (`'`, `--`, `UNION SELECT`, `OR 1=1`) appear as suspicious query strings in the access log. An application that logs the raw request captures the payload. Modern web application firewalls automatically flag these, but the raw log remains the primary forensic record.

*Privilege escalation / access-control violations.* A regular user's account suddenly making requests to `/admin/`, `/api/users/all`, or configuration endpoints produces 403 responses in the log. A series of 403s from an authenticated low-privilege account is a strong signal of an attacker probing the authorization boundary.

*Error storms.* A sudden spike in 500-series (server error) responses, especially concentrated on a single endpoint, can indicate exploitation of a code vulnerability, for example, a buffer overflow or path traversal that forces the server into an error state.

**Log levels and what to watch.** Applications use severity levels, DEBUG, INFO, WARNING, ERROR, CRITICAL, to categorize events. Security-relevant events should be logged at INFO or higher so they are not silently discarded in production (where DEBUG is typically disabled). A misconfiguration that drops INFO-level authentication events creates a blind spot an attacker can exploit by designing their probe to remain "quiet."

**Aggregation and alerting.** Raw logs are high-volume; a busy web server may produce thousands of lines per second. Security teams feed logs into a SIEM (Security Information and Event Management) system, a centralized platform that collects logs from many sources, applies detection rules, and raises alerts. A SIEM rule might say: "if the same IP produces five or more 401 events within 60 seconds, create a high-priority alert." The coding problem in `problem/` asks you to implement exactly this kind of rule as a Python function: given a list of parsed log entries, return the IP addresses that exceed the brute-force threshold.

**What logging does not catch.** Logs record what the application observes. They do not automatically capture traffic that bypasses the application (e.g., direct database access by a compromised insider), events that happen in components that are not configured to log (e.g., an unmonitored microservice), or attacks that mimic normal user behavior well enough to stay under any threshold. Logging is one layer of a defense-in-depth strategy, essential, but not sufficient on its own.

**Protecting the logs themselves.** Logs are forensic evidence. An attacker who achieves code execution on the server will often attempt to erase or tamper with logs to cover their tracks. Best practices include writing logs to a separate, append-only datastore, streaming them to a remote log aggregator in real time, and controlling write permissions so the application process cannot delete its own audit trail.

The simulation in the simulation presents a stream of synthetic log entries and asks you to classify each event and identify which ones cross the brute-force alert threshold. The coding problem formalizes that judgment as a function you implement and test automatically.

## Key terms
- **Application log**, a time-ordered record of events inside an application, including authentication attempts, errors, and resource accesses.
- **Brute-force detection**, identifying repeated, failed authentication attempts from a single source that suggest automated password guessing.
- **SIEM**, Security Information and Event Management; a platform that centralizes logs and applies detection rules to generate security alerts.
- **Log aggregation**, collecting logs from multiple sources into one place for unified analysis and long-term storage.
- **HTTP status code**, a three-digit code in web server logs indicating request outcome (e.g., 200 = OK, 401 = unauthorized, 403 = forbidden, 500 = server error).

## Common misconceptions
- "If no alarm fired, nothing bad happened." → Alarms only fire on configured rules; a misconfigured or absent rule creates a silent blind spot. Periodic manual log review is still necessary.
- "Logging is a performance problem, so we keep it minimal." → The security cost of a blind spot far exceeds the overhead of structured logging. Modern log pipelines handle high throughput efficiently.
- "Deleting the logs covers an attacker's tracks completely." → If logs stream to a remote aggregator in real time, deletion of local copies does not erase the forensic record.

## Try it
- **Simulation:** Review a synthetic log stream, identify the brute-force event window, and reach the target score by correctly classifying five log bursts.
- **Coding problem:** Parse a list of log entries and return every IP address whose failed-login count exceeds the brute-force threshold within a 60-second window.
- **Quiz:** self-check on the skill's key ideas.

## Sources (local / vendor / rebuilt)
- Deep: OWASP (Testing for Account Lockout, Web Security Testing Guide), rebuilt as original prose above; reference at `vendor/repos/OWASP-wstg`.
- Reference: NIST SP 800-92 Guide to Computer Security Log Management, reconstructed from public standard.
- Practice: PortSwigger Web Security Academy (authentication vulnerabilities), offline exercises rebuilt in the simulation.
- Repo: LetsDefend/Free-Cybersecurity-Resources, `vendor/repos/LetsDefend-Free-Cybersecurity-Resources`.
