# Lecture script: Network lab 3: DNS, a web server and a fault to find (Filius)

Network lab · about 45 minutes of lab work · about 5 minutes of narration

This is what `python tools/teach.py demo n03-filius-dns-web-and-a-fault` plays and captions, word for word, and what the voice studio
(`python tools/teach.py voice n03-filius-dns-web-and-a-fault`) shows you to read. Edit the words in seminar.json, then run
`python tools/teach.py script n03-filius-dns-web-and-a-fault` to refresh this file.

## Opening

Welcome to network lab three. So far we've used numbers for everything, but people don't type numbers; they type names. Today Banyan Books gets a website and a DNS server, so till-1 can open the site by name. Then something breaks, and you find it the way a good help desk does: calmly, one layer at a time, from the bottom up. Open your lab two network and save a copy under a new name first, so you always keep the working version.

## 1. Add a web server and a DNS server

Step one: add a web server and a DNS server. In design mode, add two computers to the back-office switch. web01 gets 192.168.2.80, and dns01 gets 192.168.2.53, both with gateway 192.168.2.1. Then run the simulation. On web01, install Web server and start it. On dns01, install DNS server, add a record for www.banyan.lan pointing to 192.168.2.80, type A, and start it.

*After it runs:*

The last numbers aren't random: 80 and 53 match the port numbers the web and DNS use, so they're easy to remember. The A record is the simplest DNS entry there is: a name, and the IPv4 address it stands for. There are others, such as AAAA for IPv6 addresses and MX for mail, but one A record is all we need today. The protocol that turns www.banyan.lan into an address is DNS.

On screen: the step text.

## 2. Open the site by name

Step two: open the site by name. Every computer needs to know where to ask, so set the DNS server on each one to 192.168.2.53. On till-1, install Web browser and open http://www.banyan.lan. Then open Show data exchange on till-1 and look at what happened before the page arrived.

*After it runs:*

The page opens. In the data exchange, the web request isn't first. First, till-1 sends a DNS question to 192.168.2.53: what's the address of www.banyan.lan? dns01 answers: 192.168.2.80. Only then does till-1 open a TCP connection to web01 and ask for the page over HTTP. Every website you've ever opened starts like this. Filius's browser speaks plain HTTP, so there's no padlock here; on the real web the DNS question still comes first, then an encrypted HTTPS connection on port 443. Here's a test worth remembering. If the name fails but typing http://192.168.2.80 works, the network is fine and the problem is DNS. The address DNS returns is 192.168.2.80.

On screen: the step text.

## 3. Find the fault

Step three: find the fault. Go to design mode and break till-2 in exactly one way: change its gateway to 192.168.1.100. Now forget you did that. Run the simulation, sit at till-2, and work up the layers, writing down what each test shows. ipconfig first. Then ping till-2's own address, and a neighbour, till-1. Then ping the router at 192.168.1.1. Then ping dns01 at 192.168.2.53, and finally open the site by name. Write the results as a small table, test, result, and what it proves, because that's exactly what you'd paste into a help desk ticket.

*After it runs:*

Here's how it reads. ipconfig: the address and netmask match the plan. Pinging itself works, so the computer's own network software is fine. till-1 answers, so the cable, the switch and the address are fine. The router at 192.168.1.1 answers too, so the router is alive. Then dns01 fails, and so does the site. Everything in the shop works, the router is up, and nothing in the other network can be reached. That pattern points at one setting. Look back at ipconfig: the gateway says 192.168.1.100, an address where nothing lives. till-2 is sending everything for the back office to nobody. The wrong setting is the gateway. Fix it, run the tests again, and write down that they pass. Notice what we didn't do: we didn't reinstall anything or restart the router. The tests pointed straight at the setting. A fix you haven't tested is a guess.

On screen: the step text.

## 4. Where next

That's lab three, and the last of the Filius labs. You gave the network names and a service, and you found a fault with a method instead of guesswork. From lab four we move to Packet Tracer and real switch and router commands, starting with VLANs.

On screen: the step text.

## Wrap-up

The method is the thing to keep. When something can't connect, test from the bottom up: the link, the computer's own address, the gateway, DNS, and then the service itself. Write down every result. The first test that fails tells you where to look. See you in lab four.

## YouTube chapters (estimate; `python tools/teach.py demo n03-filius-dns-web-and-a-fault` writes the exact ones)

```
0:00 Opening
0:44 1. Add a web server and a DNS server
1:37 2. Open the site by name
2:41 3. Find the fault
4:18 4. Where next
4:36 Wrap-up
```
