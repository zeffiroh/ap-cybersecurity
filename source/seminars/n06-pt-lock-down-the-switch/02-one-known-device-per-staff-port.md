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

Ping from staff-1 so the switch learns its MAC address, then run `show port-security interface fa0/1`.

- [ ] Port security on ports 1-12
- [ ] staff-1's MAC learned (sticky)
- [ ] show port-security checked

> Hint: Sticky learns the first MAC address seen on the port and keeps it in the configuration.

?> How many MAC addresses may each staff port learn? :: 1
