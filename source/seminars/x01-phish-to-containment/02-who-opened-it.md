## 2. Who opened it

Receiving a phishing email is not an incident. **Opening** it is. The web proxy logs every download. Search it for the look-alike domain, and turn the epoch times into UTC.

- [ ] Which internal address downloaded INV-30412.docm, and when?
- [ ] Did anyone else try? Did it work?

> Hint: `TCP_MISS/200` means the file was fetched. `TCP_DENIED/403` means the proxy blocked it: the domain was added to the blocklist at 09:18.

?> Which internal address downloaded INV-30412.docm? :: 10.20.0.14

?> Did fin-pc02 get the document? (yes or no) :: no
