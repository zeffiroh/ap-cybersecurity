# 1.3.a, Adversary skill levels (low-skilled vs high-skilled / zero-days); motivation

> **Unit 1 · 1.3 The Dangers of Public Wi-Fi**
> **AP Learning Objective(s):** 1.3.A
> **Course skill(s):** Analyze Risk

## Learning objective (student-facing)
Classify a wireless attacker by skill tier based on the tools and
techniques they use, and explain how motivation shapes which public Wi-Fi threats you face in practice.

## Lesson
Not every attacker who shows up in a coffee shop with a laptop is equally dangerous. Understanding
the spectrum of adversary capability, from the curious teenager running a downloaded script to the
nation-state operator wielding a custom radio exploit, helps you calibrate risk realistically rather
than either dismissing it or treating every threat as equally catastrophic.

**The skill spectrum.** Cybersecurity practitioners broadly group attackers into two tiers that map
to observable behavior.

A **low-skilled adversary** (sometimes called a "script kiddie") uses existing, publicly available
tools without understanding the underlying mechanics. They download a packet-capture app, run an
evil-twin script they found online, or run an automated Wi-Fi scanner without writing any code
themselves. Their attacks are largely opportunistic: they sit somewhere public, run a tool, and wait
for victims to make mistakes. The barrier to entry here is almost zero, a $30 USB Wi-Fi adapter
and a free Linux live-USB get a novice off the ground. What low-skilled attackers lack in depth
they make up for in volume; millions of potential low-skilled actors exist worldwide, so statistically
you are far more likely to encounter one of them than a sophisticated operator.

A **high-skilled adversary** writes or modifies their own tools, understands the full protocol
stack, and can adapt when defenses push back. At the extreme end, this tier develops or purchases
**zero-day vulnerabilities**, security flaws that the vendor has not yet discovered or patched
(hence zero days of warning). A zero-day in a wireless driver or a Wi-Fi chipset firmware can
allow an attacker to compromise a device before it has even finished connecting, with no action
required from the victim. High-skilled adversaries may also combine wireless access with other
attack stages: they gain initial entry on a public network, then pivot to the target's cloud
accounts, corporate VPN, or personal banking. Nation-states and advanced criminal groups operate
at this tier.

**Why skill tier matters for you.** The level of effort required from the attacker determines how
broadly they can strike. Low-skilled attacks are cheap, so they sweep widely, the attacker targets
anyone reachable. High-skilled attacks are expensive, so they are aimed precisely at high-value
targets: executives, government employees, journalists, software engineers with access to sensitive
code repositories. If you handle sensitive information, you face the full range. If you are an
ordinary student on a coffee-shop network, the realistic threat is almost certainly in the
low-skilled tier, but that is still a real threat, because those tools work.

**Motivation shapes behavior.** Attackers do not act randomly; they have goals, and those goals
predict their methods.

- **Financial gain.** The most common motivation. Attackers harvest credentials, session cookies,
  or credit card numbers for resale on underground markets. Financial attackers tend to seek
  scale, compromise as many victims as possible per hour of work.
- **Espionage.** Corporate or government spies seek specific information: trade secrets, source
  code, personnel files, negotiating positions. They are patient and selective; they may set up a
  rogue access point near a single conference room at a company's headquarters.
- **Disruption / denial of service.** Some attackers want to prevent access, not steal data. A
  disgruntled former employee, activist, or rival might jam or flood a wireless network to disrupt
  a business or event.
- **Curiosity / learning.** Some intrusions have no economic goal, the attacker is testing
  whether they can. These actors often stop short of harm but still expose victim data.

**The public Wi-Fi context.** A public network removes the primary line of defense most people
rely on without knowing it: the trust boundary of a private network. On your home Wi-Fi you
implicitly trust every device. On a coffee-shop network, every connected device is a potential
adversary. A low-skilled attacker at the next table can passively capture unencrypted traffic with
free tools in minutes. A high-skilled one can insert themselves between your device and the
legitimate access point, recording or modifying every byte you transmit, without appearing
different from the real network in any way visible to you.

The coding problem for this skill asks you to implement a classifier that reads a
description of an attacker's toolset and techniques and assigns them to the correct skill tier. The
simulation (the simulation) presents adversary profiles that you must sort into tiers before time runs
out. Both reinforce a core AP analytic skill: extracting security-relevant features from a
description and drawing a defensible conclusion.

**The key takeaway:** Public Wi-Fi changes your threat environment, not just the speed of your
internet. The risk you face depends on who is nearby and what they want. Assessing adversary
skill and motivation is the first step in any risk analysis, because it determines both the
likelihood and severity of an attack.

## Key terms
- **Low-skilled adversary**, attacker who uses existing public tools without understanding the underlying mechanics; threat is broad but shallow.
- **High-skilled adversary**, attacker who creates or modifies tools, understands full protocol stacks, and can adapt; threat is precise and deep.
- **Zero-day vulnerability**, a security flaw unknown to the vendor, giving the defender zero days of advance warning; typically exploited only by high-skilled actors.
- **Motivation**, the attacker's goal (financial gain, espionage, disruption, curiosity) that shapes which targets and methods they choose.
- **Script kiddie**, informal term for a low-skilled attacker running tools they did not write and do not fully understand.

## Common misconceptions
- "Hackers on public Wi-Fi are all elite geniuses." → Most opportunistic attacks use free, widely available tools. The ceiling is high, but the floor is very low.
- "I have nothing worth stealing, so I am safe." → Low-skilled attackers often resell any captured credential in bulk; they do not prescreen victims.
- "Zero-days only matter to governments." → Zero-day exploits are bought and sold commercially and have been used against journalists, lawyers, and activists.

## Try it
- **Simulation:** Sort ten adversary profiles into the correct skill tier (low / high) before the timer expires, and justify each classification.
- **Coding problem:** Implement `solve(adversary: dict) -> str` that returns "low" or "high" based on the features of the adversary profile.
- **Quiz:** self-check on the skill's key ideas.

## Sources (local / vendor / rebuilt)
- Deep: Open Security Training (wireless security fundamentals), rebuilt as original prose above; see `vendor/web/opensecuritytraining/`.
- Reference: NIST SP 800-153 (Guidelines for Securing Wireless Networks), `vendor/web/nist/`.
- Practice: Wikiversity cybersecurity modules, rebuilt locally as the simulation.
- Repo: CSIRT-MU/edu-resources, `vendor/repos/csirt-mu-edu-resources`.
