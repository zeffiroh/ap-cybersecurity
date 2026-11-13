## 3. Compare with the real scanners

The platform team ran Trivy on the image, Checkov on the Terraform and Prowler on the cloud account. We can't re-run them in the browser, but their output is saved. Check that our findings match, and note what each tool sees that the others don't.

- [ ] Do Trivy's library findings match the dependency tab?
- [ ] Do Checkov's five failures match the Terraform findings?
- [ ] What does Prowler see that a code scan never could?

> Hint: Trivy also sees operating system packages inside the image. Prowler sees the running account: keys, regions, logging. Code scanners see only what's written down.

?> How many Terraform checks failed in Checkov? :: 5

?> In which region were instances launched that the company doesn't use? :: ap-southeast-3
