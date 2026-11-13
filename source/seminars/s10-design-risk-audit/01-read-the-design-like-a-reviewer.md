## 1. Read the design like a reviewer

A design review starts with questions, not tools. Read the design and list, for each part: what data it holds or carries, who can reach it, and what the team has already decided. The "decisions taken" are where most of the risk hides.

- [ ] Which parts are new, which exist already, which belong to someone else?
- [ ] Where does money get decided? Where does personal data go?
- [ ] Which of the five decisions worries you most, and why?

> Hint: Decision 1 (unsigned webhook) and decision 3 (amount from the app) both let the parent's side decide what the school believes about money.

?> Which part handles the card details? :: PayGate

?> How many outside companies does Parent Pay depend on? :: 2
