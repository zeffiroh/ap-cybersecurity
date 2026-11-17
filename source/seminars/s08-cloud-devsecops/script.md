# Lecture script: Cloud and DevSecOps: posture, pipelines, secrets and automation

Seminar 8 · about 360 minutes of lab work · about 19 minutes of narration

This is what `python tools/teach.py demo s08-cloud-devsecops` plays and captions, word for word, and what the voice studio
(`python tools/teach.py voice s08-cloud-devsecops`) shows you to read. Edit the words in seminar.json, then run
`python tools/teach.py script s08-cloud-devsecops` to refresh this file.

## Opening

Hello, and welcome to Cloud and DevSecOps. Monsoon Mart is an online grocery start-up in Bengaluru. It has one repository, one pipeline and one cloud account. On Thursday the twelfth of November 2026, the cloud bill for the day before arrives, and it is 3.4 times normal. Ananya Rao, the CTO, asks for a security review of the repository, the pipeline and the cloud account. That's our job today, and we'll do it the way a cloud security engineer does. We read the code and configuration, check it against real scanners, follow a leaked key through the audit trail, cut that key down to least privilege, rank every finding, write the gate that stops it happening again, automate the response, and test a small Python check. One thing before we start: the times in this case are UTC unless they're marked. Bengaluru is five and a half hours ahead, so 21:40 in the logs is 03:10 the next morning on the office clock.

## 1. Map the repository

Step one: map the repository. Before you scan anything, know what's there. A repository isn't just application code. It holds the instructions that build it, run it and create the cloud it runs in. People call that infrastructure as code, and every one of those files can leak a secret or open a door. The Linux cell lists every file in repo, including hidden folders, and then prints the pipeline.

*After it runs:*

Eight files. The Dockerfile builds the container image. deploy/cart-api.yaml is the Kubernetes manifest that runs it: three copies of cart-api in the shop namespace. infra/main.tf is the Terraform that creates the cloud resources: a bucket, a firewall rule and a database. .ci/pipeline.yml is the pipeline that ties it all together, in a hidden folder a careless ls would miss. Then two package lists, for the Node app and a Python worker, and advisories.json, the advisory feed. The last one is git-history.patch, an old commit. In the pipeline, build tags the image latest. Deploy reads the cloud key from two CI variables, which is good. But the third variable, GIT_TOKEN, is a real token written straight into the file. Why does the old commit matter? Because Git keeps everything. A file you fixed today still holds yesterday's mistake in its history, and anyone who can clone the repository can read it. Answer the question: eight.

On screen: the step text, the Linux cell.

## 2. Scan for secrets, vulnerable packages and unsafe settings

Step two: scan for secrets, vulnerable packages and unsafe settings. The Code and config scanner looks in three places. Secrets: keys, tokens and passwords, in the current files and in Git history. Dependencies: package versions that match a known advisory. And configuration: the Dockerfile, the Kubernetes manifest and the Terraform. Press Scan everything, then read each tab. The scanner gives candidates; you decide which are real.

*After it runs:*

Seven secrets, five vulnerable packages and fourteen config problems. Start with secrets. A payment API key, sk_live, baked into the Dockerfile with ENV, so it's inside every copy of the image. The Git token in the pipeline. And in git-history.patch, a cloud key ID and its secret, on lines that start with a minus sign. That commit, from the twenty-ninth of October, says remove hard-coded cloud key. It did remove it from the file. But the minus line is the old text, and it's still in history. The key ID is SCKA4TQ7WZ0M2RB8, and if you search the audit trail for it, it belongs to ci-deployer, the pipeline's own cloud identity. Now the false alarms. STRATUS_SECRET, dollar CI_STRATUS_SECRET, in the pipeline. The same thing on the plus line of the patch. And password equals var.db_password in the Terraform. Each of those is a pointer to a secret kept somewhere else, not the secret itself. That's three false positives. Dependencies: PyYAML 5.3.1 in the worker is critical, because yaml.load on untrusted input can run code. Fixed in 5.4. jsonwebtoken 8.5.1 and lodash 4.17.15 are high. express and urllib3 are medium. Config: the critical ones are the secret baked in with ENV, a database password written into the Kubernetes manifest, a public bucket and a database reachable from the internet. Among the highs: the container runs as root, and the Dockerfile pipes a downloaded script straight into a shell. Here's the rule to remember: a secret that was ever pushed must be revoked and replaced. Deleting it never un-leaks it. Answer the questions: ci-deployer, pyyaml, and three.

