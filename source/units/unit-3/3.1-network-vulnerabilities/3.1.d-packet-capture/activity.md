# In-class activity, 3.1.d Packet capture and traffic sniffing

**Format:** small group (3-4) · **Time:** 25 min · **Offline:** yes

## Goal
Groups act as SOC analysts triaging a batch of captured packet log entries, decide which ones leak
a plaintext credential, and propose one mitigation per protocol involved. Ties to LO 3.1.B, 3.1.C
and the course skill Detect Attacks.

## Materials (all local)
- the SimLab simulation on each machine, or the printed log below.

## Capture log (print or project)

| # | Protocol/Port | Destination | Payload snippet | Verdict? |
|---|----------------|-------------|-------------------|----------|
| 1 | TCP/80 | intranet.example:80 | `POST /login ... user=alice&password=Pass123!` | ? |
| 2 | TCP/443 | payroll.example:443 | `(TLS encrypted application data)` | ? |
| 3 | TCP/23 | switch.local:23 | `login: netadmin\nPassword: Sw1tchAdmin` | ? |
| 4 | TCP/80 | wiki.example:80 | `GET /docs/onboarding.html HTTP/1.1` | ? |
| 5 | TCP/21 | ftp.example:21 | `USER backup\nPASS Backup#2024` | ? |

## Steps
1. (5 min) Each group reads rows 1-2 individually and decides LEAK or SAFE using the
   protocol/port + payload-content rule from the lesson.
2. (5 min) Group discusses row 3 (Telnet): why is the entire login exchange visible even though
   this is an "administrative" connection to network equipment, not a public website?
3. (7 min) Group works rows 4-5 together: row 4 is cleartext HTTP but the payload holds no
   credential; row 5 is a different cleartext protocol (FTP) with a different credential syntax
   (USER/PASS). Decide both, and discuss why the *port/protocol* matters as much as the payload
   content.
4. (5 min) Each group opens the simulation and checks their calls against the sim's scoring for
   analogous scenarios; groups revise any incorrect calls.
5. (3 min) Report-out: each group proposes the encrypted replacement protocol for each LEAK row
   (e.g., HTTPS for HTTP, SSH for Telnet, SFTP/FTPS for FTP).

## Collaborate (AP skill 4)
Assign roles: one member is the "capture analyst" (applies the protocol/port + payload rule), one
is the "network admin" (explains what legitimate business reason each connection might have), and
remaining members are "auditors" (challenge whether a payload really contains a credential or just
looks like one). For row 2 (HTTPS, encrypted), the group must specifically explain why a capture
analyst cannot determine anything about the login credentials even though they can see the
connection is happening.

## Exit ticket
Each student writes one sentence: "Row X is [LEAK / SAFE] because [protocol/port] is [cleartext /
encrypted] and the payload [does / does not] contain a credential."

## Answer key (instructor only)

| # | Verdict | Reasoning |
|---|---------|-----------|
| 1 | LEAK | Port 80 (HTTP, cleartext); payload contains `password=Pass123!`. |
| 2 | SAFE | Port 443 (HTTPS, encrypted); payload is unreadable ciphertext regardless of what's inside. |
| 3 | LEAK | Port 23 (Telnet, cleartext); full username/password visible. |
| 4 | SAFE | Port 80 is cleartext-capable, but this GET request has no credential in the payload. |
| 5 | LEAK | Port 21 (FTP control, cleartext); USER/PASS authentication visible in plaintext. |

## Instructor notes
- Timing: rows 1-2 are the core rule cases; row 3 reinforces that "administrative" traffic is not
  automatically safe; rows 4-5 are the deliberate teaching moment that protocol/port AND payload
  content both matter, cleartext capability alone does not mean every packet leaks something.
- Common stumble: students assume any HTTP (port 80) traffic is automatically a LEAK regardless of
  payload content, push them to check whether an actual credential is present.
- A second common stumble: students assume HTTPS traffic must be SAFE only because "it looks
  scrambled," rather than understanding WHY (TLS encryption) it is unreadable.
- Feeds forward to 3.1.b (DNS attacks) and 3.1.c (ARP spoofing/MITM), both of which are enabling
  techniques that put an attacker in a position to capture traffic like this in the first place.
