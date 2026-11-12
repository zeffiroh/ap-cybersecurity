## 4. A phishing classifier you can read

`subjects.csv` has 20 email subjects marked phish or ham (normal mail). The cell counts which words appear in each kind, then scores new subjects with naive Bayes: the words of a subject vote for the side they appear in more often.

- [ ] Run it and read the words that count most
- [ ] Add your own subject to the `tests` list and run it again

> Hint: a model trained on 20 emails is a toy. Real filters learn from millions, and attackers keep changing their words.

?> Which label does the model give "Quarter-end report attached for comments"? :: ham
