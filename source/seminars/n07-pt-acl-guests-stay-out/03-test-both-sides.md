## 3. Test both sides

From guest-1: open web-out in the browser (allowed) and ping files01 (blocked). From staff-1: ping files01 and open web-out (both still fine). Run `show access-lists` again: the counters show which rule matched each test.

- [ ] Guest to web works
- [ ] Guest to files01 blocked
- [ ] Staff unaffected
- [ ] Match counters read

> Hint: Every allow-list ends with an invisible "deny any". Writing it yourself makes the counters show what was dropped.

?> After the ACL, can guest-1 still open the web server? (yes or no) :: yes

?> After the ACL, can guest-1 ping files01? (yes or no) :: no