On screen: the step text, the codescan tool with the model answer.

## 3. Compare with the real scanners

Step three: compare with the real scanners. Our scanner is a teaching tool. The platform team ran three real ones: Trivy on the image, Checkov on the Terraform and Prowler on the live cloud account. We can't run them in the browser, but their output is saved in the captured folder. The Linux cell pulls out the important lines from each. See where they agree, and what each sees that the others can't.

*After it runs:*

Trivy first. Forty-one findings in the image: twenty-two low, fourteen medium, four high and one critical. Among the libraries, jsonwebtoken and lodash are high, the same as our dependency tab, and express is medium. The other two highs are in openssl, an operating system package inside the Debian base image. That's what Trivy adds: it sees what's actually installed in the image, not just what's in package.json. PyYAML isn't there, because the worker isn't in this image. The one critical is zlib1g, the compression library in the Debian base image, and Debian has marked it will not fix. Upgrading a library won't help: the fix is a newer base image, pinned by digest, which is finding F-10. Checkov: nine passed, five failed. The bucket isn't private, bucket versioning is off, SSH is open to 0.0.0.0/0, the database is public, and its storage isn't encrypted. Those are exactly our five Terraform findings. Now Prowler, which reads the running account, not the code. User ci-deployer has full administrator rights. Its access key is older than ninety days and has never been rotated. The invoices bucket and the orders database are public, and instances are running in region ap-southeast-3. Monsoon only uses ap-south-1, Mumbai. No code scan could ever see that: it's not written down anywhere. It's happening. Answer the questions: five, and ap-southeast-3.

On screen: the step text, the Linux cell.

## 4. What the leaked key did

Step four: what the leaked key did. Now follow the key from the history patch into the cloud. audit.json is the audit trail: every call to the account, with the identity, the key ID, the source address, the region, the resource, MFA and the user agent. The Linux cell counts calls per address and per action.

*After it runs:*

Two addresses. Five calls from 203.0.113.20, the CI runners' address, and twelve from 198.51.100.91. Start with normal. On the ninth, tenth and eleventh, at 10:12 every day, ci-deployer deploys service/cart-api from the CI runners, with the user agent monsoon-ci. Then at 21:40, the same key, from 198.51.100.91, with a different program, stratus-cli. Threat intel already lists that address as malicious, tagged key abuse and mining. The first call is GetCallerIdentity: who am I? At 21:41, DescribeRegions. Then from 21:43:00 to 21:45:20, eight RunInstances, one every twenty seconds: gpu-xl-1 to gpu-xl-8, in ap-southeast-3. That's the mining, and the bill. At 21:49, CreateAccessKey on ci-deployer: a second key, so revoking the first one won't lock them out. Both keys must go, and all eight instances must be stopped. At 21:51, GetObject on an invoice, inv-88211.pdf. Now press Check storage buckets. One of two is open to everyone. monsoon-invoices holds customer invoices, it's meant to be private, and it has no versioning and no access logging, so nobody can tell who else has read it. monsoon-assets is public too, but it holds product images, and those are meant to be public. That's the trap: public isn't always wrong. Public is wrong when the data isn't. Answer the questions: eight, and 198.51.100.91.

On screen: the step text, the Linux cell.

## 5. Least privilege for the pipeline

Step five: least privilege for the pipeline. The CI key needed to do one thing, and it was allowed to do everything. Edit the policies in the simulator, then replay the audit trail against them. The simulator gives two numbers: attacker actions still allowed, and normal actions now blocked. A fix that stops the attacker but breaks the deploy isn't a fix, it's an outage. Aim for zero and zero.

*After it runs:*

