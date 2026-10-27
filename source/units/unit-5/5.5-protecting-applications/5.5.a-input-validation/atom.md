# 5.5.a, Input validation and sanitization

> **Unit 5 · 5.5 Protecting Applications**
> **AP Learning Objective(s):** 5.5.A
> **Course skill(s):** Mitigate Risk

## Learning objective (student-facing)
Explain why every application must treat user input as untrusted,
distinguish allowlist from denylist validation, describe where validation must occur to be
trustworthy, and identify how input validation prevents injection classes like SQL injection,
cross-site scripting, and command injection.

## Lesson
Every application is, at its core, a machine that takes input from a user and does something with
it: stores it, displays it, uses it to build a database query, or passes it to another program.
The single most important security habit a developer can build is treating every piece of input
as hostile until proven otherwise, because on the internet some fraction of the people typing into
a form are not filling out their name and address, they are trying to break the application.
**Input validation** is the practice of checking that input conforms to what the application
expects before it is used. **Sanitization** goes a step further: it transforms input to remove or
neutralize dangerous content rather than simply rejecting it.

**Allowlist vs. denylist.** There are two philosophies for validation. A **denylist** (blocklist)
approach tries to enumerate the bad things: reject any input containing the word `SELECT`, or a
`<script>` tag, or a semicolon. Denylists feel intuitive but fail constantly, because attackers are
endlessly creative at encoding, obfuscating, or rephrasing an attack to slip past a specific
blocked pattern (`SELECT` becomes `SeLeCt`, a semicolon becomes its URL-encoded form `%3B`). An
**allowlist** (whitelist) approach flips the logic: define exactly what valid input looks like, a
US ZIP code is five digits, an email field matches a known pattern, a product quantity is an
integer between 1 and 99, and reject anything that does not match. Allowlisting is dramatically
more robust because it does not need to anticipate every possible attack; it only needs to know
what "correct" looks like, and correctness is usually a much smaller, well-defined space than
"every way to attack this field."

**Client-side vs. server-side validation.** Modern web forms often validate input in the browser
with JavaScript, instantly telling a user "that's not a valid email" without a round trip to the
server. This is good for user experience, but it is **worthless for security**, because a browser
is entirely under the attacker's control. An attacker can disable JavaScript, use browser developer
tools to edit the page, or simply skip the browser altogether and send a crafted HTTP request
directly to the server with a tool like curl. Any validation that lives only in the client can be
bypassed trivially. The rule every AP Cybersecurity student should memorize: **never trust
client-side validation for security; validation must be re-enforced on the server**, where the
attacker cannot tamper with it, on every request, regardless of what the client claims it already
checked.

**Canonicalization.** Before validating, an application often must reduce input to a single,
predictable form, this is **canonicalization**. The same logical string can be represented many
different ways: `../etc/passwd` versus its URL-encoded form `..%2Fetc%2Fpasswd`, or a filename using
different Unicode code points that render identically but compare as different strings. An
application that validates the raw, un-canonicalized input can be tricked into approving a
malicious value because the validator never recognized what it actually decoded to. Proper practice
is to decode/normalize first, then validate the canonical form, then reject anything that still
looks suspicious after normalization; validating before decoding is a classic bypass technique that
lets attackers smuggle path-traversal or injection payloads past naive filters.

**Encoding/escaping vs. sanitization.** These three terms are often confused. **Validation**
decides whether to accept input at all. **Sanitization** actively strips or rewrites dangerous
characters out of input that will be accepted (for example, removing HTML tags from a "comments"
field). **Output encoding/escaping** is different again: it happens later, at the point where data
is placed into a new context, HTML, a SQL query, a shell command, and it transforms special
characters in that context (`<` becomes `&lt;` in HTML) so they are displayed or stored literally
rather than interpreted as code. A common mistake is sanitizing input once at the door and assuming
that protects every later use; in reality, the same piece of data may need different encoding
depending on where it is used (HTML page, SQL query, JSON body, shell command), so secure
applications apply the correct **context-specific encoding** at each output point rather than
relying on a single upstream sanitization pass.

**Why this stops entire attack classes.** SQL injection happens when unvalidated input is
concatenated directly into a database query, letting an attacker's input change the query's
meaning. Cross-site scripting (XSS) happens when unvalidated/unescaped input is rendered as HTML or
JavaScript in another user's browser. Command injection happens when unvalidated input is passed to
a system shell. In all three cases the root failure is the same: the application trusted that input
was "just data" when the input actually contained characters that a downstream interpreter (SQL
engine, browser, shell) treats as code or control syntax. Rigorous input validation, allowlisting
the shape of legitimate data, validating on the server, canonicalizing before checking, and encoding
correctly at each output context, closes that gap at its source.

The coding problem in this skill asks you to build exactly this kind of gate: a validator that
classifies a batch of submitted field values as safe or rejected, using allowlist rules per field
type and detection of known injection meta-characters. The simulation lets you play the role of
that validator directly, classifying a stream of realistic form submissions as SAFE or
MALICIOUS/BLOCKED before the sim reveals the answer.

## Key terms
- **Allowlist (whitelist) validation**, accepting only input that matches a known-good pattern,
  rejecting everything else by default.
- **Denylist (blocklist) validation**, rejecting input that matches known-bad patterns; weaker
  because it must anticipate every attack variant.
- **Canonicalization**, reducing input to one normalized form before validating it, so encoded or
  obfuscated variants cannot slip past a filter that only checks the raw string.
- **Sanitization**, actively stripping or rewriting dangerous content out of accepted input, rather
  than just accepting or rejecting it wholesale.
- **Output encoding**, transforming data at the point it is inserted into a new context (HTML,
  SQL, shell) so special characters are treated as literal data, not executable syntax.

## Common misconceptions
- "Client-side (JavaScript) validation is good enough security." → It improves user experience but
  provides zero security guarantee, since an attacker fully controls the client and can bypass it
  entirely; all security-relevant validation must be re-checked on the server.
- "Sanitizing input once when it's received protects it everywhere it's later used." → The correct
  encoding depends on the output context (HTML vs. SQL vs. shell vs. JSON); a single upstream pass
  is not a substitute for context-specific output encoding at each use.
- "A denylist that blocks the obvious bad keywords is enough." → Attackers routinely bypass
  denylists through case changes, encoding, and alternate syntax; allowlisting known-good shapes is
  far more robust than trying to enumerate every bad one.

## Try it
- **Simulation:** Classify a stream of submitted form values as
  SAFE or BLOCKED against a fixed allowlist/injection-pattern rule set, reaching the target score.
- **Coding problem:** Implement a field validator that classifies a batch of input
  strings against per-field allowlist rules and flags injection meta-characters.
- **Quiz:** self-check on the skill's key ideas.

## Sources (local / vendor / rebuilt)
- Deep: OWASP (Input Validation Cheat Sheet, Injection Prevention), rebuilt as original prose above.
- Reference: GeeksforGeeks (Input Validation and Sanitization in web security).
- Practice: PortSwigger Web Security Academy (injection labs), rebuilt locally as the simulation.
- Repo: OWASP Web Security Testing Guide → `vendor/repos/OWASP-wstg`.
