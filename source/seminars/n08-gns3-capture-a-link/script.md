# Lecture script: Network lab 8: Capture a link (Network Emulator)

Network lab · about 40 minutes of lab work · about 5 minutes of narration

This is what `python tools/teach.py demo n08-gns3-capture-a-link` plays and captions, word for word, and what the voice studio
(`python tools/teach.py voice n08-gns3-capture-a-link`) shows you to read. Edit the words in seminar.json, then run
`python tools/teach.py script n08-gns3-capture-a-link` to refresh this file.

## Opening

Welcome to network lab eight, the last one. Until now the programs have told us whether a ping worked. Today we look at the packets ourselves. We'll build a tiny network in Network Emulator, put a capture on the cable, and watch ARP and ping happen, field by field. It's the same skill a security analyst uses on recorded evidence, and it starts with knowing what normal looks like.

## 1. Open Network Emulator, start and link three nodes

Step one: open Network Emulator, start and link three nodes. In the Hacker Room, open Start, Workplace, Network lab, and pick lab eight. Two VPCS computers and an Ethernet switch are already on the canvas, and they're stopped. Press Start all. Then press Add a link, click PC1, then SW1, pick the ports and press Connect. Do the same for PC2.

*After it runs:*

All three nodes turn green in the topology summary, and so do the ends of the links. In an emulator, nodes behave like real machines: they have to be running before they do anything, and a stopped node shows red at the end of its links. VPCS stands for Virtual PC Simulator. It isn't a full computer, just enough of one to have an address, ping and trace. That's all we need, and it starts in a second. Network engineers use emulators to test real router software before it goes near a live network; today we use only the lightest parts. The simple built-in computers are called VPCS.

On screen: the step text.

## 2. Give the computers addresses

Step two: give the computers addresses. Double-click PC1 to open its console. Type ip 10.0.0.1/24 10.0.0.254. Open PC2's console and type ip 10.0.0.2/24 10.0.0.254. Then check each one with show ip.

*After it runs:*

The ip command takes the address with its prefix length, then the gateway. VPCS checks first that nobody else has the address, and prints Checking for duplicate address. Slash twenty-four is the short way to write 255.255.255.0, the same mask as in every lab so far. The gateway, 10.0.0.254, doesn't exist here; we set it out of good habit, and nothing leaves this network today. show ip prints the name, the address, the gateway and the MAC address VPCS gave the PC. Note PC2's MAC: you'll see it again in a minute. Each console has its own tab, so you can switch between them. The command is show ip.

On screen: the step text.

## 3. Capture and read the packets

Step three: capture and read the packets. Right-click the link between PC1 and SW1 and choose Start capture. In PC1's console, type ping 10.0.0.2. Open the Capture tab, type arp in the display filter box and press Enter, and click the first row. Then change the filter to icmp. Click an echo request and read Internet Control Message Protocol in the details, then click a reply and read its time to live.

*After it runs:*

The arp filter leaves two rows, just like lab one, but now you're reading the packets yourself. PC1 asks: who has 10.0.0.2? Tell 10.0.0.1. Its Ethernet destination is ff:ff:ff:ff:ff:ff, the broadcast address, which is how the switch knows to send it out of every port. PC2 replies: 10.0.0.2 is at, followed by the MAC address you noted, and that reply goes straight back to PC1's own MAC. The icmp filter shows the echo request and echo reply pairs; VPCS sends five pings, so five pairs, with the sequence numbers counting up. In the details of a request, the ICMP type is 8, echo request. A reply is type 0. And the reply's time to live is 64, the starting value for this kind of computer, with no router in between to take any off. This is what normal looks like. When you meet a capture with ARP replies nobody asked for, or pings carrying far more data than a ping needs, you'll notice, because you know this picture. If you want one more, ping 10.0.0.9, an address nobody has. VPCS says host not reachable, and the capture shows ARP asking again and again, and no echo request at all, because PC1 never found anyone to send it to. The answers are 8, ARP, and 64.

On screen: the step text.

## 4. Where next

That's the end of the network labs. You captured packets on a link you built. Seminar one, Reading evidence, uses the same skill on recorded evidence from an incident, and the packet cases in Labs build on it.

On screen: the step text.

## Wrap-up

Eight labs ago you cabled four computers to a switch. Since then you've routed, named, split, trunked, hardened and filtered a network, and now you've read its packets yourself. Keep the habit from today: when a tool tells you what happened on the wire, capture it and look. See you in the seminars.

## YouTube chapters (estimate; `python tools/teach.py demo n08-gns3-capture-a-link` writes the exact ones)

```
0:00 Opening
0:38 1. Open Network Emulator, start and link three nodes
1:46 2. Give the computers addresses
2:42 3. Capture and read the packets
4:37 4. Where next
4:52 Wrap-up
```
