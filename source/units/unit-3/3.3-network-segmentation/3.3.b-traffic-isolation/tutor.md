# 3.3.b tutor notes

Notes for the pre- and post-lecture tutor posts.

## The intuition to hold onto
Before this lecture, sit with the uncomfortable fact this skill opens with: a VLAN-segmented network still runs on implicit trust, once you're inside a zone, or inside the perimeter at all, older security models simply assume you belong there. Zero Trust's whole premise is refusing that assumption entirely, treating a device on the corporate Wi-Fi with exactly as much suspicion as a device on the open internet, because getting in has never actually meant you should be trusted with everything inside.

## The big picture
The connection worth making explicit: 3.3.a's VLANs solved the flat-network problem from 3.1.a by drawing walls between zones, but this skill shows you the gap VLANs leave behind, devices *inside* the same zone can still scan and attack each other freely, and that gap is exactly what let the ransomware scenario in this skill's Scenario A spread to fifty machines even on a segmented network. Microsegmentation and PVLANs close that gap by treating every single host as its own isolated segment rather than trusting the zone as a whole, and the never-trust-always-verify mantra means even a successful login or a healthy-looking device gets continuously re-evaluated rather than granted a blanket pass once admission happens. Keep the assume-breach principle especially close, because it's the throughline connecting this skill back to defense in depth in 3.2.c: Zero Trust isn't a claim that breaches won't happen, it's a design philosophy built around the assumption that they *will*, engineered so a single compromised machine's blast radius stops at exactly one machine instead of cascading through an entire trust zone.
