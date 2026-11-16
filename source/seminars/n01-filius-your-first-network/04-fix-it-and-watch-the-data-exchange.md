## 4. Fix it and watch the data exchange

Go back to design mode and change stray to 192.168.1.14. Run again and ping it: it answers now.

Right-click till-1 and choose **Show data exchange**. Ping once more and read the list. Before the first ping you'll see **ARP**: till-1 shouts "who has 192.168.1.14?" and stray answers with its MAC address. Then come the ICMP echo request and echo reply.

- [ ] stray moved to 192.168.1.14 and it answers
- [ ] Data exchange window open
- [ ] Find the ARP question and answer before the first ICMP packet

> Hint: ARP only happens once: the answer is remembered for a while.

?> Which protocol finds a MAC address before the first ping? (three letters) :: arp
