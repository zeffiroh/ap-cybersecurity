## 1. Map the repository

Start with what's there. A repository is code **and** the instructions that build and run it: the Dockerfile, the Kubernetes manifest, the Terraform, the pipeline. Each is a place for a mistake.

- [ ] List every file in repo/
- [ ] Which file builds the image, which runs it, which creates the cloud resources, which deploys?
- [ ] Which file is an old commit, and why does history matter?

> Hint: `find repo -type f` lists everything, including hidden folders like .ci.

?> How many files are in repo/ (including hidden folders)? :: 8
