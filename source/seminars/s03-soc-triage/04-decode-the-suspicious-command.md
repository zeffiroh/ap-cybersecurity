## 4. Decode the suspicious command

AL-3106 is an encoded PowerShell command. Encoding hides what a command does, which is why attackers use it, but IT scripts sometimes use it too. Decode it before you judge it.

[Open the command in CyberChef](https://zeffiroh.github.io/ap-cybersecurity/cyberchef/#recipe=From_Base64%28%27A-Za-z0-9%252B/%253D%27,true,false%29Decode_text%28%27UTF-16LE%2520%281200%29%27%29&input=UndCbEFIUUFMUUJEQUc4QWJRQndBSFVBZEFCbEFISUFTUUJ1QUdZQWJ3QWdBSHdBSUFCUEFIVUFkQUF0QUVZQWFRQnNBR1VBSUFCY0FGd0FhUUJ1QUhZQU1BQXhBRndBYVFCdUFIWUFaUUJ1QUhRQWJ3QnlBSGtBWEFBa0FHVUFiZ0IyQURvQVF3QlBBRTBBVUFCVkFGUUFSUUJTQUU0QVFRQk5BRVVBTGdCMEFIZ0FkQUE9) (From Base64, then Decode text as UTF-16LE). Or decode it in the Linux cell.

- [ ] Decode the command
- [ ] What does it do? Is anything in it harmful?
- [ ] Which account runs it, and when?
- [ ] Write the disposition and a note to IT: an encoded command in a scheduled task trips the alert every day

> Hint: PowerShell's -EncodedCommand is Base64 of UTF-16LE text. On Linux, `base64 -d` decodes it and `tr -d '\000'` drops the zero bytes UTF-16 puts between letters.

?> Which PowerShell command does AL-3106 run first? (the cmdlet name) :: Get-ComputerInfo
