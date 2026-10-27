# Operation Quiet Harbor, the stealth scenario

A single, comprehensive, realistic scenario runs **underneath the whole course as a hidden
storyline**. As students complete atoms, stages unlock. Everything is synthetic, deterministic,
and fully offline, a JS/Python *fake-network engine* plays out adversary and system responses.

## The organization: Meridian Health
Meridian Health is a regional hospital network. Like real healthcare orgs, it is a high-value
target: sensitive patient data, legacy medical devices, a mix of clinical and corporate IT, and
staff under constant time pressure (perfect for social engineering). The synthetic world lives in
`world/`:
- `employees.json`, staff, roles, departments, emails, who has privileged access.
- `network.json`, subnets (DMZ, corp VLAN, clinical/OT VLAN), hosts, services, the web app + DB.
- `emails.json`, the mailflow, including the attacker's phishing campaign.
- `auth_logs.json`, VPN/login events (with the attack buried in the noise).
- `badge_logs.json`, physical door access (ties to Unit 2 later).

## The campaign (what the adversary is doing)
A financially-motivated crew ("Harbor") runs a multi-stage intrusion. Students play the **defender**
operating the provided toolkit, reconstructing and stopping the campaign stage by stage:

| Stage | AP skill | Unlocks after | What the student does |
|-------|----------|---------------|------------------------|
| 1. Recon | Analyze Risk | Unit 1 (1.1–1.3) | Map Meridian's exposed surface from synthetic OSINT/scan data. |
| 2. Entry (social engineering) | Analyze/Mitigate | Unit 1 (1.1, 1.4) | Find the phishing email that breached a clinician; identify the tactic + harden. |
| 3. Credential attack | Mitigate | Unit 4 | Spot the password spray in auth logs; enforce MFA. |
| 4. Network pivot | Analyze/Detect | Unit 3 | Trace lateral movement across VLANs; fix segmentation + firewall. |
| 5. Device compromise | Detect | Unit 4 | Find the compromised endpoint via EDR telemetry. |
| 6. App/data exfiltration | Analyze/Mitigate | Unit 5 | Identify the SQLi against the patient portal; stop the data loss. |
| 7. Detection + IR + report | Detect/Collaborate | Unit 5 | Run incident response, write the after-action report. |

**This pass implements the world, the complete toolkit, and Stages 1–2** (the Unit-1-reachable
part). Stages 3–7 unlock with Units 3–5 in later passes, same pattern.

## The toolkit (`toolkit/`)
The student is handed one coherent suite (`mhsec`), the per-atom lab primitives assembled into a
real system they operate against Meridian: `scan`, `loganalyze`, `phish`, `authtest`, `fwedit`,
`idsrule`, `crypto`, `edr`, `ir`. Each tool is a **blackbox** (interface + verified reference impl),
so a class can swap in student implementations that pass the scenario tests.

## How to play
- In the browser: open the capstone from the Course Hub (all 7 stages; start the course with the Start Offline launcher).
- Or use the CLI: `python -m toolkit.mhsec <tool> ...` from `source/capstone/`.
- Solution path + rubric: `INSTRUCTOR.md`. Stage logic + checks: `stages/`.
