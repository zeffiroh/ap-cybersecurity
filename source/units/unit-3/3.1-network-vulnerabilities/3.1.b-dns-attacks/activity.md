# In-class activity, 3.1.b DNS attacks (spoofing, cache poisoning)

**Format:** small group (3-4) · **Time:** 25 min · **Offline:** yes

## Goal
Groups act as SOC analysts reviewing a resolver's reply log to decide, for each outstanding
query, whether the resolver ends up caching a legitimate answer, gets poisoned, or correctly
rejects a mismatched reply, then propose one concrete mitigation. Ties to LO 3.1.A, 3.1.B and
the course skills Analyze Risk, Detect Attacks.

## Materials (all local)
- the SimLab simulation on each machine, or the printed log below.

## Reply log (print or project)

| # | qname | query tx_id/port | reply 1 (from, tx_id, port, qname, arrival) | reply 2 (from, tx_id, port, qname, arrival) | Verdict? |
|---|-------|-------------------|----------------------------------------------|----------------------------------------------|----------|
| 1 | pay.example | 4410 / 51000 | attacker, 4410, 51000, pay.example, arrival 1 | authoritative, 4410, 51000, pay.example, arrival 2 | ? |
| 2 | app.example | 8821 / 60010 | attacker, 1111, 60010, app.example, arrival 1 | authoritative, 8821, 60010, app.example, arrival 2 | ? |
| 3 | id.example | 2290 / 33221 | attacker, 2290, 40000, id.example, arrival 1 | (none) | ? |
| 4 | cdn.example | 7710 / 12000 | authoritative, 7710, 12000, cdn.example, arrival 1 | attacker, 7710, 12000, cdn.example, arrival 2 | ? |

## Steps
1. (5 min) Each group reads rows 1-2 individually: for each, check whether tx_id AND port AND
   qname all match the query for every reply, in arrival order, and decide the verdict (WIN /
   POISON / REJECT).
2. (5 min) Group discusses row 3: only one reply arrived, and it has the wrong port. What happens
   to the query? Is this REJECT the "safe" outcome or does the resolver just retry?
3. (7 min) Group works row 4: the legitimate reply arrived first this time. Discuss why arrival
   order, not just "does the attacker eventually send a matching reply", is what determines the
   winner.
4. (5 min) Each group opens the simulation and checks their calls against the sim's scoring for
   analogous scenarios; groups revise any incorrect calls.
5. (3 min) Report-out: each group proposes one mitigation (source-port randomization, DNSSEC, or
   DoH/DoT) and states specifically which field(s) in the log that mitigation would have changed.

## Collaborate (AP skill 4)
Assign roles: one member is the "resolver" (applies the tx_id/port/qname matching rule literally,
in arrival order), one is the "attacker" (explains what the attacker would have needed to guess
correctly to win each row), and remaining members are "auditors" (check the resolver's and
attacker's reasoning against the three-field matching rule from the lesson). For row 1, the group
must specifically explain why a wide open source port (guessable) made the poisoning possible, and
what changes if source-port randomization is added.

## Exit ticket
Each student writes one sentence: "Row X is [WIN / POISON / REJECT] because [tx_id / port / qname]
[matched / did not match] and [reasoning about arrival order]."

## Answer key (instructor only)

| # | Verdict | Reasoning |
|---|---------|-----------|
| 1 | POISON | All three fields match on both replies; attacker's forged reply arrived first and is cached. |
| 2 | WIN | Attacker's reply has the wrong tx_id (1111 vs 8821) so it's rejected as a candidate; the authoritative reply matches and is cached. |
| 3 | REJECT | Only reply has the wrong port (40000 vs 33221), no valid candidate, nothing cached. |
| 4 | WIN | Both replies match all three fields, but the legitimate reply arrived first (arrival 1) and is cached before the attacker's later reply arrives. |

## Instructor notes
- Timing: rows 1-2 are the core matching-rule cases; row 3 tests the "no valid candidate" case;
  row 4 is the deliberate teaching moment that arrival order, not merely matching, decides the
  winner when both replies are valid.
- Common stumble: students assume any attacker reply that "shows up" in the log wins, without
  checking that all three fields (tx_id, port, qname) match the outstanding query.
- A second common stumble: students think REJECT is a form of poisoning being "close", reinforce
  that REJECT means nothing was cached at all.
- Feeds forward to 3.1.c (MITM/ARP spoofing) and 3.1.d (packet capture), which use the same
  discipline of checking exact field matches in captured traffic.
