# In-class activity, 4.1.c IoT device vulnerabilities

**Format:** pairs · **Time:** 25 min · **Offline:** yes

## Goal
Students learn to identify the dominant vulnerability category in a described IoT device and
propose the matching defense. Ties to LO 4.1.A (identify vulnerability categories) and 4.1.C
(analyze IoT-specific risk).

## Materials (all local)
- the SimLab simulation on each machine, or the printed device cards below.
- Blank paper for the defense table (Step 3).

## Steps
1. **Classify the devices (10 min).** Each pair reads the five device descriptions below and
   writes the dominant vulnerability category (default credentials, outdated firmware, exposed
   port, unauthenticated API, unencrypted traffic, or secure) with a one-sentence justification.

   - **Device A:** A smart doorbell camera is still running the username/password it shipped
     with from the factory. Its firmware was updated last month and its app traffic is encrypted.
   - **Device B:** An office network-attached printer has Telnet (port 23) open for "remote
     diagnostics," left on since installation three years ago. Its password was changed at setup.
   - **Device C:** A smart thermostat's manufacturer stopped releasing firmware updates two years
     ago. A known vulnerability in its old firmware version was published last month. No default
     password, no open management ports.
   - **Device D:** A fitness tracker's companion app talks to a cloud API that returns any user's
     step data if you simply guess their numeric account ID, no login token required.
   - **Device E:** A smart plug sends its on/off commands over the local network in plain,
     unencrypted text, readable by anything else connected to that Wi-Fi network.

2. **Compare with the simulation (5 min).** Open the simulation and work through its device audit to check
   your classifications. Note any disagreements and discuss why.

3. **Build a defense table (10 min).** As a pair, fill in the table:

   | Vulnerability category | Why it's dangerous | One technical defense | One policy defense |
   |---|---|---|---|
   | Default credentials | | | |
   | Outdated firmware | | | |
   | Exposed port | | | |
   | Unauthenticated API | | | |
   | Unencrypted traffic | | | |

## Collaborate (AP skill 4)
Assign roles: one partner is the "auditor" (identifies which vulnerability category and why), the
other is the "remediator" (proposes the most effective fix). Swap roles for the defense table.
Compare your completed tables with another pair, identify any defense they listed that you missed,
and discuss whether any device in Step 1 could realistically fail more than one category at once.

## Exit ticket
Each student submits: their classification of Device D + a one-sentence explanation of why a
botnet like Mirai is dangerous even though each individual compromised device seems unimportant.

## Instructor notes
- Expected answers: A=default_credentials (factory login never changed, overrides other checks),
  B=exposed_port (Telnet open on port 23), C=outdated_firmware (EOL device, unpatched known
  vulnerability), D=unauthenticated_api (no auth token required to read another user's data),
  E=unencrypted_traffic (plaintext commands on local network).
- Common stumble: students classify Device C as "secure" because it has no open ports or default
  password. Clarify that EOL/outdated firmware is itself the vulnerability even with everything
  else locked down, the flaw lives inside the code that never gets patched.
- Defense table expected highlights: default credentials (forced password change at setup,
  unique per-device passwords); outdated firmware (vendor support lifecycle checks, network
  segmentation for EOL devices); exposed port (disable Telnet/UPnP, close unused ports);
  unauthenticated API (require auth tokens, rate-limit and validate every request); unencrypted
  traffic (enforce TLS, VPN for remote management).
- Feeds the unit project (device hardening plan) and connects to 4.1.a (malware) via the Mirai
  botnet example, an insecure IoT device is a stepping stone to a much larger attack.
