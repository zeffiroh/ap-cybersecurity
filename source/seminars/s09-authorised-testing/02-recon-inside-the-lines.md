## 2. Recon, inside the lines

Scan only what's in scope. Name each address on the command line, so you can't accidentally sweep the whole range and hit the payment host. Then look at what you found.

- [ ] Which services run on each in-scope host, with which versions?
- [ ] Which one looks like it shouldn't be on the internet?
- [ ] What did you find in the staging JavaScript file?

> Hint: A "debug" API on port 8080 is a classic staging leftover. Read the saved app.bundle.js: developers leave things in bundles that everyone can download.

?> Which port does the staging debug API listen on? :: 8080
