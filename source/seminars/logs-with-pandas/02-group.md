## 2. Who did web01 talk to?

Group by destination and port, then add up the bytes. This is the same as a SIEM `stats sum(bytes_out) by dst, dport`.

- [ ] Find the destination that received the most bytes
- [ ] Notice the unusual port

?> Which port carried most of the data? :: 4444
