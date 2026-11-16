# Lecture script: Network lab 7: An access list that keeps guests out (Packet Tracer)

Network lab · about 50 minutes · in Packet Tracer, a free program on your own computer

Read it aloud while you show the program on screen, or record your screen with the Teaching Desk. The captions are this text, word for word.

## Opening

Today we turn a written rule into a working one: guests get the web, and never staff systems. Then we test both sides, because a rule you haven't tested is a guess.

## 1. Add the servers

Today we turn a written rule into a working one: guests get the web, and never staff systems. Then we test both sides, because a rule you haven't tested is a guess.

On screen: Packet Tracer, then the step's questions here.

## 2. Write the access list

On the router: Type the commands on screen, then check the result with the show command.

On screen: Packet Tracer, then the step's questions here.

## 3. Test both sides

From guest-1: open web-out in the browser (allowed) and ping files01 (blocked). From staff-1: ping files01 and open web-out (both still fine). Run show access-lists again: the counters show which rule matched each test.

On screen: Packet Tracer, then the step's questions here.

## 4. Where next

Segmentation with VLANs, hardened switch ports, and an access list that enforces a written policy. The GNS3 lab shows the same traffic as real packets in Wireshark.

On screen: Packet Tracer, then the step's questions here.

## Closing

Policy, rule, test, counters. That's how every firewall change should go.
