# 2.3.b, Surveillance systems (CCTV, monitoring)

> **Unit 2 · 2.3 Protecting Physical Spaces**
> **AP Learning Objective(s):** 2.3.A
> **Course skill(s):** Mitigate Risk, Detect Attacks

## Learning objective (student-facing)

Describe the components and layout of physical surveillance systems, explain the security differences between active and passive monitoring, and analyze vulnerabilities in surveillance networks to recommend mitigations.

## Lesson

### The role of surveillance in physical security

If locks, badges, and biometrics control *who* enters a space, surveillance systems tell us *what* happens in and around that space. Surveillance is a dual-use control. It functions as a **detective control** by recording events and alerting operators to incidents in progress. Simultaneously, it serves as a **deterrent control** because the visible presence of cameras can discourage potential adversaries from attempting an intrusion.

Closed-Circuit Television (CCTV) is the standard term for a dedicated video system that transmits signals to a specific, limited set of monitors or recording devices. Unlike broadcast television, CCTV signals are not openly transmitted, though modern digital systems often rely on standard network protocols to carry video streams.

### CCTV architectures: analog vs. IP cameras

Surveillance technology has evolved from closed analog loops to networked digital environments:

1. **Analog CCTV systems:** Traditional systems connect cameras directly to monitors and video cassette recorders (VCRs) or Digital Video Recorders (DVRs) using dedicated coaxial cables. 
   - *Strengths:* Analog systems are immune to network hacking, IP spoofing, or remote denial-of-service (DoS) attacks.
   - *Weaknesses:* They require extensive cabling, offer limited image resolution, do not support advanced analytics, and are prone to signal degradation over distance. Physical access to the coaxial cables allows an attacker to cut or intercept the video signal directly.

2. **Internet Protocol (IP) cameras:** Modern systems use digital cameras that act as independent network devices. Each IP camera has its own IP address and transmits video over Ethernet cables (often powered by Power over Ethernet, or PoE) or Wi-Fi to a Network Video Recorder (NVR) or cloud-based server.
   - *Strengths:* IP systems support high resolutions, remote viewing, and intelligent analytics (such as motion detection, facial recognition, and license plate reading). They are highly scalable and integrate easily with other security systems.
   - *Weaknesses:* IP cameras introduce logical vulnerabilities. Since they reside on the network, they are subject to hacking, port scanning, credential stuffing, and firmware exploits. If the video stream is not encrypted, an attacker who intercepts the network traffic can view the feed or even inject fake video frames (spoofing).

### Designing surveillance: coverage, lighting, and blind spots

A poorly planned camera installation offers a false sense of security. Effective surveillance design requires careful consideration of the physical environment:

- **Placement and height:** Cameras should be mounted high enough to prevent physical tampering, vandalization, or obstruction (e.g., placing a bag or spray paint over the lens). However, they must not be so high that they only capture the tops of heads rather than identifiable facial features.
- **Blind spots:** A **blind spot** is any area within or around a facility that is not visible to surveillance cameras. Attackers actively seek out blind spots to bypass detection. System designers use overlapping fields of view, where one camera monitors the area directly beneath or behind another camera, to eliminate blind spots.
- **Lighting and environment:** Cameras require light to capture usable details. While standard cameras fail in the dark, security systems utilize infrared (IR) illuminators or thermal imaging. Thermal cameras detect heat signatures rather than visible light, making them exceptionally effective for perimeter monitoring in total darkness, fog, or heavy rain.
- **Camera types:** Fixed cameras point at a single, unchanging scene (e.g., an entrance). Pan-Tilt-Zoom (PTZ) cameras can be controlled remotely by an operator or programmed to sweep an area. While PTZ cameras offer wide coverage, they introduce a temporary blind spot: if the camera is currently panned to the left, an intruder can pass undetected on the right.

### Monitoring strategies: active vs. passive

How video feeds are processed determines their value during an incident:

