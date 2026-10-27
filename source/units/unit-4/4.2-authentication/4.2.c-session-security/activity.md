# In-class activity, 4.2.c Session security

**Format:** pairs · **Time:** 25 min · **Offline:** yes

## Goal
Students learn to classify session-security vulnerabilities by scenario description and propose
the specific technical fix for each. Ties to LO 4.2.B (mitigate session-related risk).

## Materials (all local)
- the SimLab simulation on each machine, or the printed incident cards below.
- Blank paper for the defense table (Step 3).

## Steps
1. **Classify the incidents (10 min).** Each pair reads the five scenarios below and writes the
   vulnerability class (hijacking, fixation, improper timeout, insecure cookie flag) and the
   specific fix that addresses it.

   - **Incident A:** An attacker on the same public WiFi network captures a user's session cookie
     in plaintext over HTTP and replays it to access the account without a password.
   - **Incident B:** A phishing email contains a link with a pre-set session ID embedded in the
     URL. The victim clicks the link, logs in, and the server keeps using that same session ID.
     The attacker now uses the identical ID to access the account.
   - **Incident C:** A shared office workstation stays logged into the HR portal all weekend
     because no idle timeout is configured. A janitor discovers the open session Monday morning.
   - **Incident D:** A stored XSS vulnerability lets an attacker inject a script that reads
     `document.cookie` and exfiltrates the session token, because the cookie has no HttpOnly flag.
   - **Incident E:** A user clicks "Log Out." Their browser cookie is deleted, but the server
     never marks the session record as invalid. A token captured earlier by an attacker still
     works after the "logout."

2. **Compare with the simulation (5 min).** Open the simulation and work through its incident stream to
   check your classifications. Note any disagreements and discuss why.

3. **Build a defense table (10 min).** As a pair, fill in the table:

   | Vulnerability class | Example indicator | Specific technical fix |
   |---|---|---|
   | Hijacking | | |
   | Fixation | | |
   | Improper timeout | | |
   | Insecure cookie flag | | |

## Collaborate (AP skill 4)
Assign roles: one partner is the "log auditor" (explains which vulnerability class and why), the
other is the "remediation lead" (proposes the exact fix, e.g., "add the HttpOnly flag" or
"regenerate the session ID at login"). Swap roles halfway through the incident list. Compare your
completed defense table with another pair and reconcile any fix you worded differently.

## Exit ticket
Each student submits: their classification of Incident E + a one-sentence explanation of why
deleting a client-side cookie is not equivalent to a secure logout.

## Instructor notes
- Expected answers: A=hijacking (token sniffed over unencrypted HTTP; fix: enforce HTTPS + Secure
  flag), B=fixation (attacker-supplied ID used before login; fix: regenerate session ID on
  authentication), C=improper timeout (no idle timeout; fix: configure idle + absolute timeouts),
  D=insecure cookie flag (missing HttpOnly; fix: set HttpOnly on the session cookie),
  E=improper logout / hijacking risk (server-side session not invalidated; fix: invalidate the
  session record server-side on logout, not just delete the client cookie).
- Common stumble: students conflate B (fixation) with A/E (hijacking) because both end with the
  attacker using a valid session. Clarify the timing test: did the attacker supply the ID before
  login (fixation) or steal an ID that was already authenticated (hijacking)?
- Defense table expected highlights: hijacking (HTTPS/Secure flag, HttpOnly flag, network
  encryption); fixation (session regeneration at login/privilege change); improper timeout (idle
  timeout, absolute timeout); insecure cookie flag (set Secure, HttpOnly, SameSite explicitly).
- Feeds the unit project (authentication hardening plan) and reinforces 4.2.a/4.2.b (MFA,
  password policy) as complementary, not substitute, controls for session integrity.
