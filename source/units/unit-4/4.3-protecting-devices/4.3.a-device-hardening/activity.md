# In-class activity, 4.3.a Device hardening

**Format:** pairs · **Time:** 25 min · **Offline:** yes

## Goal
Students apply a device-hardening checklist to a fictional device configuration, identify which
controls are missing, and justify each finding using the principle of least privilege and attack
surface reduction. Ties to LO 4.3.A (explain and apply hardening controls).

## Materials (all local)
- the SimLab simulation on each machine, or the printed device-configuration card below.
- Printed or on-screen hardening checklist (the five controls used in the simulation).

## Steps
1. Each pair opens the simulation and works through the device-configuration scenarios. Before
   submitting each answer they must agree and write one sentence explaining *why* that control
   reduces risk.
2. After the simulation, each pair reviews the configuration card below and identifies which of
   the five hardening controls the fictional device fails. They record their findings in a table:
   Control | Pass/Fail | Reason.
3. Pairs swap their findings table with another pair, who must either agree or rebut each finding
   with a justification.

### Fictional device configuration card (Meridian Technologies, Workstation WS-04)
```
OS: Windows 10 (installed 18 months ago, no updates applied)
Local accounts: Administrator (password: admin), Guest (enabled, password: none)
Services running: FTP server, Telnet, Remote Desktop, HTTP server, Print spooler
Firewall: disabled
Disk encryption: off
Screen lock timeout: never
```

## Collaborate (AP skill 4)
Assign roles: one partner is the "security auditor" (identifies failures and writes the finding),
the other is the "device owner" (tries to justify why the current setting might seem reasonable).
The auditor must respond to each defense with a concrete attack scenario that the control would
prevent. Swap roles after finding three issues.

## Exit ticket
Each student submits a ranked list of the three most critical controls the fictional device is
missing, with one sentence each explaining the specific risk that control addresses.

## Instructor notes
- Expected findings: default credentials (Administrator/admin, Guest enabled), unneeded services
  (FTP, Telnet, HTTP server all unnecessary for a workstation), firewall disabled, disk encryption
  off, no screen lock.
- Common stumble: students treat all missing controls as equally important. Guide them to rank by
  likely exploitation path, default credentials and disabled firewall are typically highest risk.
- Feeds the unit project (device security audit) and scenario stage 3 (attacker pivots from
  hardened network to poorly configured workstation).