Replay the policies as they are first. Twelve of twelve attacker actions allowed, because ci-deployer has AdministratorAccess, star on star. Now the changes. ci-deployer gets one statement: allow DeployService on service/cart-api, only when the source address is 203.0.113.20. That's everything it did in three days of normal logs. Next, a guardrail for the whole organisation: deny CreateAccessKey and RunInstances without MFA. And the invoices bucket: public read off, versioning on, access logging on. Replay again. Zero of twelve attacker actions allowed. Zero of five normal actions blocked: the three deploys still work, and Ananya's console session still works, because it used MFA. But keep the real fix in mind. This is still a long-lived key, and it can leak again. The better answer is no stored key in CI at all: the pipeline proves who it is at deploy time and receives short-lived credentials that expire on their own. Answer the question: zero.

On screen: the step text, the cloudiam tool with the model answer.

## 6. Rank every finding

Step six: rank every finding. You now have dozens of findings across four tools, and one small team. What goes first? The register boils them down to ten rows. Each has a CVSS vector, and two facts that matter more than the score: is it reachable from the internet, and is it already being exploited? Score F-01's vector in the calculator, then rank the whole register.

*After it runs:*

F-01, the cloud secret in Git history, scores 10.0, critical. Scope changed: a pipeline key reaches the whole account. Now rank. Two rows are patch now: F-01, and F-04, the public invoices bucket. Look at F-04's score: only 7.5. It's ranked above things scoring 9.8, because it's on the internet and it's already being used. F-02, the payment key in the Dockerfile, is 9.6 and internet-facing, so it's this week. Then this month: PyYAML at 9.8, the orders database at 8.8, the Git token and the open SSH at 8.1, and the two libraries. Last, the root container at 5.3, for the next routine cycle. Why is PyYAML, the highest score after F-01, only this month? It's in an internal worker that nobody on the internet can reach, and nobody is exploiting it. That's the lesson: the score measures how bad a flaw could be, not how likely it is to hurt you this week. Now use your judgement. I'd move F-03, the Git token, up. It's in the current pipeline file, and the attacker clearly read this repository's history. Anyone who saw the cloud key could see that token too. Every row then gets a named owner and a date. A finding with no owner is a finding nobody fixes. Answer the question: F-01.

On screen: the step text, the patch tool with the model answer.

## 7. Write the pipeline gate

Step seven: write the pipeline gate. Everything so far fixes today. The gate stops tomorrow. A gate is a policy the pipeline enforces on every change: some findings block a merge, some block a deploy, some only warn. The report builder has a policy template. The art is to be strict where a mistake is expensive and light where it isn't. A gate that blocks everything teaches people to go around it.

*After it runs:*

Read it section by section. The scope includes emergency fixes, because that's when people cut corners. Blocks the merge: any secret in the change or its history; any critical or high advisory that has a fixed version; Terraform that makes a bucket or database public or opens 22 or 3389 to the whole internet. Blocks the deploy: an image that runs as root, uses latest or an unpinned base, or has a critical OS package, and a manifest without runAsNonRoot, without allowPrivilegeEscalation false, or without resource limits. Warns only: medium and low, which go to the register with an owner. And CI uses short-lived credentials scoped to one service. Now check it against today. The cloud key, the payment key, the Git token and the database password are all secrets, so they block the merge. PyYAML, jsonwebtoken and lodash all have fixes, so they block too. The public bucket, the public database and the open SSH block. The root container and the latest tag block the deploy. Two highs from today aren't named: the curl piped into a shell, and the unencrypted database Checkov flagged. Decide whether to add them. Exceptions are written down, with an owner, a reason and an end date of at most thirty days, and the CTO approves anything over seven. And a secret is never an exception: you can't accept the risk of a key someone may already have.

On screen: the step text, the report tool with the model answer.

## 8. Automate the response

Step eight: automate the response. The miner started at 21:40, which is three in the morning in Bengaluru. Nobody was watching. A SOAR playbook does the routine part automatically: look up indicators, open tickets, block known-bad addresses, disable an account that's being abused, and page someone. It leaves the judgement calls to a person. Run it on the cloud alert queue.

*After it runs:*

