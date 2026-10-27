# 2.2.b, Environmental vulnerabilities (power, HVAC, fire, water)

> **Unit 2 · 2.2 Physical Vulnerabilities and Attacks**
> **AP Learning Objective(s):** 2.2.A
> **Course skill(s):** Analyze Risk

## Learning objective (student-facing)
Identify how power loss, HVAC (heating, ventilation, and air
conditioning) failure, fire, and water/flood events threaten the availability and integrity of
physical IT infrastructure, and you can evaluate whether a facility's environmental sensor
readings indicate a developing incident.

## Lesson
Locks and badge readers defend against a person who wants to walk into your server room. But a
server room can be destroyed just as thoroughly by things that are never "unauthorized" in the
access-control sense at all: a power outage, an overheated rack, a fire, or a burst pipe.
Environmental vulnerabilities are weaknesses in the physical conditions a facility depends on to
keep hardware running, and because they are not "attacks" in the social-engineering or
lock-bypass sense, they are easy to under-prioritize even though they routinely cause the same
outcome as ransomware: systems become unavailable, and sometimes data is destroyed outright.

**Power.** Computing equipment needs clean, continuous electrical power. A total outage stops
everything immediately unless backup power is in place. Just as damaging is a "dirty" supply:
voltage spikes, sags, and brownouts can corrupt in-flight writes or physically damage power
supplies over time. The standard controls are an **uninterruptible power supply (UPS)**, a
battery unit that bridges the gap between an outage and generator start, or rides out a short dip
entirely, and a **backup generator** for outages lasting longer than battery capacity allows.
Data centers commonly design for **N+1 redundancy**: enough generator and UPS capacity that any
single unit can fail without an outage. Power controls also include surge protection and,
critically, testing, a generator that has not been started in a year is a generator you do not
actually have.

**HVAC.** Servers generate enormous heat, and processors throttle or shut down automatically to
avoid physical damage once internal temperatures cross a safety threshold. A data center's cooling
system is not a comfort feature; it is a life-support system for the hardware. HVAC failure, a broken chiller, a clogged filter, a thermostat malfunction, can raise rack temperatures past
safe operating limits within minutes in a dense server room. Humidity is the other half of the
HVAC story: too little humidity increases static-discharge risk to circuit boards, and too much
humidity promotes condensation and corrosion on components. Facilities monitor both temperature
and relative humidity continuously and alarm on threshold crossings, typically targeting roughly
18-27°C (64-80°F) and 40-60% relative humidity per ASHRAE data-center guidelines.

**Fire.** Fire is the most destructive environmental threat because it can destroy hardware,
melt storage media, and threaten life. Electrical equipment creates ignition risk from overloaded
circuits, damaged cabling, and equipment failure, and a fire can spread through cable trays and
raised floors quickly. Fire safety for a server room has an unusual complication: water-based
sprinklers, the default fire suppressant in most buildings, will destroy the exact equipment they
are meant to protect. Data centers instead use **clean-agent fire suppression systems** (such as
FM-200 or inert-gas systems) that extinguish fire by removing oxygen or interrupting the chemical
reaction without damaging electronics, paired with **early-detection smoke/heat sensors** that
trigger well before a sprinkler-grade heat threshold would.

**Water and flooding.** Water threatens electronics through short-circuiting and corrosion. Risk
sources include burst pipes (especially plumbing routed above or near a server room, a design
flaw when data centers share a building with restrooms or kitchens on the floor above),
groundwater intrusion in basement-level facilities, and roof leaks. Controls include **raised
flooring** (elevating equipment above the slab so a shallow flood does not directly reach it),
**water sensors** placed at floor level to trigger an alarm at the first sign of moisture, and
simply avoiding locating critical infrastructure below grade or beneath water-bearing pipes in
the first place.

**Why this matters for availability.** All four categories are, first and foremost, availability
threats: an outage from any one of them takes systems offline the same way a DDoS attack does,
except the "attacker" is a physical process rather than a person. Some also threaten integrity, a partial power failure can corrupt data mid-write, and heat-induced hardware failure can silently
corrupt storage. Because environmental incidents are not caused by an adversary, they are easy to
deprioritize in a threat model that focuses only on malicious actors; a mature risk analysis
treats them with the same rigor as a targeted attack, because the impact to the organization is
identical or worse.

**Monitoring in practice.** Modern facilities instrument racks with continuous sensors, temperature, humidity, smoke, water, feeding a central monitoring dashboard that alarms when a
reading crosses a defined threshold, and escalates further if multiple readings drift together
(e.g., rising temperature *and* rising humidity, which can indicate a cooling-system failure
rather than a single sensor glitch). The coding problem for this skill asks you to build exactly
this kind of triage function: given a stream of sensor readings, classify each one by severity so
facilities staff know what needs immediate attention versus what is still within normal operating
range.

## Key terms
- **Uninterruptible power supply (UPS)**, a battery-backed unit that provides short-term power
  during an outage or dip, bridging the gap until generators start or power is restored.
- **N+1 redundancy**, a design principle where at least one extra unit of a critical system
  (power, cooling) exists beyond the minimum required, so a single failure does not cause an outage.
- **HVAC (heating, ventilation, and air conditioning)**, the system that regulates temperature
  and humidity to keep hardware within safe operating conditions.
- **Clean-agent fire suppression**, a fire-extinguishing system (e.g., FM-200, inert gas) that
  removes oxygen or interrupts combustion without damaging electronics, unlike water sprinklers.
- **Raised flooring**, elevated flooring in a data center that both routes cabling/cooling air
  and protects equipment from shallow flooding at slab level.

## Common misconceptions
- "Environmental risk isn't really a cybersecurity topic." → A power, cooling, fire, or water
  failure produces the same availability (and sometimes integrity) loss as a targeted cyberattack;
  AP Cybersecurity's Analyze Risk skill treats all threats to CIA equally regardless of whether an
  adversary is involved.
- "Sprinklers are fine for a server room like anywhere else in the building." → Water-based
  sprinklers actively destroy electronics; data centers use clean-agent suppression specifically
  because a false alarm or a real fire should not itself become a total-loss event.
- "As long as there's a backup generator, power is a solved problem." → A generator that has not
  been load-tested and does not have fuel contracts in place is a false sense of security; the
  UPS-to-generator handoff window and generator runtime under real load must be validated
  regularly.

## Try it
- **Simulation:** Monitor a stream of facility sensor readings
  (power, temperature, humidity, smoke, water) and correctly triage each reading's severity before
  a critical incident is missed.
- **Coding problem:** Implement a function that classifies a list of environmental
  sensor readings into severity levels using threshold and combined-signal rules.
- **Quiz:** self-check on the skill's key ideas.

## Sources (local / vendor / rebuilt)
- Deep: MIT OCW (physical/data-center infrastructure principles), rebuilt as original prose above;
  see `vendor/web/mit-ocw/` notes.
- Reference: GeeksforGeeks (physical security / data center overview), rebuilt locally.
- Practice: Cybrary physical-security awareness module, rebuilt locally as the simulation.
- Repo: her0marodeur/awesome-free-cybersecurity → `vendor/repos/her0marodeur-awesome-free-cybersecurity`.
