## 6. Network sensor: who talked to whom

Zeek writes one line per connection: who opened it, to which address and port, how long it lasted and how many bytes went each way. It's the fastest way to see the whole night at once. The fields are separated by tabs; the `#fields` line names them.

- [ ] List every pair: from, to, port, service, with a count
- [ ] How many connections did appt01 open to 203.0.113.77?
- [ ] Which internal machine did appt01 connect to on port 445 (Windows file sharing)? Why is that strange for an appointments server?
- [ ] Which connection moved the most bytes? Is it suspicious?

> Hint: Field 3 is id.orig_h (who opened it), 5 is id.resp_h, 6 is id.resp_p, 8 is service and 11 is resp_bytes. The biggest transfer is the nightly backup, which is internal and runs at 01:30 every night.

?> How many connections did appt01 open to 203.0.113.77? :: 5

?> Which internal address did appt01 connect to on port 445? :: 10.30.2.33
