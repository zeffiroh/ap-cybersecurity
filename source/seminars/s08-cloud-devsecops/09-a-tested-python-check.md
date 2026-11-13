## 9. A tested Python check

Write the secret check yourself, in Python, and **test it** before you trust it. Tests prove two things: it catches what it should, and it stays quiet on what it shouldn't (a CI variable like `$CI_STRATUS_SECRET` isn't a secret). Then run it on the repository.

- [ ] Every assert passes
- [ ] It finds the secrets in the Dockerfile, the manifest, the pipeline and the history patch
- [ ] It doesn't flag `$CI_...` variables or `var.db_password`
- [ ] Add one more test of your own: a secret it should catch that it doesn't yet

> Hint: A test you write before you fix a bug is the best kind: it fails first, then passes.

?> How many secrets does the Python check find in repo/? :: 5
