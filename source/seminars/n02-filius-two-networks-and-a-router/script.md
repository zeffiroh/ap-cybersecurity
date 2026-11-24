# Lecture script: Network lab 2: Two networks and a router (Network Starter)

Network lab · about 40 minutes of lab work · about 6 minutes of narration

This is what `python tools/teach.py demo n02-filius-two-networks-and-a-router` plays and captions, word for word, and what the voice studio
(`python tools/teach.py voice n02-filius-two-networks-and-a-router`) shows you to read. Edit the words in seminar.json, then run
`python tools/teach.py script n02-filius-two-networks-and-a-router` to refresh this file.

## Opening

Welcome to network lab two. Banyan Books has opened a back office, and the owner wants it on its own network: the tills in the shop on one, accounts and the manager's computer on the other. As you saw in lab one, two networks can't talk through a switch. They need a router. Today we cable both networks, join them with a router, and meet the one setting that makes it work: the gateway. Then we break it on purpose, so you'll recognise the fault when you meet it for real.

## 1. Cable both networks

Step one: cable both networks. The devices are already on the canvas: the shop's two tills and switch on the left, the back office's two computers and switch on the right, and a router in the middle. In Design mode, choose Cable and join each computer to its own switch. Then cable the router, to the shop switch first and the back-office switch second.

*After it runs:*

Why that order? Network Starter cables the first free port, so the router's first interface, G0/0, now faces the shop, and G0/1 faces the back office. Look at the plan. The shop is 192.168.1, with till-1 and till-2. The back office is 192.168.2, with accounts at 21 and manager at 22. The router sits in both. That's the whole idea of a router: it has one foot in each network, and each foot, each interface, needs its own address in the network it belongs to. A switch doesn't need an address to do its job; a router can't work without them. Why split the office at all? Each network is its own broadcast area: lab one's ARP question goes to everyone on that switch, and stops there. Fewer machines hear each other, and the router becomes the one place where you can decide what crosses. So we use two router interfaces.

On screen: the step text.

## 2. Set the router and the gateways

Step two: set the router and the gateways. Click the router. Its panel lists its interfaces. Give G0/0 192.168.1.1 slash 24, and G0/1 192.168.2.1 slash 24. Then click every computer, type its address from the plan, and fill in its default gateway: 192.168.1.1 in the shop, 192.168.2.1 in the back office.

*After it runs:*

Slash 24 is the short way to write the subnet mask 255.255.255.0. The gateway is where a computer sends anything that isn't in its own network. When till-1 wants accounts, it does the same check as in lab one: 192.168.2.21 isn't local. But this time it has somewhere to send it, the router's address on its own side. Notice the gateway always has to be inside the computer's own network. till-1 can't use 192.168.2.1 as its gateway, because reaching that address needs the router, and the router is exactly what it's trying to reach. A quick self-check: for each computer, the first three numbers of its gateway must match the first three numbers of its own address. So till-1's gateway is 192.168.1.1, and the device that carries packets between the networks is the router.

On screen: the step text.

## 3. Ping across, then break a gateway

Step three: ping across, then break a gateway. Press Simulation, click till-1, open Command line, and ping accounts at 192.168.2.21. Then open the Data exchange tab, choose accounts in the list, and click an echo request. After that, press Design, clear manager's gateway, press Simulation, and test manager twice: once to accounts, once to till-1.

*After it runs:*

The ping across answers, and every reply says TTL equals 127. TTL is time to live, a counter that every router takes one off, so a lost packet can't loop for ever. In accounts' data exchange, the echo request from till-1 arrives with a time to live of 127: till-1 sent it with 128, and the router took one off on the way through. Look at its source MAC too. It isn't till-1's any more. The router took the packet off one network and put it on the other with its own hardware address, while the IP addresses stayed the same, from 192.168.1.11 to 192.168.2.21. Now manager, with no gateway. Manager to accounts still works: same network, no router needed. Manager to till-1 says general failure, because manager has nowhere to send it. This is one of the most common faults on a real help desk. Someone says: I can print, but I can't get to the internet. The printer is local; the internet is through the gateway. So without a gateway, manager can't reach till-1, and the time to live at accounts is 127. Put the gateway back before you finish.

On screen: the step text.

## 4. Where next

That's lab two. Two networks, one router, and the gateway setting that joins them. In lab three the network gets names: a web server, a DNS server, and a fault you'll find the way a help desk does.

On screen: the step text.

## Wrap-up

Keep these from today. A router has an address in every network it joins. Every computer needs a gateway to leave its own network, and that gateway must be in its own network. And when far-away things fail while nearby things work, check the gateway first. See you in lab three.

## YouTube chapters (estimate; `python tools/teach.py demo n02-filius-two-networks-and-a-router` writes the exact ones)

```
0:00 Opening
0:47 1. Cable both networks
2:13 2. Set the router and the gateways
3:27 3. Ping across, then break a gateway
5:06 4. Where next
5:21 Wrap-up
```
