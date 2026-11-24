# Lecture script: Network lab 1: Your first network (Network Starter)

Network lab · free · about 30 minutes of lab work · about 6 minutes of narration

This is what `python tools/teach.py demo n01-filius-your-first-network` plays and captions, word for word, and what the voice studio
(`python tools/teach.py voice n01-filius-your-first-network`) shows you to read. Edit the words in seminar.json, then run
`python tools/teach.py script n01-filius-your-first-network` to refresh this file.

## Opening

Welcome to your first network lab. Banyan Books is a small bookshop, and today you're setting up its front office: two tills, an office computer, and one more that someone has typed in wrongly. We'll do it in Network Starter, the simple network builder in the Hacker Room, so there's nothing to install. By the end you'll have cabled four computers to a switch, used ping to prove which ones can talk, and read the packets that explain why one of them can't. Keep README.txt open beside you: it has the addressing plan.

## 1. Open Network Starter and meet the two modes

Step one: open Network Starter and meet its two modes. In the Hacker Room, open Start, then Workplace, then Network lab, and pick lab one. The switch and four computers are already on the canvas, and the Goals tab lists what you'll do today. Now look at the bar. Network Starter has two modes, and most beginner mistakes come from being in the wrong one.

*After it runs:*

Design, with the hammer, is where you place devices, draw cables and type settings. Simulation, with the play arrow, switches the network on, and you sit at the computers and type commands. You can't change an address while the simulation runs, and you can't ping anything in Design mode. Along the bar are the parts: Computer, Notebook, Server, Hub, Switch and Router, and then Cable. So the mode for placing and cabling devices is Design.

On screen: the step text.

## 2. Cable four computers to a switch

Step two: cable four computers to the switch. In Design mode, choose Cable, click a computer, then click the switch. Network Starter uses the first free port, so there's no counting ports. Do all four. Then click each computer in turn and type its IP address and subnet mask in the panel on the right, from the plan.

*After it runs:*

Three of them are in 192.168.1, numbered 11, 12 and 13. The fourth, stray, gets 192.168.2.14, and that's on purpose. The subnet mask on every computer is 255.255.255.0. That mask says the first three numbers name the network and the last number names the computer. So till-1, till-2 and office are all in network 192.168.1, and stray, on the same switch with the same kind of cable, is in network 192.168.2. Keep that in your head; it's about to matter. If you'd rather see addresses than names on the canvas, tick Use IP address as name.

On screen: the step text.

## 3. Ping, and explain the one that fails

Step three: ping, and explain the one that fails. Press Simulation, and click till-1: its desktop opens. Open Command line. First type ipconfig, to check the computer agrees with the plan. Then ping till-2 at 192.168.1.12, office at 192.168.1.13, and finally stray at 192.168.2.14.

*After it runs:*

ipconfig shows till-1's own address and subnet mask, exactly as you typed them, and an empty default gateway. The pings to till-2 and office come back with four replies each, and the cable flashes green as the data crosses it. The ping to stray says transmit failed, general failure, four times. Nothing is wrong with the cable, and nothing is wrong with the switch. The problem is the address. Before till-1 sends anything, it compares the destination with its own network. 192.168.2.14 isn't in 192.168.1, so till-1 won't try to reach it directly. It would hand the packet to a gateway, a router, but its gateway is empty, so it gives up before anything leaves. Write that in one line: a different network, and no router to get there. So the answers are no, and ipconfig.

On screen: the step text.

## 4. Fix it and watch the data exchange

Step four: fix it, and watch the data exchange. Press Design, click stray, and change its address to 192.168.1.14. Press Simulation, click till-1 and ping stray. It answers. Now open the Data exchange tab for till-1, press Clear, ping stray once more, and read the list from the top.

*After it runs:*

Look above the first ping. The first two rows aren't ICMP at all, they're ARP. To put a frame on the cable, till-1 needs stray's hardware address, its MAC address, and so far it only knows the IP address. So it asks everyone on the switch at once: who has 192.168.1.14? Every computer hears the question, and only stray answers, with its MAC address. Then come the ICMP echo requests and echo replies, four pairs, the ping itself. Notice there's only one ARP question for all four pings: till-1 remembers the answer for a while, in what's called the ARP cache. Click any row and you'll see its layers, Ethernet first, then IP, then ICMP. The protocol that finds the MAC address is ARP.

On screen: the step text.

## 5. Where next

That's the end of lab one. You built a network, broke it on purpose, and read the packets that fixed it. Every lab in this set works the same way: the work happens in a network program in the Hacker Room, the Goals tab ticks off what you've done, and you answer the questions on this page as you go. Network lab two adds a router, so two networks can finally talk.

On screen: the step text.

## Wrap-up

Three ideas to keep from today. A subnet mask decides which addresses are local. A computer only talks directly to addresses in its own network, however good the cabling is. And before the first packet, ARP finds the hardware address to send it to. See you in lab two.

## YouTube chapters (estimate; `python tools/teach.py demo n01-filius-your-first-network` writes the exact ones)

```
0:00 Opening
0:48 1. Open Network Starter and meet the two modes
1:44 2. Cable four computers to a switch
2:45 3. Ping, and explain the one that fails
3:57 4. Fix it and watch the data exchange
5:07 5. Where next
5:35 Wrap-up
```
