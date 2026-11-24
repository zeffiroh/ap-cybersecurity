## 5. Decode the suspicious command

AL-4106 is an encoded PowerShell command on pms01, the server that runs the hotel's booking system. Encoding hides what a command does, which is why attackers use it, but IT scripts sometimes use it too. Decode it before you judge it.

[Open the command in CyberChef]({{site}}cyberchef/#recipe=From_Base64%28%27A-Za-z0-9%252B/%253D%27,true,false%29Decode_text%28%27UTF-16LE%2520%281200%29%27%29&input=UXdCdkFHMEFjQUJ5QUdVQWN3QnpBQzBBUVFCeUFHTUFhQUJwQUhZQVpRQWdBQzBBVUFCaEFIUUFhQUFnQUVRQU9nQmNBRkFBVFFCVEFGd0FSUUI0QUhBQWJ3QnlBSFFBWEFBcUFDQUFMUUJFQUdVQWN3QjBBR2tBYmdCaEFIUUFhUUJ2QUc0QVVBQmhBSFFBYUFBZ0FGd0FYQUJ1QUdFQWN3QXdBREVBWEFCd0FHMEFjd0F0QUdJQVlRQmpBR3NBZFFCd0FGd0FjQUJ0QUhNQUxRQWtBQ2dBUndCbEFIUUFMUUJFQUdFQWRBQmxBQ0FBTFFCR0FHOEFjZ0J0QUdFQWRBQWdBSGtBZVFCNUFIa0FUUUJOQUdRQVpBQXBBQzRBZWdCcEFIQUFJQUF0QUVZQWJ3QnlBR01BWlFBPQ==) (From Base64, then Decode text as UTF-16LE). Or decode it in the Linux cell.

- [ ] Decode the command
- [ ] What does it do? Is anything in it harmful?
- [ ] Which account runs it, and when?
- [ ] Write the disposition and a note to IT: an encoded command in a scheduled task trips the alert every night

> Hint: PowerShell's -EncodedCommand is Base64 of UTF-16LE text. On Linux, `base64 -d` decodes it and `tr -d '\000'` drops the zero bytes UTF-16 puts between letters.

?> Which PowerShell command does AL-4106 run? (the cmdlet name) :: Compress-Archive
