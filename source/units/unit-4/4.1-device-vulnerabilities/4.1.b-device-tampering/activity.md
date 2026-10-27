# In-class activity, 4.1.b Device tampering and physical compromise

**Format:** small group · **Time:** 30 min · **Offline:** yes

## Goal
Students identify physical security vulnerabilities in a clinic's office layout and devise a comprehensive physical-hardening strategy to protect workstations, servers, and network devices against tampering. Ties to LO 4.1.B.

## Materials (all local)
- Paper and writing utensils.
- Workstation/Layout scenario description below.

## Steps
1.  **Analyze the Scenario (10 min):** Read the following description of a medical clinic's setup. Identify at least four distinct physical vulnerabilities that expose the clinic's devices to physical tampering or offline access:
    *   *Scenario:* A local medical clinic's reception desk is in the main lobby, where patients wait. The receptionist's workstation sits on a counter, with its back facing the waiting area, exposing the USB ports directly to visitors. A network printer sits in a hallway that patients use to reach exam rooms. The main server cabinet is located in a repurposed storage closet; the door has a standard key lock, but the keys are kept in a drawer at the reception desk, which is left unlocked during business hours. Staff laptops are left open on exam room desks while doctors step out to consult with colleagues.
2.  **Devise Hardening Countermeasures (10 min):** For each vulnerability identified, specify at least one physical and one logical mitigation. Use terms such as *port blockers*, *BIOS/UEFI hardening*, *Full Disk Encryption (FDE)*, *Kensington cable locks*, and *chassis intrusion detection*.
3.  **Refine the Defense (10 min):** Present your group's top two recommendations to the class. Discuss why logical security alone (like screen-lock passwords) fails if an attacker has physical access.

## Collaborate (AP skill 4)
Assign roles within each group:
-   **Physical Security Architect:** Focuses on structural barriers, locks, and placement.
-   **Systems Administrator:** Focuses on logical policies (FDE, BIOS/UEFI settings, device timeouts).
Work together to create a unified recommendation.

## Exit ticket
Each student submits: One reason why Full Disk Encryption (FDE) is necessary even if a server room has a physical door lock.

## Instructor notes
*   **Expected Vulnerabilities & Solutions:**
    *   *Receptionist USB ports exposed:* Patients could plug in a USB Rubber Ducky. Mitigation: USB port blockers, chassis lock box, or turning the computer case around.
    *   *Hallway network printer:* Attacker could plug an unauthorized laptop into the printer's Ethernet port. Mitigation: Mac-address filtering (logical) and physical Ethernet port locks.
    *   *Server closet keys unlocked:* Server could be stolen or offline-booted. Mitigation: Keypad access, BIOS passwords, and FDE.
    *   *Exam room laptops open:* Unauthorized reading or command execution. Mitigation: Strict screensaver auto-lock (e.g., 60 seconds) or physical cable locks.
*   **Common Stumbles:** Students may suggest software-based firewalls to prevent USB Rubber Ducky attacks. Remind them that Rubber Duckies emulate keyboards, which firewalls trust implicitly.
*   **Unit Link:** Feeds into the unit-wide device hardening guidelines.
