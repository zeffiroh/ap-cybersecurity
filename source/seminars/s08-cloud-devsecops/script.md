# Lecture script: Cloud and DevSecOps: posture, pipelines, secrets and automation

Seminar 8 · about 360 minutes of lab work · the video runs about 6 minutes

Read it aloud while the demo plays (add `&demo=1` to the lab link), or record your own screen with the Teaching Desk. The demo's captions are this text, word for word, so a recording made with `./teach demo` already has subtitles.

## Opening

Welcome to Cloud and DevSecOps. Monsoon Mart is a grocery delivery start-up: one repository, one pipeline, one cloud account, and a cloud bill that tripled overnight. Somebody is mining crypto on their account. Today you'll audit the code and the cloud like a cloud security engineer: secrets, packages, configuration, posture. Then you'll fix the key, rank everything, write the gate that stops it happening again, automate the response, and test a small Python check.

## 1. Map the repository

Start with what's there. The Dockerfile builds the image, the Kubernetes manifest runs it, the Terraform creates the cloud resources, the pipeline ties them together, and the patch is a commit from two weeks ago. Every one of them is code, and every one can leak a secret or open a door.

On screen: the step text, the Linux cell.

## 2. Scan for secrets, vulnerable packages and unsafe settings

Three tabs. Secrets: a payments key baked into the Dockerfile, a Git token in the pipeline, and the cloud key in the history patch, deleted from the file but alive in Git forever. Three more are false alarms: CI and Terraform variables are pointers, not secrets. Dependencies: PyYAML with a critical advisory, jsonwebtoken and lodash high. Config: a database password written into the Kubernetes manifest, a public bucket, a public database, root containers, an unpinned image. Every secret that was ever pushed must be revoked.

On screen: the step text, the tool with the model answer.

## 3. Compare with the real scanners

Now the real tools' output. Trivy agrees on the libraries and adds the operating system packages inside the image. Checkov agrees on all five Terraform problems. And Prowler sees what no code scan can: the CI key has full admin rights, it's never been rotated, and there are instances running in a region Monsoon doesn't use. That's our miner.

On screen: the step text, the Linux cell.

## 4. What the leaked key did

Follow the key. From 198.51.100.91, not the CI runners: who am I, which regions exist, then eight GPU instances in a region Monsoon never uses, launched in three minutes. That's the mining. Then a new access key for itself, and a peek at an invoice. The bucket check confirms it: invoices are public and shouldn't be; product images are public and should be.

On screen: the step text, the Linux cell.

## 5. Least privilege for the pipeline

The pipeline only ever deploys one service from one address, so that's all its key may do. A guardrail stops anyone minting keys or launching instances without MFA. The invoices bucket goes private with versioning and logging. Replay: zero attacker actions, zero broken deploys. And the real fix: no long-lived key in CI at all.

On screen: the step text, the tool with the model answer.

## 6. Rank every finding

Forty findings, one team. The ranking cares about two facts more than the score: can someone on the internet reach it, and is someone already using it? The leaked key and the public invoices bucket are both, so they're first. PyYAML is critical but only in an internal worker, so it's this month. Every row gets an owner and a date.

On screen: the step text, the tool with the model answer.

## 7. Write the pipeline gate

A gate is a policy the pipeline enforces. Secrets, critical packages with a fix, and public resources block the merge. Root containers and unpinned images block the deploy. Medium and low only warn, or the team learns to bypass the gate. Exceptions are written, owned and expire. And a secret is never an exception.

On screen: the step text, the tool with the model answer.

## 8. Automate the response

Alerts arrive at night, so we automate the routine. High and critical: enrich, open a ticket, block what intel says is malicious, disable an abused key, and page someone. Medium: enrich and ticket. Low: just a ticket, because a public product-images bucket and an intern's login need a person, not a robot. And nothing serious ever closes itself.

On screen: the step text, the tool with the model answer.

## 9. A tested Python check

Now write the check ourselves, in Python, with tests. Five asserts: two real secrets caught, and three things that look like secrets but aren't, like a CI variable or a Terraform variable. All pass. Then it runs on the repository and finds five: the payments key, the database password, the Git token, and both halves of the cloud key in history. Add one test of your own that fails, then make it pass.

On screen: the step text, the Python cell.

## 10. Hand in

Hand in the notebook: the scan results, the policy diff, the ranked register, the gate policy, the playbook and the tested Python check. The rubric is on screen.

On screen: the step text.

## Wrap-up

That's Monsoon Mart's audit. A secret deleted from a file but alive in history, a pipeline key that could do anything, and forty findings ranked so the team knows what to do on Monday. The gate stops the next secret and the next critical package before they ship, the playbook handles the noisy alerts, and the Python check has tests that prove it works. Next is seminar nine: authorised testing, where you attack an app on purpose, with permission.

## YouTube chapters (estimate; `./teach demo` writes the exact ones)

```
0:00 Opening
0:32 1. Map the repository
0:59 2. Scan for secrets, vulnerable packages and unsafe settings
1:39 3. Compare with the real scanners
2:09 4. What the leaked key did
2:40 5. Least privilege for the pipeline
3:08 6. Rank every finding
3:38 7. Write the pipeline gate
4:06 8. Automate the response
4:35 9. A tested Python check
5:10 10. Hand in
5:27 Wrap-up
```
