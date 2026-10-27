# In-class activity, 4.3.b Antivirus and endpoint protection

**Format:** small group · **Time:** 20 min · **Offline:** yes

## Goal
Students work in groups to analyze security logs and write behavioral rules that block malicious activities (like ransomware or keyloggers) without blocking benign administrator activities (avoiding false positives). Ties to LO 4.3.A and 4.3.B.

## Materials (all local)
- Printed or on-screen copy of the behavior log scenarios below.
- Paper or shared text editor for writing behavioral rules.

## Steps
1. Divide the class into groups of 3–4.
2. Review the behavior logs below. Each scenario contains both a **malicious** process and a **benign** process performing similar actions.
3. Your team's task is to write a single detection rule for each scenario that triggers on the malicious activity but ignores the benign activity.
4. Rules should follow a simple structure: `IF [process matches criteria] AND [performs action] THEN block`.

### Behavior Logs for Analysis

#### Scenario A: File Encryptor vs. Backup Utility
- **Process A (Malicious - Ransomware):** `supergame.exe` (run from Temp folder) opens `Documents/` and encrypts 50 files in 3 seconds, writing `.locked` extensions.
- **Process B (Benign - Backup):** `backup_agent.exe` (run from Program Files) opens `Documents/` and reads 50 files in 10 minutes, writing them to an encrypted archive `backup.zip`.

#### Scenario B: Remote Access Tool vs. Remote Admin Tool
- **Process C (Malicious - Trojan):** `explorer_patch.exe` launches, runs in the background silently, listens on port 4444 for incoming connections, and spawns `cmd.exe` when a connection is made.
- **Process D (Benign - Remote Helpdesk):** `helpdesk.exe` launches, prompts the user with a dialog "Allow agent to connect?", listens on port 5900, and starts a screen-sharing session.

#### Scenario C: Living-off-the-land Script vs. Admin Maintenance Script
- **Process E (Malicious - LOTL attack):** `powershell.exe` is spawned by `winword.exe` (Word) moments after a user opens an email attachment, immediately downloads a file from an unfamiliar external IP, and disables Windows Defender via a registry edit.
- **Process F (Benign - IT maintenance):** `powershell.exe` is spawned directly by a logged-in IT administrator's session at 2 AM (scheduled maintenance window) and runs a signed internal script that checks disk space on all endpoints.

5. For Scenario C, discuss why a signature-based tool would likely miss Process E entirely (PowerShell itself is legitimate software, not malware) and write a behavioral rule using **process parentage** (what launched the process) as the key signal.

## Collaborate (AP skill 4)
- **Role 1 (Signature Advocate):** Wants to block the threat by hashing the file (e.g., block `supergame.exe` by name or hash).
- **Role 2 (Behavioral Analyst):** Explains why signature block is insufficient (what if the attacker renames the file or compiles a new version?).
- **Role 3 (Business Operations Manager):** Warns about false positives. If the rule blocks `backup_agent.exe`, the company's daily backups will fail!
Together, negotiate a rule that satisfies all three constraints.

## Exit ticket
Each group submits their final rule for Scenario A, Scenario B, and Scenario C.

## Instructor notes
- Expected Rule A: `IF process path is NOT in C:\Program Files\* AND process modifies >10 files in <5 seconds THEN block`.
- Expected Rule B: `IF process listens on a port AND spawns a shell (cmd.exe or powershell.exe) without user interaction/authorization prompt THEN block`.
- Expected Rule C: `IF powershell.exe is spawned by an Office application (winword.exe, excel.exe) AND makes an outbound network connection THEN block`. Emphasize that the scheduled/interactive nature of Process F (2 AM maintenance window, launched from an admin's own session) is what distinguishes it, not the tool itself.
- Guide students to recognize that path restrictions (like `C:\Windows\*` or `C:\Program Files\*`) and process parentage are critical clues in separating admin tasks from user-space malware.
- Scenario C reinforces the atom's "living-off-the-land" concept: the malicious tool is a legitimate system binary, so behavior and context (parent process, timing, destination), not identity, must drive the detection rule.
