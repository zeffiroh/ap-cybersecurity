## 2. Who opened it

Receiving a phishing email is not an incident. **Opening** it is. The web proxy logs every download. Search it for the look-alike domain.

- [ ] Which internal address downloaded INV-30412.docm?

> Hint: `TCP_MISS/200` means the file was fetched. `TCP_DENIED/403` means the proxy blocked it.

?> Which internal address downloaded INV-30412.docm? :: 10.20.0.14
