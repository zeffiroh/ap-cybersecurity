## 3. Find the fault

Go to design mode and break till-2 in one way: change its gateway to **192.168.1.100**. Now pretend you don't know. On till-2, work up the layers and write what each test shows:

1. `ipconfig`: is the address right?
2. `ping 192.168.1.12` (itself) and `ping 192.168.1.11` (a neighbour): is the local network fine?
3. `ping 192.168.1.1`: is the router there? Compare it with the gateway `ipconfig` showed.
4. `ping 192.168.2.53`, then the site by name.

Fix it and test again.

- [ ] Each test written down with its result
- [ ] The failing layer named
- [ ] Fixed and tested again

> Hint: Work from the bottom up. If the neighbour answers but the other network doesn't, the cable and address are fine: look at the gateway.

?> Which setting was wrong on till-2? (one word) :: gateway
