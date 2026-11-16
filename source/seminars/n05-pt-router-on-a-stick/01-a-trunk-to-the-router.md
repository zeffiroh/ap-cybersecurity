## 1. A trunk to the router

Open your lab 4 file and save a copy. Add a **1941** (or 2911) router and cable switch **Gi0/1** to router **G0/0**. On the switch CLI:

```
enable
configure terminal
interface gi0/1
 switchport mode trunk
end
show interfaces trunk
```

A trunk carries many VLANs on one cable by tagging each frame with its VLAN number (802.1Q).

- [ ] Router added and cabled to Gi0/1
- [ ] Gi0/1 is a trunk
- [ ] show interfaces trunk lists VLANs 10 and 20

> Hint: An access port carries one VLAN untagged. A trunk carries several, tagged.

?> Which switchport mode carries both VLANs to the router? (one word) :: trunk
