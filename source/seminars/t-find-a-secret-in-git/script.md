# Lecture script: Find a secret in a Git repo

Free tutorial · about 15 minutes of lab work · about 3 minutes of narration

This is what `python tools/teach.py demo t-find-a-secret-in-git` plays and captions, word for word, and what the voice studio
(`python tools/teach.py voice t-find-a-secret-in-git`) shows you to read. Edit the words in seminar.json, then run
`python tools/teach.py script t-find-a-secret-in-git` to refresh this file.

## Opening

Hello, and welcome. Developers sometimes put passwords and cloud keys into code by mistake, then delete them and think the problem is gone. It isn't. Git remembers everything. Today you'll scan a repository for secrets, vulnerable packages and unsafe settings, including a key that was deleted but still sits in the history.

## 1. The setting

The setting. Monsoon Mart, an online grocery company in Bengaluru. Thursday the twelfth of November 2026. Times are UTC unless marked. The case folder has the code repository, the Git history as a patch file, and the company's cloud audit log.

On screen: the step text.

## 2. Scan for secrets, vulnerable packages and unsafe settings

The scanner looks in three places. Secrets: keys and passwords in the files and in the Git history. Dependencies: package versions with known security advisories. And configuration: the Dockerfile, Kubernetes and Terraform files that decide how the app runs. Scan everything, then read each tab.

*After it runs:*

Twenty-six findings: seven secrets, five dependency problems and fourteen configuration issues. Start with secrets. Some are in the current files, and one is only in the history. The patch removed a cloud key from deploy.sh, but the line starting with a minus sign, the removed line, still holds the key. Anyone who clones the repository can read it. Look up its key ID in cloud audit.json: it belongs to ci-deployer, the account the build pipeline uses. Deleting a secret never un-leaks it. You must revoke it and issue a new one. Now the false positives. A CI variable or a Terraform variable is a pointer to a secret stored somewhere safe, not the secret itself. Three of the secret findings are like that. Marking them correctly matters, because a scanner full of noise gets ignored. In the dependencies tab, one package has a critical advisory, pyyaml, and the tab shows the fixed version to upgrade to. In configuration, sort by severity and fix the critical ones first. Answer the questions: ci-deployer, pyyaml, and three false positives.

On screen: the step text, the codescan tool with the model answer.

## 3. Where next

That was one step from Seminar 8, Cloud and DevSecOps: posture, pipelines, secrets and automation. The full seminar has a longer video, every step at three levels, walkthrough, practice and solo, a graded hand-in that I mark myself, and a certificate at the end. The links are on your screen. If you want to try the Hacker Room, the analyst desktop where all these programs live together, the free trial is linked there too.

On screen: the step text.

## Wrap-up

To recap. Scan the history, not just today's files. A leaked secret must be revoked, not just deleted. Separate real secrets from pointers, so the team trusts the scanner. Upgrade vulnerable packages to the fixed version, and fix critical settings first. Thank you for watching.

## YouTube chapters (estimate; `python tools/teach.py demo t-find-a-secret-in-git` writes the exact ones)

```
0:00 Opening
0:31 1. The setting
0:48 2. Scan for secrets, vulnerable packages and unsafe settings
2:24 3. Where next
2:53 Wrap-up
```
