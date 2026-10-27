# In-class activity, 3.4.b Firewall rules and access control lists (ACLs)

**Format:** pairs · **Time:** 25 min · **Offline:** yes

## Goal
Students trace first-match-wins ACL evaluation by hand, identify a rule-shadowing bug in a
Meridian High School perimeter ACL, and fix it by reordering (not rewriting) rules. Ties to
LO 3.4.B / 3.4.C (write and evaluate firewall ACLs; identify rule-ordering vulnerabilities).

## Materials (all local)
- the SimLab simulation on each machine, or the printed ACL and packet table below.

## Steps
1. **Trace it (10 min).** Each pair receives the broken ACL and packet table below. Working
   top to bottom, they apply first-match-wins to each packet and record the verdict and which
   rule number fired.

2. **Find the bug (7 min).** Pairs identify which packet(s) got the "wrong" verdict relative to
   the security intent stated in the rule comments, and name the shadowing rule pair (which rule
   is too broad, and which rule below it never fires).

3. **Fix it (8 min).** Pairs reorder the ACL (moving rules, not rewriting their conditions) so
   every packet gets its intended verdict. They re-trace all packets against the new order to
   confirm.

## Printed ACL and packet table (deterministic)
```
# Rule set (apply top to bottom, first match wins) — as originally written (BUGGY)
Rule 1: ALLOW  TCP  any          -> any            port 22   (temporary SSH access, meant to be removed)
Rule 2: ALLOW  TCP  any          -> 10.0.1.5        port 443  (HTTPS to web server)
Rule 3: DENY   TCP  203.0.113.0  -> 10.0.1.10        port 22   (block known-hostile range from file server SSH)
Rule 4: ALLOW  TCP  10.0.4.0     -> 10.0.1.5        port 3306 (accounting subnet to DB)
Rule 5: DENY   any  any          -> any             any       (implicit deny-all)

Pkt  Src           Dst          Port  Proto  Security intent
A    203.0.113.0   10.0.1.10    22    TCP    Should be DENIED (hostile range, SSH to file server)
B    10.0.4.0      10.0.1.5     3306  TCP    Should be ALLOWED (accounting to DB)
C    198.51.100.9  10.0.1.5     443   TCP    Should be ALLOWED (HTTPS)
D    10.0.9.9      10.0.1.5     3306  TCP    Should be DENIED (not accounting subnet)
```

Traced (buggy) verdicts: A=ALLOW (rule 1 fires first, WRONG, intent was DENY), B=ALLOW (rule 4),
C=ALLOW (rule 2), D=DENY (rule 5, implicit deny). Packet A is the shadowing bug: rule 1 is too
broad and matches before rule 3 is ever reached.

## Collaborate (AP skill 4)
Assign roles: one partner is the "auditor" (traces verdicts and flags mismatches with intent), the
other is the "firewall admin" (proposes the reordering fix and defends why it does not break any
other packet's verdict). Swap roles and check the fixed ACL against two instructor-supplied packets.

## Exit ticket
Each student writes: the corrected rule order (rule numbers only) and one sentence explaining why
moving rule 3 above rule 1 fixes packet A without changing the verdict for packets B or C.

## Instructor notes
- Expected fix: move rule 3 (the specific deny) above rule 1 (the broad allow). New order:
  3, 1, 2, 4, 5 (or any order where rule 3 precedes rule 1). Re-traced: A=DENY, B=ALLOW, C=ALLOW,
  D=DENY, all match intent.
- Key learning moment: the fix never changes any rule's *content*, only its *position*. Students
  who try to rewrite rule 1's conditions instead of reordering are missing the core lesson.
- Common stumble: students think rule 3 being "more specific" gives it automatic priority. Firmly
  correct this, no such override exists in first-match-wins evaluation.
- Feeds the unit project (firewall rule design) and the scenario stage where students harden a
  simulated network perimeter.
