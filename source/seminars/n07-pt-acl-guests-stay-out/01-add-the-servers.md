## 1. Add the servers

Add **files01** to a staff port, and **web-out** on the router's **G0/1** (`ip address 203.0.113.1 255.255.255.0` and `no shutdown` on G0/1). On web-out, check **Services → HTTP** is on. From guest-1, open web-out in **Desktop → Web Browser** and ping files01: both work for now.

- [ ] files01 and web-out added
- [ ] Router G0/1 up
- [ ] Before the ACL: guest-1 reaches both

> Hint: Test before you block, so you know any failure later is caused by your rule and not by a typo.

?> Before the ACL, can guest-1 ping files01? (yes or no) :: yes
