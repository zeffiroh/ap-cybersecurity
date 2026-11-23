from kit import after, build, chapter, clear, close, cmd, edit, files_window, save_note, say, term, wait, write

FINDINGS = """FINDINGS  Monsoon Mart cart-api   12 Nov 2026
1. Cloud key STRATUS_KEY_ID SCKA4TQ7... is in git history (deploy.sh, removed lines). It belongs to ci-deployer.
   Deleting it never un-leaked it. REVOKE the key, issue a new one, store it in CI variables.
2. CI variables and Terraform variables are pointers to secrets kept elsewhere: false positives. Mark them.
3. pyyaml has a critical advisory. Upgrade to the fixed version shown in the dependency tab.
4. Configuration: fix the critical findings first (root user, payment key in an environment variable).
"""

scenes = [
 chapter("Opening"),
 files_window(),
 say("Hello, and welcome. Developers sometimes put passwords and cloud keys into code by mistake, then delete them and think the problem is gone. It isn't. Git remembers everything. Today you'll scan a repository for secrets, vulnerable packages and unsafe settings, including a key that was deleted but still sits in the history."),
 {"point": [0.45, 0.3], "in": "files", "secs": 1.0},
 say("The setting. Monsoon Mart, an online grocery company in Bengaluru. Thursday the twelfth of November 2026. Times are UTC unless marked. The case folder has the code repository, the Git history as a patch file, and the company's cloud audit log."),
 close("files"),
 term,

 chapter("1. Scan for secrets"),
 say("The scanner looks in three places. Secrets: keys and passwords in the files and in the Git history. Dependencies: package versions with known security advisories. And configuration: the Dockerfile, Kubernetes and Terraform files that decide how the app runs. gitleaks is a free, open-source secret scanner. We point it at the repository folder."),
 cmd("gitleaks dir repo --no-banner -v 2>&1 | grep -E 'Finding|Secret|RuleID|File|Line' | cut -c1-120", 6),
 after("Each finding has the rule that matched, the file and the line. A scanner gives candidates; you decide which are real. Look closely at the cloud key. The patch removed it from deploy.sh, but the line starting with a minus sign, the removed line, still holds the key."),
 cmd("grep -n -E '^[-+]export' repo/git-history.patch", 2.5),
 after("Anyone who clones the repository can read it. Look up its key ID in the cloud audit log."),
 cmd("jq -r '[.[] | select(.key_id==\"SCKA4TQ7WZ0M2RB8\")] | .[0] | [.identity, .key_id, .action] | @tsv' cloud/audit.json", 3),
 after("It belongs to ci-deployer, the account the build pipeline uses. Deleting a secret never un-leaks it. You must revoke it and issue a new one."),
 clear,

 chapter("2. Dependencies and configuration"),
 say("Now the dependencies. The platform team saved Trivy's output for the built image."),
 cmd("grep -E 'HIGH|CRITICAL|Total' captured/trivy-cart-api.txt | cut -c1-120", 3),
 after("One package has a critical advisory, pyyaml, and the output shows the fixed version to upgrade to. Now configuration: Trivy checks the Dockerfile and Kubernetes files against a library of best practices."),
 cmd("trivy config --quiet repo 2>/dev/null | grep -E '\\((dockerfile|kubernetes)\\)$|^Failures|\\((HIGH|CRITICAL)\\):' | cut -c1-140", 15),
 after("Sort by severity and fix the critical ones first. The Dockerfile keeps a payment key in an environment variable, rated critical, and nothing sets a non-root user."),
 clear,

 chapter("3. Write it up"),
 say("Separate the real secrets from the pointers. A CI variable or a Terraform variable is a reference to a secret stored somewhere safe, not the secret itself. Marking them correctly matters, because a scanner full of noise gets ignored."),
 edit("findings-notes.txt"),
 write(FINDINGS, cps=48),
 save_note(),
 close("note"),
 clear,

 chapter("Where next"),
 say("That was one step from Seminar 8, Cloud and DevSecOps: posture, pipelines, secrets and automation. The full seminar has a longer video, every step at three levels, a graded hand-in that I mark myself, and a certificate at the end. The links are on your screen."),
 chapter("Wrap-up"),
 say("To recap. Scan the history, not just today's files. A leaked secret must be revoked, not just deleted. Separate real secrets from pointers, so the team trusts the scanner. Upgrade vulnerable packages to the fixed version, and fix critical settings first. Thank you for watching."),
 wait(2),
]

build("t-find-a-secret-in-git", scenes, host="monsoon-sec")
