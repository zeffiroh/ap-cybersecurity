Saffron Dental Care, Kochi. Saturday 14 November 2026. The clinic is closed today. All times UTC (India is UTC+5:30).

You are the IT contractor on the monthly security visit. The practice manager, Anita Thomas, asked for three things:
  1. Find anything on the network that shouldn't be there.
  2. Close the doors that don't need to be open.
  3. Keep the waiting-room Wi-Fi away from patient records.

gw.saffron.lan      10.40.0.1    the internet router and firewall
sw1.saffron.lan     10.40.0.2    the switch in the comms cupboard
nas01.saffron.lan   10.40.0.10   file server: patient records, X-ray images
recep-pc            10.40.0.21   reception PC
dr-pc               10.40.0.22   dentist's PC
xray-pc             10.40.0.23   X-ray workstation
printer             10.40.0.30   reception printer
cam-nvr             10.40.0.40   CCTV recorder
Guest Wi-Fi         10.40.1.0/24 the waiting room network

What you have:
  inventory.csv        the clinic's own list of its devices
  switch-ports.txt     which wall socket each switch port goes to, and whether it is live
  dhcp-leases.txt      the router's list of addresses it has handed out
  conn.csv             a week of connection counts from the router
  firewall-rules.txt   the router's rules today
