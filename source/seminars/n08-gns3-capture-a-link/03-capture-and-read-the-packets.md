## 3. Capture and read the packets

Right-click the link between PC1 and SW1 → **Start capture**. Wireshark opens. On PC1, type `ping 10.0.0.2`. In Wireshark, type the display filter `arp || icmp` and read the list from the top: an **ARP** request (who has 10.0.0.2?), an ARP reply, then ICMP **Echo (ping) request** and **reply** pairs. Click one echo request and open **Internet Control Message Protocol** in the details pane to see its type.

- [ ] Capture running on the PC1 link
- [ ] arp || icmp filter applied
- [ ] ARP pair and echo request/reply pairs found
- [ ] ICMP type read in the details pane

> Hint: Echo request is ICMP type 8, echo reply is type 0.

?> Which ICMP type number is an echo request? :: 8

?> Which protocol asks "who has 10.0.0.2" first? (three letters) :: arp
