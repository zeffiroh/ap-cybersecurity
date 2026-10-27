# In-class activity, 5.3.a Encryption vs. hashing

**Format:** pairs · **Time:** 20 min · **Offline:** yes

## Goal
Analyze real-world business scenarios and decide whether each data element should be encrypted, hashed (with salt), or encoded, defending the choice based on the requirements for reversibility and confidentiality.

## Materials (all local)
- Pen and paper (or a local text editor)
- The scenarios listed below

## Steps
1. **Analyze Scenarios (8 mins):** With your partner, read the following three scenarios and determine which control (Encryption, Hashing, or Encoding) is required for each data field.
   - **Scenario A:** A patient portal stores medical records (diagnosis, prescription history). The system must display these records to the patient and their doctor.
   - **Scenario B:** An e-commerce database stores customer login passwords so the site can authenticate users when they sign in.
   - **Scenario C:** An application needs to transmit a binary image file inside a JSON payload (which only supports text strings).
2. **Draft the Defense (6 mins):** Write a 2-sentence justification for each choice. Address:
   - Does the data need to be recovered in its original form?
   - What happens if the database is breached?
3. **Present (6 mins):** Pair up with another group, compare your choices, and discuss any differences in your justifications.

## Collaborate (AP skill 4)
With your partner, roleplay as a Security Auditor and a Software Developer. The Developer wants to use symmetric encryption for passwords "just in case they need to recover a forgotten password for a VIP user." The Auditor must explain the security risks of this approach and advocate for salted hashing.

## Exit ticket
Write down the main difference between Encryption and Hashing in terms of mathematical reversibility and why this difference makes hashing the only acceptable choice for password storage.

## Instructor notes
- **Scenario A Answer:** Encryption. Medical records must be read in their original form (reversible) to provide patient care, but must remain confidential.
- **Scenario B Answer:** Hashing (with salt). Passwords should never be recovered. Verification only requires checking if the computed hash matches the stored hash.
- **Scenario C Answer:** Encoding (Base64). This is a formatting change to allow binary data in text environments. It provides no security.
- **Common stumbling block:** Students often confuse encoding with encryption. Emphasize that encoding is a public, keyless standard that anyone can reverse.
