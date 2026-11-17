# Lecture script: Network lab 8: Capture a link in Wireshark (GNS3)

Network lab · about 40 minutes of lab work · about 5 minutes of narration

This is what `python tools/teach.py demo n08-gns3-capture-a-link` plays and captions, word for word, and what the voice studio
(`python tools/teach.py voice n08-gns3-capture-a-link`) shows you to read. Edit the words in seminar.json, then run
`python tools/teach.py script n08-gns3-capture-a-link` to refresh this file.

## Opening

Welcome to network lab eight, the last one. Until now we've trusted the simulator to tell us what the packets were doing. Today we look at them ourselves. We'll build a tiny network in GNS3, put a capture on the cable, and watch ARP and ping happen in Wireshark, field by field. It's the same skill a security analyst uses on recorded evidence, and it starts with knowing what normal looks like.

## 1. Install GNS3 and place three nodes

Step one: install GNS3 and place three nodes. GNS3 is free and open source. Download it from gns3.com, which asks for a free account, and say yes when the installer offers Wireshark. We only use GNS3's built-in parts, so you don't need router images or the GNS3 virtual machine; if it asks where to run nodes, choose your own computer. Start a new project. From End devices, drag two VPCS nodes; from Switches, one Ethernet switch. Use Add a link to join each VPCS to the switch, then press the green Start button.

*After it runs:*

All three nodes turn green in the topology summary, and so do the ends of the links. VPCS stands for Virtual PC Simulator. It isn't a full computer, just enough of one to have an address, ping and trace. That's all we need, and it starts in a second. Network engineers use GNS3 to test real router software before it goes near a live network; today we use only its lightest parts. GNS3's built-in simple computers are called VPCS.

On screen: the step text.

## 2. Give the computers addresses

Step two: give the computers addresses. Right-click PC1 and choose Console. Type ip 10.0.0.1/24 10.0.0.254. Open PC2's console and type ip 10.0.0.2/24 10.0.0.254. Then check each one with show ip.

*After it runs:*

The ip command takes the address with its prefix length, then the gateway. VPCS checks first that nobody else has the address, which takes a moment. Slash twenty-four is the short way to write 255.255.255.0, the same mask as in every lab so far. The gateway, 10.0.0.254, doesn't exist here; we set it out of good habit, and nothing leaves this network today. show ip prints the name, the address, the gateway and the MAC address VPCS gave the PC. Note PC2's MAC: you'll see it again in a minute. The command is show ip.

On screen: the step text.

## 3. Capture and read the packets

Step three: capture and read the packets. Right-click the link between PC1 and SW1 and choose Start capture. Wireshark opens. On PC1, type ping 10.0.0.2. In Wireshark, type the display filter arp, two vertical bars, icmp, and press Enter. Read the list from the top. Then click one echo request, and in the details pane open Internet Control Message Protocol.

*After it runs:*

The first two lines are ARP, just like lab one, but now you're reading the real packets. PC1 asks everyone: who has 10.0.0.2? Tell 10.0.0.1. PC2 replies: 10.0.0.2 is at, followed by the MAC address you noted. Then come the echo request and echo reply pairs; VPCS sends five pings by default, so five pairs. In the details of a request, the ICMP type is 8, echo request. A reply is type 0. Now open the Ethernet layer of the ARP request: its destination is ff:ff:ff:ff:ff:ff, the broadcast address, which is how the switch knows to send it out of every port. The reply goes straight back to PC1's own MAC. Notice the sequence numbers counting up, and Wireshark linking each reply to the request it answers. This is what normal looks like. When you meet a capture with ARP replies nobody asked for, or pings carrying far more data than a ping needs, you'll notice, because you know this picture. If you want one more, ping 10.0.0.9, an address nobody has. You'll see ARP asking again and again, and no echo request at all, because PC1 never found anyone to send it to. The answers are 8, and ARP.

On screen: the step text.

## 4. Where next

That's the end of the network labs. You captured real packets on a link you built. Seminar one, Reading evidence, uses the same skill on recorded evidence from an incident, and the packet cases in Labs build on it.

On screen: the step text.

## Wrap-up

Eight labs ago you cabled four computers to a switch. Since then you've routed, named, split, trunked, hardened and filtered a network, and now you've read its packets yourself. Keep the habit from today: when a tool tells you what happened on the wire, capture it and look. See you in the seminars.

## YouTube chapters (estimate; `python tools/teach.py demo n08-gns3-capture-a-link` writes the exact ones)

```
0:00 Opening
0:39 1. Install GNS3 and place three nodes
1:48 2. Give the computers addresses
2:38 3. Capture and read the packets
4:22 4. Where next
4:38 Wrap-up
```
