# 1.3.d, War driving; protecting yourself (verify SSIDs, avoid open networks, VPN)

> **Unit 1 · 1.3 The Dangers of Public Wi-Fi**
> **AP Learning Objective(s):** 1.3.B, 1.3.C
> **Course skill(s):** Mitigate Risk

## Learning objective (student-facing)
Explain what war driving is and why it enables targeted
wireless attacks, evaluate a Wi-Fi network against a set of risk criteria, and apply a
systematic risk-flagging process to decide whether connecting is safe.

## Lesson
**War driving** is the practice of driving or walking through a geographic area with a
laptop, smartphone, or dedicated wireless scanner to discover, log, and map Wi-Fi networks.
The term dates to the early 2000s, when attackers would drive through business districts
with directional antennas to find corporate networks with no security, a practice made
famous by the 2001 film *Antitrust* and subsequent security conference demonstrations. Today,
the equipment required has shrunk to a smartphone running a scanning app, but the fundamental
practice and its implications for defenders remain unchanged.

**Why war driving matters.** A war driver builds a database of networks: their SSIDs,
BSSIDs, security types, GPS coordinates, and signal strengths. This database has several
uses. Legitimate uses include academic Wi-Fi research and coverage planning. Malicious uses
include identifying targets for follow-on attacks: open networks that can be joined without
a password, networks with weak or legacy security (WEP, which was broken in 2005), networks
whose SSIDs reveal organizational or personal details, and networks that can be reached from
a public space such as a parking lot.

A war driver who discovers a corporate network broadcasting from a parking lot, using WEP
security, with an SSID that reveals the company name, has all the information needed to plan
an intrusion. They can park outside, crack the WEP key in minutes using freely available
tools, and join the network as if they were an authorized employee.

**What makes a network risky from a user's perspective.** Even as a user connecting to a
network rather than an attacker scanning them, you face analogous risks. When you sit in a
cafe or airport and open your device's Wi-Fi list, you are performing your own informal scan.
The networks you see carry risk signals that you can evaluate:

- **Open network (no security):** any device can join; all traffic is unencrypted at the
  Wi-Fi layer. Anyone on the same network can passively capture your unencrypted traffic.
- **Unverified SSID:** you see a network named "AirportFreeWifi" but you have not confirmed
  with venue staff that this is the correct SSID. It may be an evil twin (see 1.3.b) or
  simply a different network with a similar name.
- **No VPN:** even on a legitimate, encrypted network, the access point operator can observe
  your DNS queries and unencrypted traffic. If the network is open, any co-joined user can.
  A VPN encrypts your traffic before it leaves your device, so neither the network operator
  nor other users can read it.

**The three-step personal protocol.** The coding problem in this skill implements a
risk-assessment function that applies exactly the checks above. But as a mental model, the
protocol is:

1. **Verify the SSID.** Ask venue staff for the correct network name before connecting.
   Do not guess based on what sounds plausible. If you cannot verify, treat the network as
   unverified.
2. **Avoid open networks** for any sensitive activity. If the only available network is open,
   use your phone's cellular data or tether from it instead. If you must use an open network,
   use a VPN.
3. **Always use a VPN** when connecting to public Wi-Fi, including networks that appear
   legitimate. A VPN gives you an encrypted tunnel to a trusted exit point regardless of what
   the local network does. This mitigates both passive interception and active MitM attacks.

**Why these three steps are ordered.** Verifying the SSID comes first because connecting to
the wrong network (an evil twin or an unrelated network) makes all subsequent protections
less effective, you are giving your traffic to an adversary before your VPN even initializes.
Avoiding open networks comes second because even a brief unencrypted connection before the
VPN tunnel is established can leak credentials or session tokens. The VPN comes third as the
defense-in-depth layer that protects you even when the first two steps are imperfect.

**Institutional context.** Organizations often publish an approved network list and require
employees to use a corporate VPN whenever working outside the office. This policy
operationalizes exactly the personal protocol above at scale. The risk-assessment logic in
the coding problem models what a network-policy enforcement tool would do: given a network's
properties, determine which risk flags apply and report them in a consistent, sorted format
so the user or administrator can make an informed decision.

**Common attacker exploitation of war-driving data.** Beyond the direct-attack use, war-driving
databases are sometimes used to support social engineering: an attacker who knows your
organization's SSID from a public war-driving database can use that name in a phishing email
("Your corporate Wi-Fi password expires tomorrow, click here to renew") with higher
plausibility. The intersection of physical-layer reconnaissance and social engineering is a
recurring theme in advanced attacks.

## Key terms
- **War driving**, moving through a geographic area with a wireless scanner to discover and log Wi-Fi networks; used in legitimate research and as an attack-planning technique.
- **Open network**, a Wi-Fi network requiring no password; all traffic is unencrypted at the wireless layer, visible to any device that joins or captures the channel.
- **VPN (Virtual Private Network)**, software that creates an encrypted tunnel from your device to a trusted server before your traffic reaches the internet; protects against interception on hostile networks.
- **SSID verification**, confirming the correct network name with venue staff or an official source before connecting, to avoid accidentally joining an evil twin or lookalike network.
- **Risk flag**, a specific, nameable property of a network that raises the probability of interception or attack (e.g., "open-network", "unverified-ssid", "no-vpn").

## Common misconceptions
- "A password-protected network means I am safe." → WPA2 encrypts the air interface, but the access point operator can still read unencrypted traffic, and a compromised or malicious AP can intercept HTTPS via SSL stripping. A VPN provides an additional layer.
- "I can tell if a network is legitimate by its name." → SSIDs are trivially spoofed. Only direct verification with venue staff is reliable.
- "War driving is only done by sophisticated attackers." → Modern war-driving apps run on smartphones and require no technical skill; the barrier to reconnaissance is extremely low.

## Try it
- **Simulation:** Assess a sequence of networks against the three risk criteria and produce the correct flag list before connecting.
- **Coding problem:** Implement `solve(network: dict) -> list[str]` that returns sorted risk flags for a given network description.
- **Quiz:** self-check on the skill's key ideas.

## Sources (local / vendor / rebuilt)
- Deep: NIST SP 800-153 (wireless network guidelines), rebuilt as original prose above; see `vendor/web/nist/`.
- Reference: FCC consumer guidance on public Wi-Fi, `vendor/web/fcc/`.
- Practice: Cybrary wireless security awareness module, rebuilt locally as the simulation.
- Repo: CSIRT-MU/edu-resources, `vendor/repos/csirt-mu-edu-resources`.
