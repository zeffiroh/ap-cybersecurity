# Lecture script: Network lab 6: Lock down the switch (Network Simulator)

Network lab · about 45 minutes of lab work · about 5 minutes of narration

This is what `python tools/teach.py demo n06-pt-lock-down-the-switch` plays and captions, word for word, and what the voice studio
(`python tools/teach.py voice n06-pt-lock-down-the-switch`) shows you to read. Edit the words in seminar.json, then run
`python tools/teach.py script n06-pt-lock-down-the-switch` to refresh this file.

## Opening

Welcome to network lab six. Think of Tulsi Travels' switch as a building. Right now every door is unlocked, even in the empty rooms, and the key to the building manager's office hangs on the front door. Today we fix that with the short checklist network teams run on every new switch: shut the unused ports, allow one known device per staff desk, and lock the management access. Then we try to get in with an unknown laptop. Lab five's network is already built for you.

## 1. Park and shut the unused ports

Step one: park and shut the unused ports. Double-click the switch for its CLI. Create VLAN 999 and name it PARKING. Then take ports 21 to 24, make them access ports in VLAN 999, and shut them down. End, then show interfaces status.

*After it runs:*

Ports 21 to 24 now show as disabled, in VLAN 999. Why both, the parking VLAN and the shutdown? A live wall port in an empty office is an open door: anyone can plug in a laptop and they're on the network. Shutting the port closes the door. Parking it in a VLAN that leads nowhere means that if someone turns it back on by mistake, it still connects to nothing. Two locks, because one of them will fail one day. The command that switches a port off is shutdown.

On screen: the step text.

## 2. One known device per staff port

Step two: one known device per staff port. On ports 1 to 12, turn on port security, set the maximum to one MAC address, make it sticky, and set the violation action to shutdown. Then, from staff-1's Command Prompt, ping staff-2 at 192.168.10.12, so both ports hear from their computers. Finally, run show port-security on the switch.

*After it runs:*

show port-security lists Fa0/1 to Fa0/12, each with a maximum of one secure address and the action Shutdown. Fa0/1 and Fa0/2 show one current address each: staff-1 and staff-2. Sticky means the switch keeps the first MAC address it saw on the port and writes it into the running configuration, so it stays. That's why the ping matters on a real switch: a port that has never heard from its computer would simply learn whoever plugs in first. From now on each staff port accepts its own computer and nothing else. Each staff port may learn one MAC address.

On screen: the step text.

## 3. Plug in an unknown laptop

Step three: plug in an unknown laptop. Click the cable between staff-2 and the switch and press Unplug it. Add a laptop from the bar, give it 192.168.10.50, and cable it to Fa0/2 with Copper Straight-Through. Ping staff-1 from the laptop, and watch the link light. Then, on the switch, run show interfaces status and show port-security.

*After it runs:*

The ping fails, and the light on Fa0/2 turns red. show interfaces status says err-disabled. show port-security shows a security violation count of one on Fa0/2. The switch saw an unknown device on a port that allows one known one, and shut the port, exactly as we told it to. In real life, that's someone unplugging the office PC to plug in their own machine, and the network saying no. To bring the port back once you've checked who it was, unplug the laptop, plug staff-2 back in, then on interface fa0/2 type shutdown, and then no shutdown. On a real switch, the port stays err-disabled until you do. The blocked port's status is err-disabled.

On screen: the step text.

## 4. Protect the management access

Step four: protect the management access. Anyone with a console cable could undo everything we just did. So in configuration mode, set an enable secret. Then go to line console 0, set a password, and type login, so the password is actually asked for. End, save with copy running-config startup-config, and then look at show running-config.

*After it runs:*

The save prints Building configuration, then OK. At the top of the running configuration you'll see enable secret 5, followed by a scrambled string, not the word you typed. Two details matter. Use enable secret, never the older enable password: the secret is stored as a one-way hash, while enable password sits in the configuration in plain text, or behind a weak scramble that's easy to reverse. And save. The running configuration lives in memory; if the switch restarts before you copy it to the startup configuration, today's work is gone. The save command is copy running-config startup-config. Choose your own passwords, and write them in your notes, not in the lab files.

On screen: the step text.

## 5. Where next

That's lab six: unused ports shut and parked, one known device per desk, and management locked and saved. Lab seven adds the access list that keeps guests away from staff.

On screen: the step text.

## Wrap-up

Hardening isn't clever. It's a short checklist done every time: shut what you don't use, allow only what you know, lock the management, save the configuration. When one of those steps is skipped, an intruder rarely needs anything clever either. See you in lab seven.

## YouTube chapters (estimate; `python tools/teach.py demo n06-pt-lock-down-the-switch` writes the exact ones)

```
0:00 Opening
0:45 1. Park and shut the unused ports
1:38 2. One known device per staff port
2:41 3. Plug in an unknown laptop
3:49 4. Protect the management access
4:57 5. Where next
5:09 Wrap-up
```
