# Lecture script: Network lab 8: Capture a link in Wireshark (GNS3)

Network lab · about 40 minutes · in GNS3, a free program on your own computer

Read it aloud while you show the program on screen, or record your screen with the Teaching Desk. The captions are this text, word for word.

## Opening

In this lab we build a tiny network in GNS3 and put a capture on the cable, so you can watch ARP and ping happen in Wireshark.

## 1. Install GNS3 and place three nodes

In this lab we build a tiny network in GNS3 and put a capture on the cable, so you can watch ARP and ping happen in Wireshark.

On screen: GNS3, then the step's questions here.

## 2. Give the computers addresses

Right-click PC1 → Console, and type ip 10.0.0.1/24 10.0.0.254. On PC2: ip 10.0.0.2/24 10.0.0.254. Check with show ip.

On screen: GNS3, then the step's questions here.

## 3. Capture and read the packets

Right-click the link between PC1 and SW1 → Start capture. Wireshark opens. On PC1, type ping 10.0.0.2. In Wireshark, type the display filter arp || icmp and read the list from the top: an ARP request (who has 10.0.0.2?), an ARP reply, then ICMP Echo (ping) request and reply pairs. Click one echo request and open Internet Control Message Protocol in the details pane to see its type.

On screen: GNS3, then the step's questions here.

## 4. Where next

You captured real packets on a link you built, the same skill the packet labs and Seminar 1 use on recorded evidence.

On screen: GNS3, then the step's questions here.

## Closing

Every packet lab starts here: know what normal ARP and ICMP look like, and the odd ones stand out.
