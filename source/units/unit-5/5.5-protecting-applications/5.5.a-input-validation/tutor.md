# 5.5.a tutor notes

Notes for the pre- and post-lecture tutor posts.

## The intuition to hold onto
The rule worth memorizing cold before this lecture: client-side validation is a user-experience feature, not a security control, full stop, an attacker who disables JavaScript or sends a request with curl never touches your browser-side checks at all. That single fact rhymes directly with 5.1.c's BOLA lesson about hidden UI buttons: anything enforced only in the client was never actually enforced. Everything security-relevant in this skill has to happen again, independently, on the server, on every request, because the server is the one place the attacker can't reach in and edit.

## The big picture
The idea worth keeping longest is that this skill is the unifying prevention layer for practically everything in 5.1: SQL injection, XSS, and command injection are three different *symptoms* of the exact same root failure, an application trusted that input was just data when a downstream interpreter (a SQL engine, a browser, a shell) was ready to treat some of those characters as instructions. Allowlisting flips the entire defensive posture from "try to anticipate every attack" to "define what correct looks like and reject everything else," which is a fundamentally smaller and more stable problem to solve than enumerating attacker creativity. Keep canonicalization close too, validating before decoding is a classic bypass, because a filter checking the raw string never sees what the string actually becomes after the browser or server normalizes it, which is precisely how encoded path-traversal and injection payloads slip past naive filters.
