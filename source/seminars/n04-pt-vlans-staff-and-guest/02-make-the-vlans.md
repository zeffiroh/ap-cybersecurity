## 2. Make the VLANs

Click the switch, open the **CLI** tab, and type:

```
enable
configure terminal
vlan 10
 name STAFF
vlan 20
 name GUEST
interface range fa0/1 - 12
 switchport mode access
 switchport access vlan 10
interface range fa0/13 - 20
 switchport mode access
 switchport access vlan 20
end
show vlan brief
```

- [ ] Both VLANs exist with names
- [ ] Ports 1-12 in VLAN 10, 13-20 in VLAN 20
- [ ] show vlan brief checked

> Hint: `interface range` sets many ports at once. Unused ports 21-24 stay in VLAN 1: you lock those down in lab 6.

?> Which command lists every VLAN and its ports? :: show vlan brief
