## 2. Linux: who was knocking

appt01 is open to the internet on port 22. `auth.log` records every SSH login, good or bad. Count the failures, then count them **by source address**: one address making dozens of guesses is a brute force.

- [ ] How many failed passwords in total?
- [ ] Which address made most of them, and how many?
- [ ] Which user names did it try? Which one is a real account here?

> Hint: `grep -o 'from [0-9.]*'` keeps only the address part of each line; `sort | uniq -c | sort -rn` counts and ranks them.

?> How many failed passwords are in auth.log in total? :: 50

?> Which address made the most failed attempts? :: 198.51.100.23

?> How many failed attempts came from that address? :: 46
