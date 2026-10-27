# 5.1.c tutor notes

Notes for the pre- and post-lecture tutor posts.

## The intuition to hold onto
Hold onto this distinction walking in: authentication answers "who are you," authorization answers "what are you allowed to touch", and BOLA exists in the gap between an API asking the first question and forgetting to ask the second. A valid login token is not a blank check; it's proof of identity, and every single request still needs its own separate check of whether *this* identity is allowed to touch *this* specific object. That's a genuinely different mental habit than the input-sanitization mindset from 5.1.a/b, here the data going in is perfectly well-formed, the attacker just changed a number in a URL, so no amount of escaping or query parameterization would have caught it.

## The big picture
The idea worth keeping past this lecture is that BOLA is what happens when a UI's convenience gets mistaken for a security boundary. Hiding the "view account 483" button for a user who's logged in as account 482 feels like it should be protective, but an attacker who calls the API directly with curl never sees that button in the first place, the missing check was never really enforced, only politely suggested by the interface. That's the same lesson 5.5.a will drive home about client-side validation being worthless for security, just applied one layer earlier: whatever the client shows or hides is a UX decision, and every security-relevant decision has to be re-verified on the server, on every request, with no exceptions.
