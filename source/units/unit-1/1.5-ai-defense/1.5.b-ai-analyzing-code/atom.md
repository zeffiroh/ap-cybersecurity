# 1.5.b, AI analyzing code for vulnerabilities

> **Unit 1 · 1.5 Leveraging AI in Cyber Defense**
> **AP Learning Objective(s):** 1.5.A
> **Course skill(s):** Detect Attacks, Collaborate

## Learning objective (student-facing)
Explain how AI-powered static analysis scans source code for
known vulnerability patterns, identify specific risky constructs in Python code, and articulate
why each flagged pattern creates a security risk.

## Lesson
Writing software that is both functional and secure is hard. Developers focus on making code work;
security analysis is often an afterthought. For decades, the answer was manual code review, a
senior engineer reading every line looking for bugs. That approach does not scale: modern software
projects contain millions of lines and deploy dozens of times a day. AI-assisted static analysis
tools now fill this gap, scanning source code for dangerous patterns in milliseconds before the
code ever runs.

**What static analysis means.** Static analysis examines code without executing it. It reads the
source text and matches patterns against a database of known-dangerous constructs. This is
different from dynamic analysis (running the code and watching what it does) and from fuzzing
(sending random inputs to trigger crashes). Static analysis is fast, cheap, and catches whole
classes of bugs regardless of the inputs the developer happened to test. The tradeoff is that it
can produce false positives, flagging code that is technically fine in its specific context, and
it cannot find bugs that only appear at runtime from unexpected state.

**Six risky patterns every analyst should know.** The rule set for this skill covers the patterns
an AI code reviewer would look for in Python:

`eval(`, Python's `eval` executes an arbitrary string as code. If user input reaches `eval`,
an attacker can execute any Python expression on the server. This is a classic code injection
vulnerability. Virtually no legitimate production code needs `eval`.

`os.system(`, passes a shell command string to the operating system. If user data is interpolated
into that string, an attacker can append shell metacharacters (`;`, `|`, `&&`) to run additional
commands. This is called OS command injection, and it is listed every year in OWASP's Top 10.

`subprocess` with `shell=True`, the `subprocess` module is the modern replacement for `os.system`,
but the `shell=True` flag restores the same injection risk. When `shell=True` is present and
combined with user-controlled input, the result is identical to the `os.system` vulnerability.

`md5(`, MD5 is a broken cryptographic hash function. It was cracked for collision attacks in
2004, and rainbow tables make it trivially reversible for passwords. Any code still using MD5 for
security (password storage, file integrity verification, digital signatures) has a cryptographic
weakness. `sha1` is similarly broken; `sha256` or better should be used instead.

`pickle.loads(`, Python's `pickle` module serializes and deserializes Python objects. Deserializing
a pickle from an untrusted source is dangerous because a maliciously crafted pickle can execute
arbitrary Python code during deserialization, no exploit needed, just loading the data. This is
a deserialization vulnerability, one of the most severe categories of software bugs.

Hardcoded passwords, the pattern `password =` followed by a string literal in source code means
the credential is checked into version control, visible to every developer, and often leaked in
public repositories. Credential exposure is consistently one of the most common causes of cloud
security breaches.

**How AI improves on grep.** The simplest version of code scanning is a regex search, grep for
dangerous function names. AI tools go further: they build an abstract syntax tree (AST) of the
code, track data flow to see whether user input reaches a dangerous sink, and score confidence
levels. For the AP course, the rule-engine (substring matching) layer is the right foundation,
because it makes the detection logic transparent and auditable. The sim lets you practice the
human analyst's role; the coding problem implements the rule engine itself.

**The role of context.** As with config review, a finding is not a verdict. `eval(` inside a
security-research tool that processes trusted, sandboxed input may be acceptable. `md5(` used to
generate a cache key (not a password hash) is not a vulnerability. The security engineer reviews
each finding and decides: fix, document as intentional exception, or escalate. AI handles scale;
humans handle judgment.

**Why this matters for the AP framework.** The "Detect Attacks" skill is not just about network
intrusion detection, it includes detecting vulnerable code before it ships. A single `pickle.loads`
on a web endpoint that accepts user-uploaded data is effectively a remote code execution
vulnerability waiting to be discovered. AI code review is one of the highest-leverage defensive
tools available: catching vulnerabilities before deployment prevents the breach entirely rather than
detecting it afterward.

The coding problem builds a static scanner: given a string of source code, return sorted finding
tags for every dangerous pattern present. Completing it will give you an intuition for both the
power and the limits of pattern-based vulnerability detection.

## Key terms
- **Static analysis**, examining source code without executing it to detect bugs and security
  vulnerabilities by pattern matching or data-flow modeling.
- **Code injection**, a class of attacks where an attacker supplies input that is interpreted as
  code by the application (e.g., via `eval`).
- **OS command injection**, an attack where user input is passed to a shell, allowing the attacker
  to append arbitrary shell commands (`os.system`, `subprocess shell=True`).
- **Deserialization vulnerability**, a bug where loading serialized data from an untrusted source
  executes attacker-controlled code (e.g., `pickle.loads`).
- **Broken cryptography**, use of algorithms (MD5, SHA-1) that are no longer considered secure
  for the intended purpose (passwords, signatures).
- **Hardcoded credential**, a password or key embedded directly in source code, making it
  accessible to anyone who can read the file.

## Common misconceptions
- "Static analysis finds all vulnerabilities." → Static analysis finds known patterns; novel
  logic bugs, authentication flaws, and business-logic errors usually require human review or
  dynamic testing.
- "MD5 is only a problem for passwords." → MD5 is broken for any security use: file integrity,
  signatures, or tokens. It is fine for non-security checksums (e.g., cache keys).
- "subprocess is safe if I use it instead of os.system." → subprocess with `shell=True` has the
  same injection risk as os.system. The safe usage is passing a list of arguments with
  `shell=False`.

## Try it
- **Simulation:** Act as an AI code reviewer, read each code
  snippet and flag all dangerous patterns, reaching the target score.
- **Coding problem:** Implement `solve(code)` that returns sorted vulnerability tags
  for a Python source string.
- **Quiz:** self-check on the skill's key ideas.

## Sources (local / vendor / rebuilt)
- Deep: MIT OCW (software security, static analysis), rebuilt as original prose above.
- Reference: GeeksforGeeks (Python security anti-patterns, OWASP Top 10).
- Practice: Cybrary / LetsDefend secure-code-review challenges, rebuilt locally as the simulation.
- Repo: LetsDefend/Free-Cybersecurity-Resources → `vendor/repos/letsdefend-free-cybersecurity-resources`.
