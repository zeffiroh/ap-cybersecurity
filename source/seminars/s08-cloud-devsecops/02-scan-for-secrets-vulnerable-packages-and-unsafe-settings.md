## 2. Scan for secrets, vulnerable packages and unsafe settings

The scanner looks in three places: **secrets** (keys and passwords in files and in Git history), **dependencies** (package versions with known advisories) and **configuration** (Dockerfile, Kubernetes, Terraform). Scan everything, then read each tab.

```tool codescan
{"counts": {"secrets": 7, "deps": 5, "iac": 14}, "n": 26, "blank": []}
```

- [ ] Secrets: which are in current files, which only in history? Which must be revoked?
- [ ] Which secret findings are false positives? (a CI variable or a Terraform variable is a pointer, not a secret)
- [ ] Dependencies: which packages, which advisories, which fixed version?
- [ ] Config: which problems are critical?

> Hint: The patch **removed** the key from deploy.sh, but the line starting with `-` still holds it. Anyone who clones the repo can read it. Deleting a secret never un-leaks it: revoke it.

?> Which identity does the key in Git history belong to? (see cloud/audit.json for the key ID) :: ci-deployer

?> Which package has a critical advisory? :: pyyaml

?> How many of the scanner's secret findings are false positives? :: 3
