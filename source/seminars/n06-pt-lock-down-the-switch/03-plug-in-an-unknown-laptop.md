## 3. Plug in an unknown laptop

Click the cable between staff-2 and the switch and press **Unplug it**. Add a **Laptop** from the bar, give it 192.168.10.50 in its panel, and cable it to **Fa0/2** with **Copper Straight-Through**. Ping staff-1 from the laptop. Look at the link light, then run `show interfaces status` and `show port-security` on the switch.

The port has shut itself down. To bring it back after a check, unplug the laptop, plug staff-2 back into Fa0/2, and on that port run `shutdown` then `no shutdown` (on a real switch the port stays err-disabled until you do).

- [ ] Unknown laptop blocked
- [ ] Port state read in show interfaces status
- [ ] staff-2 back on Fa0/2 and connected

> Hint: The link light turns red and the status says err-disabled.

?> Which status does show interfaces status give the blocked port? :: err-disabled
