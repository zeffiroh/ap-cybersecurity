# 2.3.d, Environmental controls (HVAC, fire suppression, power)

> **Unit 2 · 2.3 Protecting Physical Spaces**
> **AP Learning Objective(s):** 2.3.C
> **Course skill(s):** Mitigate Risk

## Learning objective (student-facing)
Explain how HVAC, fire suppression, and power systems protect
physical infrastructure and describe the alert thresholds that define safe operating ranges.

## Lesson

### Why the environment is part of cybersecurity

Physical hardware is the foundation of every digital system. A server does not care whether its
data was stolen by a hacker or destroyed because a room hit 50 degrees Celsius, the outcome is
the same: the data is gone and the service is unavailable. Environmental controls are the systems
that keep temperature, humidity, air quality, and electrical power within the narrow ranges that
hardware requires to operate reliably. When those controls fail, availability collapses. AP
Learning Objective 2.3.C asks you to mitigate risk to physical spaces; environmental controls are
a core part of that answer.

### HVAC: temperature and humidity

HVAC stands for Heating, Ventilation, and Air Conditioning. In a data center or server room the
goal is not human comfort, it is maintaining a stable environment for hardware. Industry guidance
(ASHRAE A1 class) sets the recommended server inlet air temperature between 18 degrees Celsius
and 27 degrees Celsius. Below 18 C, condensation risk increases and some mechanical parts
(spinning hard drives, older power supplies) can be stressed by cold. Above 27 C, transistor
leakage current rises, thermal throttling engages, and component lifespan drops sharply. Every
10-degree rise above the rated maximum roughly doubles the failure rate of electronic components.

Humidity matters as much as temperature. The safe band is roughly 40 to 60 percent relative
humidity. Too dry (below 20 percent) and electrostatic discharge (ESD) becomes a hazard: a spark
invisible to the human eye carries enough voltage to destroy a chip. Too humid (above 60 percent)
and condensation can form on cold surfaces, corroding circuit traces and shorting components.

#### Hot aisle / cold aisle containment

A large server room does not just "run the AC." Racks are arranged so that servers draw cool air
from a dedicated cold aisle (where raised-floor vents or overhead ducts deliver chilled air) and
exhaust hot air into a hot aisle behind them. Physical curtains, doors, or roof panels contain
each aisle so cool and hot air cannot mix. This doubles the efficiency of cooling: the HVAC unit
sees a higher return temperature and can run at greater efficiency, and the servers see a more
uniform inlet temperature. Without containment, hot spots form, and a single overheated rack can
cause correlated failures across many systems.

The simulation in the simulation shows a monitoring console that reports sensor readings for
temperature and humidity across multiple zones. Your task is to recognize which readings fall
outside the safe window, exactly the logic you will also implement in the coding problem.

### Fire suppression

A fire inside a data center is catastrophic, but so is a badly chosen suppression system. Water
sprinkler systems work but destroy electronics: even a false activation can write off an entire
server room. Modern data centers use clean-agent suppression systems. The most common is FM-200
(heptafluoropropane), a gas that suppresses fire by absorbing heat and interrupting the chemical
chain reaction of combustion. It leaves no residue, does not damage equipment, and dissipates
quickly. Other clean agents include NOVEC 1230 (a fluoroketone with lower global-warming
potential) and inert gas blends such as Inergen (a mix of nitrogen, argon, and carbon dioxide).

Clean-agent systems depend on sealed rooms. If a data center door is left open during a
discharge, the gas concentration drops below the suppression threshold and the fire continues.
Physical controls, door closers, gaskets, and cable-entry seals, are therefore part of the fire
suppression design, not separate from it.

Early-warning smoke detection (VESDA, Very Early Smoke Detection Apparatus) samples air
continuously and can detect smoke particles at concentrations far below what a standard ionization
detector triggers on. A VESDA system gives operators minutes of warning instead of seconds,
allowing orderly shutdown before suppression is needed.

### Power: UPS, generators, and PDUs

Electrical power is the most common environmental threat to availability. Problems include:

- **Blackout** (complete loss of utility power)
- **Brownout** (voltage sag, power is present but below nominal, causing instability)
- **Surge/spike** (momentary over-voltage that can destroy power supplies and motherboards)
- **Harmonics and noise** (distortion that causes errors in sensitive analog or storage circuits)

The standard mitigation stack has three layers:

