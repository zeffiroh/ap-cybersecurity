## 2. Recon inside the lines

Scan only the two staging hosts, by address, never the whole range: 192.0.2.12 sits in the same range and belongs to the payment provider.

- [ ] Which services and versions run on each host?
- [ ] Which one looks like it shouldn't be reachable?

> Hint: `nmap -sV 192.0.2.10 192.0.2.11` names each address. `192.0.2.0/24` would include the out-of-scope payment host.

?> Which port does the staging debug API listen on? :: 8080
