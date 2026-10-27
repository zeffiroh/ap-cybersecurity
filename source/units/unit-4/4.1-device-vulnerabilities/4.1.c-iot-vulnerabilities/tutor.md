# 4.1.c tutor notes

Notes for the pre- and post-lecture tutor posts.

## The intuition to hold onto
Don't memorize the IoT vulnerability list as five unrelated facts, notice they're all downstream of the same root cause: nobody thinks of a light bulb, thermostat, or doorbell as "a computer that needs security," so it never gets treated like one. The device has no screen to prompt you for a password change, no icon in your mental model of "things I should patch," and often no vendor still supporting it a few years in. Every weakness in this skill, default credentials nobody changes, firmware nobody updates, ports nobody closes, traces back to that one blind spot in how people categorize what counts as a computer.

## The big picture
The Mirai botnet is worth remembering not as a scary anecdote but as proof of a genuinely counterintuitive idea: individually worthless devices become collectively catastrophic purely through scale, with no sophistication required at all, just a scanner trying the same three or four factory passwords against every IP address on the internet. That should reshape how you think about "shadow IoT" as a risk category: it's not dangerous because any one unapproved smart plug is powerful, it's dangerous because attack surface is additive and invisible devices can't be hardened by a team that doesn't know they exist. Hold onto that connection into 4.3.a, where device hardening turns out to be the direct answer to exactly the first two bullet points here, change every default credential, close every unnecessary port, applied as a discipline to *every* device, not just the traditional laptops and servers a security team is used to thinking about.
