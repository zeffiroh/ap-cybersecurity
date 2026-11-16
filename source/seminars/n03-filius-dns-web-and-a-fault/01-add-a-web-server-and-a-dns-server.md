## 1. Add a web server and a DNS server

Open your lab 2 network and save it under a new name. Add two computers to the back-office switch: **web01** (192.168.2.80) and **dns01** (192.168.2.53), gateway 192.168.2.1.

In simulation mode, install **Web server** on web01 and start it. Install **DNS server** on dns01, add a record **www.banyan.lan → 192.168.2.80** (type A), and start it.

- [ ] web01 and dns01 added with gateways
- [ ] Web server running on web01
- [ ] DNS record www.banyan.lan → 192.168.2.80

> Hint: A DNS "A record" maps a name to an IPv4 address.

?> Which protocol turns www.banyan.lan into an address? (three letters) :: dns
