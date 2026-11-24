## 3. Ping, and explain the one that fails

Press **Simulation** and click **till-1**: its desktop opens. Open **Command line** and type `ipconfig`, then `ping 192.168.1.12` and `ping 192.168.1.13`. Then `ping 192.168.2.14`.

The first two answer. The last one says **PING: transmit failed. General failure.**, even though the cable and the switch are fine: 192.168.2.14 is in a different network (192.168.2.0/24), and till-1 has no gateway to send it to.

- [ ] ipconfig shows till-1's address and subnet mask
- [ ] Pings to till-2 and office get replies
- [ ] Ping to stray fails: write one line on why

> Hint: Same cable, same switch, different network number. Computers only talk directly to addresses inside their own network.

?> Can till-1 reach stray at 192.168.2.14? (yes or no) :: no

?> Which command shows a computer's own address in the Command line? (one word) :: ipconfig
