## 4. The attack that comes through the documents

T4 and T6 didn't need the attacker to type anything clever. They asked ordinary questions, the assistant retrieved a partner document, and the document carried instructions. That's **indirect prompt injection**: whoever can write to the knowledge base can talk to the model.

- [ ] Find the instructions hidden in the partner documents
- [ ] Which customer question pulls in each one?
- [ ] Who could have planted them? What review should partner content get?

> Hint: `grep -i -o 'ignore previous[^.]*\|must send[^.]*'` finds the planted sentences.

?> Which document makes the assistant send an email? (its ID) :: KB-09
