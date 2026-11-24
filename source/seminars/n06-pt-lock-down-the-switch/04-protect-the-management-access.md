## 4. Protect the management access

Anyone with a console cable could change all of this. Add passwords:

```
configure terminal
enable secret <choose one>
line console 0
 password <choose another>
 login
end
copy running-config startup-config
show running-config
```

Read the top of `show running-config`: the enable secret is stored as a hash (`enable secret 5 ...`), never as the word you typed.

- [ ] enable secret set
- [ ] Console password with login
- [ ] Configuration saved ([OK])

> Hint: `enable secret` is stored as a hash; the old `enable password` isn't. Always use secret.

?> Which command saves the configuration so it survives a restart? :: copy running-config startup-config
