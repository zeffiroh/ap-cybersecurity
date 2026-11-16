NETWORK LAB 2: two networks and a router, in Filius

Banyan Books has opened a back office. Shop and back office are separate networks joined by one router.

Shop network 192.168.1.0/24          Back office 192.168.2.0/24
  till-1   192.168.1.11                  accounts  192.168.2.21
  till-2   192.168.1.12                  manager   192.168.2.22
  router   192.168.1.1 (interface 1)     router    192.168.2.1 (interface 2)
  Netmask 255.255.255.0 everywhere. Gateway: the router's address on your own side.

Filius is free and open source, made for school network lessons. Download it from https://www.lernsoftware-filius.de (Windows installer, or the .zip that runs anywhere with Java). Start it and pick English.
