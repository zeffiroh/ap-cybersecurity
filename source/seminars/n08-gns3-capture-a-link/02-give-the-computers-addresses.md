## 2. Give the computers addresses

Double-click PC1 (or right-click it → **Console**), and type `ip 10.0.0.1/24 10.0.0.254`. On PC2: `ip 10.0.0.2/24 10.0.0.254`. Check each with `show ip`. Each console gets its own tab in **Consoles**.

- [ ] PC1 and PC2 addressed
- [ ] show ip checked on both, and PC2's MAC noted

> Hint: The VPCS `ip` command takes the address with its prefix length, then the gateway.

?> Which VPCS command shows a computer's address? :: show ip
