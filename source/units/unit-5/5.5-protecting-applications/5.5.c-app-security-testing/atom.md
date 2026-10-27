# 5.5.c, Application security testing (SAST/DAST)

> **Unit 5 · 5.5 Protecting Applications**
> **AP Learning Objective(s):** 5.5.B, 5.5.C
> **Course skill(s):** Detect Attacks, Mitigate Risk

## Learning objective (student-facing)
Explain how static application security testing (SAST) and
dynamic application security testing (DAST) find different classes of vulnerabilities, describe
the tradeoffs of each, and classify a given finding as something SAST would catch, something DAST
would catch, or neither.

## Lesson
Writing secure code is not the same as knowing your code is secure. Every application security
program eventually asks the same question: how do we find the vulnerabilities before an attacker
does? Two complementary families of automated testing answer that question from opposite
directions, **SAST** (static application security testing) and **DAST** (dynamic application
security testing).

**SAST reads the source code without running it.** A static analysis tool parses the codebase, source files, sometimes compiled bytecode, and searches for patterns known to be dangerous: a SQL
query built by string concatenation instead of parameterization, a call to `eval()` on
user-controllable input, a hardcoded password or API key sitting in a config file, a missing
input-validation check before a sensitive operation. Because SAST never executes the program, it
can be run the moment code is written, often directly inside the developer's editor or as a gate
in the CI/CD pipeline before the code ever merges. This means vulnerabilities are caught at the
cheapest possible point to fix them: before deployment, sometimes before the pull request is even
opened. SAST can also see *every* code path, including rarely-exercised error handlers and admin
features that a live test might never stumble into. The tradeoff is a **high false-positive rate**:
a static tool cannot always tell whether a flagged string concatenation actually reaches a database
call with attacker-controlled input, so it tends to over-flag, and developers must triage the
noise. SAST also cannot find vulnerabilities that only exist because of how the deployed system is
configured, misconfigured servers, weak TLS settings, or authentication bypasses that only appear
when the application is actually running.

**DAST tests the application from the outside while it runs.** A dynamic scanner treats the
application as a black box: it sends real HTTP requests, fuzzes form fields and URL parameters,
manipulates cookies and headers, and observes the responses for signs of a vulnerability, a
reflected `<script>` tag echoed back unescaped (XSS), a login form that can be bypassed with a
crafted payload, an endpoint that leaks a stack trace or internal file path. Because DAST interacts
with the live system exactly the way an attacker would, it naturally catches runtime and
configuration issues that source code alone cannot reveal, and its findings tend to have a
**lower false-positive rate**, if the scanner successfully injected a payload and got a
suspicious response back, something real is usually happening. The tradeoff is that DAST needs a
running, reachable instance of the application (which means it typically happens later in the
development cycle, closer to release), and it can only find what it actually tests: code paths the
scanner's crawler never reaches, or input fields it never fuzzes, stay invisible.

**The two approaches complement each other rather than compete.** SAST is cheap, early, and
exhaustive over source code but blind to runtime behavior and prone to false alarms. DAST is
realistic and low-noise but late, incomplete in coverage, and blind to the code that produced what
it observes. A mature CI/CD pipeline runs SAST on every commit (fast feedback for developers) and
DAST against a staging deployment before release (a realistic pre-flight check), then correlates
the two: a finding confirmed by both tools is high-confidence; a SAST-only finding needs a human to
check reachability; a DAST-only finding needs a human to trace back to the responsible line of
code.

**Automated scanning is not the same as penetration testing.** SAST and DAST tools are automated,
repeatable, and cheap to run continuously, but they follow known patterns and cannot improvise.
A **penetration test** is performed by a skilled human (or team) who chains together multiple weak
findings, thinks creatively about business logic flaws automated tools cannot recognize (like "can
a regular user manipulate this parameter to view another user's invoice?"), and reports with
attacker-style narrative. Most mature programs use automated SAST/DAST for continuous, high-volume
coverage and reserve human penetration testing for periodic, deeper assurance, especially before
major releases or as a compliance requirement.

The simulation in the simulation gives you a queue of findings, a snippet of source code or a scan
result from a running application, and asks you to classify each as something SAST would catch,
something DAST would catch, or neither. The coding problem in `problem/` asks you to build a
miniature static-analysis scanner: given a list of source-code lines, flag the ones matching known
dangerous patterns, exactly like a real SAST tool's rule engine.

## Key terms
- **SAST (static application security testing)**, analyzing source code without executing it to
  find patterns such as unsafe SQL construction, hardcoded secrets, or dangerous function calls.
- **DAST (dynamic application security testing)**, testing a running application from the outside
  by sending real requests and observing responses for vulnerabilities like XSS or auth bypass.
- **False positive**, a tool flagging something as a vulnerability that is not actually
  exploitable; SAST tools tend to produce more of these than DAST tools.
- **CI/CD pipeline integration**, running SAST/DAST automatically on every commit or deployment so
  vulnerabilities are caught continuously rather than only at a scheduled audit.
- **Penetration testing**, human-driven security testing that chains findings and business-logic
  reasoning together in ways automated SAST/DAST scanners cannot.

## Common misconceptions
- "SAST and DAST find the same bugs, so you only need one." → They find different, mostly
  non-overlapping classes of issues, SAST sees the code but not runtime behavior; DAST sees
  runtime behavior but not the code. Mature pipelines run both.
- "A clean SAST/DAST scan means the application has no vulnerabilities." → Both tools only find
  what they are built to look for; business-logic flaws and novel attack chains typically require
  human penetration testing to uncover.
- "DAST can run as early as SAST in the pipeline." → DAST requires a running, reachable instance of
  the application, so it necessarily happens later than source-level SAST scanning.

## Try it
- **Simulation:** Correctly classify a queue of findings as
  SAST-catchable, DAST-catchable, or neither, reaching the target score.
- **Coding problem:** Implement a static-analysis scanner that flags dangerous
  patterns (unsafe SQL construction, `eval()` use, hardcoded secrets) in a list of source lines.
- **Quiz:** self-check on the skill's key ideas.

## Sources (local / vendor / rebuilt)
- Deep: OWASP (Static/Dynamic Analysis, Testing Guide), rebuilt as original prose above; reference
  at `vendor/repos/OWASP-wstg`.
- Reference: GeeksforGeeks (Software Testing, Static vs Dynamic Analysis), reconstructed summary.
- Practice: PortSwigger Web Security Academy (automated scanning concepts), rebuilt locally as
  the simulation.
- Repo: OWASP/wstg → `vendor/repos/OWASP-wstg`.
