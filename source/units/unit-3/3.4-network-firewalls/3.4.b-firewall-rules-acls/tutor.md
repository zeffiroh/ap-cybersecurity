# 3.4.b tutor notes

Notes for the pre- and post-lecture tutor posts.

## The intuition to hold onto
The one fact worth having memorized before you even open this lecture: order is not a formatting choice in an ACL, it is the entire logic of the ACL. First-match-wins means a firewall stops reading the instant a packet matches any rule, so the identical set of rules written in a different order can produce a completely different, and completely wrong, security outcome, with zero code changed, only the order of lines on a page.

## The big picture
Rule shadowing is the concept to walk away from this skill actually able to *diagnose*, not just define: a broad allow rule sitting above a narrow, more careful deny rule doesn't conflict with that deny rule, it makes it unreachable dead code, and the fix is never to argue about which rule is more correct, it's purely about which one is physically listed first. That's a sharper, more mechanical version of the same lesson 3.3.a taught about misconfigured inter-VLAN routing defeating segmentation: a security boundary that looks correct on paper can be silently defeated by one ordering mistake nobody would notice just by reading the rules in isolation. Tie the implicit deny-all back to 3.2.b's least-privilege framing too, default-deny is least privilege applied to an entire network boundary, permitting only what's explicitly needed and rejecting everything else by default rather than trying to enumerate every possible bad packet, which is a losing game against an adversary who only needs to find the one case you forgot to write a rule for.
