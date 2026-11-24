NETWORK LAB 2: two networks and a router, in Network Starter

Banyan Books has opened a back office. Shop and back office are separate networks joined by one router.

Shop network 192.168.1.0/24          Back office 192.168.2.0/24
  till-1   192.168.1.11                  accounts  192.168.2.21
  till-2   192.168.1.12                  manager   192.168.2.22
  router   192.168.1.1 (G0/0)            router    192.168.2.1 (G0/1)
  Subnet mask 255.255.255.0 everywhere. Gateway: the router's address on your own side.

Cable the router to the shop switch first, so G0/0 faces the shop.

Where: this lab runs in the Hacker Room's Network Starter, with its starting network and goals. Nothing to install. In the Hacker Room open Start, Workplace, Network lab and pick this lab, or open netbuilder.json from Files.