- **Active monitoring:** Security personnel watch live video feeds in real time on a monitor wall. Active monitoring allows guards to detect anomalies (such as a tailgating event or a fence breach) as they happen and dispatch response teams immediately. The primary constraint is human attention; studies show that a operator's ability to spot incidents degrades significantly after just 20 minutes of watching multiple static screens.
- **Passive monitoring:** Video feeds are recorded to local storage (DVR/NVR) or cloud storage and are only reviewed after an incident has occurred. Passive monitoring is inexpensive and useful for forensic investigations, but it does nothing to prevent or interrupt an attack in progress.

### Vulnerabilities of surveillance systems

Surveillance systems themselves are targets. Attackers use several vectors to compromise them:
- **Physical tampering:** Cutting power or transmission cables, spray-painting the lens, or physically moving the camera angle.
- **Logical compromise:** Many IP cameras ship with default admin credentials (e.g., `admin`/`admin`) that administrators fail to change. Attackers search the local network or use public internet scanners (like Shodan) to find these cameras and take control.
- **Network sniffing:** Intercepting unencrypted Real-Time Streaming Protocol (RTSP) streams to view sensitive operations.
- **Denial of Service (DoS):** Flooding the camera's network port or NVR with traffic to drop frames or take the recording offline entirely.

To mitigate these risks, organizations must isolate surveillance networks on dedicated Virtual Local Area Networks (VLANs), enforce strong unique credentials, apply firmware updates regularly, and encrypt video streams in transit and at rest.

## Key terms

- **CCTV (Closed-Circuit Television)**, A video system where signals are transmitted privately to a specific set of monitors and recording units.
- **IP Camera**, A digital video camera that sends and receives data over an IP network.
- **Active Monitoring**, The real-time viewing of live video feeds by security personnel to detect and respond to incidents as they occur.
- **Passive Monitoring**, Recording video feeds for storage and forensic retrieval after an incident.
- **Blind Spot**, An unmonitored area within a facility's layout where an intruder can avoid camera coverage.
- **Thermal Imaging**, A camera technology that detects infrared radiation (heat) rather than visible light, allowing detection in complete darkness or harsh weather.

## Common misconceptions

- "CCTV prevents physical security breaches.", CCTV is fundamentally a **detective** control, not a preventive one. A camera cannot stop an intruder from climbing a fence; it only records the action or alerts a guard. To prevent breaches, cameras must be paired with preventive controls (like fences and locks) and active response protocols.
- "Networked IP cameras are inherently more secure than old analog systems.", While IP cameras provide better image quality and analytics, they also introduce a cyber-attack surface. An analog coaxial system cannot be hacked over the internet; an IP camera connected to an insecure network can.

## Try it

- **Simulation:** Open the simulation in your browser. Design a surveillance layout for a corporate facility. Ensure that you place cameras to eliminate blind spots, select the appropriate active/passive monitoring plan, and defend your IP cameras from cyber attacks to achieve a perfect audit score.
- **Coding problem:** In the folder, implement the surveillance coverage validator to calculate the percentage of secure zones that are monitored and identify any blind spots.
- **Quiz:** Check your understanding of surveillance architectures, camera placement, and monitoring strategies by completing self-check on the skill's key ideas.

## Sources (local / vendor / rebuilt)

- Deep: NIST SP 800-53 Rev. 5 (PE-6: Physical Access Monitoring), vendor path `vendor/nist/sp800-53-pe6.md`
- Reference: GeeksforGeeks, "Physical Security: Surveillance Systems", rebuilt equivalent at `vendor/reference/2.3.b-surveillance-ref.md`
- Practice: Wikiversity, "CCTV and Facility Audits", rebuilt equivalent at `vendor/practice/2.3.b-surveillance-practice.md`
- Repo: LetsDefend/Free-Cybersecurity-Resources, `vendor/repos/LetsDefend-Free-Cybersecurity-Resources/`
