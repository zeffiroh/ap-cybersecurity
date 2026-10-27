# In-class activity, 2.1.a CIA triad: confidentiality, integrity, availability

**Format:** pairs · **Time:** 20 min · **Offline:** yes

## Goal
Students classify real-ish security scenarios by which CIA pillar(s) are violated and propose at least one countermeasure for each. Ties to LO 2.1.A (identify which CIA property a threat targets) and the course skill Analyze Risk.

## Materials (all local)
- the SimLab simulation on each machine, or the printed scenario set below.
- One copy of the scenario card per pair (print or display on screen).

## Scenario card (print or project)

| # | Incident description | Pillar(s) violated | One countermeasure |
|---|---------------------|--------------------|-------------------|
| 1 | A disgruntled employee emails the customer list to a competitor. | ? | ? |
| 2 | A web server is flooded with fake traffic and goes down for six hours. | ? | ? |
| 3 | An attacker intercepts an unencrypted login and reads the password. | ? | ? |
| 4 | A backup database is found to have corrupted records after a botched migration script. | ? | ? |
| 5 | Ransomware encrypts all files on a school network; teachers cannot access lesson plans. | ? | ? |
| 6 | A developer accidentally pushes a config file with an API key to a public repository. | ? | ? |

## Steps
1. (5 min) Each pair reads scenarios 1-3 independently and writes their pillar classification and countermeasure in the table. Partners do not discuss yet.
2. (5 min) Partners compare answers. Where they disagree, they must each defend their classification with one sentence citing the lesson definition. They settle on a consensus answer.
3. (5 min) Repeat for scenarios 4-6.
4. (5 min) Each pair opens the simulation and verifies their answers against the sim's scoring. For any scenario they got wrong, they revise their countermeasure.

## Collaborate (AP skill 4)
Assign roles: one partner is the "security analyst" (defends the classification), the other is the "devil's advocate" (argues whether a second pillar is also violated). For scenarios that clearly violate multiple pillars (e.g., #5), they must rank which pillar is the primary violation and explain why. Swap roles halfway through.

## Exit ticket
Each student writes one sentence: "Scenario X primarily violates [pillar] because [definition match], and [countermeasure] would reduce the risk by [mechanism]."

## Answer key (instructor only)

| # | Pillar(s) | Countermeasure (sample) |
|---|-----------|------------------------|
| 1 | Confidentiality | Data classification policy; access control limiting who can export customer lists; DLP (data loss prevention) software |
| 2 | Availability | DDoS mitigation service; rate limiting; redundant hosting |
| 3 | Confidentiality | Encrypt credentials in transit (TLS/HTTPS); never transmit plaintext passwords |
| 4 | Integrity | Cryptographic checksums on backups; tested restore procedures; version-controlled migration scripts |
| 5 | Availability (primary); Integrity (secondary if files are modified before encryption) | Offline backups not connected to main network; ransomware-aware endpoint protection |
| 6 | Confidentiality | Secret scanning in CI/CD pipeline; API key rotation; `.gitignore` for config files; principle of least privilege |

## Instructor notes
- Timing: scenarios 1-3 are more clear-cut; 4-6 introduce ambiguity about multiple pillars, which is intentional.
- Common stumbles: students sometimes label ransomware as an integrity violation because "files were changed." Clarify that ransomware's primary harm is denial of access (availability); the encryption is the mechanism, not the security goal violated from the victim's perspective.
- Scenario 6 often prompts debate about whether it's also an integrity issue (key could be used to modify data). Accept either classification if the student can cite the pillar definition. This is a realistic gray area.
- Feeds the unit project (threat modeling a small network) and the subsequent atoms on threat actors (2.1.b) and risk scoring (2.1.c).
