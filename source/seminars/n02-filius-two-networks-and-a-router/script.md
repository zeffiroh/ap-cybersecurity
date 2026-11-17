# Lecture script: Network lab 2: Two networks and a router (Filius)

Network lab · about 40 minutes of lab work · about 5 minutes of narration

This is what `python tools/teach.py demo n02-filius-two-networks-and-a-router` plays and captions, word for word, and what the voice studio
(`python tools/teach.py voice n02-filius-two-networks-and-a-router`) shows you to read. Edit the words in seminar.json, then run
`python tools/teach.py script n02-filius-two-networks-and-a-router` to refresh this file.

## Opening

Welcome to network lab two. Banyan Books has opened a back office, and the owner wants it on its own network: the tills in the shop on one, accounts and the manager's computer on the other. As you saw in lab one, two networks can't talk through a switch. They need a router. Today we build both networks, join them with a router, and meet the one setting that makes it work: the gateway. Then we break it on purpose, so you'll recognise the fault when you meet it for real.

## 1. Build both networks

Step one: build both networks. In design mode, place two computers and a switch for the shop, and two computers and a switch for the back office. Then add a router between the two switches. Filius asks how many interfaces it should have: give it two, one for each network. Cable the router to both switches, and type the computers' addresses from README.txt.

*After it runs:*

Look at the plan. The shop is 192.168.1, with till-1 and till-2. The back office is 192.168.2, with accounts at 21 and manager at 22. The router sits in both. That's the whole idea of a router: it has one foot in each network, and each foot, each interface, needs its own address in the network it belongs to. A switch doesn't need an address to do its job; a router can't work without them. Why split the office at all? Each network is its own broadcast area: lab one's ARP question goes to everyone on that switch, and stops there. Fewer machines hear each other, and the router becomes the one place where you can decide what crosses. The Packet Tracer labs use exactly that. So the router needs two interfaces.

On screen: the step text.

## 2. Set the gateways

Step two: set the gateways. Click the router. Give interface one 192.168.1.1, and interface two 192.168.2.1, both with netmask 255.255.255.0. Check which interface is cabled to which switch, so the shop side really gets the shop address. Then click every computer and fill in its gateway: 192.168.1.1 in the shop, 192.168.2.1 in the back office.

*After it runs:*

The gateway is where a computer sends anything that isn't in its own network. When till-1 wants accounts, it does the same check as in lab one: 192.168.2.21 isn't local. But this time it has somewhere to send it, the router's address on its own side. Notice the gateway always has to be inside the computer's own network. till-1 can't use 192.168.2.1 as its gateway, because reaching that address needs the router, and the router is exactly what it's trying to reach. A quick self-check: for each computer, the first three numbers of its gateway must match the first three numbers of its own address. So till-1's gateway is 192.168.1.1, and the device that carries packets between the networks is the router.

On screen: the step text.

## 3. Ping across, then break a gateway

Step three: ping across, then break a gateway. Run the simulation. Install the command line on till-1 and ping accounts at 192.168.2.21. While it runs, open Show data exchange on the router. Then go back to design mode, delete manager's gateway, run again, and test manager twice: once to accounts, once to till-1.

*After it runs:*

The ping across answers. On the router you see the same packet twice: it arrives on one interface from the shop and leaves on the other into the back office, and the reply makes the trip the other way. Now manager, with no gateway. Manager to accounts still works: same network, no router needed. Manager to till-1 fails, because manager has nowhere to send it. This is one of the most common faults on a real help desk. Someone says: I can print, but I can't get to the internet. The printer is local; the internet is through the gateway. So without a gateway, manager can't reach till-1. Put the gateway back before you finish.

On screen: the step text.

## 4. Where next

That's lab two. Two networks, one router, and the gateway setting that joins them. In lab three the network gets names: a web server, a DNS server, and a fault you'll find the way a help desk does.

On screen: the step text.

## Wrap-up

Keep these from today. A router has an address in every network it joins. Every computer needs a gateway to leave its own network, and that gateway must be in its own network. And when far-away things fail while nearby things work, check the gateway first. See you in lab three.

## YouTube chapters (estimate; `python tools/teach.py demo n02-filius-two-networks-and-a-router` writes the exact ones)

```
0:00 Opening
0:47 1. Build both networks
2:05 2. Set the gateways
3:16 3. Ping across, then break a gateway
4:23 4. Where next
4:38 Wrap-up
```
