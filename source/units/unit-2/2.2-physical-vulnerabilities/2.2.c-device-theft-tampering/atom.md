# 2.2.c, Device theft and tampering

> **Unit 2 · 2.2 Physical Vulnerabilities and Attacks**
> **AP Learning Objective(s):** 2.2.B, 2.2.C
> **Course skill(s):** Analyze Risk

## Learning objective (student-facing)
Distinguish device theft from device tampering, identify the
attack techniques each enables (offline password reset, disk imaging, hardware implants, evil-maid
attacks), and evaluate whether a given device's configuration (encryption, boot protections,
asset tracking) would contain the damage if the device were stolen or tampered with.

## Lesson
Unauthorized physical access (2.2.a) gets an attacker into a building. Once inside, or once a
device leaves the building on an employee's backpack, the attacker's goal shifts to the device
itself. **Device theft** is the straightforward case: a laptop, phone, external drive, or backup
tape is physically taken. **Device tampering** is subtler and often more dangerous: the device is
briefly and covertly altered, hardware implanted, firmware modified, a peripheral swapped, and
then returned to its owner, who has no idea anything happened. A stolen laptop is a known loss you
can respond to; a tampered laptop is a known-good device that is quietly lying to you.

**What theft actually costs you.** The naive view of device theft is "we lost a $1,500 laptop."
The real cost is almost always the data on it, not the hardware. A stolen unencrypted laptop
hands an attacker every file, cached credential, saved browser session, and locally stored
password on the disk, often without needing to guess a single password, because many attacks on
a physically possessed device bypass the login screen entirely. Booting from a USB drive lets an
attacker mount the internal disk directly, read files, or reset the local administrator password,
all without ever authenticating through the intended operating-system login. This is why
**full-disk encryption** (BitLocker, FileVault, LUKS) is the single most effective control against
device theft: if the drive is encrypted and the device was powered off (so the key is not sitting
in memory), the stolen disk is unreadable without the key even after physical removal.

**Tampering and the "evil maid" attack.** The term **evil-maid attack** describes a scenario
where an attacker with brief, unsupervised physical access to a device (the classic example is a
hotel room cleaner) tampers with it and leaves. A common evil-maid technique against an encrypted
laptop is to boot a malicious USB image that replaces the boot loader with a fake password prompt
that looks identical to the real one. The next time the legitimate user enters their disk-encryption
password, the fake loader silently captures it and reboots into the real system as if nothing
happened. The user never notices; the attacker now has the encryption key and returns later (or
relies on a network exfiltration channel) to unlock the stolen data. This defeats a security control
(full-disk encryption) not by breaking the cryptography but by exploiting the brief window of
unsupervised physical access before the encryption is even engaged for that session.

**Hardware implants.** Tampering is not limited to software. A rogue USB device, a "keylogger
dongle" placed inline between a keyboard and a computer, silently records every keystroke,
including passwords, and can be retrieved later or exfiltrate data over its own hidden radio.
Rogue network taps inserted into a cable run can mirror traffic to an attacker. Malicious
peripherals (a "free" USB charging cable, a promotional USB drive) can present themselves as an
innocuous device to the OS while secretly acting as a keyboard that types malicious commands the
instant they are plugged in, an attack class sometimes called "juice jacking" or "BadUSB,"
depending on the vector. Because these implants are physically small and often hidden in plain
sight (inside a cable, inside a wall jack), tampering can go undetected for a long time unless
staff are trained to notice inconsistencies.

**Detecting tampering.** Because tampering, by design, tries to leave no obvious trace, detection
relies on physical evidence and behavioral cues rather than a login prompt. **Tamper-evident
seals**, stickers that visibly tear, discolor, or reveal a "VOID" pattern if removed, placed
over a laptop's screws or a server's chassis panel let staff visually confirm a device has not
been opened. Comparing a device's serial number, asset tag, and physical condition against an
inventory record on a scheduled basis can catch a swapped device. Users should be trained to
notice inconsistencies: an unfamiliar dongle plugged into their keyboard port, a laptop that took
longer than usual to boot the last time it was left unattended, or a password prompt that "looks
slightly different." None of these are proof on their own, but they are the kind of signal that
should trigger an IT security review rather than being dismissed.

**Asset tracking and remote response.** Organizations reduce the impact of theft with **asset
tags and inventory tracking** (so a missing device is noticed quickly rather than months later),
**remote wipe / remote lock** capabilities (mobile device management tools that can erase a stolen
phone or laptop once it is reported missing and reconnects to a network), and **Kensington locks**
or similar physical cable locks that make opportunistic theft from a shared workspace harder,
though they do not stop a determined, prepared attacker. The coding problem for this skill asks you
to build an incident-triage function: given a list of reported device incidents (with attributes
like encryption status, whether a tamper-evident seal was intact, and time since last inventory
check), classify each incident by its actual risk level to the organization.

## Key terms
- **Device theft**, the physical removal of a device (laptop, phone, drive, tape) from its
  authorized location or owner.
- **Device tampering**, a covert, typically brief physical alteration of a device (hardware,
  firmware, or peripheral) intended to compromise it without the owner's knowledge.
- **Evil-maid attack**, a tampering attack in which an attacker with brief unsupervised access to
  a device (e.g., in a hotel room) modifies it, often to capture credentials on next use, then
  restores its appearance and leaves.
- **Full-disk encryption**, encryption of an entire storage volume so its contents are
  unreadable without the decryption key, even if the physical drive is removed.
- **Tamper-evident seal**, a sticker or mechanism that visibly and irreversibly shows evidence
  (tearing, a "VOID" pattern, discoloration) if a device enclosure has been opened.
- **Remote wipe**, a mobile-device-management capability that erases a device's data remotely,
  typically once it is reported lost or stolen and reconnects to a network.

## Common misconceptions
- "If a laptop is password-protected, a thief can't get the data." → A login password protects the
  operating system's normal boot path, but an attacker with physical possession can often boot
  from external media and read the disk directly unless the disk itself is encrypted.
- "Tampering only matters for spy-movie scenarios." → Evil-maid attacks and rogue USB implants are
  documented techniques used against real targets (executives, journalists, researchers) whenever
  a device is left briefly unattended in a hotel, shared office, or conference venue.
- "A locked laptop bag is enough physical security." → A cable lock or bag deters casual,
  opportunistic theft but does nothing against a prepared attacker with cutting tools, and does
  nothing at all against tampering, which does not require removing the device from the room.

## Try it
- **Simulation:** Review a queue of reported device incidents
  and correctly classify each as LOW, MEDIUM, or HIGH organizational risk based on its details.
- **Coding problem:** Implement a function that triages device theft/tampering
  incident reports into risk levels using the device's encryption status, seal status, and
  time-since-last-check.
- **Quiz:** self-check on the skill's key ideas.

## Sources (local / vendor / rebuilt)
- Deep: MIT OCW (physical/device security principles), rebuilt as original prose above; see
  `vendor/web/mit-ocw/` notes.
- Reference: GeeksforGeeks (physical security overview), rebuilt locally.
- Practice: Cybrary physical-access awareness module, rebuilt locally as the simulation.
- Repo: her0marodeur/awesome-free-cybersecurity → `vendor/repos/her0marodeur-awesome-free-cybersecurity`.
