## 3. Test both sides

From guest-1: `curl 203.0.113.10` (allowed) and `ping 192.168.10.10` (blocked: **Destination net unreachable** from the router). From staff-1: `ping 192.168.10.10` and `curl 203.0.113.10` (both still fine). Then try `ping 203.0.113.10` from guest-1: blocked too, because the policy allows the web, not ping.

- [ ] Guest to web works
- [ ] Guest to files01 blocked
- [ ] Staff unaffected
- [ ] Guest ping to web-out blocked, and you can say which line did it

> Hint: Every allow-list ends with an invisible "deny any". Writing it yourself makes the policy plain to whoever reads it next.

?> After the ACL, can guest-1 still open the web server? (yes or no) :: yes

?> After the ACL, can guest-1 ping files01? (yes or no) :: no
