# Lecture script: Network lab 7: An access list that keeps guests out (Packet Tracer)

Network lab · about 50 minutes of lab work · about 5 minutes of narration

This is what `python tools/teach.py demo n07-pt-acl-guests-stay-out` plays and captions, word for word, and what the voice studio
(`python tools/teach.py voice n07-pt-acl-guests-stay-out`) shows you to read. Edit the words in seminar.json, then run
`python tools/teach.py script n07-pt-acl-guests-stay-out` to refresh this file.

## Opening

Welcome to network lab seven. In lab five you wrote a short policy for Tulsi Travels: guests may use the web, and must never reach staff systems. Today that sentence becomes a working rule on the router, an access list. Then we test both sides, guests and staff, because a rule you haven't tested is a guess. Open your lab six file and save a copy.

## 1. Add the servers

Step one: add the servers. Add a server called files01 on a free staff port, with address 192.168.10.10 and gateway 192.168.10.1. Then add a second server, web-out, to stand in for the internet, and cable it to the router's G0/1. A router joined straight to a server takes a Copper Cross-Over cable, or use the lightning bolt and let Packet Tracer choose. On the router, give G0/1 the address 203.0.113.1 and no shutdown, and give web-out 203.0.113.10 with gateway 203.0.113.1. Check HTTP is on in web-out's Services tab. Then, from guest-1, open the web browser at 203.0.113.10, and ping files01.

*After it runs:*

Both work. The web page opens, and files01 answers. That's the point of this step: test before you block. If something fails after the access list, you'll know your rule did it, and not a typo in an address. A note on 203.0.113: it's a range set aside for documentation and examples, so it can never clash with a real site on the internet. Before the access list, guest-1 can ping files01, so the answer is yes.

On screen: the step text.

## 2. Write the access list

Step two: write the access list. On the router, in configuration mode, write access list 120 with four lines, in this order. One: deny ip from the guest network to the staff network. Two: permit tcp from the guest network to any address on port 80, the web. Three: permit udp from the guest network to any address on port 53, DNS. Four: deny ip any any. Then go into interface g0/0.20 and type ip access-group 120 in. End, and show access-lists.

*After it runs:*

Order matters, because the router reads the list from the top and stops at the first line that matches. If the port 80 line came first, a guest could open a web page on a staff computer. The deny for the staff network goes first, so nothing gets past it. The DNS line is there for when the office has a real DNS server; today we browse by address. The numbers after each address are wildcard masks, the opposite of a netmask: 0.0.0.255 means any value in the last number, so it matches a whole slash twenty-four network. And the place: inbound on the guest subinterface, where guest traffic first enters the router, so it's checked before it goes anywhere. The answers are 0.0.0.255, and g0/0.20.

On screen: the step text.

## 3. Test both sides

Step three: test both sides. From guest-1, open web-out in the browser, then ping files01. From staff-1, ping files01 and open web-out. Then run show access-lists again and read the match counts at the end of each line.

*After it runs:*

guest-1 gets the web page, and the ping to files01 fails. staff-1 does both, untouched. The counters tell you which line did what: the deny for the staff network counted the guest's pings to files01, and the port 80 line counted the web visit. That's why the last line is written out. Every access list ends with an invisible deny anyway, but writing it gives you a counter for everything else that was dropped. And you'll find things there. guest-1 can't ping web-out, or even its own gateway, because ping isn't on the allowed list. That's correct: the policy said web, not ping. And if staff-1 pings guest-1, that fails too: the request gets out, but the reply comes in on the guest side and hits line one. A list like this doesn't remember conversations; a stateful firewall does. So after the access list, guest-1 can still open the web server, and can't ping files01.

On screen: the step text.

## 4. Where next

That's lab seven, and the last of the Packet Tracer labs: segmentation with VLANs, hardened switch ports, and an access list that enforces a written policy. The last lab, in GNS3, shows the same kind of traffic as real packets in Wireshark.

On screen: the step text.

## Wrap-up

Policy, rule, test, counters. That's how every firewall change should go, whether it's one router in a travel agent or a whole data centre. Start from a sentence someone agreed, put the most specific lines first, test from both sides, and read the counters to prove it. See you in lab eight.

## YouTube chapters (estimate; `python tools/teach.py demo n07-pt-acl-guests-stay-out` writes the exact ones)

```
0:00 Opening
0:37 1. Add the servers
1:48 2. Write the access list
3:11 3. Test both sides
4:28 4. Where next
4:45 Wrap-up
```
