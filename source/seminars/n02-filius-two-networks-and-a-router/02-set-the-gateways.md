## 2. Set the gateways

Click the router and give interface 1 192.168.1.1 and interface 2 192.168.2.1, both with netmask 255.255.255.0. Now set every computer's **Gateway**: shop computers use 192.168.1.1, back-office computers use 192.168.2.1.

The gateway is where a computer sends anything that isn't in its own network.

- [ ] Router interfaces set
- [ ] Shop gateways 192.168.1.1
- [ ] Back-office gateways 192.168.2.1

> Hint: A gateway must be inside the computer's own network. 192.168.2.1 is useless as a gateway for till-1.

?> What is till-1's gateway? :: 192.168.1.1

?> Which device carries packets between the two networks: the switch or the router? :: router
