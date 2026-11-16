## 3. Ping across, then break a gateway

Run the simulation. From till-1, ping accounts at 192.168.2.21: it answers. Open **Show data exchange** on the router while you ping, and see the same packet arrive on one interface and leave on the other.

Now go back to design mode, delete manager's gateway, and run again. Manager can still ping accounts (same network) but not till-1. Put the gateway back.

- [ ] till-1 to accounts works
- [ ] Router data exchange shows the packet on both interfaces
- [ ] Without a gateway, manager only reaches its own network

> Hint: A missing gateway is one of the most common faults on real help desks: "I can print but I can't reach the internet".

?> Without a gateway, can manager reach till-1? (yes or no) :: no
