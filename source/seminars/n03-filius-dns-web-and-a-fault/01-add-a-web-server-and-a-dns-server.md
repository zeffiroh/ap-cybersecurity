## 1. Set up a web server and a DNS server

Your lab 2 network is already built, and two servers are cabled to the back-office switch. In **Design** mode, click **web01** and give it 192.168.2.80 with gateway 192.168.2.1, then **dns01**: 192.168.2.53, gateway 192.168.2.1.

Press **Simulation**. Click web01, open **Web server** on its desktop and press **Start**. Click dns01, open **DNS server**, add the record **www.banyan.lan → 192.168.2.80** and press **Add**, then **Start**.

- [ ] web01 and dns01 addressed with gateways
- [ ] Web server running on web01
- [ ] DNS record www.banyan.lan → 192.168.2.80, DNS server running

> Hint: A record that maps a name to an IPv4 address is called an "A record".

?> Which protocol turns www.banyan.lan into an address? (three letters) :: dns