1. **UPS (Uninterruptible Power Supply):** A battery bank that responds in milliseconds, faster than utility failover can operate. A UPS provides clean, regulated power during
   brief outages and bridges the gap until a generator starts. It also filters surges and
   brownouts before they reach the equipment.

2. **Generator:** A diesel or natural-gas generator provides extended runtime (hours to days)
   once it has started and stabilized, typically within 10 to 30 seconds. Critical facilities
   may have N+1 or 2N redundant generators so that a single generator failure does not drop
   the load.

3. **PDU (Power Distribution Unit):** A rack-mounted or room-level PDU distributes power from
   the UPS or generator to individual devices. Managed PDUs allow remote monitoring of per-outlet
   current and can remotely cycle power to a locked-up server, eliminating the need for a
   technician to enter the room for a routine reboot.

A facility without a UPS relies entirely on the utility, meaning a single momentary fault causes
an uncontrolled shutdown. Uncontrolled shutdowns are among the most common causes of filesystem
corruption and data loss even when the hardware itself survives intact.

### Monitoring and the alert lifecycle

Environmental monitoring systems poll sensors continuously and generate alerts when readings cross
thresholds. An operator who receives a HIGH_TEMP alert for a single sensor might investigate a
failing server fan. An operator who receives HIGH_TEMP alerts across an entire aisle suspects
HVAC failure and escalates to facilities. The coding problem in `problem/` asks you to implement
exactly this triage logic: given a list of raw sensor readings, produce a sorted list of alert
codes so that an operator can act on the right problem first.

### Connecting to availability

Environmental controls are a physical layer defense-in-depth measure. They do not prevent
intrusions, but they protect availability, one of the three pillars of the CIA triad. A threat
actor who understands a target facility's HVAC schedule might deliberately trigger a temperature
anomaly to cause a denial of service without ever touching a keyboard. Recognizing that
environmental systems are attack surfaces, not just maintenance concerns, is part of a mature
cybersecurity perspective.

## Key terms
- **HVAC**, Heating, Ventilation, and Air Conditioning; the system that maintains temperature and humidity within safe operating ranges for hardware.
- **Hot aisle / cold aisle**, A data center rack layout that separates cool intake air from hot exhaust air to maximize cooling efficiency and prevent hot spots.
- **Clean agent**, A gaseous fire suppressant (such as FM-200 or NOVEC 1230) that extinguishes fire without leaving residue or damaging electronic equipment.
- **UPS (Uninterruptible Power Supply)**, A battery-backed device that provides immediate clean power during outages or power quality events, bridging the gap until a generator starts.
- **PDU (Power Distribution Unit)**, A device that distributes electrical power to multiple rack components; managed PDUs support remote monitoring and outlet control.
- **VESDA**, Very Early Smoke Detection Apparatus; a system that continuously samples air and detects smoke at extremely low concentrations, providing early warning before a fire develops.
- **Brownout**, A condition where utility voltage drops below nominal, causing hardware instability without a full outage.

## Common misconceptions
- Sprinkler systems are fine for data centers -> Water damages electronics on contact and even a false activation can destroy an entire room; clean-agent suppression is the appropriate choice for most data center spaces.
- UPS units are only needed for long outages -> A UPS is most critical for the first few milliseconds to seconds of an outage, before a generator can start; it also filters everyday power quality problems that would otherwise cause silent corruption.
- Cold is always safer than warm for servers -> Temperatures below 15 C increase condensation risk and ESD from dry air, and can mechanically stress some components; the safe window has a lower bound as well as an upper bound.

## Try it
- **Simulation:** Monitor a live environmental console, identify out-of-range sensor readings, and flag the correct alerts across 6 rounds.
- **Coding problem:** Implement `solve(sensors)` to analyze a list of sensor dicts and return a sorted list of alert strings based on defined thresholds.
- **Quiz:** self-check on the skill's key ideas.

## Sources (local / vendor / rebuilt)
- Deep: NIST SP 800-12 Rev.1 and NIST SP 800-53 Rev.5 (PE family, Physical and Environmental Protection), rebuilt-equivalent notes in `vendor/nist/`
- Reference: GeeksforGeeks, "Physical Security in Cybersecurity", rebuilt summary in `vendor/reference/2.3.d-geeksforgeeks.md`
- Practice: Wikiversity, "Introduction to Computer Security / Physical Security", rebuilt in `vendor/practice/2.3.d-wikiversity.md`
- Repo: LetsDefend/Free-Cybersecurity-Resources -> `vendor/repos/LetsDefend-Free-Cybersecurity-Resources/`
