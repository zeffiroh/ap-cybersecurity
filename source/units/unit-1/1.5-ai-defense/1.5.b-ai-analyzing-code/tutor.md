# 1.5.b tutor notes

Notes for the pre- and post-lecture tutor posts.

## The intuition to hold onto
Static analysis is worth understanding by contrast with what it *isn't*: it never runs your code, it just pattern-matches the text against a list of historically dangerous constructs. That's simultaneously its superpower (catches bugs before a single test case ever executes, scales to millions of lines in milliseconds) and its ceiling (a `pickle.loads` call is flagged the same way whether it's processing untrusted user uploads or a trusted internal config file, the tool has no idea which). The six patterns here aren't an arbitrary list to memorize; each one is a place where a *string* can become *code* or a *choice* can become a *weakness* (MD5), and once you see that unifying shape, you'll start recognizing the pattern in code you've never seen flagged before.

## The big picture
It's worth explicitly connecting this skill back to 1.4.c's regex output filters: both are pattern-matching layers sitting between untrusted input and a dangerous action, and both share the exact same limitation, they catch what the defender anticipated. The difference is what's being scanned (source code here, model output there) but the underlying philosophy, and its blind spot, is identical. Recognizing that a defense technique repeats across contexts is a genuinely transferable skill, more valuable long-term than memorizing any single rule list.
