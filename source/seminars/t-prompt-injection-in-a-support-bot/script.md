# Lecture script: Prompt injection in a support bot

Free tutorial · about 25 minutes of lab work · the video runs about 9 minutes

Read it aloud while the demo plays (add `&demo=1` to the lab link), or record your own screen with the Teaching Desk. The demo's captions are this text, word for word.

## Opening

Welcome. Large language model apps have a new kind of bug: you attack them with words. You will talk a support bot into leaking a secret, then see a document do it without you.

## 1. The setting

Read the setting so you know the company, the date and the time zone. Then open the evidence in the case folder.

On screen: the step text and the tool.

## 2. Talk to it like an attacker

Open the simulator and chat with Tara. Try to get the staff code three ways: a direct order, a role-play, and an encoding trick. Watch the trace on the side. It shows how the assistant classified your prompt, what it retrieved and which tools it called. Nothing here is a real model; the rules are scripted so you can see why each attack works. The lesson: the system prompt is a request, not a lock.

On screen: the step text and the tool.

## 3. The attack that comes through the documents

Now the attack that needs no clever typing. T4 and T6 asked ordinary questions, the assistant retrieved a partner document, and the document carried instructions. That is indirect prompt injection: whoever can write to the knowledge base can talk to the model. Use grep to find the planted sentences, then decide what the defence is: treat retrieved text as data, limit the tools the assistant can call, and check outputs.

On screen: the step text and the tool.

## 4. Where next

Seminar 11 covers attacking and governing LLM apps, with a threat model and a governance pack at the end.

On screen: the step text and the tool.

## Wrap-up

Seminar 11 covers attacking and governing LLM apps, with a threat model and a governance pack at the end.

## YouTube chapters (estimate; `./teach demo` writes the exact ones)

```
0:00 Opening
0:24 1. The setting
1:36 2. Talk to it like an attacker
2:47 3. The attack that comes through the documents
4:00 4. Where next
```
