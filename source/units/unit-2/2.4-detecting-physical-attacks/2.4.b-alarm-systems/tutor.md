# 2.4.b tutor notes

Notes for the pre- and post-lecture tutor posts.

## The intuition to hold onto
The single most important sentence in this skill is the one about what an alarm is *not*: nothing about a siren physically stops anyone from walking through a broken window. An alarm is a detective control that happens to be loud, not a barrier, and confusing the two is the single most common mistake in physical security planning, because "we have an alarm" feels like it should mean "this door can't be opened" when it actually just means "someone will eventually find out it was."

## The big picture
The exit/entry delay problem is a small, elegant example of a hard engineering tradeoff you'll see again throughout this course: how do you tell a real event apart from an expected, harmless one that looks identical on a single sensor? The system can't out-think the ambiguity, it resolves it with time, giving the legitimate occupant a window to prove they're legitimate by disarming before the trip counts. Cross-zone verification solves the same ambiguity a different way: don't trust one sensor, require two independent ones to agree. Both are the same underlying lesson, a single signal is cheap to fake or misread, but two independent signals agreeing is much harder to produce by accident, which is exactly why the panic button is allowed to skip all of this: a human deliberately pressing a button is already about as high-confidence as a signal gets.
