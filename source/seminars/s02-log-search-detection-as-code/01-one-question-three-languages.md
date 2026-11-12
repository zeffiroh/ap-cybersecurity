## 1. One question, three languages

A hunt starts with a question, not a tool. Ours: **did anyone guess an SSH password on web01, get in, and do something with it?** You'll answer it three times: in SPL, in KQL and in SQL. Real teams use different SIEMs, and moving a hunt between them is a daily job.

The SIEM search here is a **teaching subset** of each language over the case logs, so not every command works. When you want the real thing, the free [KC7](https://kc7cyber.com) game and the free Azure Data Explorer help cluster run full KQL.

First look at the raw log with `grep`, so you know what the search engine is reading.

- [ ] How many lines does auth.log have?
- [ ] Which line types do you see: Failed, Accepted, sudo?
- [ ] Which address keeps failing?

> Hint: `grep -c` counts matching lines. `awk '{print $(NF-3)}'` prints the fourth word from the end, which is the source address on every Failed line.

?> How many lines in auth.log contain "Failed password"? :: 7
