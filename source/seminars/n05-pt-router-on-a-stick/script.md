# Lecture script: Network lab 5: Routing between VLANs (Packet Tracer)

Network lab · about 50 minutes · in Packet Tracer, a free program on your own computer

Read it aloud while you show the program on screen, or record your screen with the Teaching Desk. The captions are this text, word for word.

## Opening

VLANs keep people apart. Sometimes they need to meet, through a router we control. Today: one trunk, two subinterfaces, two gateways.

## 1. A trunk to the router

Open your lab 4 file and save a copy. Add a 1941 (or 2911) router and cable switch Gi0/1 to router G0/0. On the switch CLI: Type the commands on screen, then check the result with the show command.

On screen: Packet Tracer, then the step's questions here.

## 2. A gateway per VLAN

On the router CLI: Type the commands on screen, then check the result with the show command.

On screen: Packet Tracer, then the step's questions here.

## 3. Test, and notice the new risk

From guest-1, ping staff-1 (192.168.10.11). It works now, because the router joins the VLANs. Good for printing; bad for security: guests can reach staff computers again.

On screen: Packet Tracer, then the step's questions here.

## 4. Where next

VLANs, a trunk and a router. Before the access list, lab 6 hardens the switch itself.

On screen: Packet Tracer, then the step's questions here.

## Closing

Routing joins the VLANs again, which is exactly why the next labs add switch hardening and access lists.
