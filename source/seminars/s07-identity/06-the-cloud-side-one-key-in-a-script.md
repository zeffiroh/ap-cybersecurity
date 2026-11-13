## 6. The cloud side: one key in a script

The findstr found what it was looking for: a cloud access key in sync.ps1. Read the cloud audit trail and see what the key did, from where. Then load the policies into the Cloud IAM simulator and replay the audit log **as it is**: everything the attacker did was allowed.

- [ ] Which identity, from which address, did what, in order?
- [ ] What did it create so it could come back?
- [ ] What was stopped, and by what?
- [ ] Why did reporting-sync have permission to do any of this?

> Hint: `grep -o '"action": "[A-Za-z]*"'` lists the actions. The office's address is 203.0.113.60.

?> From which address did the stolen key work? :: 198.51.100.200

?> Which user did the attacker create? :: ops-backup
