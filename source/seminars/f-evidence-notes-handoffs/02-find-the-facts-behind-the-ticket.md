## 2. Find the facts behind the ticket

A good note is built from evidence, not from what someone said on the phone. Start with the reported message in the mail log, then see who downloaded the attachment.

`nrcpt=` is the number of people the email went to. In the proxy log, `TCP_MISS/200` means the download worked and `TCP_DENIED/403` means the proxy blocked it.

- [ ] How many people received the email, and who are they?
- [ ] Which internal address downloaded the invoice, and was anyone blocked?
- [ ] Write each fact down with its time and the file you saw it in

> Hint: Proxy times are Unix epoch seconds. The Python cell turns them into UTC clock times, so every fact in your note uses one time zone.

?> How many people received the fake invoice? :: 3

?> Which internal IP address downloaded the invoice successfully? :: 10.20.0.14
