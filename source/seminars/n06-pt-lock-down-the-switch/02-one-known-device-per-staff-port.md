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

From staff-1's Command Prompt, ping staff-2 (192.168.10.12), so both staff ports hear from their computers, then run `show port-security` on the switch. (On a real switch, a port that has never heard from its computer learns whatever plugs in first.)

- [ ] Port security on ports 1-12
- [ ] Fa0/1 and Fa0/2 each show 1 current address
- [ ] show port-security checked

> Hint: Sticky learns the first MAC address seen on the port and keeps it in the configuration.

?> How many MAC addresses may each staff port learn? :: 1
