# Lecture script: Find a secret in a Git repo

Free tutorial · about 15 minutes of lab work · the video runs about 6 minutes

Read it aloud while the demo plays (add `&demo=1` to the lab link), or record your own screen with the Teaching Desk. The demo's captions are this text, word for word.

## Opening

Welcome. Keys leak through Git more often than through any clever attack. Here you scan a repository for secrets, including ones that were deleted but are still in the history.

## 1. The setting

Read the setting so you know the company, the date and the time zone. Then open the evidence in the case folder.

On screen: the step text and the tool.

## 2. Scan for secrets, vulnerable packages and unsafe settings

The scanner looks in three places. Secrets: keys and passwords in files and in Git history. Dependencies: package versions with known advisories. Configuration: the Dockerfile, Kubernetes and Terraform. Scan everything, then read each tab. The important finding is in the history. A patch removed the key from deploy dot sh, but the old line still starts with a minus sign in the diff, and anyone who clones the repo can read it. Deleting a secret never un-leaks it. The fix is to revoke the key and issue a new one.

On screen: the step text and the tool.

## 3. Where next

Revoke first, clean up after. Seminar 8 builds the pipeline checks that stop this reaching the repository at all.

On screen: the step text and the tool.

## Wrap-up

Revoke first, clean up after. Seminar 8 builds the pipeline checks that stop this reaching the repository at all.

## YouTube chapters (estimate; `./teach demo` writes the exact ones)

```
0:00 Opening
0:24 1. The setting
1:36 2. Scan for secrets, vulnerable packages and unsafe settings
2:47 3. Where next
```
