## 3. Linux: the login and what came next

A brute force only matters if it worked. Find the **Accepted** line, then read everything the account did afterwards: `sudo` lines show each command run as root. Then check the two things an attacker leaves to come back: a scheduled job and a running process.

- [ ] Which account logged in from 198.51.100.23, when, and with what (password or key)?
- [ ] Which commands did it run with sudo?
- [ ] What did the script change? Read recovered/m.sh
- [ ] Which cron line and which process are new?

> Hint: The deploy account logs in with a key from the IT admin PC every night; that one is normal. Compare the cron lines with what the script added.

?> Which account logged in with a password from 198.51.100.23? :: vendor

?> What file does the new cron job run? (full path) :: /usr/local/bin/.sysmon-agent

?> At what time (UTC, HH:MM:SS) did that login succeed? :: 01:19:44
