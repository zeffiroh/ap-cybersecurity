# 5.3.b tutor notes

Notes for the pre- and post-lecture tutor posts.

## The intuition to hold onto
The image worth holding onto before this lecture: ECB mode is what happens when you encrypt each block of a message completely independently, and independence is exactly the problem, identical plaintext blocks produce identical ciphertext blocks, so the *shape* of your data leaks straight through the encryption, like tracing a photograph through frosted glass. That single image (the ECB-encrypted bitmap where you can still see the outline of the picture) is worth more than the definition, because it makes viscerally clear that "encrypted" is not a binary property, a cipher can be mathematically unbreakable and still leak everything that matters if it's chained together wrong.

## The big picture
The concept worth keeping past this lecture is envelope encryption, because it's the practical answer to a problem you'd hit the moment you tried to deploy any of this at scale: you can't re-encrypt a terabyte database every time you rotate a key, so instead you rotate a small key that only protects other keys. DEK encrypts the data, KEK encrypts the DEK, and the expensive operation (touching the actual data) never has to happen during rotation, only the cheap operation (re-wrapping a tiny key) does. That's a pattern worth generalizing: whenever a system needs frequent rotation of something expensive to change, look for a cheaper intermediary you can rotate instead. And notice the throughline back to 5.2's least privilege: an HSM that never releases a key in plaintext is least privilege applied to the key itself, even the system using the key never actually holds it.