Twelve automatic actions on six alerts. CL-501, high, at 21:40:12: ci-deployer's key used from a new country. Enrich finds 198.51.100.91 malicious, so the playbook blocks it. The rule says access key, so it disables ci-deployer, opens a ticket and pages someone. CL-502, critical, at 21:43:30: a burst of GPU instances in an unused region. Another ticket and another page. CL-503, medium, at 21:52:10: gpu-xl-1 opened port 3333 to pool.hashfarm.example, a known mining pool. The domain is blocked and a ticket opened. CL-505, high: the invoices bucket is public. A ticket and a page, but no automatic change. Now the two that matter for judgement. CL-504, low: monsoon-assets is public, and it's supposed to be. CL-506, low: intern.test signed in without MFA, from 49.36.12.80, which intel lists as the office Wi-Fi. Both just get a ticket. A robot that made every public bucket private would break the shop's product images. And nothing high or critical closes itself: there's no close action anywhere in this playbook. One honest trade-off: disabling ci-deployer also stops tonight's deploys. With a miner running, that's the right call, but say so in the ticket, so the developers know why the pipeline failed. Answer the question: ci-deployer.

On screen: the step text, the soar tool with the model answer.

## 9. A tested Python check

Step nine: a tested Python check. Now write the secret check ourselves, and test it before we trust it. The script has six rules, one per kind of secret. The password rule has a guard: it skips anything that starts with a dollar sign or var dot, because those are pointers, not secrets. Then five asserts, and only then a run over the whole repository.

*After it runs:*

All tests pass. Two asserts catch real secrets: a cloud key ID and a Git token. Three must find nothing: a CI variable, a Terraform variable and a plain sentence. A check that cries wolf gets switched off. Then the run: five secrets. The Git token in pipeline.yml on line 19. The database password in the Kubernetes manifest, line 25. The payment key in the Dockerfile, line 7. And the cloud key ID and secret on lines 9 and 10 of the history patch. Compare that with step two. The scanner raised seven secret findings, three of them false. Our check finds the four real ones, and it also finds the manifest password, which the scanner reported on its config tab instead. Now add one test of your own: a secret this check should catch but doesn't yet. A private key block is a good one, or a password inside a URL. Write the test first, watch it fail, then fix the rule until it passes. Answer the question: five.

On screen: the step text, the Python cell.

## 10. Hand in

Step ten: hand in. The notebook carries everything you've done: the scan results, the policy replay at zero and zero, the ranked register, the gate policy, the playbook run and the Python tests. Check the list, then press Hand in.

*After it runs:*

The rubric is on screen. The most points, five, go to the ranked register, because ranking is where judgement shows: every finding needs a priority and a reason, not just a score. If you're short of time, don't skip the reasons. A register with priorities but no reasons can't be argued with, and it can't be trusted either.

On screen: the step text.

## Wrap-up

That's Monsoon Mart's review. One commit tried to do the right thing and removed a cloud key from a file, but Git kept it. The key belonged to a pipeline that only ever deployed one service, yet it could do anything, so someone launched eight GPU machines in a region nobody watched. You cut it down to one action from one address, with zero attacker actions and zero broken deploys. You ranked ten findings by reachability and exploitation, not just score, wrote a gate that would have stopped every critical finding, let the playbook handle the routine alerts, and tested your own check. The lessons to keep: a pushed secret must be revoked, not deleted; give every identity only what its job needs; and test your tools before you trust them. Next is seminar nine, Authorised testing, where you test a web shop and its APIs on purpose, with permission, and write findings that get fixed. Thank you for watching.

## YouTube chapters (estimate; `python tools/teach.py demo s08-cloud-devsecops` writes the exact ones)

```
0:00 Opening
1:16 1. Map the repository
2:49 2. Scan for secrets, vulnerable packages and unsafe settings
5:09 3. Compare with the real scanners
7:10 4. What the leaked key did
9:00 5. Least privilege for the pipeline
10:37 6. Rank every finding
12:37 7. Write the pipeline gate
14:47 8. Automate the response
16:38 9. A tested Python check
18:16 10. Hand in
18:55 Wrap-up
```
