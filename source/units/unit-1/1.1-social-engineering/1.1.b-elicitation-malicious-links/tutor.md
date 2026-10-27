# 1.1.b tutor notes

Notes for the pre- and post-lecture tutor posts.

## The intuition to hold onto
Think of elicitation and malicious links as two different keys to the same lock. Elicitation gets the attacker information; links and files get them execution. A useful intuition: elicitation is *slow and social*, it works over minutes or days of conversation, and each fragment feels harmless in isolation, which is exactly why it's dangerous. Link and file attacks are *fast and technical*, one click, one moment of inattention, and it's over. Defending against the first requires a habit of mind (need-to-know discipline); defending against the second requires a habit of hand (hover before you click, check the extension before you open).

## The big picture
The right-to-left URL-reading rule is one of the highest-leverage five seconds you'll spend in this entire course. Almost every lookalike-domain attack banks on the reader's eye landing on the trusted brand name wherever it appears in the string, rather than immediately before the first slash. Once that habit is automatic, an astonishing fraction of phishing links stop working on you, not because you got smarter about attacks in general, but because you fixed one specific, mechanical reading error that every browser and every attacker already knows humans make by default.
