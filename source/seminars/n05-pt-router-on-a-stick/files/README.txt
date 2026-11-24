NETWORK LAB 5: router on a stick, in Network Simulator

Lab 4 is already done: VLANs 10 and 20, the four PCs cabled and addressed. A 1941 router is waiting, not yet cabled.

Switch Gi0/1  trunk to the router
Router 1941, interface G0/0 (no address on the main interface)
  G0/0.10  VLAN 10  192.168.10.1/24  gateway for staff
  G0/0.20  VLAN 20  192.168.20.1/24  gateway for guests
Every PC: set the gateway for its VLAN.

Where: this lab runs in the Hacker Room's Network Simulator, with its starting network and goals. Nothing to install. In the Hacker Room open Start, Workplace, Network lab and pick this lab, or open netbuilder.json from Files.
