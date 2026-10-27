# 1.2.a, Password-attack signs (failed attempts, unusual times, unknown devices)

> **Unit 1 · 1.2 Suspicious Wi-Fi Login**
> **AP Learning Objective(s):** 1.2.A
> **Course skill(s):** Detect Attacks

## Learning objective (student-facing)
Read an authentication log, identify the three key signals of a
password attack (repeated failed attempts, logins at anomalous times, and access from unknown
devices), and write a rule that flags brute-force attempts automatically.

## Lesson
When an attacker wants access to an account they do not own, the simplest path is to guess the
password. Modern attackers do not guess slowly and manually, they use automated tools that can
submit hundreds or thousands of login attempts per minute. The digital fingerprints those attempts
leave in authentication logs are predictable, and recognizing them is one of the most fundamental
skills in defensive security.

**What brute-force looks like in a log.** Every login generates an event. In a typical system,
that event records: the timestamp, the username, whether the login succeeded, and where the
request came from (IP address or device name). A normal user generates a handful of these events
per day, one success in the morning, one when they unlock their screen after lunch. An automated
attack generates dozens or hundreds of failures in rapid succession, all for the same username, all
within a very short time window. The pattern is unmistakable: a burst of `FAILED` events followed
by either a stop (the attacker gave up, moved on, or was locked out) or a single `SUCCESS` (the
attack succeeded and the account is compromised).

**Signal 1: Repeated failed attempts.** Security operations professionals use the term
"authentication failure spike" to describe this pattern. A single failed login is noise, every
user misses their password occasionally. Five failures for the same account within sixty seconds
is a threshold that most real-world intrusion-detection systems use to raise an alert. The exact
number varies by policy, but five-in-sixty is a widely cited baseline for catching automated
credential stuffing and dictionary attacks without drowning in false positives from fat-fingered
typing. This is the signal your coding problem for this skill asks you to implement.

**Signal 2: Unusual times.** People are creatures of habit. A user whose account normally shows
activity between 08:00 and 18:00 on weekdays, but suddenly shows a successful login at 02:47 on
a Saturday, is almost certainly compromised, or on a very unusual trip. Attackers often operate
in a different time zone, or deliberately run attacks at night when security teams are understaffed
and response is slower. Many SIEM (Security Information and Event Management) systems build a
behavioral baseline for each account and alert on deviations. Even without a SIEM, a defender can
spot the pattern by scanning the timestamp column for after-hours or weekend access. On a home
Wi-Fi router, unusual login times are among the easiest anomalies to see in the admin log.

**Signal 3: Unknown devices.** Most routers, corporate access points, and cloud platforms track
which devices have authenticated historically, by MAC address, device name, or IP-to-hostname
mapping. A new device that has never appeared before, especially combined with a successful login
after many failures, is a strong indicator that the account was compromised. Modern routers
display connected devices in their admin panel; checking that list regularly is a basic defensive
hygiene step. Unknown device detection also catches a different scenario: an attacker who obtained
the password by other means (phishing, data breach) and is now logging in for the first time from
their own machine.

**Why all three signals matter together.** Each signal alone generates false positives. A new
device might be a new phone. An odd login time might be someone working late. A few failures might
be a user with a new keyboard layout. But when signals stack, five failures at 3 a.m. from a
device never seen before, followed by a success, the combined probability of a legitimate
explanation collapses. Security rules are more reliable when they combine multiple indicators, a
principle called **correlation**.

**The attacker's perspective: dictionary and credential-stuffing attacks.** The attacker on the
other side of these logs is not random. Dictionary attacks try passwords from a curated wordlist, common words, known leaked passwords, keyboard patterns. Credential stuffing takes username-and-
password pairs from one leaked breach and tries them across many services, exploiting the fact
that people reuse passwords. Both generate the same log signature: many failures, same account,
short window. Understanding what the attacker is doing helps you tune the detection correctly, the threshold should be low enough to catch fast automated tools but high enough to avoid alerting
on a user who typed their password wrong twice.

**What happens after detection.** Recognizing the pattern is only the first step. A complete
response includes: locking the account after threshold breaches (automatic lockout), alerting the
account owner through a side channel (email or SMS, not the compromised system), requiring a
password reset from a verified device, and reviewing the logs to determine whether any successful
login occurred before the lockout. If a success appears before the threshold was reached, the
account may already be compromised and a fuller incident response is warranted.

**In the context of the "Suspicious Wi-Fi Login" scenario.** Imagine your home router logs show
that someone attempted to log in to the admin panel forty times between 02:15 and 02:17 last
night, using common passwords like `admin`, `123456`, and `password1`. The attacker tried from an
IP you do not recognize. This is a textbook brute-force attempt. The simulation for this skill lets
you step through a live-looking login monitor and flag the suspicious account before the attacker
succeeds.

## Key terms
- **Brute-force attack**, automated, exhaustive attempt to guess a credential by trying many
  possible values.
- **Dictionary attack**, brute-force variant that tries passwords from a wordlist rather than
  every possible character combination.
- **Credential stuffing**, using username/password pairs from a known breach to attack other
  services, exploiting password reuse.
- **Authentication failure spike**, a rapid burst of failed login events for the same account, a
  primary indicator of automated attack.
- **Behavioral baseline**, the normal pattern of activity for an account; deviations from it
  trigger anomaly-based alerts.
- **Correlation**, combining multiple signals to reduce false positives in security detection.

## Common misconceptions
- "A few failed logins are not a big deal." → A few in an hour is noise. Five in sixty seconds is
  a strong indicator of automation; the rate, not the raw count, is what matters.
- "The attacker needs to know my username to try passwords." → Credential stuffing uses lists of
  real usernames from breaches. On Wi-Fi routers the admin username (`admin`) is often public
  knowledge from the manufacturer's manual.
- "A locked account means I am safe." → Lockout stops the brute-force, but if a success event
  appears in the log before the lockout triggered, the account may already be compromised.

## Try it
- **Simulation:** Watch the live login monitor and flag the
  account under brute-force attack before the attacker succeeds; reach 4 correct detections.
- **Coding problem:** Implement `solve(events)` that returns a sorted list of
  usernames with five or more failed logins within any 60-second window.
- **Quiz:** self-check on the skill's key ideas.

## Sources (local / vendor / rebuilt)
- Deep: SANS Cyber Aces (authentication and access control), prose rebuilt as original lesson
  above from foundational principles; see `vendor/repos/LetsDefend-Free-Cybersecurity-Resources`.
- Reference: NIST SP 800-63B (Digital Identity Guidelines), baseline thresholds and lockout
  policy rationale.
- Practice: Cybrary authentication-log analysis exercises, rebuilt locally as the simulation.
- Repo: LetsDefend/Free-Cybersecurity-Resources → `vendor/repos/LetsDefend-Free-Cybersecurity-Resources`.
