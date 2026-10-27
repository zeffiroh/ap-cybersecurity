# 1.5.a, AI reviewing security configurations

> **Unit 1 · 1.5 Leveraging AI in Cyber Defense**
> **AP Learning Objective(s):** 1.5.A
> **Course skill(s):** Mitigate Risk, Collaborate

## Learning objective (student-facing)
Describe how AI-assisted tools audit security configuration files
for common misconfigurations, identify specific insecure settings in a sample config, and explain
why automated review catches issues that manual checklists often miss.

## Lesson
Every server, network device, and cloud service is controlled by a configuration file, a plain-text
document that specifies exactly how the system behaves. Get that file right and you have a hardened
system. Get it wrong and you have an open door. Historically, reviewing configuration files was a
slow, error-prone manual task performed by experienced engineers who had to memorize long checklists
of insecure defaults. Today, AI-assisted tools automate this review, scanning thousands of lines in
seconds and flagging exactly which settings violate security best practices.

**Why configurations matter so much.** Every service ships with default settings tuned for
convenience, not security. OpenSSH's default configuration, for example, historically allowed the
root user to log in directly over the network (`PermitRootLogin yes`), a gift to attackers who only
need to crack one account to own the entire machine. Password-based authentication over SSH
(`PasswordAuthentication yes`) exposes the system to brute-force attacks. Web servers default to
advertising their version string, helping attackers match known exploits. Databases bind to all
network interfaces instead of localhost. These defaults exist because vendors ship general-purpose
software; tightening them for each deployment is the operator's job, and operators make mistakes.

**What AI config review actually does.** An AI-powered configuration auditor reads a config file
and compares each directive against a rule database encoding thousands of known-bad settings. The
simplest version is a rule engine: if `PermitRootLogin` is set to anything other than `no`,
emit a finding. More sophisticated ML-based tools go further, they model the entire configuration
as a graph of interdependent settings and flag combinations that are individually acceptable but
dangerous together (for example, allowing password auth *and* disabling login attempt limits).

For the AP course, focus on the rule-engine layer, which is transparent, auditable, and teaches the
underlying security principle for each rule. Consider an SSH configuration file:

```
Port 22
PermitRootLogin yes
PasswordAuthentication yes
X11Forwarding yes
```

A rule engine would flag `PermitRootLogin yes` (direct root access), `PasswordAuthentication yes`
(enables brute force), and `X11Forwarding yes` (unnecessary attack surface). It would *not* flag
`Port 22` since running SSH on the standard port, while debated, is not itself insecure. This
precision matters: alert fatigue from false positives causes operators to dismiss real findings.

Other classic insecure patterns span many protocols: `ssl false` or `TLS off` in database or
messaging configs disables encryption in transit; `Port 23` means Telnet rather than SSH, Telnet
transmits credentials in cleartext. When the AI flags these, it also explains *why* they are
dangerous, making the output educational, not just a list of red dots.

**The human-AI collaboration model.** AI config review does not replace human judgment, it
accelerates it. The tool handles the mechanical layer (did this directive match a bad-practice
rule?), freeing the security engineer to focus on the contextual layer (does this organization have
a compensating control? Is this an intentional exception that needs documentation?). This is the
"Collaborate" skill in action: the human provides organizational context; the AI provides exhaustive
pattern matching across the entire file.

**Where this fits in the security lifecycle.** Configuration review fits into two stages:
*before deployment* (shift-left security, catching misconfigurations in a pull request before the
server goes live) and *on a schedule* (continuous compliance, re-checking configs after every
change). Some organizations run config auditors as part of CI/CD pipelines, blocking a deployment
if a critical misconfiguration is introduced. This is how AI makes the process not just faster but
continuous, no misconfiguration survives more than a commit cycle.

**Scope and limits.** AI config review excels at finding known-bad patterns but cannot detect
*contextually wrong* settings, a setting that is fine for a public-facing service but wrong for an
internal one. It also cannot assess intent: if a developer deliberately opened a port for debugging
and documented it, the tool will still flag it. This is why AI review outputs a *finding*, not a
*verdict*. A human closes the loop.

The coding problem in this skill builds a simplified config auditor: given a list of configuration
lines, return the set of offending line markers based on a fixed rule set. Working through it
concretely anchors the abstract idea of "AI reviewing configs" to a deterministic, auditable
algorithm.

## Key terms
- **Configuration file**, a plain-text file specifying system behavior; the primary control
  surface for hardening.
- **Misconfiguration**, a setting that deviates from security best practice, intentionally or not.
- **Rule engine**, a component that checks each config directive against a database of known-bad
  patterns and emits findings.
- **PermitRootLogin**, SSH directive controlling whether the root account can authenticate
  directly; should be `no` on any production system.
- **Hardening**, the process of reducing a system's attack surface by disabling unnecessary
  services and correcting insecure defaults.
- **Shift-left security**, moving security checks earlier in the development cycle, catching
  issues before they reach production.

## Common misconceptions
- "Default settings are safe because the vendor tested them." → Defaults are tuned for
  compatibility and ease of setup, not for security. Hardening requires deliberate reconfiguration.
- "Flagging a setting means it must be changed." → A finding is a question, not a command. The
  human reviewer decides whether a compensating control or documented exception is acceptable.
- "AI config review replaces a security engineer." → It replaces the mechanical checklist step,
  not the judgment step. The engineer still interprets context, approves exceptions, and owns the
  outcome.

## Try it
- **Simulation:** Act as an AI config auditor, read each
  config file presented, select which lines are insecure, and reach the target score.
- **Coding problem:** Implement `solve(config_lines)` that returns sorted offending
  line markers for a given SSH/service config.
- **Quiz:** self-check on the skill's key ideas.

## Sources (local / vendor / rebuilt)
- Deep: MIT OCW (security engineering, configuration management), rebuilt as original prose above.
- Reference: GeeksforGeeks (SSH hardening, common misconfigurations).
- Practice: Cybrary / LetsDefend config-audit modules, rebuilt locally as the simulation.
- Repo: LetsDefend/Free-Cybersecurity-Resources → `vendor/repos/letsdefend-free-cybersecurity-resources`.
