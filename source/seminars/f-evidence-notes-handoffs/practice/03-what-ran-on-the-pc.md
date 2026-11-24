## 3. What ran on the PC

"Nothing happened, closed a popup" is what the user saw. The process list says what really ran on acct-lt04. Follow the `ppid` column from explorer.exe down.

- [ ] Which program ran the file from the archive? Should a "PDF" ever be run by it?
- [ ] Where does the program PowerShell started live? Where does the real OneDrive live on the same laptop?
- [ ] What did that program do in its first minute?
- [ ] When did it reach the file share?

?> Which program started cmd.exe? (file name) :: wscript.exe

?> What is the PID of the OneDriveSync.exe that PowerShell started? :: 5302

?> How many seconds after the script ran did OneDriveSync.exe start? :: 51

?> Which account did the attacker add to Administrators? :: svc_sync
