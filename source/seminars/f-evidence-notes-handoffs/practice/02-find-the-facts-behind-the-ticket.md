## 2. Find the facts behind the ticket

Build the note from the logs, not from what someone said on the phone. Start with the reported message in mail.log, then find every download in proxy.log that came from it, and what came after.

- [ ] Who received the email, and when?
- [ ] Which internal address downloaded the archive, and was anyone blocked?
- [ ] What did the same address download next, and what does it keep doing?
- [ ] Write each fact with its UTC time and the file you saw it in

?> How many people received the fake courier email? :: 3

?> Which internal IP address downloaded the archive successfully? :: 10.30.0.21

?> How many encrypted (CONNECT, TCP_TUNNEL) sessions did that address open to files-cdn-sync.example? :: 6

?> How many seconds apart are those sessions? :: 600
