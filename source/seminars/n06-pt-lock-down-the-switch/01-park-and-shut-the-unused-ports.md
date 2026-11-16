## 1. Park and shut the unused ports

A live, empty wall port is an open door: anyone can plug in. On the switch:

```
enable
configure terminal
vlan 999
 name PARKING
interface range fa0/21 - 24
 switchport mode access
 switchport access vlan 999
 shutdown
end
show interfaces status
```

- [ ] VLAN 999 made
- [ ] Ports 21-24 in VLAN 999 and shut down
- [ ] show interfaces status shows them disabled

> Hint: Shut ports show as "disabled" in `show interfaces status`.

?> Which command switches a port off? :: shutdown
