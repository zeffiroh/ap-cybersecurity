## 4. Fix it and watch the data exchange

Press **Design**, click stray and change its address to 192.168.1.14. Press **Simulation**, click till-1 and ping it: it answers now.

Open the **Data exchange** tab for till-1, press **Clear**, ping stray once more, and read the list from the top. Before the first ping you'll see **ARP**: till-1 asks "who has 192.168.1.14?" and stray answers with its MAC address. Then come the ICMP echo requests and echo replies. Click any row to see its layers.

- [ ] stray moved to 192.168.1.14 and it answers
- [ ] Data exchange open for till-1
- [ ] Find the ARP question and answer before the first ICMP packet

> Hint: ARP happens once, before the first packet: the answer is remembered for a while, so the next pings go straight out.

?> Which protocol finds a MAC address before the first ping? (three letters) :: arp
