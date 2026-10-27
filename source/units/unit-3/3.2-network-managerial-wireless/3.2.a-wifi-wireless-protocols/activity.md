# In-class activity, 3.2.a Wi-Fi basics and wireless security protocols (WPA2/WPA3)

**Format:** pairs · **Time:** 25 min · **Offline:** yes

## Goal
Students evaluate six printed Wi-Fi configuration cards and classify each as secure, acceptable,
or insecure. By the end, each pair produces a written justification for every classification and
articulates one concrete remediation step for each insecure card. Ties to LO 3.2.A (evaluate
controls that protect a network).

## Materials (all local)
- the SimLab simulation on each machine, or the printed Wi-Fi configuration cards below.
- Printed "Wi-Fi Config Card Set" (teacher prints pages 2-3 of this file, one set per pair).

## Wi-Fi Configuration Card Set (print and cut)

Card A: protocol=WPA3, password_length=22, guest_vlan=yes, firmware=current
Card B: protocol=WPA2-AES, password_length=18, guest_vlan=no, firmware=current
Card C: protocol=WPA2-TKIP, password_length=8, guest_vlan=no, firmware=outdated
Card D: protocol=WEP, password_length=10, guest_vlan=no, firmware=outdated
Card E: protocol=WPA3, password_length=25, guest_vlan=yes, firmware=current
Card F: protocol=WPA2-AES, password_length=6, guest_vlan=yes, firmware=current

## Steps
1. Each pair reads `atom.md` (or opens the simulation) to confirm the criteria for secure vs.
   insecure. Criteria: protocol must be WPA2-AES or WPA3; password length at least 20 characters;
   guest VLAN isolated; firmware current.
2. Working together, classify each card (secure / acceptable / insecure) using the criteria.
   Record the classification and a one-sentence reason on the answer sheet.
3. For each insecure card, write one concrete remediation step, the exact change an admin would
   make (e.g., "upgrade protocol to WPA3 and regenerate a 24-character random password").
4. Open the simulation and run the configuration classifier simulation. Compare the simulation's
   verdict for each card to your written answer. Note any discrepancy and discuss why.

## Collaborate (AP skill 4)
Assign roles within each pair: one is the "network admin" who argues for the current
configuration, the other is the "security auditor" who flags gaps. After classifying all six
cards, swap roles and revisit any card where you disagreed. Write a final joint verdict.

## Exit ticket
Each student submits (individually, written or typed):
- Which card was the most ambiguous to classify, and why?
- State the one criterion you found most impactful for security and justify it in two sentences.

## Instructor notes
- Expected classifications: A=secure, B=acceptable (password length below 20 is the gap),
  C=insecure (TKIP + short password + outdated firmware), D=insecure (WEP is completely broken),
  E=secure, F=insecure (password too short).
- Common stumble: students accept WPA2-TKIP as "just WPA2." Clarify that TKIP reintroduced RC4
  weaknesses and must be rejected; AES-CCMP is the only acceptable WPA2 cipher.
- This activity feeds the unit 3 project (network security assessment) and scenario stage 3
  (the attacker uses an evil-twin AP because the target network still uses WPA2-PSK with a
  weak password).
