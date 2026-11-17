## 2. One known device per staff port

```
configure terminal
interface range fa0/1 - 12
 switchport port-security
 switchport port-security maximum 1
 switchport port-security mac-address sticky
 switchport port-security violation shutdown
end
```

From staff-1, ping staff-2 (192.168.10.12), so the switch learns both computers' MAC addresses, then run `show port-security interface fa0/1`. (If staff-2 never sends anything, Fa0/2 learns whatever plugs in first, and step 3 won't be blocked.)

- [ ] Port security on ports 1-12
- [ ] staff-1's MAC learned (sticky)
- [ ] show port-security checked

> Hint: Sticky learns the first MAC address seen on the port and keeps it in the configuration.

?> How many MAC addresses may each staff port learn? :: 1
