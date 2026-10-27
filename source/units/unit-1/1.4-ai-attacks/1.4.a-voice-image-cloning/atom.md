# 1.4.a, Voice/image cloning for impersonation

> **Unit 1 · 1.4 AI-Based Cybersecurity Attacks**
> **AP Learning Objective(s):** 1.4.A
> **Course skill(s):** Analyze Risk

## Learning objective (student-facing)
Identify the signals that suggest a voice or image has been
AI-cloned and describe why deepfakes make identity verification harder for defenders.

## Lesson
For decades, the phrase "I heard his voice, so I knew it was him" carried real weight. A voice on
the phone, a face on a video call, or a signature on an image felt like trustworthy proof of
identity. That assumption is now dangerously fragile. Generative AI models, specifically
voice-cloning synthesizers and image/video diffusion models, can produce audio and imagery that
are perceptually indistinguishable from genuine content to the average human listener or viewer.
Attackers are already using these capabilities to impersonate executives, impersonate family
members in distress calls, and fabricate photographic evidence for extortion.

**How voice cloning works.** A text-to-speech synthesis model can be fine-tuned on a speaker's
voice using as little as three to ten seconds of audio, scraped from a public video, a voicemail
greeting, or a social-media post. The fine-tuned model then reads any text in that person's voice
with realistic intonation, pausing, and accent. A 2023-era consumer-grade laptop can run this
process entirely offline. The attacker supplies the target voice sample and the script; the model
supplies the rest.

**How image and video cloning works.** Diffusion models and face-swapping architectures allow
attackers to replace a face in a video (deepfake video) or generate entirely synthetic images of a
real person. Both techniques require very little source material because modern foundation models
already understand how faces work; the attacker only needs to steer that knowledge toward a
specific target. Real-time deepfake video, where an attacker presents a synthesized face during a
live video call, is an active threat against financial and executive verification workflows.

**The vishing variant.** "Vishing" (voice phishing) combined with cloning is perhaps the most
immediately dangerous variant. In a documented attack pattern, an attacker identifies a financial
approver's manager, clones that manager's voice using public audio, and calls the approver with an
urgent wire-transfer request. The approver hears a voice they recognize, under a cover story that
explains why normal channels are unavailable, and approves a fraudulent transfer. Because the
attack exploits audio identity rather than any software flaw, traditional controls (email filters,
anti-malware) cannot stop it.

**Signals of a cloned call or image.** Because cloning is not perfect, defenders can watch for
indicators. In audio: unnatural cadence around pauses, missing background noise, the voice never
deviates from a flat emotional baseline, or the call breaks up when the topic requires improvised
response. In images and video: unnatural blinking rate, inconsistent lighting on the face versus
the background, hair edges that look blurred or pixelated, and faces that move slightly out of
sync with audio. However, relying on perceptual spotting alone is not a sustainable strategy, models improve continuously. The robust defense is procedural.

**Why procedural defenses matter.** The moment an organization's security posture depends on
employees correctly spotting AI artifacts, the attacker only needs to improve the model. Procedural
defenses do not depend on cloning quality and therefore generalize to future-generation tools.
Three procedural controls are covered in more depth in Topic 1.4.e and the simulation:

- **Shared secrets (code words).** A pre-agreed word or phrase known only to caller and callee
  can be requested at any time. A synthesized voice cannot supply a secret it was never trained on.
- **Callback on a trusted number.** Instead of trusting an inbound call, hang up and call back on
  the number from an official directory, not a callback number provided by the caller.
- **Out-of-band confirmation.** Approve high-value requests (wire transfers, credential resets)
  only after a confirmation over a separate channel (in person, separate device, separate app).

These defenses work because they are *asymmetric*: the attacker can clone voice and image but
cannot clone access to a pre-shared secret or to the target's personal messaging on a separate
authenticated channel, unless they have already compromised far more than an audio clip.

The social-engineering tactics from Topic 1.1 amplify deepfake attacks. An attacker who layers
urgency ("I'm in an emergency meeting, need this done NOW") onto a cloned voice call reduces the
chance the target will pause to verify. The combination of a familiar voice and manufactured
urgency is especially potent because it exploits two separate cognitive shortcuts simultaneously.
Recognition ("I know this voice") suppresses skepticism; urgency suppresses the verification step
that skepticism would trigger. Recognizing this double-stack is the first defense.

## Key terms
- **Deepfake**, synthetic media (audio, image, or video) in which AI replaces or fabricates a
  person's appearance or voice.
- **Voice cloning**, fine-tuning a speech-synthesis model on a speaker's audio to produce new
  utterances in that speaker's voice.
- **Vishing**, voice-based phishing; often combined with cloned audio.
- **Shared secret**, a pre-agreed code word used to verify identity out-of-band, defeating
  audio/video impersonation.
- **Out-of-band confirmation**, approval over a channel separate from the one being manipulated.

## Common misconceptions
- "I can always tell if a voice is fake." → Current cloning quality fools trained humans the
  majority of the time. Perceptual detection is not a reliable control.
- "Deepfakes require a lot of source material." → Three to ten seconds of audio is sufficient for
  modern voice cloning; a few public photos suffice for image synthesis.

## Try it
- **Simulation:** Correctly classify each caller as "suspect" or
  "ok" using the documented indicator signals, and reach the target score.
- **Coding problem:** Build a classifier that evaluates a dictionary of call/media
  signals and returns "suspect" or "ok" per the documented rules.
- **Quiz:** self-check on the skill's key ideas.

## Sources (local / vendor / rebuilt)
- Deep: MIT OCW (human-factors security, voice biometrics lectures), rebuilt as original prose above.
- Reference: GeeksforGeeks (deepfake overview, vishing examples).
- Practice: Cybrary (AI-based threat awareness), rebuilt locally as the simulation.
- Repo: her0marodeur/awesome-free-cybersecurity → `vendor/repos/awesome-free-cybersecurity`.
