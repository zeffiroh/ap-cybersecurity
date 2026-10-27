# 4.1.b, Device tampering and physical compromise

> **Unit 4 · 4.1 Device Vulnerabilities and Attacks**
> **AP Learning Objective(s):** 4.1.B
> **Course skill(s):** Analyze Risk

## Learning objective (student-facing)
Identify physical security threats (including hardware keyloggers, malicious USB drop attacks, and unauthorized physical access), explain how physical compromise bypasses logical network defenses, and analyze strategies to mitigate device tampering.

## Lesson
The fundamental rule of hardware security is simple: *if an attacker has physical access to your device, it is no longer your device.* Logical controls, such as passwords, firewalls, and network access lists, assume that the physical chassis of the machine is secure. If an adversary can touch a computer, plug a device into it, or open its case, they can bypass almost every software-based defense. 

### Common Physical Attacks
Physical compromise does not always involve stealing the entire machine. Often, it involves subtle hardware modifications that intercept data or execute unauthorized commands.

*   **Keystroke Injection (USB Rubber Ducky):** A standard USB drive is recognized by the operating system as storage. However, a keystroke injection tool (often called a "USB Rubber Ducky") is programmed to mimic a USB keyboard. When plugged in, the computer immediately trusts the device as a typing human. The device then types out scripted commands at hundreds of words per minute, opening a terminal, downloading and executing malware, and exfiltrating data. Because it acts as a keyboard, antivirus software does not block the "typing," allowing it to bypass logical security controls.
*   **Hardware Keyloggers:** A hardware keylogger is a tiny adapter connected inline between the keyboard cable and the computer's USB port. It intercepts every electric signal from the keyboard and logs the letters typed (including passwords, emails, and credit card numbers) to its own internal storage. Because the keylogger functions entirely in hardware before the signals reach the operating system, no software-based malware scanner or antivirus can detect it. The attacker recovers the logs by returning later to retrieve the device.
*   **Offline Storage Access:** If a computer is stolen or left unattended, an attacker can simply remove the hard drive or boot the machine from a portable USB drive running a live Linux operating system. By booting into an alternative operating system, they bypass the local Windows or macOS password prompt entirely and read all user files directly from the drive.
*   **Cold Boot Attacks:** When a computer is powered off, the contents of its random-access memory (RAM) do not disappear instantly; they degrade over several seconds or minutes. In a cold boot attack, an attacker sprays the memory chips with a chemical coolant (like compressed air held upside down) to freeze them, then quickly transfers the physical RAM module to another machine. This preserves the memory state, allowing the attacker to extract cryptographic keys or passwords that were recently loaded in RAM.

### Bypassing Logical Controls
Security policies often focus heavily on preventing remote network attacks, leaving physical ports unguarded. A physical attacker takes advantage of this asymmetric trust:
1.  **Implicit Hardware Trust:** Operating systems are built to plug-and-play. They automatically load drivers for keyboards, mice, and network adapters without requiring administrator privileges.
2.  **Lack of Boot Integrity:** Unless configured otherwise, a computer will gladly boot from whichever storage device is connected, allowing a live USB to override the installed operating system and its active protections.

### Physical and Logical Mitigations
Defending against physical tampering requires combining physical barriers with cryptographic logical controls. No single layer is sufficient on its own, a locked door does nothing against an insider, and encryption does nothing if the boot process itself can be tampered with.

*   **BIOS/UEFI Hardening:** You should set a password on the system BIOS/UEFI to prevent unauthorized changes, and disable the option to boot from external media (USB, DVD, or Network). This forces the machine to only boot the trusted internal operating system.
*   **Full Disk Encryption (FDE):** FDE (using tools like BitLocker or LUKS) encrypts the entire hard drive, including the operating system files. If an attacker removes the drive or boots from a USB, they cannot read the files without the decryption key. FDE is typically bound to a **Trusted Platform Module (TPM)**, a specialized security chip on the motherboard that verifies the boot files haven't been tampered with before releasing the decryption key.
*   **Port Blocking and Physical Locks:** Port blockers are physical plastic inserts locked into unused USB or Ethernet ports to prevent malicious devices from being inserted. Workstations can be locked to desks with security cables, and servers must be locked inside server racks with chassis intrusion switches that alert administrators if the case is opened.
*   **User Training (USB Drop Awareness):** Attackers often scatter malicious USB drives in office parking lots or lobbies, hoping an employee will find one and plug it into a work computer out of curiosity. Training employees to never plug untrusted media into their devices is a crucial human defense.

