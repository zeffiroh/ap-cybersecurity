# 2.4.b, Alarm systems

> **Unit 2 · 2.4 Detecting Physical Attacks**
> **AP Learning Objective(s):** 2.4.B
> **Course skill(s):** Detect Attacks

## Learning objective (student-facing)
Identify the components of an intrusion detection alarm system,
explain how arm states and entry/exit delay affect whether a sensor trip is a real event, and
classify alarm events (true alarm, false alarm, suppressed) to decide which should escalate to
central-station dispatch.

## Lesson

### What an alarm system actually does
A lock keeps someone out. A camera records that they got in anyway. An **alarm system** sits in
between: it is a **detective control** whose job is to notice an intrusion attempt in progress and
trigger a response fast enough to matter. It is not a barrier, nothing about a beeping siren
physically stops a person from walking through a broken window. Treating an armed alarm as if it
were a lock is the single most common mistake in physical security planning, and it matters because
budget and attention get misallocated when "we have an alarm" is treated as equivalent to "this
door cannot be opened."

### Components
A residential or commercial intrusion alarm has four parts. **Sensors** detect a specific physical
event at a specific location: a **door/window contact sensor** (a reed switch pair, one half on
the frame, one on the door, that opens the circuit when the door swings) detects an opening;
a **glass-break sensor** listens (acoustically, or via a shock/vibration transducer) for the
specific frequency signature of breaking glass rather than any loud noise, which reduces false
trips from, say, a dropped plate. A **panic button** (also called a duress button) is different in
kind from the others, it is not triggered by an intrusion event at all, but by a person
deliberately signaling that they need help, whether from a burglary, a medical emergency, or a
threat of violence. The **control panel** is the brain: it tracks which zones are armed, runs the
entry/exit delay timers, and decides whether a sensor trip should sound the local siren, call the
monitoring center, or both. The **monitoring / central station** is a staffed facility (in-house or
third-party) that receives the panel's signal, attempts to verify the alert, and if warranted
contacts the customer and/or dispatches police. The **siren/notification** is the local audible and
visual output, its purpose is as much to scare off an intruder and alert neighbors as it is to
notify occupants.

### Arm states and the entry/exit delay problem
A system can be **disarmed** (no zones monitored), **armed-away** (all zones, including interior
motion, monitored, for when the building is empty), or **armed-stay** (perimeter zones like doors
and windows monitored, but interior zones bypassed, for when occupants are inside and moving
around). The hardest engineering problem in alarm design is not detecting a sensor trip; it is
telling apart a sensor trip caused by an intruder from one caused by the legitimate occupant who
just armed the system and is walking out the door. This is solved with timed grace periods: an
**exit delay** gives the occupant, say, 45-60 seconds to leave through a designated door after
arming before that door's contact sensor trip counts as an alarm condition; an **entry delay**
gives an arriving occupant a similar window to reach the panel and disarm before a trip escalates.
A door contact trip that happens one second after arming, during the exit delay window, is expected
behavior, not an intrusion, the panel must know to treat it as such and not immediately dispatch.

### Verification and false-alarm reduction
False alarms are the central operational problem for the alarm industry: the overwhelming majority
of police dispatches to alarm calls turn out to be pets, wind-blown curtains, user error, or a door
not fully latched, and many jurisdictions now fine repeat false-alarm addresses or even decline to
dispatch without verification. **Alarm verification** techniques reduce false dispatch: **cross-zone
verification** requires two different sensors (e.g., a door contact and a motion sensor, or sensors
in two separate zones) to trip within a short window of each other before the event is treated as
high-confidence, since a single sensor trip is more likely to be a glitch or a pet than two
independent sensors agreeing. **Video verification** sends a short clip or live feed to the
monitoring center so an operator can visually confirm a person is present before calling police.
Systems that support verification typically get faster, higher-priority police response, because
dispatchers can trust the alert.

### Response tiers
Not every alarm event should produce the same response. A **local-only** response, siren and
strobe only, no call to authorities, suits low-confidence, single-sensor trips, or systems without
a monitoring contract; it deters an opportunist but does nothing if no one is around to hear it. A
**monitored, verified dispatch** response, the monitoring center attempts to verify (via
cross-zone signal or callback to a keyholder) and then calls police, is reserved for high-confidence
events. Panic/duress signals are handled differently from every other sensor type: they bypass
verification and arm-state checks entirely and escalate straight to dispatch, because a human
deliberately pressed the button and false-positive risk from a panic press is treated as acceptable
given the cost of ignoring a real one. The coding problem for this skill asks you to implement this
exact triage: given a stream of sensor events with zone, sensor type, timestamp, and arm state,
classify each as suppressed, false alarm, local-only, or dispatch-worthy.

## Key terms
- **Door/window contact sensor**, a two-part reed switch (frame + door/window) that reports an
  open circuit when the door or window is opened while the zone is armed.
- **Glass-break sensor**, a sensor tuned to the acoustic or vibration signature of breaking glass,
  reducing false trips from generic loud noises.
- **Exit/entry delay**, a timed grace period after arming (exit) or before a trip escalates
  (entry) that lets a legitimate occupant leave or disarm without triggering a false alarm.
- **Panic/duress button**, a manually-triggered alert for personal safety or an in-progress
  emergency, independent of arm state and sensor zones, that escalates straight to dispatch.
- **Cross-zone verification**, requiring two independent sensors/zones to trip within a short time
  window before treating an event as high-confidence, to cut down false dispatch.
- **Monitoring / central station**, a staffed facility that receives alarm signals, attempts
  verification, and dispatches police when warranted.

## Common misconceptions
- "An armed alarm prevents a break-in." → An alarm is a detective and response control, not a
  preventive one; it can only notice and react to an intrusion that has already started, not
  physically stop it. Preventive controls are locks, barriers, and access control.
- "A silent/panic alarm is always about a burglary." → A panic or duress button is most often used
  for personal safety, a medical emergency, a threat of violence, a robbery in progress, and is
  deliberately designed to bypass the arm-state and verification logic that governs ordinary
  intrusion sensors, because a human pressing it is already high-confidence.

## Try it
- **Simulation:** Given an alarm event's sensor type, zone, arm
  state, and timing, classify it correctly (suppressed / false alarm / local-only / dispatch) to
  reach the scoring goal.
- **Coding problem:** Implement a function that classifies a stream of alarm events
  using exit-delay, arm-state, and cross-zone verification rules.
- **Quiz:** self-check on the skill's key ideas.

## Sources (local / vendor / rebuilt)
- Deep: NIST SP 800-53 Rev. 5 (PE-6: Physical Access Monitoring), vendor path
  `vendor/nist/sp800-53-pe6.md`.
- Reference: Wikiversity, "Intrusion Alarm Systems", rebuilt equivalent at
  `vendor/reference/2.4.b-alarm-systems-ref.md`.
- Practice: Cybrary physical-security alarm-response module, rebuilt equivalent at
  `vendor/practice/2.4.b-alarm-systems-practice.md`.
- Repo: LetsDefend/Free-Cybersecurity-Resources, `vendor/repos/LetsDefend-Free-Cybersecurity-Resources/`.
