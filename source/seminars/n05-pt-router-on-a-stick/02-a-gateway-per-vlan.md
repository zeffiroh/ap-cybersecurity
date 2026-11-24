## 2. A gateway per VLAN

Double-click the router for its CLI:

```
enable
configure terminal
interface g0/0
 no shutdown
interface g0/0.10
 encapsulation dot1Q 10
 ip address 192.168.10.1 255.255.255.0
interface g0/0.20
 encapsulation dot1Q 20
 ip address 192.168.20.1 255.255.255.0
end
show ip interface brief
```

Then click each PC and set its **Default gateway**: staff 192.168.10.1, guests 192.168.20.1.

- [ ] Main interface up
- [ ] Two subinterfaces with dot1Q tags and addresses
- [ ] Gateways set on all four PCs

> Hint: Router interfaces start shut down. The subinterfaces only work once the main interface has `no shutdown`.

?> Which command tags a subinterface with VLAN 20? :: encapsulation dot1q 20

?> What gateway do guest PCs use? :: 192.168.20.1
