# 4.2.c, Session security

> **Unit 4 · 4.2 Authentication**
> **AP Learning Objective(s):** 4.2.B
> **Course skill(s):** Mitigate Risk

## Learning objective (student-facing)
Explain how session tokens keep a user authenticated across
requests, identify session hijacking and session fixation from a described scenario, and
recommend the specific control (secure cookie flag, timeout, or session regeneration) that
mitigates each.

## Lesson
Authentication (checking a username and password) happens once, but a user typically stays
"logged in" across many page loads and API calls. Re-entering a password on every click would be
unusable. To solve this, the server issues a **session** the moment authentication succeeds: a
record, stored server-side, that says "this browser has proven who it is." The server hands the
browser a **session token** (often called a **session cookie**), a long, random, unpredictable
string, and the browser automatically resends that token with every subsequent request. The
server looks up the token, finds the matching session record, and treats the request as coming
from the authenticated user. No password re-entry needed. This is convenient, but it also means
the token itself becomes as valuable as the password: whoever holds a valid session token *is*
that user, as far as the server can tell.

**Session hijacking** is the theft and reuse of a legitimate, already-authenticated session
token. An attacker does not need to know the victim's password at all, only the token. Common
theft paths include: cross-site scripting (XSS), where injected JavaScript reads the cookie and
sends it to the attacker; sniffing unencrypted HTTP traffic on a shared or public network, where
the token is visible in plaintext; and malware on the victim's own device reading browser storage.
Once the attacker has the token, they present it to the server and are treated as the victim, no login screen, no alert, until something looks unusual.

**Session fixation** is a related but distinct attack. Instead of stealing an existing session,
the attacker *forces* the victim to use a session ID the attacker already knows, for example, by
sending the victim a link containing a pre-set session identifier. If the victim then logs in
without the server changing that ID, the attacker's known ID is now attached to an authenticated
session. The attacker simply uses the same ID to walk in as the victim. Key distinguishing trait:
in fixation the attacker supplies the ID *before* login; in hijacking the attacker steals an ID
*after* the victim is already authenticated.

**Session expiration** limits how much damage a stolen or fixated token can do. An **idle
timeout** ends a session after a period of no activity (e.g., 15 minutes), which protects users
who walk away from a logged-in device. An **absolute timeout** ends a session after a fixed total
duration (e.g., 8 hours) regardless of activity, which limits how long a stolen token remains
useful even if the attacker keeps it "alive" with periodic requests. Sessions with no timeout at
all are a serious risk: a token leaked once could be replayed indefinitely.

**Secure cookie flags** reduce the attack surface of the token itself. The **Secure** flag tells
the browser to send the cookie only over HTTPS, so it cannot be sniffed on plaintext HTTP. The
**HttpOnly** flag tells the browser to hide the cookie from JavaScript entirely, so even a
successful XSS injection cannot read and exfiltrate it. The **SameSite** flag restricts whether
the cookie is sent along with cross-site requests, which helps mitigate cross-site request
forgery (CSRF) by preventing another site from silently riding on the user's session. None of
these flags is a complete defense alone, they are layers that close off specific theft or misuse
paths.

**Session regeneration** is the standard fix for fixation: the server issues a brand-new,
freshly-random session ID at the moment of login (and again at any privilege change, such as
becoming an admin). Any ID an attacker planted beforehand is discarded and never becomes
authenticated, so fixation fails even if the attacker successfully set an ID on the victim's
browser.

**Logout must be a server-side action, not just a client-side one.** A "logout" that only deletes
the cookie from the browser leaves the session record alive on the server. If an attacker
captured the token before logout, that token still works, the user's action of clicking
"logout" gave them no real protection. Proper logout invalidates the session record on the
server, so the token is permanently useless the instant the user logs out, no matter who holds a
copy of it.

## Key terms
- **Session**, a server-side record that a specific browser has successfully authenticated.
- **Session token / session cookie**, the random string identifying a session, sent by the
  browser on every request.
- **Session hijacking**, stealing and reusing a victim's already-authenticated session token.
- **Session fixation**, forcing a victim to authenticate under a session ID the attacker
  already controls.
- **Idle timeout**, session expiration triggered by a period of no activity.
- **Absolute timeout**, session expiration triggered after a fixed total duration.
- **Secure flag**, cookie attribute restricting transmission to HTTPS only.
- **HttpOnly flag**, cookie attribute hiding the cookie from JavaScript, blunting XSS theft.
- **SameSite**, cookie attribute limiting cross-site sending, mitigating CSRF.
- **Session regeneration**, issuing a fresh session ID at login / privilege change, defeating
  fixation.

## Common misconceptions
- "Deleting the cookie on logout fully logs the user out." → False. If the server does not
  invalidate the session record, a copy of the token captured earlier (e.g., via network sniffing)
  remains valid and can still be replayed after the user thinks they logged out.
- "HTTPS alone makes sessions un-hijackable." → False. HTTPS protects the token in transit, but if
  the cookie is missing the HttpOnly flag, a successful XSS injection can still read it directly
  from the page's JavaScript context and send it to the attacker, no network sniffing required.
- "Session fixation and session hijacking are the same attack." → False. Fixation plants a known
  ID *before* login; hijacking steals a live ID *after* login. The defenses differ: regeneration
  stops fixation, while secure flags and encrypted transport stop hijacking.

## Try it
- **Simulation:** Review a stream of session-related incident
  logs and classify each as hijacking, fixation, improper timeout, insecure cookie flag, or
  secure, reaching the target score.
- **Coding problem:** Implement a classifier that maps session-incident description
  strings to the correct vulnerability category.
- **Quiz:** self-check on the skill's key ideas.

## Sources (local / vendor / rebuilt)
- Deep: NIST, session management guidance, rebuilt as original prose above; see
  `vendor/web/nist/` notes.
- Reference: Wikiversity (session security overview), cross-checked for accuracy.
- Practice: SANS Cyber Aces session-security micro-challenges, rebuilt locally as the simulation.
- Repo: LetsDefend/Free-Cybersecurity-Resources → `vendor/repos/letsdefend-free-cybersecurity-resources`.
