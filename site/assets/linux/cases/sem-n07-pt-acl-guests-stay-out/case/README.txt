NETWORK LAB 7: access lists, in Packet Tracer

Start from your lab 6 file.

Add a Server-PT  files01  192.168.10.10/24  gateway 192.168.10.1   (staff VLAN)
Add a Server-PT  web-out  203.0.113.10/24   gateway 203.0.113.1    (stands in for the internet)
  Router G0/1  203.0.113.1/24, cabled to web-out

Policy
  Guests (192.168.20.0/24) may reach web-out on HTTP.
  Guests may not reach anything in 192.168.10.0/24.
  Staff are not restricted.

Cisco Packet Tracer is free with a Cisco Networking Academy account. Sign up at https://www.netacad.com, enrol in the free "Getting Started with Cisco Packet Tracer" course, and download it from the course page (Windows, macOS or Linux).
