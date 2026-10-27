# 1.1.c, Email, text, and social media attacks

> **Unit 1 · 1.1 Understanding Social Engineering**
> **AP Learning Objective(s):** 1.1.A, 1.1.C
> **Course skill(s):** Analyze Risk, Detect Attacks

## Learning objective (student-facing)
Identify the distinguishing features of phishing attacks
delivered over email, SMS, and social media, and explain how channel-specific trust cues make
each delivery method effective.

## Lesson
The tactics covered in 1.1.a (urgency, authority, scarcity, intimidation) and the link and file
indicators from 1.1.b are the content of social-engineering attacks. This skill examines the
delivery channels, the pipes through which that content reaches victims, and why each channel
has its own set of exploitable trust assumptions.

### Email phishing

Email remains the dominant channel for social engineering because it is ubiquitous, inexpensive,
and easily spoofed. The core technical weakness is that the Simple Mail Transfer Protocol (SMTP)
was designed without built-in authentication: any server can claim to be any sender. Modern
defenses like SPF, DKIM, and DMARC address this partially, but misconfigured or non-adopting
domains leave the door open to spoofing.

**Phishing** (pronounced "fishing") is the mass variant: one deceptive email sent to thousands of
recipients hoping a percentage takes the bait. The attacker does not know who specifically will
respond, they cast a net. The email typically impersonates a trusted institution (a bank, a
service provider, the IRS, an employer) and directs the recipient to a lookalike credential-
harvesting page or to open a malicious attachment.

**Spear phishing** is the targeted variant. The attacker researches a specific person or
organization first, using public social media, LinkedIn, company websites, or elicitation
(1.1.b), then crafts a message tailored to that person's role, relationships, and current
context. A spear-phishing email to a finance employee might reference the company's real CEO by
name, mention an upcoming acquisition the attacker learned about from a press release, and ask
for an urgent wire transfer. The specificity makes the message far more convincing.

**Whaling** applies the spear-phishing model to high-value targets (executives, board members,
legal counsel) whose authority enables large financial transfers or access to sensitive systems.
A whaling email impersonating outside legal counsel about a confidential matter is especially
effective because the target feels the communication should stay discreet, bypassing the
normal chain of approval.

Indicators specific to email: look at the actual sending address (not just the display name),
hover over links, check whether the request asks you to bypass normal process ("please don't
loop in finance on this one"), and treat generic greetings ("Dear Customer") as a sign of a
mass phishing campaign.

### SMS phishing (smishing)

SMS attacks ("smishing") exploit the trust most people place in text messages combined with
the limited screen real estate that makes full URL inspection difficult. A phone number is easy
to spoof using commercial VoIP services. Smishing messages frequently impersonate banks,
package delivery services, or government agencies.

Channel-specific features that make smishing effective: SMS lacks the rich formatting and
branding inspection points of email; there is no sender domain to examine; URLs are often
shortened and displayed without hover-preview capability; and people receive texts on personal
devices they consider private and trusted. A message appearing to be from "UPS" about a held
package, with a link to "reschedule delivery," feels natural and time-sensitive.

Defense specific to SMS: your bank and your package carrier already have your real phone
number; they do not send you to a link to re-enter your credentials. Any text asking you to
click a link and log in is suspicious. Call the organization directly using the number on their
official website, not a number in the text.

### Social media attacks

Social media platforms offer attackers a third channel with its own distinct trust model.
Several attack forms are common:

**Impersonation of real accounts.** Attackers create accounts visually identical to a person's
or organization's legitimate profile (same avatar, same name, slightly different handle, an
extra letter, a substituted character) and use them to send direct messages to the target's
followers. Because the message appears to come from a known contact in a familiar context, the
recipient's guard is lower than with unsolicited email.

**Fake giveaways and prize notifications.** "Congratulations, you have been selected for a
$500 gift card. Click here to claim." These exploit scarcity and urgency simultaneously and
require the victim to provide personal or financial information to "receive" a reward that does
not exist.

**Watering-hole delivery.** Attackers post malicious links into communities, comment sections,
or interest groups the target is known to frequent. Because the link appears within a trusted
community context, even from apparent community members, victims are more likely to click.

**Business email compromise through social media reconnaissance.** Attackers gather org-chart
details, job titles, project names, and relationships from LinkedIn and then use that
intelligence to craft targeted email or voice attacks (covered in 1.4 in the context of AI
voice cloning). Social media is frequently the intelligence source that makes a spear-phishing
campaign convincingly specific.

### Comparing channels

Each channel exploits a different default trust assumption:
- **Email** → "This looks like it's from an organization I deal with."
- **SMS** → "Texts are personal and direct; this is from someone who has my number."
- **Social media** → "This is from someone in my network, or a brand I follow."

Attackers choose channels strategically. A target who has been trained to scrutinize email
links may still click a social media DM from what appears to be a friend. Multi-channel
campaigns are increasingly common: an attacker sends a "pre-warning" text ("expect an
important email from us"), then follows with a phishing email that now has built-in social
proof.

The defense that generalizes across all three channels: verify through an independent path.
Do not use a phone number, link, or profile provided in the suspicious message. Look up the
organization's real contact information separately, and reach out that way.

## Key terms
- **Phishing**, a mass social-engineering attack via email (or another channel) that impersonates
  a trusted entity to harvest credentials or deliver malware.
- **Spear phishing**, a targeted phishing attack crafted using intelligence about a specific
  person or organization.
- **Whaling**, spear phishing directed at high-value targets such as executives.
- **Smishing**, phishing delivered via SMS (text message).
- **Social media impersonation**, creating a fake account that closely mimics a real person or
  organization to deceive their contacts.
- **Business email compromise (BEC)**, an attack in which the attacker impersonates an
  executive or business partner to authorize fraudulent transfers or disclose sensitive data.

## Common misconceptions
- "I can always tell a phishing email by its grammar." → Spear phishing and AI-generated phishing
  (1.4.b) can be grammatically perfect and contextually accurate. Grammar is an unreliable
  signal.
- "Only email matters; texts are safe." → Smishing is growing rapidly and often bypasses the
  security awareness training that focuses on email.
- "Checking the sender name is enough." → Display names are trivially spoofed. Always inspect
  the actual sending address, not just what appears in the "From:" field.

## Try it
- **Simulation:** Classify each incoming message across a
  simulated multi-channel inbox (email, SMS, social media DM) as phishing or legitimate, and
  reach the target score.
- **Coding problem:** Implement a channel-aware phishing classifier that accepts a
  message dict with channel, sender, and body fields and returns "phishing" or "legit".
- **Quiz:** self-check on the skill's key ideas.

## Sources (local / vendor / rebuilt)
- Deep: MIT OCW (human-factors security and network security), rebuilt as original prose above.
- Reference: GeeksforGeeks (phishing, smishing, social engineering variants overview).
- Practice: Cybrary / Try Cyber phishing-awareness challenges, rebuilt locally as the simulation.
- Repo: labex-labs/cybersecurity-free-tutorials, `vendor/repos/labex-cybersecurity-free-tutorials`.
