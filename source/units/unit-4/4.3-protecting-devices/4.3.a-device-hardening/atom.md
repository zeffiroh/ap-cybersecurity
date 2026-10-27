# 4.3.a, Device hardening

> **Unit 4 · 4.3 Protecting Devices**
> **AP Learning Objective(s):** 4.3.A
> **Course skill(s):** Mitigate Risk

## Learning objective (student-facing)
Describe the core device-hardening controls, apply a hardening
checklist to a sample configuration, and explain why reducing a device's attack surface lowers
organizational risk.

## Lesson
Every device shipped from the factory arrives with a default configuration designed to maximize
compatibility and ease of setup, not security. Default administrator passwords are identical
across thousands of units. Unneeded services run because the manufacturer assumed the buyer might
want them. Remote-management ports are open so technicians can connect easily. File sharing is
enabled. Diagnostic interfaces are active. Each of these defaults is a potential door an attacker
can walk through.

**Device hardening** is the systematic process of closing those unnecessary doors before a device
is deployed, and periodically re-closing them as configurations drift. The goal is to reduce the
device's attack surface: the set of all ways an attacker could interact with it to cause harm.

### Why hardening matters
A device that has never been hardened is not simply "unsecured", it is actively broadcasting
invitations. Attackers use automated scanners to find machines running known-vulnerable default
services within minutes of them coming online. Real-world compromises frequently begin not with
a sophisticated exploit but with an attacker logging in as "admin" with password "admin" —
because no one changed the factory default. The 2016 Mirai botnet, which caused large-scale
internet outages, was built almost entirely from IoT devices still running factory credentials.

Hardening does not make a device perfectly impenetrable. It shrinks the target, forces attackers
to use harder and noisier techniques, and buys defenders more time to detect and respond.

### The hardening checklist
Security frameworks (including CIS Benchmarks and NIST SP 800-70) decompose hardening into four
broad categories:

**1. Change defaults.**
The first and most important action is changing every default password to a unique, strong
credential. This applies to the operating system account, the firmware management interface (BIOS/
UEFI), any built-in web admin panel (routers, printers, cameras), and application service accounts.
Default credentials are publicly documented; there is no secrecy to rely on.

**2. Remove or disable what is not needed.**
Every software package, service, protocol, and open port that is not actively required by the
device's function is an unnecessary risk. An office workstation does not need a web server running.
A printer does not need Telnet enabled. A file server does not need Bluetooth. The concept of
removing unnecessary components is called reducing the attack surface. The key question for each
item is: "Does this device's legitimate business function require this?" If no, disable or remove it.

**3. Enable protective features.**
Modern operating systems and firmware include defenses that are often off by default because they
add friction. Enable host-based firewalls that block inbound connections on unused ports. Turn on
full-disk encryption (BitLocker, FileVault, LUKS) so stolen hardware does not yield readable data.
Enable automatic screen lock after inactivity. Enable Secure Boot to prevent unsigned code from
running during startup. These settings cost little effort to enable and significantly raise the cost
of attacks.

**4. Lock down accounts and privileges.**
Apply the principle of least privilege: each user account and service should hold only the
permissions it needs and nothing more. Disable built-in guest accounts. Rename or disable the
"Administrator" or "root" account where possible. Require that administrative tasks be performed
only through explicit privilege elevation (sudo, UAC) rather than running everything as root.
Create separate accounts for daily work versus administrative work.

### Configuration drift
A hardened device does not stay hardened forever. Administrators install new software, enable a
port "temporarily" for a project, or reset a setting during troubleshooting. Each change is a
potential re-opening of a closed door. Professional security programs address this with automated
configuration-management tools (Ansible, Puppet, Group Policy) that continuously compare the
device's live state against a known-good baseline and alert on or automatically correct deviations.
This process, checking the current configuration against a hardening baseline, is exactly what
the coding problem in this skill asks you to implement.

### Hardening in layers
Device hardening is one layer in a defense-in-depth architecture. Even a perfectly hardened device
can still be compromised if a user is tricked into running malicious software (covered in 4.3.b)
or if unpatched vulnerabilities are exploited (covered in 4.3.c). Hardening removes unnecessary
risk before those incidents happen; the other controls handle the residual risk that remains.

A useful mental model: a hardened device is like a building with locked doors, no unlabeled master
keys, and only the windows that are actually needed, versus a building where every door is
propped open and spare keys hang on a hook by the entrance.

## Key terms
- **Device hardening**, the process of systematically removing or disabling unnecessary features,
  services, and accounts to reduce a device's attack surface before deployment.
- **Attack surface**, the total set of points where an unauthorized user could attempt to interact
  with or exploit a system.
- **Default credentials**, factory-set usernames and passwords that are identical across many
  units of the same device model and are publicly known.
- **Principle of least privilege**, every account and process should operate with only the
  minimum permissions required for its legitimate function.
- **Configuration baseline**, a documented record of the approved secure state of a device,
  used as a reference to detect and correct drift.
- **Configuration drift**, the gradual accumulation of unauthorized or unintended changes to a
  device's configuration over time.

## Common misconceptions
- "Only servers need hardening." → Every device with a network connection, laptops, printers,
  phones, cameras, has an attack surface and must be hardened.
- "Changing the password is enough." → Changing the default password is the single most important
  first step, but a hardened device also disables unneeded services, enables protective features,
  and restricts account privileges.
- "Hardening is a one-time task." → Configuration drift means hardening must be monitored
  continuously; a hardened device today may have re-opened attack surfaces tomorrow.

## Try it
- **Simulation:** Score a simulated device configuration against
  a hardening checklist and identify which controls are missing.
- **Coding problem:** Implement a function that compares a device configuration
  dictionary against a hardening baseline and returns the list of failing controls.
- **Quiz:** self-check on the skill's key ideas.

## Sources (local / vendor / rebuilt)
- Deep: NIST SP 800-70 (National Checklist Program), rebuilt as original prose above.
- Reference: GeeksforGeeks (system hardening overview), rebuilt locally.
- Practice: Cybrary (hardening micro-challenges), rebuilt locally as the simulation.
- Repo: LetsDefend/Free-Cybersecurity-Resources → `vendor/repos/letsdefend-free-cybersecurity`.
