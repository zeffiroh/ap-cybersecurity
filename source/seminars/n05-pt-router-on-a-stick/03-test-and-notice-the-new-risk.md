## 3. Test, and notice the new risk

From guest-1's Command Prompt, ping staff-1 (192.168.10.11). It works now, because the router joins the VLANs. Good for printing; bad for security: guests can reach staff computers again.

Write down which traffic guests should be allowed (the internet) and which they shouldn't (staff computers and the file server). Lab 7 enforces that with an access list.

- [ ] Guest to staff ping works through the router
- [ ] A short list: what guests may and may not reach

> Hint: Routing between VLANs is all or nothing until you add rules. That's why segmentation always comes with an access list or a firewall.

?> After routing, can guest-1 ping staff-1? (yes or no) :: yes
