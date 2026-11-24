NETWORK LAB 4: VLANs, in Network Simulator

Tulsi Travels' front office has one 24-port switch. Staff and visiting customers must not share a network.

VLAN 10  STAFF   ports Fa0/1 to Fa0/12   192.168.10.0/24
VLAN 20  GUEST   ports Fa0/13 to Fa0/20  192.168.20.0/24

staff-1  Fa0/1   192.168.10.11/24
staff-2  Fa0/2   192.168.10.12/24
guest-1  Fa0/13  192.168.20.31/24
guest-2  Fa0/14  192.168.20.32/24

Network Simulator speaks the real switch and router commands (IOS). Double-click a switch for its CLI, or a PC for its Command Prompt.

Where: this lab runs in the Hacker Room's Network Simulator, with its starting network and goals. Nothing to install. In the Hacker Room open Start, Workplace, Network lab and pick this lab, or open netbuilder.json from Files.
