# 2.4.c tutor notes

Notes for the pre- and post-lecture tutor posts.

## The intuition to hold onto
The framing worth keeping: a motion sensor answers exactly one narrow question, did something change in this zone, and that narrowness is a feature, not a limitation. It doesn't know who moved, why, or whether they belong there; it hands a single yes/no signal to the alarm system covered in the last atom for a decision-maker (human or rule engine) to interpret with context the sensor itself doesn't have. Once you see the sensor as a narrow, fast tripwire rather than a smart observer, PIR's biggest quirk, that a person standing perfectly still can go undetected, stops being a flaw and starts being exactly what "detects change" should mean.

## The big picture
Dual-technology sensors are this skill's best worked example of a principle worth generalizing across the whole course: two independent detectors are dramatically stronger together than either is alone, precisely *because* their false-positive causes don't overlap. Sunlight fools a PIR element but produces no Doppler shift; HVAC airflow fools a microwave element but produces no meaningful heat delta. Requiring both to agree (AND-logic) filters out almost every nuisance trigger that would fool either one individually, the same cross-zone-verification idea from alarm systems, one atom earlier, just implemented inside a single sensor housing instead of across a room. And the misconception about sensitivity is worth remembering on its own: cranking sensitivity to maximum doesn't make a system more secure, it makes it noisier, and a system that cries wolf constantly is a system whose real alerts eventually get ignored, alarm fatigue is a security failure, not a technical inconvenience.
