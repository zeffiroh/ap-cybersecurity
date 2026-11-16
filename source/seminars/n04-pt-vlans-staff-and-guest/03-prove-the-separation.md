## 3. Prove the separation

From staff-1's **Command Prompt**, ping staff-2 (192.168.10.12): it answers. Ping guest-1 (192.168.20.31): it fails.

Now the real test: change guest-1's address to 192.168.10.99, as if a visitor guessed the staff range. Ping staff-1 again. It still fails, because the switch never forwards VLAN 20 frames to VLAN 10 ports. Put the address back.

- [ ] Staff to staff works
- [ ] Staff to guest fails
- [ ] A guest using a staff address still can't reach staff

> Hint: VLANs separate at layer 2. Choosing a different IP address doesn't move you into another VLAN: the port decides.

?> With a staff-range address on a guest port, can guest-1 reach staff-1? (yes or no) :: no

?> What decides which VLAN a computer is in: its IP address or its switch port? :: switch port
