# 5.1.c, API vulnerabilities

> **Unit 5 · 5.1 Application and Data Vulnerabilities and Attacks**
> **AP Learning Objective(s):** 5.1.B
> **Course skill(s):** Analyze Risk

## Learning objective (student-facing)
Explain how broken object-level authorization (BOLA/IDOR) and
excessive-data-exposure flaws let an attacker abuse an application programming interface (API) to
access data or objects they should not be able to reach, and can identify the missing check that
causes it.

## Lesson
An **API (application programming interface)** is the set of URLs, request formats, and response
formats a client application uses to talk to a server. Modern apps, mobile, web, IoT, are almost
entirely built on APIs: the mobile banking app calls `GET /api/accounts/482` to show your balance,
a shopping site calls `GET /api/orders/9931` to show your order status. Because APIs expose
structured, predictable endpoints directly, they are an especially attractive and easy target: an
attacker doesn't need to reverse-engineer a page, they just change a number in a URL and see what
happens.

The single most common and most damaging API flaw in the field, and the one this skill focuses on, is **Broken Object Level Authorization (BOLA)**, also widely known as **Insecure Direct Object
Reference (IDOR)**. It happens when an API endpoint accepts an object identifier from the client
(an account ID, order ID, invoice number, file ID) and fetches/returns that object **without
verifying that the currently authenticated user is actually allowed to access it**. The API checks
"is this token valid?" (authentication) but skips "does this specific token's owner have
permission to see *this specific object*?" (authorization). Those are two different questions, and
BOLA is what happens when only the first one gets asked.

Concretely: suppose you are logged in as user 482 and the app calls `GET /api/accounts/482` and
correctly shows your balance. If you (or an attacker with a valid account of their own) instead
call `GET /api/accounts/483`, a BOLA-vulnerable API will happily return account 483's private
balance too, because the server only checked "is there a valid session," not "does this session
belong to account 483." This is exactly the vulnerability OWASP ranks as the #1 API security risk,
because object identifiers (database primary keys, sequential order numbers) are frequently
predictable, and the fix is easy to describe but easy to forget: **every** request that reads,
writes, or deletes a specific object must re-check that the authenticated identity owns or is
authorized for that specific object, on the server, on every request, never trust that "the
client only shows the buttons for your own data" is enough, because an attacker can call the API
directly with a tool like curl or Postman, bypassing the UI entirely.

A close cousin is **excessive data exposure**: an API endpoint that returns a full internal object
(including fields like password hashes, internal notes, or another user's email) because a
developer serialized the whole database row instead of filtering to only the fields the client
actually needs, trusting the front-end to hide the extra fields, while an attacker inspecting the
raw response sees everything. **Broken function-level authorization** is a related flaw where an
endpoint meant only for admins (e.g., `POST /api/users/482/promote`) is reachable by any
authenticated user because the server never checks the caller's role, only that they are logged in.

Why do APIs make this class of bug more common than in traditional web pages? Because APIs are
designed to be called directly and repeatedly by automated clients, they expose the raw
object-identifier pattern more transparently than a rendered HTML page would, and because access
control has to be re-implemented correctly on *every single endpoint*, a large API surface with
dozens or hundreds of endpoints multiplies the chance that one of them forgets the ownership check.

The coding problem in this skill asks you to build exactly that missing check: given a simulated
API request (the authenticated caller's identity plus the object being requested) and a simulated
object-ownership table, decide whether the request should be allowed or rejected as a BOLA
violation. The simulation puts you in the attacker's seat at a fake API console, letting you probe
endpoints by changing an ID parameter and observing (safely, against synthetic data) whether the
mock API leaks another user's object.

## Key terms
- **API (application programming interface)**, the defined set of endpoints/requests a client
  uses to interact with a server's data and functionality.
- **Broken Object Level Authorization (BOLA) / IDOR**, an API accepts a client-supplied object ID
  and returns/modifies that object without verifying the caller is authorized for that specific
  object.
- **Authentication vs. authorization**, authentication proves *who you are*; authorization checks
  *what that identity is allowed to do/see*. BOLA is an authorization failure, not an
  authentication failure.
- **Excessive data exposure**, an endpoint returns more fields/data than the client needs,
  relying on the front-end (not the server) to hide sensitive fields.
- **Broken function-level authorization**, an endpoint intended for a privileged role is
  reachable by any authenticated user because the server never checks role/permission.

## Common misconceptions
- "If the request needs a valid login token, it's secure." → Authentication only proves identity;
  BOLA happens precisely when authorization (per-object permission) is never checked afterward.
- "Hiding a button in the UI prevents unauthorized access." → Attackers call the API directly with
  tools like curl/Postman; hiding a button does not stop a raw HTTP request.

## Try it
- **Simulation:** Probe a mock API console by varying object IDs
  and correctly identify which requests are BOLA violations before the mock server flags them.
- **Coding problem:** Build an authorization-check function that decides whether an
  API request is allowed given the caller's identity and the object's owner.
- **Quiz:** self-check on the skill's key ideas.

## Sources (local / vendor / rebuilt)
- Deep: OWASP (API Security Top 10, BOLA), rebuilt as original prose above.
- Reference: GeeksforGeeks (IDOR / API vulnerability overview).
- Practice: PortSwigger Web Security Academy (access-control labs) → rebuilt locally as the simulation.
- Repo: OWASP/wstg (Web Security Testing Guide) → `vendor/repos/OWASP-wstg`.
