# 2.2.c tutor notes

Notes for the pre- and post-lecture tutor posts.

## The intuition to hold onto
The distinction to hold onto: a stolen laptop is a loss you already know about; a tampered laptop is a loss you don't know has happened yet. Theft interrupts your day. Tampering doesn't interrupt anything, it just quietly turns a device you trust into one you shouldn't, while it keeps behaving normally in every way you'd notice. That asymmetry is why tamper-evident seals and inventory audits matter even when nothing looks wrong: the whole point of a good tampering attack is that nothing *looks* wrong.

## The big picture
The evil-maid attack is worth remembering not because you'll personally be targeted by one, but because it's the cleanest illustration in this unit of a principle that recurs constantly in security: a control can be cryptographically perfect and still fail because of *when* it's applied. Full-disk encryption is genuinely strong, but only from the moment it's engaged. An attacker who gets brief unsupervised access before you've entered your password that session isn't breaking the encryption at all; they're intercepting the one narrow window where the protection hasn't started yet. That's a lesson worth generalizing: don't just ask "is this control strong," ask "is there a gap in time or scope where it isn't running."
