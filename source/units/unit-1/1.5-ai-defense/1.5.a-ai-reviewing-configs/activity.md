# In-class activity, 1.5.a AI reviewing security configurations

**Format:** pairs · **Time:** 25 min · **Offline:** yes

## Goal
Students practice reading configuration files with an auditor's eye: identifying insecure
directives, naming the specific risk, and proposing the corrected setting. Ties to LO 1.5.A
(explain how AI tools support configuration review and risk mitigation).

## Materials (all local)
- the SimLab simulation on each machine, the config auditor simulation.
- Printed config snippets below (or displayed on screen).

## Config snippets for review

**Config A, SSH server (sshd_config)**
```
Port 22
PermitRootLogin yes
PasswordAuthentication yes
X11Forwarding yes
AllowTcpForwarding yes
```

**Config B, database proxy**
```
bind_address = 0.0.0.0
port = 5432
ssl = false
max_connections = 100
log_connections = off
```

**Config C, hardened SSH (compare)**
```
Port 22
PermitRootLogin no
PasswordAuthentication no
PubkeyAuthentication yes
X11Forwarding no
AllowTcpForwarding no
```

## Steps
1. Each pair reads Config A. For each line, decide: insecure (flag it) or acceptable (pass).
   Write the finding tag (e.g., `insecure:PermitRootLogin`) and one sentence explaining the risk.
2. Repeat for Config B. Note that `ssl = false` uses different syntax than SSH, discuss why a
   rule engine must handle multiple config formats.
3. Compare Config A and Config C. List every change and explain why each change reduces attack
   surface. Identify which changes are "must fix" vs. "nice to have."
4. Open the simulation and work through the auditor simulation, reaching the target score.

## Collaborate (AP skill 4)
Assign roles: one partner is the "AI auditor" (reads each line, applies the rule set, emits
findings), the other is the "security engineer" (reviews each finding and decides: fix, document
as exception, or dismiss with justification). Swap roles between configs.

## Exit ticket
Each student submits: one insecure directive from today's configs + the corrected setting +
a one-sentence explanation of why the original was dangerous.

## Instructor notes
- Expected flags for Config A: PermitRootLogin yes, PasswordAuthentication yes, X11Forwarding yes.
- Expected flag for Config B: ssl = false (maps to insecure:SSLDisabled rule).
- Config C should produce zero findings, students should notice ALL changes from A.
- Common stumble: students flag `AllowTcpForwarding yes`, it is a legitimate security concern
  (can tunnel traffic through SSH), but it is not in the rule set for this skill. Discuss how rule
  sets are curated and never exhaustive.
- Feeds the unit project (hardened server config) and scenario stage where an AI audit catches a
  misconfiguration that enabled the attacker's initial foothold.
