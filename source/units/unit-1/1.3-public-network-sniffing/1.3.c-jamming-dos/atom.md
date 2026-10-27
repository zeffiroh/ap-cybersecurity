# 1.3.c, Jamming / denial-of-service attack

> **Unit 1 · 1.3 The Dangers of Public Wi-Fi**
> **AP Learning Objective(s):** 1.3.B
> **Course skill(s):** Analyze Risk

## Learning objective (student-facing)
Explain how radio-frequency jamming causes a wireless
denial-of-service, describe what a sustained jamming event looks like in signal-strength
monitoring data, and implement a detector that flags sustained interference in a sample series.

## Lesson
Every Wi-Fi access point communicates by broadcasting radio waves on a shared spectrum.
The 2.4 GHz and 5 GHz bands used by Wi-Fi are unlicensed, meaning any device is legally
allowed to transmit on them, subject to power limits set by the FCC or equivalent regulator.
This openness is a deliberate design choice that made Wi-Fi affordable and widespread, but it
also means an adversary can intentionally flood the spectrum with noise to prevent legitimate
communication. That attack is called **radio-frequency (RF) jamming**, and its effect on the
network is a **denial-of-service (DoS)**, users are prevented from accessing the network not
because they have been blocked by a firewall or authentication failure, but because the
underlying medium has been rendered unusable.

**How jamming works.** A Wi-Fi radio uses a technique called CSMA/CA (Carrier Sense Multiple
Access with Collision Avoidance): before transmitting, a device listens for other traffic on
the channel. If it hears noise, either legitimate traffic or deliberate interference, it
backs off and waits. A jammer exploits this courtesy: by continuously emitting noise at a
level above the ambient threshold, it forces every legitimate device on that channel to back
off indefinitely. Even a low-power jammer placed near an AP can render a channel unusable for
devices in its vicinity while consuming almost no resources for the attacker.

**Jamming versus interference.** Not all high-noise readings are attacks. Interference from
microwave ovens, baby monitors, Bluetooth devices, and neighboring Wi-Fi networks causes
transient noise on the 2.4 GHz band. The distinguishing characteristic of a jamming attack is
**sustained, high-level noise over multiple consecutive samples**. An isolated spike from a
microwave running for a few seconds is transient. A jammer that runs for minutes produces a
prolonged plateau of elevated noise, the kind that coincides with an operational event such
as an exam, a court proceeding, or a targeted intrusion support operation.

**Signal strength versus noise floor.** In wireless monitoring, the relevant metric is the
**received signal strength indicator (RSSI)**, measured in dBm. This value is always negative:
-30 dBm is a very strong signal (very close to the AP), -90 dBm is weak. A network adapter
also measures the **noise floor**, background radio energy on the channel, and the usable
signal is the difference between the two (the signal-to-noise ratio, SNR). A jammer raises
the noise floor, shrinking the SNR even if the AP's transmit power is unchanged. Monitoring
tools surface this as an anomalously high noise reading. In the simplified model used by the
coding problem, a noise-floor sample is an integer (the raw noise measurement in a synthetic
unit): values above a detection threshold, maintained over at least a minimum number of
consecutive samples, indicate a sustained jamming event.

**Legal context and real-world use.** Jamming devices are illegal for civilian use in most
jurisdictions, in the United States, the FCC explicitly prohibits the sale, import, or
operation of jammers under 47 U.S.C. 333. Despite this, jammers are available and are used
in targeted attacks against conference venues, examination halls, and occasionally in support
of physical security breaches where the attacker wants to disrupt wireless alarm systems or
security cameras during entry. Detection is the practical countermeasure available to
defenders who cannot prevent the attack outright.

**Detection approach.** The simplest effective detection rule is a **consecutive-sample
threshold**: if the noise measurement exceeds a defined threshold (T) for at least N
consecutive samples, declare a jamming event. This is the rule implemented in the coding
problem: `solve(samples: list[int]) -> bool`. The threshold and window size are defined in
`interface.md`. The simulation (the simulation) lets you watch a live noise-floor plot and
toggle a jammer on and off to see how the signal-monitor responds.

**Defenses.** Against a physically present jammer, a network defender's options include:
moving to a different frequency channel (a jammer targeting one channel may not cover others);
switching from 2.4 GHz to 5 GHz or 6 GHz, which have more channels and shorter range; using
directional antennas to improve SNR; and alerting venue security to locate and remove the
device. The 802.11w standard (Management Frame Protection) does not prevent RF jamming but
does protect against deauthentication-based software DoS attacks, which are a related but
distinct threat. The WIDS (wireless intrusion detection system) discussed in atom 1.3.b can
also be configured to alert on sustained noise-floor anomalies.

Understanding jamming matters beyond the specific attack itself: the same detection logic, sustained anomaly above a threshold for a minimum duration, underlies many network and
host-based intrusion detection systems. Jamming is a concrete, physical example that makes the
abstract principle tangible.

## Key terms
- **Jamming**, deliberate transmission of radio-frequency noise to prevent legitimate wireless communication on a channel.
- **Denial-of-service (DoS)**, an attack that makes a resource unavailable to legitimate users without necessarily compromising data.
- **RSSI (Received Signal Strength Indicator)**, a measurement of the power level of a received radio signal, expressed in dBm (always negative for Wi-Fi).
- **Noise floor**, the level of background radio noise on a channel; jamming raises this, reducing the usable signal-to-noise ratio.
- **CSMA/CA (Carrier Sense Multiple Access with Collision Avoidance)**, the access-control protocol Wi-Fi uses; devices back off when they detect noise, making them vulnerable to deliberate jamming.
- **Sustained anomaly**, a condition maintained across multiple consecutive measurement samples, distinguishing attacks from transient interference.

## Common misconceptions
- "High noise always means jamming." → Transient interference from household devices is common on 2.4 GHz. A jamming attack is characterized by *sustained*, not momentary, elevated noise across several consecutive samples.
- "Jamming is only a problem for military networks." → Civilian Wi-Fi is equally vulnerable; jammers are used in corporate espionage, exam-hall cheating, and as a physical-intrusion aid.
- "Switching channels defeats a jammer." → It can help if the jammer targets a specific channel, but wideband jammers can cover all 2.4 GHz channels simultaneously.

## Try it
- **Simulation:** Observe the noise-floor monitor, toggle the simulated jammer, and correctly identify whether each sample series represents a jamming event.
- **Coding problem:** Implement `solve(samples: list[int]) -> bool` that returns `True` when at least N consecutive samples exceed threshold T.
- **Quiz:** self-check on the skill's key ideas.

## Sources (local / vendor / rebuilt)
- Deep: NIST SP 800-153 (wireless network security guidelines), rebuilt as original prose above; see `vendor/web/nist/`.
- Reference: FCC Part 15 regulations (unlicensed spectrum rules), `vendor/web/fcc/`.
- Practice: Open Security Training (wireless attacks module), rebuilt locally as the simulation.
- Repo: CSIRT-MU/edu-resources, `vendor/repos/csirt-mu-edu-resources`.
