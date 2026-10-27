# 2.2.a tutor notes

Notes for the pre- and post-lecture tutor posts.

## The intuition to hold onto
Notice the throughline from Unit 1: tailgating works for the exact same psychological reason phishing works, it exploits the awkwardness of demanding verification from someone who seems legitimate. A locked door is a technical control, but the moment a human decides whether to hold it open, you're back in social-engineering territory, just wearing a badge instead of an email. That's why this skill belongs right after Unit 1 rather than off in its own silo: physical security and social engineering aren't two separate topics, they're the same vulnerability, human courtesy under mild social pressure, showing up in a different setting.

## The big picture
The access-log heuristics here are worth sitting with because they're your first real taste of *anomaly detection logic*, a skill this course keeps returning to in more technical forms later on. A single badge swipe at two doors 13 seconds apart isn't proof of anything by itself, it's a physically implausible pattern that a human reviewing logs by eye would probably miss, but a simple rule (time gap too short for travel distance) catches automatically. Keep that idea in your pocket: piggybacking and tailgating look identical in the log, and the only thing that changes is intent, which is precisely why you can't rely on trust or recognition ("I know that guy") as a substitute for a system that verifies every credential every time.
