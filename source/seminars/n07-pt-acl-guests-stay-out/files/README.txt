NETWORK LAB 7: access lists, in Network Simulator

Lab 6 is already done. Two servers are waiting, not yet cabled:

files01  192.168.10.10/24  gateway 192.168.10.1   (staff VLAN, cable to Fa0/3)
web-out  203.0.113.10/24   gateway 203.0.113.1    (stands in for the internet)
  Router G0/1  203.0.113.1/24, cabled to web-out

Policy
  Guests (192.168.20.0/24) may reach web-out on HTTP.
  Guests may not reach anything in 192.168.10.0/24.
  Staff are not restricted.

Where: this lab runs in the Hacker Room's Network Simulator, with its starting network and goals. Nothing to install. In the Hacker Room open Start, Workplace, Network lab and pick this lab, or open netbuilder.json from Files.
