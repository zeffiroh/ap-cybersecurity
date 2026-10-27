# 1.2.a tutor notes

Notes for the pre- and post-lecture tutor posts.

## The intuition to hold onto
The professor's shortcut for this whole atom: a single anomaly is a coincidence; a stack of anomalies is an incident. Five failed logins alone might just be someone who forgot their password twice and fat-fingered it three more times. Five failed logins from a device you've never seen, at 3 a.m., ending in a success? Each individual fact is explainable on its own, it's the *conjunction* that collapses the space of innocent explanations. This is the same correlation principle real SIEM systems are built around, and you'll see it again every time this course asks you to combine weak signals into a strong verdict.

## The big picture
Notice something quietly important buried in "what happens after detection": a lockout stops future guesses, but it does nothing to undo a success that already happened before the threshold tripped. That's why the response checklist ends with "review the logs to determine whether a successful login occurred before the lockout", detection isn't the finish line, it's the trigger for an investigation. Carry that distinction with you into every later detection topic in this course: catching the pattern and confirming the blast radius are two separate jobs.
