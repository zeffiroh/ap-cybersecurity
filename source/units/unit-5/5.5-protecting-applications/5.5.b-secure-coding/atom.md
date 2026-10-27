# 5.5.b, Secure coding practices

> **Unit 5 · 5.5 Protecting Applications**
> **AP Learning Objective(s):** 5.5.A, 5.5.B
> **Course skill(s):** Mitigate Risk

## Learning objective (student-facing)
List the core secure-coding practices that prevent common
vulnerability classes, explain why each practice works, and audit a piece of application
configuration or code against those practices to identify violations.

## Lesson
Input validation (5.5.a) stops one specific failure, trusting untrusted data, but it is only
one piece of a much larger discipline called **secure coding**: the set of habits and defaults a
development team builds into *every* line of code so that vulnerabilities are prevented by
construction rather than caught after the fact. Secure coding is not a single technique; it is a
checklist of practices that, applied consistently, close off entire categories of attack before
an attacker ever gets a chance to try them.

**Least privilege in code, not just accounts.** The principle of least privilege, giving a user
or process only the access it needs, and no more, applies just as much to running application
code as it does to human accounts. An application's database connection should use a database
account that can only read and write the specific tables it needs, never one with administrative
rights over the whole database. A web server process should never run as `root`/Administrator; if
an attacker exploits a bug in a process running with excessive privilege, that bug becomes a
full system compromise instead of a contained failure. Secure coding means deliberately choosing
the *minimum* privilege a piece of code needs to do its job, every time.

**Parameterized queries, not string-built SQL.** The single highest-leverage secure-coding habit
against SQL injection is never building a query by concatenating strings with user input.
Compare `"SELECT * FROM users WHERE name = '" + name + "'"` (dangerous, the attacker's input
becomes part of the query's syntax) to a parameterized query `SELECT * FROM users WHERE name = ?`
with `name` passed separately as a bound parameter (safe, the database driver treats the
parameter strictly as data, never as SQL syntax, no matter what characters it contains). This one
habit, applied everywhere a query touches user input, eliminates SQL injection as a risk
regardless of what validation is or is not done upstream, which is why it is considered
defense-in-depth alongside input validation, not a replacement for it.

**Secrets do not belong in source code.** A hardcoded password, API key, or encryption key sitting
in a source file is a secret that lives forever in version control history, is visible to
anyone with repository read access, and is trivially found by both automated scanners (attacker's
and defender's) and human code review. Secure coding practice keeps secrets out of code entirely,
loading them at runtime from environment variables, a dedicated secrets manager, or an encrypted
configuration store, so rotating a compromised secret does not require a code change and
deployment, and the secret never appears in a commit history an attacker might later find.

**Fail securely, and do not leak information in errors.** When something goes wrong, an
application has a choice: fail open (allow the action anyway) or fail closed/securely (deny by
default). Secure code always fails closed, an authentication check that throws an unexpected
exception must not accidentally grant access. Equally important is *what* the failure reveals: a
verbose error page that shows a full stack trace, internal file paths, or a database error
message hands an attacker a roadmap of the application's internals. Production code should log
detailed errors internally for developers while showing the end user (and any external attacker)
only a generic message.

**Dependency management.** Modern applications are built on dozens or hundreds of third-party
libraries, and a vulnerability in any one of them becomes a vulnerability in the whole
application, this is exactly how many major breaches have happened. Secure coding practice
means pinning dependency versions (so a build is reproducible and doesn't silently pull in a
compromised update), tracking known vulnerabilities in the dependencies actually in use, and
patching promptly when a fix is published. An application with excellent code but a five-year-old
unpatched library is not secure.

**Code review as a control, not a courtesy.** No individual developer catches every mistake.
Requiring a second engineer to review code before it merges, specifically looking for the
patterns above (string-built queries, hardcoded secrets, missing privilege checks, verbose error
handling), catches classes of bugs that automated tools miss and spreads secure-coding knowledge
across the team. Mature organizations pair human code review with the automated SAST scanning
covered in the next atom.

The coding problem in `problem/` asks you to build an automated secure-coding auditor: given a
small application configuration, flag every practice it violates, exactly like a lightweight
policy-as-code linter would. The simulation lets you play code reviewer directly, examining short
code/config snippets and deciding PASS or FLAG against the same rule set.

## Key terms
- **Least privilege (in code)**, running application processes and database connections with
  only the minimum access they need to function.
- **Parameterized query**, a database query where user-supplied values are passed as separate,
  typed parameters rather than concatenated into the query string, preventing SQL injection.
- **Secrets management**, storing credentials, API keys, and encryption keys outside source code
  (environment variables, a secrets manager) so they can be rotated without a code change.
- **Fail securely**, designing error/exception paths to deny access by default rather than
  accidentally granting it when something unexpected happens.
- **Dependency management**, pinning, tracking, and patching third-party library versions so a
  known vulnerability in a dependency does not become an unpatched vulnerability in the app.

## Common misconceptions
- "Secure coding is just input validation done well." → Input validation is one practice among
  several; parameterized queries, secrets management, least privilege, and dependency management
  each close a different, independent class of vulnerability.
- "A verbose error message is only a usability issue." → Detailed stack traces and internal paths
  shown to an attacker are reconnaissance information that materially helps them plan an attack.
- "As long as the code works and passes QA, it's secure enough." → Functional correctness and
  security are different properties; code can pass every functional test while still building
  queries insecurely or running with excessive privilege.

## Try it
- **Simulation:** Review a queue of code/config snippets and
  correctly PASS or FLAG each against the secure-coding rule set, reaching the target score.
- **Coding problem:** Implement an automated auditor that flags which secure-coding
  practices a given application configuration violates.
- **Quiz:** self-check on the skill's key ideas.

## Sources (local / vendor / rebuilt)
- Deep: OWASP (Secure Coding Practices Quick Reference Guide), rebuilt as original prose above.
- Reference: GeeksforGeeks (Secure Coding Practices in software development).
- Practice: PortSwigger Web Security Academy (SQL injection, information disclosure labs), rebuilt locally as the simulation.
- Repo: OWASP Web Security Testing Guide → `vendor/repos/OWASP-wstg`.
