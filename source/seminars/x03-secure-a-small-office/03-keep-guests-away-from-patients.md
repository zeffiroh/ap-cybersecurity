## 3. Keep the guests away from the patient records

Today the router lets the waiting-room Wi-Fi reach everything. conn.csv shows a guest phone talking to the NAS on 445. Rewrite the rules so guests reach the internet (web and DNS) and nothing inside.

- [ ] Guests: DNS to the router, web to the internet, nothing else
- [ ] The clinic keeps working: PCs to the NAS, the X-ray PC to its cloud
- [ ] Run your rules in the Firewall program and check the guest-to-NAS flow is denied

> Hint: Rules are read top to bottom. Put the guest rules first, and end with `default deny`.

?> How many guest connections to the NAS are in conn.csv? :: 6
