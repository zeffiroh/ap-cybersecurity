# In-class activity, 5.3.b Symmetric encryption and key management

**Format:** small group (3-4) · **Time:** 25 min · **Offline:** yes

## Goal
Students work through a set of fictional data-protection scenarios, choosing the correct mode of
operation (ECB / CBC / GCM) or key-management practice (generation, storage, wrapping, rotation)
for each one, and justify why the wrong choices fail. Ties to LO 5.3.A, 5.3.B.

## Materials (all local)
- the SimLab simulation on each machine, or the printed scenario cards below.
- One "decision sheet" per group (paper) to record answers and justifications.

## Steps
1. Each group opens the simulation and works through the scenario queue, picking a mode of operation
   or key-management action for each fictional situation (e.g., "encrypt a bitmap image for
   storage," "encrypt a database column of SSNs," "generate an AES key for a new microservice,"
   "store a DEK long-term," "a key is suspected compromised").
2. For each scenario, before submitting an answer in the sim, the group must first write one
   sentence on the decision sheet explaining WHY the chosen mode/practice is correct and what
   would go wrong with the most tempting wrong answer (e.g., "ECB would let an attacker see
   repeated plaintext blocks as repeated ciphertext blocks").
3. After finishing the sim's scenario queue, the group sketches the key lifecycle diagram from
   atom.md from memory (Generate -> Store -> Rotate -> Retire) and annotates each stage with the
   one control that protects it (CSPRNG, HSM/secrets manager, scheduled rotation, cryptographic
   erasure).

## Collaborate (AP skill 4)
Assign roles: a "cryptographer" proposes the mode/practice for each scenario, a "red teamer"
argues for the tempting wrong answer and explains why it would actually fail, and a "recorder"
writes the final justification and draws the lifecycle diagram. Rotate roles halfway through the
scenario queue.

## Exit ticket
Each student submits: one scenario they got wrong (or found hardest) + the correct choice + a
one-sentence explanation of what an attacker could exploit if the wrong choice had been used.

## Instructor notes
- Expected reasoning: ECB is disqualified whenever the data has repeating structure (images,
  repeated field values); GCM is preferred whenever both confidentiality AND tamper-detection
  matter (e.g., sensitive database columns, network traffic); CBC is an acceptable middle ground
  when only confidentiality is needed and a fresh IV is guaranteed each time.
- Common stumble: students think "AES is AES" and forget that the mode of operation, not just
  the cipher, determines whether patterns leak, reinforce with the ECB bitmap example from
  atom.md.
- Common stumble on key management: students propose storing the DEK in plaintext "since it's
  already encrypted data next to it", steer them to envelope encryption (wrap the DEK with a
  KEK) and remind them a hardcoded/plaintext key defeats the whole system if the storage leaks.
- Feeds the unit project (data-at-rest protection plan) and the coding problem's key-wrapping /
  weak-RNG / ECB-leakage toolkit.
