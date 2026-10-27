# In-class activity, 3.3.a VLANs and network segmentation

**Format:** pairs · **Time:** 20 min · **Offline:** yes

## Goal
Students design a VLAN segmentation scheme for a small office network, assign hosts to VLANs, and argue which traffic flows should be permitted or blocked. Ties to LO 3.3.A (explain how VLANs segment a network to reduce risk).

## Materials (all local)
- the SimLab simulation on each machine, or the printed host inventory below.
- Paper or whiteboard for drawing the VLAN diagram.

## Printed host inventory (if no laptop)

| Host | Role |
|------|------|
| WS-01, WS-02 | Employee workstations |
| PRT-01 | Department printer |
| SRV-01 | File server |
| SRV-02 | HR payroll database |
| CAM-01 | IP security camera |
| GUEST-01 | Visitor laptop |
| MGMT-01 | Network switch management interface |

## Steps
1. Each pair draws four VLAN boxes on paper (Management, Employee, Server, Guest/IoT) and assigns each host in the inventory to one VLAN. They must be ready to justify each placement.
2. The pair writes three traffic flow statements (e.g., "WS-01 sends a file request to SRV-01") and decides: Allow or Block? They circle their answer and write one sentence of justification.
3. Pairs open the simulation, enter their VLAN assignments, and run the test flows to see whether the sim agrees. For any disagreement, they revise their reasoning.

## Collaborate (AP skill 4)
Assign roles: one partner is the "network designer" (defends the VLAN placement), the other is the "red team analyst" (argues which flows an attacker would try first if they compromised GUEST-01). After step 3, swap roles and repeat with MGMT-01 as the hypothetical target.

## Exit ticket
Each student submits: their finalized VLAN map (4 VLANs, all 7 hosts assigned) plus one sentence explaining why SRV-02 (payroll) should never be reachable from the Guest VLAN even if a firewall rule was accidentally left open.

## Instructor notes
- Expected placement: MGMT-01 in Management; WS-01, WS-02, PRT-01 in Employee; SRV-01, SRV-02 in Server; CAM-01, GUEST-01 in Guest/IoT.
- Common stumble: students place PRT-01 in the Server VLAN. Printers belong with employees, not servers. Printers on the server VLAN create a pivot path into server resources.
- Another stumble: placing CAM-01 on the Employee VLAN because "cameras watch employees." Cameras belong in the IoT VLAN; their firmware is notoriously unpatched and should never share a broadcast domain with workstations.
- This activity feeds the unit project (network hardening design) and scenario stage 3 (containing lateral movement after initial breach).
