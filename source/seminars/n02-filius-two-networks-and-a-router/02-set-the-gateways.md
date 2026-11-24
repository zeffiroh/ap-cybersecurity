## 2. Set the router and the gateways

Click the router: its panel lists its interfaces. Give **G0/0** `192.168.1.1/24` and **G0/1** `192.168.2.1/24`. Now click each computer and type its address from README.txt and its **Default gateway**: shop computers use 192.168.1.1, back-office computers use 192.168.2.1.

The gateway is where a computer sends anything that isn't in its own network.

- [ ] Router interfaces set
- [ ] Shop gateways 192.168.1.1
- [ ] Back-office gateways 192.168.2.1

> Hint: A gateway must be inside the computer's own network. 192.168.2.1 is useless as a gateway for till-1.

?> What is till-1's gateway? :: 192.168.1.1

?> Which device carries packets between the two networks: the switch or the router? :: router
