# 1.3.b tutor notes

Notes for the pre- and post-lecture tutor posts.

## The intuition to hold onto
The evil twin attack is a great case study in a pattern you'll see across this entire course: an attacker exploiting a gap between what a system *displays* and what it actually *verifies*. Your device shows you an SSID, a plain-text label anyone can broadcast, and calls that "the network." It never asks the deeper question: which piece of hardware, identified by which BSSID, is actually on the other end? The name is theater; the BSSID is the closest thing to ground truth available, and even that only works if someone maintained an approved list to check it against.

## The big picture
Notice how directly this connects back to 1.3.a: setting up an evil twin requires no zero-day, no custom exploit, nothing beyond a laptop's built-in hotspot feature, which is exactly why it's a low-skilled attacker's favorite tool despite sounding technically sophisticated. That gap between "sounds scary" and "costs nothing to execute" is worth remembering: the attacks worth worrying about most on public Wi-Fi are rarely the exotic ones, they're the cheap, high-yield ones that exploit a blind spot everyone shares.
