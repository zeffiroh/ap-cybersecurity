## 1. Add the servers

Two servers are waiting below the switch. Cable **files01** to **Fa0/3** (a staff port) with **Copper Straight-Through** and give it 192.168.10.10, gateway 192.168.10.1. Set the **Cable** list back to **Automatic** and cable **web-out** to the router: it takes the router's first free port, **G0/1**. Give web-out 203.0.113.10, gateway 203.0.113.1; its **Web server** is already ticked. On the router CLI:

```
enable
configure terminal
interface g0/1
 ip address 203.0.113.1 255.255.255.0
 no shutdown
end
```

From guest-1's Command Prompt, type `curl 203.0.113.10` (it fetches web-out's home page) and `ping 192.168.10.10`: both work for now.

- [ ] files01 and web-out cabled and addressed
- [ ] Router G0/1 up
- [ ] Before the ACL: guest-1 reaches both

> Hint: Test before you block, so you know any failure later is caused by your rule and not by a typo.

?> Before the ACL, can guest-1 ping files01? (yes or no) :: yes
