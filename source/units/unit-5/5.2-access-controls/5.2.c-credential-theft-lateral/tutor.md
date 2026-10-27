# 5.2.c tutor notes

Notes for the pre- and post-lecture tutor posts.

## The intuition to hold onto
The frame worth walking in with: almost no breach ends where it starts, so the interesting security question is rarely "how did they get in" but "how far did they get once they were in." A phished marketing laptop is a nuisance by itself; it only becomes a catastrophe if it can reach the finance database from there. That reframes least privilege and network segmentation from 5.2.a/b, they're not abstract hygiene, they're literally the walls that determine whether an attacker's first foothold stays a foothold or becomes the whole building.

## The big picture
The detail worth remembering past this lecture is pass-the-hash: an attacker moving laterally frequently never needs your actual password at all, because many authentication protocols will accept a stolen hash or ticket as proof of identity just as readily as the plaintext would have been. That single fact should reshape how you think about password strength, a 20-character unguessable password does nothing to stop an attacker who scraped its hash straight out of memory on a compromised machine and replayed it. This is exactly why MFA earns its place as the standout defense in this skill: it's the one control that breaks the assumption underlying every credential-theft technique here, because a stolen credential, hashed, plaintext, or ticketed, is worthless without the second factor. Keep this skill in mind through the rest of the unit as the connective tissue to Unit 4's detection material: the behavioral signals described here (unusual host counts, atypical hours, first-time admin-tool use) are the same anomaly-detection logic as 5.6's log analysis, just applied to authentication events specifically.
