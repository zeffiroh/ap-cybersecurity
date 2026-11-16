# Lecture script: Network lab 6: Lock down the switch (Packet Tracer)

Network lab · about 45 minutes · in Packet Tracer, a free program on your own computer

Read it aloud while you show the program on screen, or record your screen with the Teaching Desk. The captions are this text, word for word.

## Opening

A switch with every port live and no passwords is an open building. Today we shut the empty doors, allow one known device per desk, and lock the management access.

## 1. Park and shut the unused ports

A live, empty wall port is an open door: anyone can plug in. On the switch: Type the commands on screen, then check the result with the show command.

On screen: Packet Tracer, then the step's questions here.

## 2. One known device per staff port

 Type the commands on screen, then check the result with the show command.

On screen: Packet Tracer, then the step's questions here.

## 3. Plug in an unknown laptop

Unplug staff-2 from Fa0/2 and plug a new Laptop into Fa0/2 instead. Give it 192.168.10.50 and ping staff-1. Look at the link light, then run show interfaces status and show port-security interface fa0/2.

On screen: Packet Tracer, then the step's questions here.

## 4. Protect the management access

Anyone with a console cable could change all of this. Add passwords: Type the commands on screen, then check the result with the show command.

On screen: Packet Tracer, then the step's questions here.

## 5. Where next

Unused ports shut, known devices only, management protected. Lab 7 adds the access list that keeps guests away from staff.

On screen: Packet Tracer, then the step's questions here.

## Closing

Hardening is a short checklist done every time. Next, an access list that keeps guests out of staff systems.
