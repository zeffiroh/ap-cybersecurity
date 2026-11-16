## 3. Plug in an unknown laptop

Unplug staff-2 from Fa0/2 and plug a new **Laptop** into Fa0/2 instead. Give it 192.168.10.50 and ping staff-1. Look at the link light, then run `show interfaces status` and `show port-security interface fa0/2`.

The port has shut itself down. To bring it back after a check, plug staff-2 back in and run `shutdown` then `no shutdown` on the port.

- [ ] Unknown laptop blocked
- [ ] Port state read in show interfaces status
- [ ] Port brought back with shutdown / no shutdown

> Hint: In Packet Tracer the light turns red and the status says err-disabled.

?> Which status does show interfaces status give the blocked port? :: err-disabled
