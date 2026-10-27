# 2.4.c, Motion detectors and sensor-based detection

> **Unit 2 · 2.4 Detecting Physical Attacks**
> **AP Learning Objective(s):** 2.4.B, 2.4.C
> **Course skill(s):** Detect Attacks

## Learning objective (student-facing)

Explain how PIR, microwave, and dual-technology motion sensors
detect intrusions, evaluate sensor placement and sensitivity tradeoffs, and classify a given
sensor trigger event as a true detection or a false positive.

## Lesson

### Why motion sensors exist

A locked door stops someone from walking in cleanly. A camera records what happens if they don't.
But neither a lock nor a camera actively notices an intruder who is already inside a room after
hours, a badge reader only fires when a badge is presented, and nobody is watching every camera
feed in real time. Motion sensors close that gap: they are always-on detective controls that
generate an alert the instant something moves in a space that should be empty. A motion sensor
does not identify *who* moved or *why*, it answers one narrow question, "did something change in
this zone," and hands that signal to an alarm system (covered in 2.4.b) for the response side of
detection. This skill is about the sensor technology itself: how each kind decides "yes, something
moved," and why that decision is harder to get right than it sounds.

### Passive infrared (PIR) sensors

The most common interior motion sensor is the **passive infrared (PIR) sensor**. "Passive" means
it does not emit any energy of its own, it simply watches the infrared (heat) radiation already
present in a room. A PIR sensor divides its field of view into multiple detection segments using a
lens (usually a Fresnel lens) and continuously compares the infrared level in each segment. A
warm object, a human body is about 37°C, which radiates strongly in the infrared band, moving
across segment boundaries produces a rapid *change* in the infrared reading. PIR sensors detect
that change, not the presence of heat itself, which is why a person standing perfectly still for
long enough can sometimes go undetected: no motion means no delta, and no delta means no trigger.
This is also why PIR sensors are cheap, low-power, and hard to defeat by simply staying warm, they
respond to movement, not temperature alone.

### Active sensors: microwave and ultrasonic

Where PIR is passive, **microwave sensors** are active: they emit a continuous microwave signal
and measure the reflection bouncing back. A moving object changes the frequency of the reflected
wave, the **Doppler shift**, the same physics behind radar guns measuring car speed, and the
sensor flags motion when it detects that shift. Microwave energy passes through some materials
(thin walls, glass) that block infrared, so microwave sensors can "see" through more of the
environment than a PIR sensor, which is a strength for coverage and a weakness for containment: a
microwave sensor may trigger on motion in an adjacent room or hallway outside the zone it is
meant to protect. **Ultrasonic sensors** work on the same Doppler principle using high-frequency
sound instead of microwaves, with a shorter effective range and susceptibility to false triggers
from HVAC air currents and vibration.

### Dual-technology sensors and AND-logic