### Physical Security in Layers
Security professionals describe physical protection as a series of concentric rings, each one buying time or raising the cost of an attack rather than making compromise impossible. The outermost ring is the building itself, badge readers, security guards, and visitor sign-in logs control who gets near a device at all. The next ring is the room: server closets and network cabinets should be locked separately from general office space, since an attacker who can walk into an unattended office has already defeated the outer ring. The innermost ring is the device itself, chassis locks, port blockers, and cable locks that make tampering slow and noisy even for someone standing right in front of the machine. A single missing ring (for example, an unlocked server closet inside a badge-controlled building) collapses the whole strategy, because the attacker only needs to find the weakest layer, not defeat every layer at once.

**Detecting tampering after the fact.** Not every physical attack can be prevented, so detection matters as much as prevention. Chassis intrusion switches log a timestamp whenever a case is opened, even if no data was visibly taken. Asset inventory audits that periodically verify serial numbers and physical location can catch a swapped or missing device before it is used for anything. Tamper-evident seals, stickers that visibly tear or change color if removed, are cheap and widely used on point-of-sale terminals and ATMs specifically so employees can visually confirm a device has not been opened since the last check.

## Key terms
- **Device tampering**, unauthorized physical modification or interception of a device to compromise its security.
- **USB Rubber Ducky**, a keystroke injection tool disguised as a standard USB flash drive that executes pre-programmed commands by mimicking a keyboard.
- **Hardware keylogger**, a physical device connected between a keyboard and computer that records all keystrokes.
- **Full Disk Encryption (FDE)**, a cryptographic method that encrypts all data on a storage drive, including the operating system, protecting it from offline reading if the drive is stolen.
- **Trusted Platform Module (TPM)**, a dedicated microchip on the motherboard designed to secure hardware by integrating cryptographic keys and verifying boot sequence integrity.
- **Port blockers**, physical inserts placed into unused external ports (like USB or Ethernet) to prevent unauthorized devices from being plugged in.
- **Chassis intrusion detection**, a switch inside a device's case that logs or alerts when the case is opened, providing after-the-fact evidence of physical tampering.
- **Tamper-evident seal**, a sticker or label placed over a device's case or port that visibly tears, discolors, or breaks if removed, letting staff visually confirm a device has not been opened.

## Common misconceptions
- "Operating system passwords protect my data if my laptop is stolen." → Bypassed. An attacker can remove the hard drive and read it on another system, or boot from a Linux USB to browse files, unless Full Disk Encryption (FDE) is enabled.
- "Antivirus software will block malicious USB keyboard emulators." → Antivirus scans files, but a USB Rubber Ducky acts as a keyboard. The OS trusts it as a typing human, meaning it bypasses software-level malware scans unless specific USB device whitelisting is active.
- "A locked office building means the devices inside are physically secure." → Building access controls only stop outsiders; they do nothing against a malicious insider, a visitor left unattended, or a device sitting in an unlocked room within an otherwise secure building. Physical security requires layered controls at the building, room, and device level.

## Try it
- **Simulation:** Detect physical tampering anomalies on a corporate workstation network and deploy physical/logical mitigations.
- **Coding problem:** Parse a hardware system audit log to detect physical security events (chassis intrusion, unauthorized USB device insertion).
- **Quiz:** self-check on the skill's key ideas.

## Sources (local / vendor / rebuilt)
- Deep: Open Security Training (hardware security modules), rebuilt as original prose above.
- Reference: GeeksforGeeks (physical cybersecurity threats), cross-checked for accuracy.
- Practice: Cybrary device security labs, rebuilt locally as the simulation.
- Repo: her0marodeur/awesome-free-cybersecurity → `vendor/repos/her0marodeur-awesome-free-cybersecurity`.
