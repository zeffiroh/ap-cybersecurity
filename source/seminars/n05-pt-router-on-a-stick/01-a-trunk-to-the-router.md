## 1. A trunk to the router

Lab 4's office is already built, and a **1941** router is waiting below the switch. With **Copper Straight-Through** chosen, press **Connect**, click sw1, then the router, and pick switch **Gi0/1** and router **G0/0**. On the switch CLI:

```
enable
configure terminal
interface gi0/1
 switchport mode trunk
end
show interfaces trunk
```

A trunk carries many VLANs on one cable by tagging each frame with its VLAN number (802.1Q).

- [ ] Router cabled to Gi0/1
- [ ] Gi0/1 is a trunk
- [ ] show interfaces trunk shows Gi0/1 trunking

> Hint: An access port carries one VLAN untagged. A trunk carries several, tagged.

?> Which switchport mode carries both VLANs to the router? (one word) :: trunk