Every single-technology sensor has a characteristic false-positive profile: PIR sensors trigger on
sudden heat-source movement that isn't a person (a heating vent kicking on, direct sunlight
sweeping across a wall, a pet), and microwave/ultrasonic sensors trigger on motion the PIR would
never see (vibration from a passing truck, HVAC airflow, radio interference). **Dual-technology
sensors** combine a PIR element and a microwave (or ultrasonic) element in one housing and require
**both** technologies to detect motion at roughly the same time before the sensor triggers an
alert, logical AND rather than OR. This dramatically reduces false positives, because the two
technologies' false-trigger causes rarely overlap: sunlight glare fools a PIR element but produces
no Doppler shift, and HVAC airflow can fool a microwave element but produces no meaningful infrared
delta. The tradeoff is a small risk of a missed true detection if an intruder's movement fails to
trigger both elements simultaneously (for example, moving very slowly along a sensor's boundary),
so dual-technology sensors are typically deployed for zones where false alarms are costly (a
monitored central station charges for every dispatched false alarm) rather than for every zone in
a facility.

### Placement, coverage, and sensitivity tuning

A motion sensor has a **detection cone** or coverage pattern, not omnidirectional vision, just
like a camera, it has blind spots outside its field of view and behind obstacles such as shelving
or open doors. Placement decisions mirror camera placement: mount high enough to resist tampering
and to see across the room, angle the cone to cover doors and choke points rather than open floor
space, and avoid pointing a PIR sensor at a window (sunlight and outdoor heat sources cause false
triggers), an HVAC vent or supply duct (moving warm/cool air mimics a moving heat source), or a
spot where foliage, curtains, or hanging decorations can sway. **Sensitivity tuning** is the
dial that trades detection reliability against false-positive rate: turning sensitivity up catches
smaller or slower movements (good against a careful intruder) but also catches a mouse, an insect,
or a shifting shadow; turning sensitivity down suppresses those nuisance triggers but risks missing
a genuine slow or partial-body intrusion, such as someone reaching an arm through a cracked window
without fully entering the room. There is no universally "correct" sensitivity, the right setting
depends on the environment (a pet-free vault room can run high sensitivity; a warehouse with
pets, forklifts, or dust cannot) and on how expensive a false alarm is to the organization.

### Layered and zoned detection

A single sensor covering an entire building is a single point of failure and a poor forensic tool, it tells you "something moved somewhere" with no location detail. Facilities instead deploy
**zoned detection**: separate sensors (or sensor groups) covering distinct areas, each reporting
independently, so a triggered alert also identifies *where*. Layering adds a second dimension:
**perimeter sensors** (fences, exterior door/window contacts, exterior motion sensors) detect an
intrusion attempt before entry, while **interior sensors** (room-level PIR, dual-technology units
in high-value rooms) provide defense in depth if the perimeter is defeated. Overlapping coverage
between adjacent zones, similar to overlapping camera fields of view, closes gaps where an intruder
might otherwise cross from one sensor's blind spot directly into another's. The coding problem for
this skill asks you to apply exactly this reasoning in code: given a sensor type, its environment,
and the tag describing what triggered it, decide whether the event is a true detection or a false
positive using the same AND-logic and known-cause reasoning developed above.

## Key terms
- **Passive infrared (PIR) sensor**, a motion sensor that detects a *change* in infrared (heat)
  radiation across segments of its field of view, without emitting any energy itself.
- **Doppler shift**, the change in frequency of a reflected wave (microwave or ultrasonic) caused
  by a moving object, used by active sensors to detect motion.
- **Dual-technology sensor**, a sensor combining two detection technologies (typically PIR +
  microwave) that must both trigger together (AND-logic) before an alert fires, reducing false
  positives.
- **Detection cone / coverage pattern**, the limited field of view a motion sensor can actually
  see; anything outside it, or behind an obstruction, is a blind spot.
- **Sensitivity tuning**, adjusting a sensor's trigger threshold to trade off missed detections
  (too insensitive) against false-positive alerts (too sensitive).
- **Zoned / layered detection**, deploying multiple sensors across distinct perimeter and
  interior zones with overlapping coverage, so an alert both localizes an intrusion and provides
  defense in depth if one layer is bypassed.

## Common misconceptions

- "A motion sensor sees everything in the room." → Motion sensors have a limited detection cone
  and blind spots just like cameras; furniture, doorways, and mounting angle can all hide an
  intruder's movement from a single sensor.
- "Higher sensitivity is always better security." → Sensitivity is a tradeoff, not a one-directional
  dial: maximum sensitivity catches pets, insects, HVAC airflow, and sunlight glare as false
  positives, which trains staff to ignore alerts (alarm fatigue) and can get a sensor's alerts
  deprioritized or disabled entirely, the opposite of better security.

## Try it
- **Simulation:** For each sensor trigger event, classify it as a
  TRUE DETECTION or a FALSE POSITIVE, or choose the correct sensor technology for a described
  environment, and reach the objective score.
- **Coding problem:** Implement a function that classifies motion-sensor trigger
  events as true detections or false positives using dual-technology AND-logic and known
  false-positive cause rules.
- **Quiz:** self-check on the skill's key ideas.

## Sources (local / vendor / rebuilt)
- Deep: NIST (physical security sensor/intrusion-detection guidance), rebuilt as original prose
  above; see `vendor/nist/` notes.
- Reference: Wikiversity (intrusion detection sensor technology overview), rebuilt locally.
- Practice: Cybrary physical-security awareness module, rebuilt locally as the simulation.
- Repo: LetsDefend/Free-Cybersecurity-Resources → `vendor/repos/LetsDefend-Free-Cybersecurity-Resources/`.
