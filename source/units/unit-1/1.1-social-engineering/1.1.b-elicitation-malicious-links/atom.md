# 1.1.b, Elicitation; malicious links and files

> **Unit 1 · 1.1 Understanding Social Engineering**
> **AP Learning Objective(s):** 1.1.A, 1.1.C
> **Course skill(s):** Analyze Risk

## Learning objective (student-facing)
Describe how elicitation extracts sensitive information through
conversation, and you can identify the technical indicators that distinguish a malicious link or
file from a legitimate one.

## Lesson
Social engineering has two operational phases. The first is pressure, the psychological levers
covered in 1.1.a. The second is extraction and delivery: getting the victim to surrender
information through conversation, or to open something dangerous. This skill covers both sides of
that second phase.

### Elicitation

Elicitation is the technique of drawing out sensitive information from someone through seemingly
casual conversation, without the target realizing they are being interrogated. It is a staple of
intelligence tradecraft, competitive espionage, and social-engineering attacks that begin over
the phone or in person before moving online.

Unlike a direct question, "What is your VPN password?", elicitation is indirect. An attacker
posing as a new IT contractor might complain about forgetting the naming convention used for
internal servers, hoping the target helpfully fills in the detail. Common elicitation gambits:

**Flattery and appeal to expertise.** "You clearly know this system better than anyone. I'm
embarrassed to ask, but how exactly does the authentication flow work here?" People enjoy being
recognized as knowledgeable and will often explain at length to demonstrate that expertise,
revealing architecture or process details the attacker wanted all along.

**Deliberate incorrect statements.** The attacker states something slightly wrong. Humans have a
near-universal impulse to correct errors, and in doing so the target volunteers the accurate
information unprompted. "I heard your backup server sits on subnet 10.0.10.x, oh, that's the
old location, isn't it?"

**Mutual disclosure (quid pro quo).** The attacker shares something benign about themselves
first, establishing an implied social contract of reciprocity. The target feels obligated to
share something equivalent, even if the "something" the attacker originally shared was fabricated.

**Third-party reference.** "Your colleague Davis told me the process. I just need the
confirmation code you use on your end." Invoking a trusted name lowers suspicion and frames
compliance as a normal, already-endorsed action.

What makes elicitation hard to defend against is that each piece of information given up seems
harmless in isolation. The target may genuinely believe nothing sensitive was revealed.
Attackers build a complete picture from fragments gathered across multiple conversations.

**Defense against elicitation:** apply need-to-know discipline. Before answering any question
about systems, processes, or people, ask: does this person have a verified reason to know this?
Verify identity through official channels before sharing operational details. Report suspicious
questioning to the security team.

### Malicious links

A malicious link is a URL engineered to look legitimate while routing the victim to an
attacker-controlled destination. Several technical indicators distinguish these from real URLs.

**Lookalike domains (typosquatting and homograph attacks).** Attackers register domains that
visually resemble trusted ones: `paypa1.com` (numeral 1 replacing lowercase l), `arnazon.com`
(r and n adjacent and visually similar to m), or `microsoft.com.evil.net` (where the actual
domain is `evil.net` and the trusted name appears as a subdomain). The rule: read URLs
right-to-left from the first slash. The portion immediately before the first slash is the real
domain. Everything to the left of the root domain is a subdomain controlled by whoever owns
that root.

**IP-literal URLs.** Legitimate services almost never send you directly to a raw IP address:
`http://192.168.44.23/reset?token=abc`. An IP-literal URL in a message is a strong indicator
that the link does not go where the surrounding text implies.

**Mismatched link text.** The visible text of a hyperlink says one thing; the underlying href
goes somewhere else. "Click here to verify your account at bankofamerica.com" with an href of
`http://verify.bank-secure-login.xyz/` is a classic mismatch. In email, hover before clicking
to reveal the real destination. On mobile, long-press to preview the URL before opening it.

**URL shorteners.** `bit.ly/xr94k` and similar services hide the real destination entirely.
Legitimate organizations sending security-sensitive links rarely need to obscure where they
lead. Treat unresolvable short links in unsolicited messages with skepticism.

### Malicious files

The delivery vehicle is often a file rather than a live URL. Dangerous extensions to recognize:

**Directly executable files:** `.exe`, `.scr` (screensaver format, but fully executable),
`.bat`, `.cmd`, `.ps1` (PowerShell script), `.vbs` (VBScript), `.js` (JScript on Windows),
`.jar` (Java archive). Opening any of these can run arbitrary code with the user's permissions.

**Office files with macros:** `.docm`, `.xlsm`, `.pptm`. Modern Office versions disable macros
by default, but attackers use social pressure, "you must enable content to view this
document", to override that protection.

**Archive wrappers:** A `.zip` or `.rar` does not execute on its own, but these formats are
commonly used to hide an executable inside, bypassing email filters that block `.exe` directly.

**Double extensions:** `invoice.pdf.exe` is a filename designed to look like a PDF. Windows
hides known extensions by default, so this file appears as `invoice.pdf` in the file browser,
and many users double-click it expecting a document.

The principle is the same for links and files: the attacker controls what the victim sees, and
what the victim sees is designed to suggest something safe and familiar. The actual destination
or payload is neither.

**Defense:** hover before clicking and read URLs methodically. Never open an unsolicited
attachment without verifying the sender through a second, independent channel. Turn on
file-extension visibility in your operating system. Treat any request to disable a security
warning, macro prompts, browser warnings, extension-mismatch alerts, as itself a red flag.

## Key terms
- **Elicitation**, covert extraction of information through conversation, without the target
  realizing that sensitive details are being gathered.
- **Typosquatting**, registering a domain visually similar to a trusted brand to deceive users.
- **Homograph attack**, using visually identical characters from different scripts in a domain
  name to impersonate a legitimate domain.
- **IP-literal URL**, a URL using a raw IP address instead of a hostname, often signaling
  deception because legitimate services rarely use this form in communications.
- **Mismatched link**, a hyperlink whose visible anchor text differs from its actual href
  destination.
- **Dangerous extension**, a file extension (.exe.scr.ps1.vbs, etc.) indicating the
  file can execute arbitrary code when opened.
- **Double extension**, a filename like `report.pdf.exe` used to disguise an executable as
  a harmless file type by exploiting OS defaults that hide the final extension.

## Common misconceptions
- "HTTPS means the site is safe." → HTTPS only means the connection is encrypted. Attackers
  routinely obtain free TLS certificates for malicious domains; the padlock proves encryption,
  not legitimacy.
- "Antivirus will catch every malicious file." → Novel malware and fileless payloads frequently
  evade signature-based detection. Recognizing dangerous extensions adds a layer that does not
  depend on vendor updates.
- "I would notice a fake domain." → Homograph and typosquatting attacks are specifically
  designed to defeat casual visual inspection. Always read URLs from right to left, methodically.

## Try it
- **Simulation:** Inspect a series of messages with links and
  attachments; flag the malicious indicators in each and reach the target score.
- **Coding problem:** Implement a URL/filename analyzer that returns a sorted list
  of malicious indicators such as "lookalike-domain", "ip-url", "dangerous-extension", and
  "mismatched-link".
- **Quiz:** self-check on the skill's key ideas.

## Sources (local / vendor / rebuilt)
- Deep: MIT OCW (human-factors security and network security), rebuilt as original prose above.
- Reference: GeeksforGeeks (social engineering, malicious URLs overview).
- Practice: Cybrary / Try Cyber phishing-awareness challenges, rebuilt locally as the simulation.
- Repo: labex-labs/cybersecurity-free-tutorials, `vendor/repos/labex-cybersecurity-free-tutorials`.
