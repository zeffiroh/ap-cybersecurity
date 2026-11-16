# Lecture script: Network lab 2: Two networks and a router (Filius)

Network lab · about 40 minutes · in Filius, a free program on your own computer

Read it aloud while you show the program on screen, or record your screen with the Teaching Desk. The captions are this text, word for word.

## Opening

In this lab we join two networks with a router. The key setting is the gateway, and we'll break it on purpose to see what it does.

## 1. Build both networks

In this lab we join two networks with a router. The key setting is the gateway, and we'll break it on purpose to see what it does.

On screen: Filius, then the step's questions here.

## 2. Set the gateways

Click the router and give interface 1 192.168.1.1 and interface 2 192.168.2.1, both with netmask 255.255.255.0. Now set every computer's Gateway: shop computers use 192.168.1.1, back-office computers use 192.168.2.1.

On screen: Filius, then the step's questions here.

## 3. Ping across, then break a gateway

Run the simulation. From till-1, ping accounts at 192.168.2.21: it answers. Open Show data exchange on the router while you ping, and see the same packet arrive on one interface and leave on the other.

On screen: Filius, then the step's questions here.

## 4. Where next

Two networks, one router, and the setting that joins them. Network lab 3 adds names: a DNS server and a web server, then a fault to find.

On screen: Filius, then the step's questions here.

## Closing

Every computer needs a gateway to leave its own network. Next: names, a web server, and a fault to find.
