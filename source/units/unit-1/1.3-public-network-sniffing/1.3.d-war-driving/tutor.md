# 1.3.d tutor notes

Notes for the pre- and post-lecture tutor posts.

## The intuition to hold onto
War driving is worth understanding less as an attack in itself and more as *reconnaissance infrastructure*, the map an attacker builds before deciding where to strike. What makes it unsettling is how little it costs: the tool that once required a car, a directional antenna, and real dedication is now a free app on a phone already in everyone's pocket. The barrier to *finding* a target has collapsed even where the barrier to *exploiting* one hasn't.

## The big picture
The three-step protocol, verify, avoid open networks, VPN, is deliberately ordered, and the ordering itself teaches something: each step is a fallback for when the previous one fails. Verifying the SSID doesn't help if you can't actually verify it. Avoiding open networks doesn't help if the only option is open. The VPN is the last line specifically because it's the only one of the three that still protects you even when everything upstream of it went wrong, the same defense-in-depth logic you'll see formalized later in this course as a named principle, first encountered here as plain common sense.
