# In-class activity, 3.3.b Traffic isolation and zero-trust segmentation

**Format:** Pairs or small groups · **Time:** 30 min · **Offline:** yes

## Goal
Students will design a secure network topology for a healthcare clinic using Private VLAN (PVLAN) isolation and Zero Trust principles. They will identify port-isolation states and specify access-control policies to prevent lateral movement of malware (e.g., ransomware) between patient-facing and backend medical devices.

## Materials (all local)
- Whiteboard, paper, or local drawing tools.
- A printed copy of the scenario details below.

## Scenario: The Oakridge Clinic
Oakridge Clinic has a flat network where everything is on one subnet (192.168.1.0/24). They recently experienced a security incident where malware on a waiting room check-in tablet spread to their local Electronic Health Records (EHR) server. 
The clinic's devices include:
1. **Default Gateway / Router (192.168.1.1):** Connects the clinic to the internet.
2. **EHR Local Database Server (192.168.1.10):** Contains sensitive patient medical histories.
3. **Doctor Workstations (3 hosts):** Used by doctors to retrieve and update records.
4. **Waiting Room Check-in Tablets (2 hosts):** Used by patients to check in.
5. **Guest Wi-Fi Access Point (1 host):** Used by patients waiting in the lobby.
6. **MRI Imaging Machine (1 host):** Runs an older legacy operating system that cannot be updated.

## Steps
1. **Analyze Vulnerabilities (10 min):** In your group, list the traffic flows that are absolutely necessary for the clinic to function. For example, do the check-in tablets need to speak to the doctor workstations? Does the MRI machine need internet access?
2. **Apply Private VLANs (10 min):** Map the 6 types of devices listed above to Private VLAN port designations to restrict layer-2 communication:
   - **Promiscuous Port(s):** Which devices must talk to everything?
   - **Isolated Port(s):** Which devices must never talk to each other?
   - **Community Port(s):** Which devices need to talk to each other in a small group, but not the rest of the network?
3. **Zero Trust Access Policy (5 min):** The clinic plans to place a Zero Trust Access Proxy in front of the EHR Database Server. Define a set of 3 rules/checks the proxy must run before allowing a doctor workstation to query the server (e.g., identity, location, device health posture).

## Collaborate (AP skill 4)
Assign roles within your pair/group:
- **Network Architect:** Designs the PVLAN mapping.
- **Security Analyst:** Designs the Zero Trust policy rules.
Compare designs with another group. Discuss: *If an attacker compromises the Guest Wi-Fi Access Point, does your design prevent them from reaching the EHR Server or the legacy MRI machine? Why?*

## Exit ticket
Each student submits a written response:
"Explain how Private VLAN (PVLAN) isolated ports differ from traditional VLANs in limiting the blast radius of a compromised device inside a corporate office."

## Instructor notes
- **PVLAN Design Solution:**
  - **Promiscuous:** Default Gateway (192.168.1.1).
  - **Isolated:** Guest Wi-Fi AP, Waiting Room Check-in Tablets, MRI Imaging Machine. (This prevents guest devices or compromised tablets from scanning/reaching each other or the MRI machine).
  - **Community:** Doctor Workstations (can be placed in a community so they can collaborate or share local resources like a shared printer if needed, or they can also be isolated if zero trust is fully enforced).
- **Zero Trust Proxy Policy Solution:**
  - Must authenticate user identity (MFA).
  - Must verify device posture (e.g., antivirus is active, OS is patched).
  - Must authorize the request (only allow access during clinic hours and block access if requests occur from external/unusual IPs).
