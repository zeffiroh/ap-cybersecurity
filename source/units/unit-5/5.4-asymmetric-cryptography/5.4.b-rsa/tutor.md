# 5.4.b tutor notes

Notes for the pre- and post-lecture tutor posts.

## The intuition to hold onto
Walk into this lecture ready to do actual arithmetic, RSA is one of the few places in this course where the security concept and the math are the same object, not just a metaphor for it. Everything reduces to modular exponentiation done twice, once with each exponent, and the entire security guarantee rests on one asymmetry: computing `m^e mod n` is fast in both directions if you know the right exponent, but recovering d from e and n alone requires factoring n, which is the one direction nobody has found a fast way to do at real key sizes. Small numbers like p=3, q=11 make the steps legible; they don't make RSA weak, the operations at 2048 bits are identical, just computationally hopeless to reverse without d.

## The big picture
The connection worth keeping past this lecture is that encryption and signing (5.4.c) are the exact same modular-exponentiation machinery, just with the two exponents swapped in role: encrypting uses the public exponent first, decrypting uses the private one to undo it; signing uses the private exponent first, and anyone can verify with the public one. If the arithmetic in this skill feels solid, 5.4.c is not new math, it's the same math pointed the other direction for a different goal. Also worth remembering: real systems use e=65537 specifically because it's prime, computationally cheap to exponentiate with (thanks to its binary form), and large enough to dodge low-exponent attacks, a reminder that even in cryptography, the "obvious" choice (e=3, the smallest valid option) is often the wrong one once you account for how attackers actually behave.
