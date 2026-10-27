# In-class activity, 1.3.b Evil twin attack

**Format:** pairs · **Time:** 25 min · **Offline:** yes

## Goal
Students practice the core analytic skill: given a raw wireless scan table (SSID, BSSID,
security level, signal strength), identify which entries are suspicious and justify each
flagged entry by citing a specific indicator. Ties to LO 1.3.B (identify indicators of
evil-twin attacks on public Wi-Fi).

## Materials (all local)
- the SimLab simulation, animated scan list
- `problem/`, coding challenge
- Printed scan table below (or display on the board)

## Printed scan table

| # | SSID             | BSSID             | Security | Signal |
|---|------------------|-------------------|----------|--------|
| 1 | CafeGuest        | AA:BB:CC:11:22:33 | WPA2     | -55    |
| 2 | CafeGuest        | DE:AD:BE:EF:00:01 | OPEN     | -42    |
| 3 | Airport-Free     | 00:11:22:33:44:55 | OPEN     | -70    |
| 4 | Airport-Free     | FF:EE:DD:CC:BB:AA | OPEN     | -48    |
| 5 | CorpNet          | 0A:1B:2C:3D:4E:5F | WPA3     | -60    |
| 6 | HotelLobby       | 11:22:33:44:55:66 | WPA2     | -65    |

## Steps
1. (5 min) Each pair reads the scan table silently and writes down which rows they think are
   suspicious, without discussing yet.
2. (8 min) Partners compare their lists. For each disagreement, argue your case using the
   detection rules from atom.md: same SSID / different BSSID, or same SSID / weaker security.
   Agree on a final answer.
3. (7 min) Open the simulation. Work through its scan rounds. Check whether your reasoning from the
   table translates, the sim uses the same analytic rules.
4. (5 min) One partner reads from the scan table, acting as the "attacker", they explain why
   their evil-twin entry (row 2 or 4) would fool a casual user. The other partner explains the
   defensive response.

## Collaborate (AP skill 4)
Assign roles: one partner is the **WIDS analyst** (identifies and justifies flags), the other
is the **attacker** (argues why each evil twin is convincing to a victim). Swap roles for the
second round. Both record: indicator observed, reason it is suspicious, defensive action.

## Exit ticket
Each student submits one written sentence per suspicious row: name the row, the specific
indicator (duplicate BSSID, security downgrade, etc.), and one action a user could take to
avoid connecting to that AP.

## Instructor notes
- Expected suspicious rows: 2 (CafeGuest OPEN vs. WPA2), 4 (Airport-Free duplicate BSSID, both OPEN, but two BSSIDs for a single-AP public network is suspicious). Row 5 (CorpNet
  single BSSID, WPA3) is intentionally clean; some students flag it anyway, redirect them to
  the rule: a single BSSID alone is not an indicator.
- Common stumble: students flag strong signal as the sole indicator. Clarify: stronger signal
  is a tiebreaker, not a primary indicator, BSSID anomaly and security mismatch are primary.
- Feeds the unit project (wireless risk report) and scenario stage 2 (evil-twin interception).
