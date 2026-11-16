# Lecture script: Network lab 4: VLANs for staff and guests (Packet Tracer)

Network lab · about 45 minutes · in Packet Tracer, a free program on your own computer

Read it aloud while you show the program on screen, or record your screen with the Teaching Desk. The captions are this text, word for word.

## Opening

One switch, two kinds of people. In this lab we split a switch into a staff VLAN and a guest VLAN, and prove that a visitor can't reach staff computers even by guessing an address.

## 1. Install Packet Tracer and build the office

One switch, two kinds of people. In this lab we split a switch into a staff VLAN and a guest VLAN, and prove that a visitor can't reach staff computers even by guessing an address.

On screen: Packet Tracer, then the step's questions here.

## 2. Make the VLANs

Click the switch, open the CLI tab, and type: Type the commands on screen, then check the result with the show command.

On screen: Packet Tracer, then the step's questions here.

## 3. Prove the separation

From staff-1's Command Prompt, ping staff-2 (192.168.10.12): it answers. Ping guest-1 (192.168.20.31): it fails.

On screen: Packet Tracer, then the step's questions here.

## 4. Where next

One switch, two separate networks. Guests still need the internet, and that needs a router: lab 5 joins the VLANs on purpose, with control.

On screen: Packet Tracer, then the step's questions here.

## Closing

The switch port decides the VLAN. Next we route between VLANs, on purpose and under control.
