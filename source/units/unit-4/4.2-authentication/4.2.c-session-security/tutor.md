# 4.2.c tutor notes

Notes for the pre- and post-lecture tutor posts.

## The intuition to hold onto
Here's the mental model to hold before the lecture starts: a session token is a temporary password that gets reissued every time you log in, and whoever holds a copy of it *is* you, as far as the server is concerned. That single fact reframes everything else in this skill, hijacking isn't about breaking your real password at all, it's about stealing the token that already proves you logged in, which means every defense here is really about protecting a piece of data, not a secret you memorized.

## The big picture
The distinction the exam will test hardest is fixation versus hijacking, and the cleanest way to keep them straight is by timing: fixation plants a known ID *before* you ever log in and just waits for you to authenticate into it, while hijacking steals a live ID *after* you're already authenticated, which is exactly why they need different fixes. Session regeneration (a fresh ID issued at the moment of login) defeats fixation because the attacker's pre-planted ID never becomes valid; secure cookie flags and encrypted transport defeat hijacking because they close the specific paths, XSS reading JavaScript-accessible cookies, plaintext sniffing on public Wi-Fi, that let an attacker steal a token that already works. The detail most students miss, and that connects directly back to 4.2.b's MFA fatigue lesson, is that logout has to be a server-side action: deleting a cookie from your browser is cosmetic if the server-side session record is still alive, because a token an attacker copied five minutes ago is just as valid after you click "logout" as it was before, the button gave you the feeling of safety without the substance of it.
