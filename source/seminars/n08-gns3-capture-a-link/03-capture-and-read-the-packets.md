## 3. Capture and read the packets

Right-click the link between PC1 and SW1 → **Start capture**. In PC1's console, type `ping 10.0.0.2`. Open the **Capture** tab, type `arp` in the **Display filter** box and press Enter: an **ARP** request (who has 10.0.0.2?) and its reply. Click the request and read its Ethernet destination. Then filter `icmp`: five **Echo (ping) request** and **reply** pairs. Click a request and read **Internet Control Message Protocol** in the details to see its type; click a reply and read its **Time to live**.

- [ ] Capture running on the PC1 link
- [ ] arp filter: the request and reply found
- [ ] icmp filter: echo request and reply pairs found
- [ ] ICMP type and TTL read in the details

> Hint: Echo request is ICMP type 8, echo reply is type 0.

?> Which ICMP type number is an echo request? :: 8

?> Which protocol asks "who has 10.0.0.2" first? (three letters) :: arp

?> What Time to live does PC2's echo reply carry? :: 64
