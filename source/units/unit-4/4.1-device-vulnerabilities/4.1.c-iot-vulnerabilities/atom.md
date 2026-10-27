# 4.1.c, IoT device vulnerabilities

> **Unit 4 · 4.1 Device Vulnerabilities and Attacks**
> **AP Learning Objective(s):** 4.1.A, 4.1.C
> **Course skill(s):** Analyze Risk

## Learning objective (student-facing)
Explain why Internet of Things (IoT) devices carry unusually high
risk, identify the specific vulnerability categories that make them easy targets, and classify a
described smart device by its dominant weakness.

## Lesson
The Internet of Things (IoT) is the broad category of everyday physical devices, cameras,
routers, thermostats, door locks, baby monitors, medical sensors, industrial controllers, that
connect to a network and, usually, to the internet. There are tens of billions of these devices
in use worldwide, and from a security standpoint they are collectively the softest target on the
modern network. Understanding *why* IoT devices are so weak, not just memorizing the list of
weaknesses, is what lets you reason about risk in a device you have never seen before.

**Weak or default credentials.** Many IoT devices ship from the factory with a built-in username
and password, `admin`/`admin`, `root`/`12345`, or nothing at all, intended for initial setup.
Manufacturers assume the owner will change it. Most owners never do, because the device has no
screen, no obvious settings menu, or the owner does not think of a light bulb as a computer that
needs a password. Attackers know this. Automated scanners try well-known default credential lists
against every IP address on the internet and log in successfully within seconds wherever the
default was never changed.

**Unpatched, hard-to-update firmware.** Firmware is the low-level software baked into a device
that controls how it operates. Unlike a phone or laptop, most IoT devices have no automatic update
mechanism, and many manufacturers stop supporting a device (it becomes end-of-life, or EOL) within
a year or two of release. A vulnerability discovered in the firmware may never be patched, and the
device keeps running the flawed code for its entire operational life, often five or ten years for
things like security cameras or industrial sensors.

**Exposed management interfaces and open ports.** To make setup convenient, many devices expose an
administrative interface over an old, insecure protocol. Telnet (a plaintext remote-login protocol
on port 23) and UPnP (Universal Plug and Play, a protocol that lets devices automatically open
ports on a router) are classic offenders. UPnP in particular can silently punch a hole through a
home firewall, exposing a device's management interface directly to the internet without the
owner's knowledge. Any open, unauthenticated management port is a direct invitation.

**Insecure cloud APIs and unencrypted traffic.** Most IoT devices talk to a cloud service to
enable the mobile app that controls them. If that API does not properly authenticate requests, an
attacker can control or query devices belonging to other users. If the device does not encrypt its
traffic (no TLS), anyone on the same network segment, a coffee-shop Wi-Fi, a compromised router, can read or alter the data in transit, including credentials.

**Physical accessibility.** Unlike a server in a locked data center, IoT devices are frequently
installed in publicly accessible or semi-public locations: a doorbell camera on an exterior wall,
a smart thermostat in a shared hallway, a sensor in a parking garage. Physical access often allows
an attacker to extract firmware directly from a chip, reset the device, or attach a debug
interface, bypassing network defenses entirely.

**Botnets: the aggregate risk.** Any single insecure smart plug seems low-stakes. The real danger
is scale: an attacker who can compromise the same vulnerability across thousands or millions of
identical devices gains a botnet, a network of hijacked devices that can be commanded together.
The 2016 Mirai botnet is the canonical example: it scanned the internet for IoT devices still using
factory default Telnet credentials, logged in, and enlisted each one. Mirai grew to hundreds of
thousands of devices and used them to launch some of the largest distributed denial-of-service
(DDoS) attacks ever recorded, briefly taking down major internet services. No single device was
"important," but the aggregate was devastating. This is why security teams increasingly worry
about **shadow IoT**, devices connected to a network that IT never approved, inventoried, or
secured, expanding the attack surface (the total set of points an attacker could exploit) without
anyone tracking it.

**Putting it together.** When you evaluate an IoT device's risk, work through the categories in
priority order: does it still use a default password? Is the firmware current, or is the device
EOL? Are unnecessary ports or protocols (Telnet, UPnP) exposed? Does its API require
authentication? Is its traffic encrypted? A device can fail more than one check at once, and the
most severe issue usually dominates the practical risk. The simulation in the simulation has you audit
a list of smart devices and flag each one's primary vulnerability, and the coding problem in
`problem/` asks you to formalize that same triage logic as a function.

## Key terms
- **IoT (Internet of Things)**, everyday physical devices that connect to a network/internet
  (cameras, sensors, appliances, controllers) beyond traditional computers and phones.
- **Default credentials**, the factory-set username/password shipped on a device, often never
  changed by the owner, and widely known/scanned for by attackers.
- **Firmware**, the low-level software embedded in a device that controls its core operation;
  often lacks an automatic update mechanism on IoT hardware.
- **Attack surface**, the complete set of points where an attacker could try to get into or
  extract data from a system; more exposed devices/services/ports means a larger attack surface.
- **Botnet**, a network of compromised devices remotely controlled by an attacker as a group,
  often used for large-scale DDoS attacks.
- **Mirai**, a 2016 botnet malware that hijacked IoT devices via default Telnet credentials and
  launched record-setting DDoS attacks; the canonical real-world IoT botnet example.
- **UPnP (Universal Plug and Play)**, a protocol that lets devices automatically open ports on a
  router, which can unintentionally expose management interfaces to the internet.
- **Shadow IoT**, devices connected to a network without IT's knowledge, approval, or security
  oversight, silently expanding the attack surface.
- **EOL (end-of-life) device**, a device whose manufacturer has stopped issuing updates or
  support, leaving any undiscovered or unpatched vulnerabilities permanently exploitable.

## Common misconceptions
- "IoT devices are too small or simple to be worth attacking." → False. Attackers rarely care
  about the device itself; they want it as a botnet node, a pivot point into the rest of the
  network, or a source of sensitive data (camera feeds, sensor logs). Scale, not sophistication,
  is what makes IoT attractive.
- "If a device isn't connected to the internet, it's safe." → A device on a local network can
  still be reached by anything else already on that network (a compromised laptop, a malicious
  guest device), and many "local-only" devices still phone home to a cloud API. Network placement
  reduces but does not eliminate risk.
- "Changing the Wi-Fi password protects every device on the network." → A Wi-Fi password
  controls who can join the network, not whether devices on that network trust each other. A
  device with default admin credentials or an exposed Telnet port is just as exploitable by
  another device already inside the network (or through UPnP-punched holes from outside it).

## Try it
- **Simulation:** Audit a list of smart devices and correctly
  flag each device's vulnerability status, reaching the target score.
- **Coding problem:** Implement a function that inspects a device's attributes and
  returns its primary security verdict.
- **Quiz:** self-check on the skill's key ideas.

## Sources (local / vendor / rebuilt)
- Deep: Open Security Training (IoT/embedded security fundamentals module), rebuilt as original
  prose above; see `vendor/web/open-security-training/` notes.
- Reference: GeeksforGeeks (IoT security / vulnerabilities overview), cross-checked for accuracy.
- Practice: Cybrary IoT security awareness micro-challenges, rebuilt locally as the simulation.
- Repo: her0marodeur/awesome-free-cybersecurity → `vendor/repos/her0marodeur-awesome-free-cybersecurity`.
