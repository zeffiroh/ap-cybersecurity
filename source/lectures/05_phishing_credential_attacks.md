---
deck:
  title: Phishing & Credential Attacks
  kicker: Class 5
  accent: "#B3001B"
  background: "#FFFFFF"
  logo: logo.png
  background_image: bg.png
  class_number: 5
  description: How phishing emails, malicious links, fake websites, and spoofing work together to steal credentials.
  topics: [Phishing Emails, Malicious Links, Fake Websites, Credential Harvesting, Email Spoofing]
---

---
title: Phishing & Credential Attacks
cover: true
---
:::text class=sub
The most common vector for social engineering attacks, phishing targets human psychology to compromise digital identities and systems.
:::
:::list style=chips
- Phishing
- Credential Harvesting
- Social Engineering
- Identity Deception
:::

::::columns
::col::
::::card
:::text
**Phishing Overview**
A form of social engineering that uses deceptive communication, typically via email, to trick individuals into revealing sensitive information such as usernames, passwords, or financial data.
:::
::::

::col::
::::card
:::text
**Credential Harvesting**
The process of collecting user login credentials through malicious means, often executed via phishing kits, fake login pages, or man-in-the-middle attacks.
:::
::::
::::

:::image src="images/05_cover_phishing_overview.png" alt="Split illustration showing a phishing email on the left with red warning indicators, spoofed sender address, urgent subject line, and embedded malicious link, and a credential harvest funnel on the right collecting usernames and passwords into an attacker's server database" caption="Phishing and credential harvesting: two stages of the same attack chain, deception leads directly to identity theft" width=full
:::

:::notes
Phishing remains the most prevalent and effective attack vector for initial compromise in cyber intrusions. Defined in NIST Special Publication 800-61 Rev. 2 (Computer Security Incident Handling Guide), phishing is a subset of social engineering that exploits human trust and cognitive biases rather than technical vulnerabilities. These attacks typically manifest as fraudulent emails, SMS messages, or websites designed to mimic legitimate entities such as banks, cloud service providers, or corporate portals.

Credential harvesting, often a downstream objective of phishing, involves capturing authentication data through methods like fake login forms, keyloggers, or session hijacking. The harvested credentials may then be used for direct access, sold on dark web marketplaces, or leveraged in downstream attacks such as lateral movement or privilege escalation. According to the MITRE ATT&CK framework (TA0001 - Initial Access), phishing techniques like spearphishing (T1566.001) and phishing via compromised trusted entities are categorized under common adversary tactics.

These attacks exploit the principle of authority bias and urgency, manipulating users into bypassing normal security protocols. Real-world examples include CVE-2021-40539, where credential harvesting occurred through a phishing campaign targeting Zoho ManageEngine, and widespread use of open-source phishing frameworks like Gophish for red team operations.

Understanding phishing and credential harvesting is foundational to implementing controls aligned with ISO/IEC 27001 and NIST Cybersecurity Framework (ID.AM, PR.AC), which emphasize identity management and access control as core security functions.

The scale of credential theft enabled by phishing is staggering. According to the Verizon 2023 Data Breach Investigations Report, phishing was present in 36% of all analyzed breaches, more than any other single initial access technique. Real-world campaigns such as the 2022 Uber breach (where an attacker employed MFA fatigue, flooding a victim with push notifications until one was approved, after first obtaining credentials via a phishing SMS) and the 2023 MGM Resorts incident (initiated via a vishing call impersonating an IT support agent to the company help desk) illustrate how phishing continues to evolve well beyond classic email lures. ISO/IEC 27001:2022 Annex A.6.3 explicitly requires organizations to address phishing through structured awareness programs, reinforcing the standard's recognition that human factors remain the primary and most persistent attack surface across all modern threat landscapes.
:::

%%%

---
unit: Foundations
code: PHI
title: Phishing, Social Engineering's Favorite Delivery Method
---
:::callout style=soft
**Phishing** is a form of social engineering that leverages digital communication channels, primarily email, to deceive individuals into performing actions that compromise security, such as clicking malicious links, opening infected attachments, or revealing sensitive credentials.
:::

::::columns
::col::
:::list heading="Core Phishing Characteristics" style=plain
- **Delivery Mechanism**: Primarily email, but also SMS (smishing), voice (vishing), and social media
- **Intent**: Elicit an immediate, unverified response from the target
- **Psychological Leverage**: Exploits cognitive biases like authority, urgency, and familiarity
- **Payloads**: Credential harvesters, malware delivery, or financial fraud
:::

::col::
:::list heading="Common Psychological Triggers" style=chips
- Urgency ("Act now or your account will be closed")
- Authority ("This is a security alert from IT")
- Trust ("Your friend sent you a document")
- Scarcity ("Only 24 hours left to claim your prize")
:::
::::

:::pullquote
Every technique from last class shows up here, urgency, authority, trust.
:::

:::image src="images/05_phishing_delivery_mechanisms.png" alt="Hub-and-spoke diagram with 'Phishing' at the center and labeled spokes radiating outward to Email, SMS (Smishing), Voice (Vishing), Social Media, and Instant Messaging; each spoke includes a channel icon and the primary psychological trigger it exploits, such as authority for email and urgency for SMS" caption="Phishing delivery channels: email dominates but the same psychological manipulation is deployed across every digital communication medium" width=full
:::

:::notes
Phishing represents the convergence of human psychology and cyberattack strategy. It is one of the most prevalent and effective attack vectors because it bypasses technical defenses by targeting the human element, often the weakest link in the security chain. Defined by NIST SP 800-61 Rev. 2 as a form of social engineering, phishing exploits cognitive biases and emotional triggers to manipulate users into performing unintended actions.

At its core, phishing relies on the attacker's ability to impersonate trusted entities. This impersonation is achieved through carefully crafted messages that mimic legitimate communication, such as bank alerts, corporate IT notices, or invoices. These messages often incorporate psychological manipulation techniques introduced in earlier discussions on social engineering, including:

- **Urgency**: Prompting immediate action without time for reflection.
- **Authority**: Impersonating figures of power or institutional trust.
- **Familiarity/Trust**: Masquerading as known contacts or reputable organizations.

Phishing attacks are not limited to email. Variants include smishing (SMS phishing), vishing (voice phishing), and spear phishing (highly targeted phishing). According to the 2023 Verizon Data Breach Investigations Report (DBIR), phishing remains the most common initial attack vector in data breaches, contributing to over 30% of incidents.

From a technical standpoint, phishing often involves the use of spoofed sender addresses, malicious URLs, and embedded scripts. These elements are frequently obfuscated or encoded to evade detection by email filters. For example, attackers may use IDN homograph attacks (e.g., using Cyrillic characters that resemble Latin ones) to mimic trusted domains.

Organizations should implement layered defenses including email filtering (aligned with NIST SP 800-177 on email security), user awareness training, and technical safeguards such as DMARC, SPF, and DKIM to detect and block spoofed emails. Additionally, frameworks like ISO/IEC 27001 emphasize the importance of continuous education and phishing simulation exercises to reduce susceptibility.

Ultimately, phishing is not just a technical problem, it is a human one. Its persistence and effectiveness underscore the critical need for integrating behavioral science into cybersecurity education and defense strategies.
:::

%%%

---
unit: Anatomy
code: ANA
title: Anatomy of a Phishing Email
---

::::columns
::col::
:::list heading="Structural Indicators of Phishing" style=plain
- **Sender Address**, Spoofed or subtly altered domains (e.g., `support@paypa1.com`)
- **Subject Line**, Emotional triggers: urgency, fear, greed (e.g., "Your account will be closed!")
- **Greeting**, Generic or absent (e.g., "Dear Valued Customer")
- **Body Content**, Vague language, poor grammar, branding inconsistencies
- **Call to Action**, Embedded links or attachments with malicious payloads
:::

::col::
:::list heading="Behavioral Cues" style=plain
- **Tone**, Coercive or manipulative language ("Act now or face consequences")
- **Urgency**, Time-sensitive deadlines ("24 hours left!")
- **Authority Mimicry**, Impersonation of trusted entities (banks, government, tech support)
- **Social Proofing**, Fake testimonials or claims of widespread impact
:::
::::

:::callout style=pull
A phishing email is a precision-crafted deception, optimized to bypass cognitive scrutiny and trigger impulsive action.
:::

:::steps heading="How Each Email Element Targets Psychology"
1. **Spoofed Sender**, Establishes false legitimacy before the email is even opened; exploits authority bias by appearing to come from a trusted institution
2. **Alarming Subject Line**, Triggers emotional arousal (fear or urgency), activating System 1 fast thinking and bypassing deliberate evaluation
3. **Generic Greeting**, Passes unnoticed when the reader is already primed by urgency from step 2; the cognitive load from step 2 suppresses attention to this warning sign
4. **Urgency-Laden Body**, Sustains emotional pressure through loss aversion framing ("your account will be permanently closed"), suppressing rational analysis
5. **Embedded Call-to-Action**, Delivers the payload: a malicious link or attachment clicked under peak cognitive load, when the victim is least likely to verify the destination
:::

:::image src="images/05_anatomy_phishing_email.png" alt="Annotated screenshot of a phishing email with five numbered callout bubbles: (1) spoofed sender domain with a substituted character highlighted in red; (2) urgent subject line printed in bold with an exclamation mark; (3) generic salutation 'Dear Valued Customer'; (4) body text with urgency language and a subtle grammatical error circled; (5) a blue 'Verify Now' button with a tooltip revealing the actual malicious URL beneath it" caption="Anatomy of a phishing email: each structural element serves a precise psychological function, attacker craft maps directly onto cognitive bias" width=full
:::

:::notes
Phishing remains one of the most prevalent and effective initial access vectors in cyberattacks, as documented in the MITRE ATT&CK framework under Initial Access > Phishing (T1566). The anatomy of a phishing email is deliberately engineered to exploit human cognitive biases such as authority bias, scarcity bias, and loss aversion. Each component of the email serves a functional role in the attacker's social engineering strategy.

The **sender address** often employs domain spoofing or typosquatting to mimic legitimate entities. For example, `notificat1on@microsoft.com` instead of `notification@microsoft.com`. Techniques like display name spoofing (RFC 5322) are also common, where the display name appears legitimate, but the underlying email address differs. NIST Special Publication 800-62 recommends validating sender authenticity through SPF, DKIM, and DMARC protocols to detect such spoofing attempts.

The **subject line** is crafted to provoke an immediate emotional response. Phishing campaigns frequently exploit urgency ("Urgent: Verify Your Account") or fear ("Security Alert: Unauthorized Login") to bypass rational decision-making. Research in behavioral psychology, particularly Kahneman's dual-process theory, supports how phishing exploits System 1 (fast, intuitive) thinking over System 2 (slow, analytical).

The **greeting** is often generic due to the mass distribution nature of phishing. Personalization, when present, is typically achieved through data harvested from previous breaches or social media scraping. ISO/IEC 27001 Annex A.6 emphasizes the importance of user awareness training to detect such impersonal cues.

The **body content** usually contains branding inconsistencies, grammatical errors, or mismatched logos, red flags that are often overlooked under time pressure. The **call to action** is the payload delivery mechanism, often a hyperlink to a spoofed login page or a malicious attachment exploiting vulnerabilities such as those cataloged under CVEs like CVE-2021-40444 (MSHTML RCE).

Understanding these structural and behavioral cues is foundational to implementing effective phishing countermeasures, as outlined in NIST SP 800-175B and ISO/IEC 27035 incident response frameworks.
:::

%%%

---
unit: Links
code: LNK
title: Malicious Links
---
::::columns
::col::
:::table
| Trick | Example | Description |
|---|---|---|
| **Lookalike Domain** | `micros0ft-login.com` | Replaces characters with visually similar ones (e.g., `0` for `o`) |
| **Subdomain Spoofing** | `microsoft.com.secure-verify.net` | Embeds a trusted domain name within a malicious one |
| **URL Shorteners** | `https://bit.ly/3xyzABC` | Obscures the true destination of the link |
| **Mismatched Anchor Text** | `[Click Here](http://malicious.net)` | Display text misleads the user about the actual URL |
:::
::col::
:::callout style=line
Hovering over a hyperlink reveals its actual destination in most email clients and browsers. This simple action is a frontline defense against phishing.
:::

:::text
Malicious links are a core mechanism in phishing campaigns, often engineered to deceive users into visiting fraudulent login pages or malware distribution sites. These links exploit cognitive biases and limitations in how URLs are displayed by default in browsers and email clients.
:::

:::list heading="Common Techniques" style=plain
- **Homograph Attacks**: Using internationalized domain names (IDNs) that mimic ASCII characters (e.g., Cyrillic `а` instead of Latin `a`). Also known as script spoofing.
- **Path Confusion**: Embedding the real domain in the path or subdomain to mask the actual destination (e.g., `secure.bank.com.phishingsite.com`).
- **Link Obfuscation**: Employing URL shorteners or redirectors to hide the final endpoint from the user.
- **Display Text Manipulation**: The clickable text does not match the underlying `href` attribute, misleading the user.
:::
::::

:::image src="images/05_malicious_link_techniques.png" alt="Four-panel comparison of malicious URL techniques: panel 1 shows a lookalike domain with a character substitution (zero for o) circled in red; panel 2 shows subdomain spoofing with the malicious TLD underlined; panel 3 shows a shortened URL with an expanding arrow to its hidden destination; panel 4 shows anchor text mismatch with visible display text and the contrasting actual href shown below; each panel includes the technique name and a one-line detection tip" caption="Four URL deception techniques: each exploits a different assumption users make when reading a link, character recognition, domain structure, brevity, and display text trust" width=full
:::

:::notes
Malicious links are a foundational component of phishing attacks, designed to deceive users into visiting fraudulent websites that harvest credentials or deliver malware. These links exploit both technical limitations in how URLs are rendered and human cognitive biases that favor speed over scrutiny.

One of the most common techniques is the use of **lookalike domains**, where attackers register domains that visually resemble legitimate ones. This often involves substituting characters such as replacing an "o" with a zero (`0`) or using visually similar Unicode characters. This technique is sometimes referred to as a **homograph attack**, especially when leveraging internationalized domain names (IDNs) to mimic Latin characters using Cyrillic or other scripts. The goal is to bypass visual inspection by users and sometimes even automated detection systems.

Another tactic is **subdomain spoofing**, where the attacker places a trusted domain name within a longer, malicious URL. For example, `microsoft.com.secure-verify.net` may trick a user into believing the link is related to Microsoft. This abuses the common user assumption that a trusted string in the URL implies safety.

**URL shorteners** such as Bit.ly or TinyURL are also frequently abused. While useful for legitimate purposes, they obscure the final destination of a link, making it difficult for users to assess its legitimacy without clicking. Advanced phishing kits often chain multiple redirects to evade detection and confuse tracking mechanisms.

Additionally, **mismatched anchor text** is a deceptive practice where the visible hyperlink text does not match the actual destination. For instance, a link may display "Update Your Account" but actually point to `http://attackersite.net/login`. This discrepancy is often hidden in HTML-based emails or web pages.

According to **NIST Special Publication 800-62**, phishing remains one of the most prevalent attack vectors targeting human factors in cybersecurity. The publication emphasizes the importance of user awareness and defensive behaviors such as link hovering, which allows users to preview the actual URL before navigating.

From a technical standpoint, browsers and email clients have implemented various countermeasures, including IDN display policies and link tooltip previews. However, attackers continue to evolve their tactics, often leveraging legitimate services and complex redirect chains to bypass these protections.

Understanding these mechanisms is essential for both end users and security professionals. Recognizing deceptive URLs is a foundational skill in defending against credential harvesting and social engineering attacks.
:::

%%%

---
unit: Harvesting
code: CRD
title: Fake Websites & Credential Harvesting
---
:::callout style=soft
A phishing link often leads to a **cloned login page**, a pixel-perfect copy of a real site, built only to capture whatever you type into it.
:::

:::image src="images/05_credential_harvesting_flow.png" alt="Sequential five-step diagram: a phishing email with an embedded link arrow leading to a cloned bank login page rendered in a browser window; a second arrow shows the submitted credentials transmitted over an encrypted channel to an attacker's remote server labeled 'C2 Exfil'; a third arrow shows the victim's browser silently redirected to the legitimate bank website; the attacker's server displays a growing credential database table; timestamps mark each step showing the entire sequence completes in under 10 seconds" caption="Credential harvesting lifecycle: the victim experiences a seamless login while credentials are silently exfiltrated, the redirect to the real site is a deliberate anti-detection measure" width=full
:::

:::flow
Click link
Land on fake login page
Enter credentials
Credentials sent to attacker
Redirected to real site
:::

:::notes
Once you click that link, you usually land somewhere designed to look
exactly like a site you trust, your email provider, your bank, your
school portal. It's often a pixel-perfect copy.

Here's the part that makes it so effective: you type your username and
password, the page sends that straight to the attacker, and then quietly
redirects you to the real site. Many victims never even realize anything
happened, because from their perspective, they just logged in like
always.

The technical mechanism behind credential harvesting pages is considerably more sophisticated than a simple static HTML clone. Modern phishing kits, pre-packaged toolsets distributed and sold on criminal forums, can proxy authentication requests to the real website in real time. The fake page dynamically fetches and renders live content from the legitimate site, including current branding, SSL certificate indicators, and CAPTCHA challenges, making visual detection nearly impossible. This reverse-proxy architecture, implemented in adversary toolkits such as Evilginx2 and Modlishka, also captures authenticated session cookies in addition to raw credentials, enabling attackers to bypass multi-factor authentication entirely by replaying a valid post-authentication session token rather than needing to pass the MFA challenge themselves.

According to the MITRE ATT&CK framework, credential harvesting via fake web portals maps to technique T1056.003 (Input Capture: Web Portal Capture) and T1539 (Steal Web Session Cookie). The Anti-Phishing Working Group (APWG) tracked over 1.3 million unique phishing sites in Q3 2023 alone, illustrating the industrial scale at which these operations now run. Many of these sites are hosted on legitimate cloud infrastructure (AWS, Azure, Cloudflare Pages) to inherit trusted TLS certificates and IP reputation, further complicating detection.

From a forensic and incident response standpoint, the redirect to the legitimate site after credential capture is a deliberate anti-detection measure designed to delay victim awareness. NIST SP 800-61 Rev. 2 recommends that organizations monitor authentication logs for anomalous patterns, simultaneous or near-simultaneous logins from geographically disparate IP addresses are a key indicator that harvested credentials are being actively used. ISO/IEC 27035 further outlines incident response procedures that include immediate credential revocation and active session termination as primary containment actions following confirmed credential compromise. Organizations should also integrate with threat intelligence feeds that flag newly registered phishing domains mimicking their brand, enabling proactive takedown before credentials are captured at scale.
:::

%%%

---
unit: Spoofing
code: SPF
title: Email Spoofing
---
:::callout style=soft
**Email spoofing** is a technique used by attackers to forge the sender's address in an email header, making the message appear as if it originates from a trusted or legitimate source.
:::

:::list heading="Why Email Spoofing is Possible" style=plain
- The foundational protocols of email, particularly SMTP (Simple Mail Transfer Protocol), as defined in RFC 5321, were designed in an era of trusted networks and lack inherent sender authentication.
- SMTP does not verify the identity of the sender by default, allowing malicious actors to specify arbitrary "From" addresses.
- Without additional security layers, receiving mail servers have no reliable method to confirm the authenticity of the sender's domain.
:::

:::list heading="Core Email Authentication Mechanisms" style=tight
- **SPF (Sender Policy Framework)**, RFC 7208, allows domain owners to specify which IP addresses are authorized to send mail on behalf of their domain.
- **DKIM (DomainKeys Identified Mail)**, RFC 6376, adds a digital signature to outgoing emails, enabling recipients to verify message integrity and sender authenticity.
- **DMARC (Domain-based Message Authentication, Reporting, and Conformance)**, RFC 7489, builds on SPF and DKIM by providing domain-level policies and reporting mechanisms to handle failed authentication attempts.
:::

::::columns
::col::
:::table
| Mechanism | Purpose                        | Standard    |
|-----------|--------------------------------|-------------|
| SPF       | Authorize sending IPs          | RFC 7208    |
| DKIM      | Sign messages for integrity    | RFC 6376    |
| DMARC     | Enforce policy and gain insight| RFC 7489    |
:::
::col::
:::steps heading="How Email Spoofing is Mitigated"
1. Receiving server checks SPF record of sender domain
2. Verifies DKIM signature against public key in DNS
3. Evaluates DMARC policy to decide whether to accept, quarantine, or reject the message
:::
::::

:::image src="images/05_email_spoofing_spf_dkim_dmarc.png" alt="Layered email authentication architecture diagram: at the top a sending mail server dispatches an outgoing email; a middle layer shows three parallel verification tracks, SPF performing a DNS TXT record lookup to verify the sending IP address, DKIM retrieving the public key from DNS to validate the message signature, and DMARC reading the domain policy record to determine disposition; at the bottom a receiving mail server shows three outcome branches labeled Accept (green), Quarantine (yellow), and Reject (red) based on combined results" caption="SPF, DKIM, and DMARC operate as complementary layers: DMARC uses the pass/fail results of both SPF and DKIM checks to enforce the sending domain's stated policy" width=full
:::

:::notes
Email spoofing exploits the inherent lack of sender authentication in the original design of the Simple Mail Transfer Protocol (SMTP), which was standardized in RFC 5321. SMTP was developed in the early days of the internet when network participants were largely trusted, and as such, it does not include built-in mechanisms to verify the identity of the sender. This allows attackers to trivially forge the "From" field in an email header, making messages appear to originate from legitimate or authoritative sources, a technique widely exploited in phishing and business email compromise (BEC) attacks.

To combat this vulnerability, three complementary email authentication protocols have been widely adopted:

**SPF (Sender Policy Framework)**, defined in RFC 7208, enables domain owners to publish DNS TXT records that specify which IP addresses are authorized to send email on behalf of their domain. When a receiving server processes an incoming email, it performs an SPF check by querying the sender domain's DNS records to verify whether the sending IP is listed.

**DKIM (DomainKeys Identified Mail)**, outlined in RFC 6376, provides cryptographic authentication by attaching a digital signature to the email header. The sending server signs the message using a private key, and the recipient retrieves the corresponding public key from the DNS to validate the signature. This ensures that the message has not been altered in transit and that it originated from an authorized source.

**DMARC (Domain-based Message Authentication, Reporting, and Conformance)**, described in RFC 7489, unifies SPF and DKIM by allowing domain owners to publish policies that instruct receiving servers on how to handle emails that fail authentication. DMARC also provides feedback reports, giving domain owners visibility into who is sending emails on their behalf.

Despite these defenses, email spoofing is not completely eliminated. Misconfigurations, lack of enforcement, or partial deployment of these standards can still leave organizations vulnerable. For example, CVE-2021-34805 highlighted weaknesses in certain SPF implementations that could be exploited for spoofing. Therefore, while SPF, DKIM, and DMARC significantly raise the bar for attackers, they must be correctly implemented and monitored as part of a layered defense strategy, in alignment with frameworks such as NIST SP 800-177 on email security and ISO/IEC 27001 for information security management.
:::

%%%

---
unit: Variants
code: VAR
title: Phishing Comes in Many Forms
---
::::columns
::col::
:::table
| Type         | Description                                                                 |
|--------------|-----------------------------------------------------------------------------|
| Spear Phishing | Highly targeted phishing using personalized information to deceive a specific individual |
| Whaling        | A form of spear phishing focused on high-profile targets such as executives or senior officials |
| Smishing       | Phishing conducted via SMS (Short Message Service) on mobile devices         |
| Vishing        | Phishing performed over voice calls, often mimicking trusted entities       |
:::
::col::
:::callout
Each variant exploits the same core principle, social engineering, but adapts delivery mechanisms to context and target behavior. Understanding these distinctions is essential for designing layered defenses aligned with frameworks like NIST SP 800-61 (Computer Security Incident Handling Guide) and ISO/IEC 27001.
:::
::::

:::image src="images/05_phishing_variants_comparison.png" alt="Four-quadrant grid comparing phishing variants: top-left quadrant shows Spear Phishing with a targeting reticle over a single person icon and the label 'Personalized, one target'; top-right shows Whaling with an executive silhouette wearing a crown and the label 'High-value target'; bottom-left shows Smishing with a smartphone displaying a fake parcel-delivery SMS notification; bottom-right shows Vishing with a headset icon and a simulated caller ID spoofing a known bank number; each quadrant lists the delivery channel and the primary psychological lever exploited" caption="Phishing variants taxonomy: spear phishing and whaling narrow the target; smishing and vishing shift the delivery channel, psychological manipulation remains constant across all four" width=full
:::

:::notes

Phishing is not a monolithic attack vector but rather a broad category of social engineering techniques that manipulate human behavior to obtain sensitive information, typically usernames, passwords, or financial data. Each variant modifies the attack's delivery mechanism while preserving the psychological manipulation at its core.

Spear phishing targets a specific individual, often leveraging publicly available personal information from social media or corporate websites to craft convincing messages. This precision increases the likelihood of success compared to generic phishing campaigns. Whaling is a specialized subset of spear phishing aimed at high-value individuals, CEOs, CFOs, or other executives, who have access to critical systems or financial authority. These attacks often mimic legal, regulatory, or business communications to exploit urgency and authority.

Smishing (SMS phishing) exploits the trust users place in text messaging platforms, which are often less scrutinized than email. Attackers send links or prompts to induce victims to reveal credentials or install malware. Vishing (voice phishing), on the other hand, uses voice communication, either live or automated, to impersonate trusted entities such as banks or IT support. These attacks exploit real-time interaction to pressure victims into compliance.

From a defense perspective, mitigating these threats requires a combination of technical controls (e.g., DMARC for email authentication), user awareness training, and incident response procedures outlined in standards such as NIST SP 800-61 and ISO/IEC 27001. Each delivery mechanism demands tailored detection and prevention strategies due to differences in protocol, platform, and user behavior.

High-profile real-world incidents illustrate the severity of each variant. The 2016 Podesta email hack, a pivotal event in the U.S. presidential election, was a spear phishing attack in which a targeted email convinced the victim to reset his Google account password on a fake page, granting the attacker full access to tens of thousands of emails. The 2020 Twitter Bitcoin scam was initiated by vishing: attackers called Twitter employees, impersonating internal IT staff, to harvest credentials providing access to internal admin tools used to hijack high-profile accounts. The FluBot SMS campaign (active 2021–2022) compromised hundreds of thousands of Android devices across Europe via fake parcel-delivery text messages containing links to malicious APKs. These cases confirm NIST SP 800-61 Rev. 2's recommendation that organizations maintain separate detection and response playbooks for each phishing variant, since the indicators of compromise, affected platforms, and forensic evidence differ substantially across delivery channels.

:::

%%%

---
unit: Walkthrough
code: WLK
title: A Phishing Attack, Step by Step
---
::::columns
::col::
:::steps
1. A finance employee receives an "urgent invoice" email from a "vendor"
2. The email looks legitimate, correct logo, plausible amount, real-sounding contact
3. The employee clicks the attached "invoice" link
4. The link opens a fake login page mimicking the company's portal
5. The employee enters their username and password to "view the invoice"
6. The attacker now has valid credentials to the real company account
:::
::col::
:::callout
Credential harvesting via phishing remains one of the most prevalent and effective attack vectors due to its exploitation of human trust rather than technical vulnerabilities.
:::
::::

:::image src="images/05_phishing_attack_walkthrough.png" alt="Six-panel storyboard illustrating the phishing attack walkthrough: panel 1 shows a finance employee receiving an email at their desk with a vendor company logo visible in the email preview; panel 2 shows a close-up of the convincing email body with a plausible invoice amount and professional formatting; panel 3 shows a mouse cursor clicking a 'View Invoice' button link; panel 4 shows a browser loading a fake company portal login page with a lock icon visible in the address bar but a subtly wrong domain name; panel 5 shows hands typing a username and password into the login form; panel 6 shows a split screen, the employee is redirected to the real portal showing 'Welcome back' while the attacker's terminal simultaneously displays the captured valid credentials" caption="Six-step phishing attack chain: the entire sequence from email open to credential capture completes in under two minutes and leaves no malware trace on the victim's machine" width=full
:::

:::notes
This scenario exemplifies a credential harvesting phishing attack, a technique categorized under **Initial Access** within the MITRE ATT&CK framework (T1566). Unlike traditional attacks that exploit software vulnerabilities, phishing leverages social engineering to manipulate users into performing actions that compromise security, in this case, voluntarily submitting valid login credentials.

The attack begins with reconnaissance and crafting of a **spear-phishing** email, a targeted message tailored to the recipient's role and context. The attacker incorporates branding elements such as logos and uses language consistent with business norms to establish legitimacy. This phase aligns with NIST Special Publication 800-61 Rev. 2 on Computer Security Incident Handling, which emphasizes the importance of understanding attacker methodologies for detection and response.

Upon clicking the embedded hyperlink, the user is directed to a **cloned authentication page**, often hosted on a domain that visually mimics the organization's legitimate portal (e.g., `secure-login-portal.com` instead of `secure.company.com`). This is known as **typosquatting** or **domain spoofing**. The fake login form captures the submitted credentials in real time, often relaying them to the attacker while simultaneously redirecting the victim to the actual service to avoid suspicion.

Once the attacker possesses valid credentials, they gain persistent, authenticated access to internal systems without triggering traditional malware-based detection mechanisms. This technique is especially dangerous because it bypasses perimeter defenses and can persist undetected for long periods, as noted in the Verizon Data Breach Investigations Report (DBIR), where over 70% of phishing incidents result in credential misuse.

From a compliance perspective, this attack impacts controls outlined in ISO/IEC 27001 (A.9.2.3 - User Access Management) and NIST SP 800-53 (IA-6 - Authentication Feedback), which stress the need for secure credential handling and user awareness training to mitigate such risks.
:::

%%%

---
unit: Defense
code: RED
title: If You Click, What to Do
---
:::list heading="Immediate Response Actions" style=plain
- Cease all interaction with the phishing page immediately
- Change the password for the targeted account using a trusted device
- Report the incident to IT or security operations without delay
- Monitor account activity for signs of unauthorized access or misuse
:::

:::callout style=pull
Rapid reporting is the single most effective action in minimizing breach impact.
:::

::::columns
::col::
:::steps heading="Post-Click Protocol"
1. **Stop Engagement**  
   Do not input additional data or click links on the malicious page.

2. **Credential Reset**  
   Use a separate, uncompromised device to change passwords via official channels.

3. **Incident Reporting**  
   Notify your organization's security team using established communication paths.

4. **Account Surveillance**  
   Enable multi-factor authentication (MFA) and review login history for anomalies.
:::
::col::
:::table
| Action | Purpose | Timeframe |
|--------|---------|-----------|
| Stop Interaction | Prevent credential theft | Immediate |
| Password Change | Revoke attacker access | < 5 minutes |
| Report Incident | Initiate containment | < 10 minutes |
| Monitor Activity | Detect lateral movement | Ongoing |
:::
::::

:::image src="images/05_post_click_response_protocol.png" alt="Four-step response timeline diagram drawn on a horizontal time axis labeled 'Minutes after click'; Step 1 at 0 minutes shows a red stop-sign icon labeled 'Cease Interaction'; Step 2 at under 5 minutes shows a lock-reset icon labeled 'Change Password on Clean Device'; Step 3 at under 10 minutes shows an alert-bell icon labeled 'Report to Security Team'; Step 4 spanning from 10 minutes onward shows a monitoring dashboard icon labeled 'Ongoing Account Surveillance'; urgency color bands (red, orange, yellow, green) span the timeline beneath each step" caption="Post-click incident response timeline: the first five minutes are the most critical window, a fast password reset and immediate report can contain the breach before the attacker establishes persistence" width=full
:::

:::notes
Even well-trained individuals may inadvertently click a phishing link. The critical determinant of outcome is not the click itself, but the immediacy and correctness of the response. The first step is to disengage from the malicious page to prevent further data exposure. This includes avoiding any form of interaction such as form submissions, link clicks, or file downloads.

Next, the user must change the password for the targeted account. This should be done from a different device that is presumed clean, to ensure the new credentials are not intercepted. According to NIST Special Publication 800-63B, credential compromise should trigger immediate re-authentication and, where possible, revocation of session tokens.

Reporting the incident is often underemphasized but is vital for organizational defense. Prompt reporting enables security teams to initiate incident response protocols, such as network isolation, threat hunting, and user notification cascades. Delay in reporting increases the risk of credential replay, as seen in attacks leveraging CVE-2021-40539-style authentication bypasses.

Finally, continuous monitoring of account behavior is essential. This includes reviewing access logs, enabling MFA if not already active, and observing for indicators of compromise (IoCs) such as unexpected geolocation logins or privilege escalations. These practices align with both NIST SP 800-82 (Industrial Control Systems) and ISO/IEC 27001 incident management frameworks.

The organizational dimension of post-phishing response is frequently underestimated in technical training. ISO/IEC 27035-2 (Information Security Incident Management, Guidelines to Plan and Prepare for Incident Response) specifies that employee-reported phishing incidents should be triaged within one hour, with initial containment actions, session revocation, account lockdown, and notification to affected parties, completed within four hours of detection. Establishing a low-friction reporting pathway, such as a dedicated "Report Phishing" button integrated directly into the email client (available in Microsoft Outlook and Google Workspace), measurably increases reporting rates and reduces mean time to detect (MTTD). Critically, organizations should treat employees who report phishing attempts, including those who clicked before reporting, as security allies rather than policy violators. Research shows that blame-based cultures suppress voluntary reporting, increasing the window of attacker access from hours to days or weeks. The NIST Cybersecurity Framework's "Respond" function (RS.CO) explicitly emphasizes organizational communication and coordination as core incident response capabilities, recognizing that technical containment is impossible without timely human reporting.
:::

%%%

---
unit: Summary
code: SUM
title: Reading Past the Disguise
---
:::pullquote
A phishing email, a malicious link, a fake login page, and a spoofed sender are four parts of the same machine, built to turn one click into a stolen credential.
:::

::::columns
::col::
:::list heading="Core Attack Vectors" style=plain
- Phishing Emails
- Malicious Links
- Spoofed Senders
- Credential Harvesting Pages
:::
::col::
:::list heading="Tactics & Techniques" style=plain
- Social engineering
- URL obfuscation
- Domain mimicry
- Form hijacking
:::
::col::
:::list heading="Common Payloads" style=plain
- Fake login portals
- Malware downloads
- Session hijacking scripts
- Data exfiltration forms
:::
::::

:::image src="images/05_attack_chain_summary.png" alt="Left-to-right attack chain diagram with four connected nodes joined by arrows: node 1 labeled 'Spoofed Email' shows an envelope icon with a red warning badge and the MITRE ID T1566.001 below it; node 2 labeled 'Malicious Link' shows a chain-link icon with a broken lock and ID T1598; node 3 labeled 'Fake Login Page' shows a browser window icon with a skull watermark and ID T1056.003; node 4 labeled 'Credential Theft' shows a key being passed to a shadowed figure and ID T1078; below the chain a horizontal bar lists layered defenses at each stage: DMARC enforcement, URL reputation filtering, MFA, and behavioral monitoring" caption="Phishing attack chain mapped to MITRE ATT&CK: each stage has a corresponding technique ID, enabling defenders to detect and disrupt at multiple points rather than relying on a single control" width=full
:::

:::notes
In this final segment of our exploration into phishing and credential attacks, we synthesize the psychological and technical mechanisms that underpin these pervasive threats. Phishing is not merely a matter of deception; it is a structured attack chain that exploits both human cognition and system vulnerabilities. At its core lies the manipulation of trust, whether through a spoofed sender identity (often leveraging techniques like display name spoofing or domain shadowing), a malicious hyperlink masked as legitimate, or a cloned authentication interface designed to harvest credentials.

Each component of the phishing attack serves a specific function within a broader adversarial framework, such as the MITRE ATT&CK framework, where initial access techniques like "Phishing" (T1566) often lead directly to credential access via methods like "Credentials from Password Stores" (T1555) or "Input Capture" (T1056.002). The ultimate objective is typically to obtain valid authentication tokens or passwords, which can then be used for lateral movement, privilege escalation, or persistent access.

From a defensive standpoint, understanding this chain is critical. Standards such as NIST SP 800-63B emphasize the importance of secure authentication practices, including multi-factor authentication (MFA), which introduces an additional verification factor that disrupts the efficacy of stolen passwords. Similarly, ISO/IEC 27001 highlights the need for awareness training and technical safeguards to detect and prevent phishing attempts.

By recognizing the interplay between social manipulation and technical exploitation, students begin to appreciate why layered defenses, spanning people, processes, and technology, are essential in mitigating credential-based threats.

Defenders who internalize the full attack chain, from initial reconnaissance through credential exfiltration and post-compromise lateral movement, are best positioned to implement controls that break the chain at multiple simultaneous points. Deploying DMARC at enforcement policy (`p=reject`) disrupts the spoofed sender stage. Providing users with real-time URL reputation checking (browser extensions integrating VirusTotal or Google Safe Browsing) disrupts the malicious link stage. Implementing phishing-resistant MFA via FIDO2/WebAuthn hardware keys disrupts the credential harvesting stage by ensuring captured credentials cannot be replayed at all, since authentication is cryptographically bound to the legitimate domain origin. Establishing continuous behavioral monitoring through a SIEM, aligned with NIST SP 800-137 Continuous Monitoring guidance, detects post-compromise credential use even when earlier controls are bypassed. No single control is sufficient; the chain must be challenged at every link, and detection capability must exist at each stage to enable rapid containment when a control fails.
:::

%%%

---
unit: Deep Dive
code: SPR
title: Spear Phishing, When Attackers Do Their Homework
---
:::callout style=soft
**Spear phishing** elevates generic phishing into a precision weapon: attackers invest hours or days researching the target before sending a single message, radically increasing the probability of success.
:::

::::columns
::col::
:::list heading="Reconnaissance Sources" style=plain
- **LinkedIn**, job title, reporting structure, colleagues, project names
- **Corporate website**, executive names, org charts, press releases, vendor partnerships
- **Twitter / X**, recent travel, conferences attended, personal interests
- **Data breach dumps**, previously compromised email and password pairs
- **WHOIS / certificate transparency**, internal subdomains and infrastructure hints
:::
::col::
:::list heading="Spear Phishing vs. Generic Phishing" style=plain
- **Generic**: Sent to thousands; generic branding; low open rate (~3%)
- **Spear**: Sent to one or a handful; references real names, projects, dates
- **Personalization increases click-through rate from ~3% to as high as 70%** per Proofpoint 2023 State of the Phish
- **Harder to filter**: passes content heuristics because details are accurate
:::
::::

:::steps heading="Spear Phishing Workflow"
1. **Target Selection**, Choose individual based on access level or role (finance, IT admin, executive assistant)
2. **Reconnaissance**, Harvest public information from social media, LinkedIn, and news articles
3. **Pretext Crafting**, Build a believable scenario tied to real events (e.g., "following up on the Q3 vendor review you mentioned at RSA")
4. **Payload Delivery**, Send highly personalized email with credential harvesting link or malicious attachment
5. **Exploitation**, Use harvested credentials immediately for lateral movement before password is changed
:::

:::code language=mermaid caption="Spear phishing workflow: the investment in reconnaissance dramatically compresses the time between delivery and successful credential harvest"
flowchart TB
  A["1 Target selection<br/>finance manager chosen"] --> B["2 OSINT<br/>LinkedIn, social media, company site"]
  B --> C["3 Pretext<br/>a believable business reason"]
  C --> D["4 Tailored email<br/>names, projects, timing"]
  D --> E["5 Action<br/>payment, login or attachment"]
:::

:::notes
Spear phishing is classified under MITRE ATT&CK technique T1566.001 (Spearphishing Attachment) and T1566.002 (Spearphishing Link). Unlike bulk phishing, which relies on probability, sending millions of messages and waiting for a small percentage to bite, spear phishing inverts the strategy: invest heavily upfront in reconnaissance to achieve near-certain success against a single high-value target.

The reconnaissance phase typically leverages Open Source Intelligence (OSINT) gathering. LinkedIn alone provides attackers with an organizational chart, role descriptions, reporting lines, names of direct colleagues, and sometimes even the internal project names an employee is working on. Platforms like Hunter.io allow enumeration of corporate email address formats (e.g., firstname.lastname@company.com), while certificate transparency logs (accessible via crt.sh) reveal internal subdomains that hint at infrastructure and services. Combine this with data from prior breaches available on platforms like Have I Been Pwned, and an attacker can quickly assemble a detailed profile of the target before writing a single line of the phishing email.

The resulting pretext is what makes spear phishing so dangerous. A message that references the target's actual manager by name, mentions a real project they are working on, and arrives during a busy period (such as fiscal year-end or a known upcoming audit) will bypass the mental pattern-matching that identifies generic phishing. The cognitive load required to question a contextually accurate message is significantly higher than questioning a generic "Dear Customer" email.

A professional profile is a reconnaissance resource. From LinkedIn alone, an attacker can build a detailed dossier on most people in under thirty minutes, which is the link between OSINT and targeted social engineering.

From a defensive standpoint, NIST SP 800-177 Rev. 1 (Trustworthy Email) recommends that organizations combine technical email authentication controls (SPF, DKIM, DMARC) with behavioral analytics that flag emails referencing insider context from unexpected senders. ISO/IEC 27001:2022 control A.6.3 (Information security awareness, education, and training) specifies that awareness programs should include targeted training on spear phishing recognition, particularly for employees in finance, HR, and executive support roles who are disproportionately targeted. The FBI's IC3 reported that spear phishing-enabled Business Email Compromise caused over $2.7 billion in losses in 2022 alone, more than any other category of internet crime.
:::

%%%

---
unit: Deep Dive
code: BEC
title: Business Email Compromise, Whaling at Scale
---
:::callout style=soft
**Business Email Compromise (BEC)** is a financially motivated attack in which an adversary impersonates an executive or trusted business partner to manipulate employees into authorizing fraudulent wire transfers, disclosing sensitive data, or purchasing gift cards.
:::

:::table
| BEC Scenario | Impersonation Target | Requested Action | Avg. Loss |
|---|---|---|---|
| CEO Fraud | CEO / President | Urgent wire transfer | $125,000+ |
| Vendor Invoice Fraud | Known supplier | Change bank account on file | $80,000+ |
| Attorney Impersonation | External legal counsel | Confidential fund transfer | $60,000+ |
| HR / Payroll Redirect | HR or Payroll manager | Change direct deposit details | $30,000+ |
:::

:::callout style=line
BEC does not require malware. The attacker's only tool is a convincing email and an employee authorized to move money or data.
:::

::::columns
::col::
:::list heading="Why BEC Works" style=plain
- Exploits authority hierarchy, employees are conditioned to comply with executive requests
- Creates artificial urgency ("wire must clear by 5 PM today")
- Requests secrecy ("do not discuss with finance team, confidential deal")
- Often arrives on a Friday afternoon when oversight is lowest
:::
::col::
:::list heading="BEC Red Flags" style=plain
- Request originates from a free email domain (Gmail, Yahoo) mimicking corporate name
- Unusual payment amount or destination country
- Request to bypass normal approval workflows
- Executive "traveling" and "unreachable by phone"
:::
::::

:::code language=mermaid caption="Four BEC attack scenarios: each exploits a different trusted relationship, but all rely on the same formula, authority plus urgency plus secrecy"
flowchart LR
  A["<b>CEO fraud</b><br/>Spoofed executive asks for<br/>an urgent wire transfer"] ~~~ B["<b>Vendor invoice fraud</b><br/>Real-looking invoice with<br/>changed bank details"]
  C["<b>Attorney impersonation</b><br/>Confidential deal, pressure<br/>to skip normal checks"] ~~~ D["<b>Payroll diversion</b><br/>Employee's direct deposit<br/>switched to attacker account"]
:::

:::notes
Business Email Compromise is the most financially damaging form of cybercrime tracked by the FBI Internet Crime Complaint Center (IC3). Unlike ransomware or data theft, BEC produces an immediate, direct, and often irreversible financial loss, wire transfers to overseas accounts can be nearly impossible to claw back once processed. The FBI IC3 2022 report documented $2.7 billion in BEC losses, representing a 65% increase over 2019 figures, confirming this as the single highest-loss cybercrime category.

BEC maps to MITRE ATT&CK T1534 (Internal Spearphishing) when the attacker has already compromised an internal email account, and T1566.001 or T1566.002 when operating from external spoofed or look-alike domains. The most sophisticated BEC operations begin with credential theft, a phishing campaign against a mid-level employee, whose compromised mailbox is then used to silently monitor email traffic for weeks, learning the cadence of financial conversations, the names of banking partners, and the approval workflows before launching the actual BEC request. This silent monitoring phase (MITRE T1114, Email Collection) means by the time the fraudulent request arrives, it arrives knowing exactly what language, amount thresholds, and approval processes the target organization uses.

BEC attacks cluster on Friday afternoons before long weekends. The finance staff who approve wires are less available, the impersonated executive is "traveling", and the target is under pressure to finish before the weekend. The countermeasure is policy: any wire request above a threshold requires a same-day call-back to a known number, however legitimate the email looks.

NIST SP 800-177 Rev. 1 recommends implementing strict sender authentication (DMARC at p=reject) as a first-layer defense, since many BEC campaigns rely on look-alike domains rather than full account compromise. ISO/IEC 27001:2022 Annex A.8.8 (Management of technical vulnerabilities) and A.5.19 (Information security in supplier relationships) both address the vendor impersonation vector. The most robust procedural control against BEC is a mandatory out-of-band verification step, calling the requestor at a known, pre-established phone number before authorizing any change to banking details or any unusual financial transaction, regardless of email authority level.
:::

%%%

---
unit: Deep Dive
code: SMI
title: Smishing, Phishing Moves to Your Phone
---
:::callout style=soft
**Smishing** (SMS phishing) delivers phishing content via text message. The high open rate of SMS (98% vs. ~20% for email) and the reduced screen real estate for URL inspection make it a highly effective attack channel.
:::

::::columns
::col::
:::list heading="Why SMS Is a Dangerous Vector" style=plain
- SMS messages are opened within 3 minutes of receipt on average
- Mobile browsers display truncated URLs, full destination is hidden
- No equivalent of email's SPF/DKIM/DMARC for SMS sender verification
- Personal device = reduced organizational oversight and endpoint security
- Blending with legitimate delivery notifications and bank alerts
:::
::col::
:::list heading="Common Smishing Pretexts" style=plain
- Parcel delivery failure ("Your package is held, confirm address")
- Bank fraud alert ("Unusual activity detected, verify now")
- Government / tax authority ("IRS: You owe back taxes, pay now or face penalty")
- Prize or contest winner notification
- COVID / health authority alerts (active heavily in 2020–2022)
:::
::::

:::steps heading="Anatomy of a Smishing Attack"
1. **Mass SMS blast**, Attacker purchases bulk SMS sending credits and target phone number lists from data brokers or breach dumps
2. **Pretext message**, Short, urgent message impersonating a brand or authority with a shortened or cloaked URL
3. **Mobile landing page**, Responsive fake login page optimized for mobile; often uses legitimate brand CSS
4. **Credential capture**, Victim enters credentials; data is logged and attacker is notified in real time
5. **Optional malware delivery**, On Android, the page may also prompt installation of a malicious APK (e.g., FluBot, TangleBot)
:::

:::code language=mermaid caption="Smishing exploits SMS's high trust and open rate: a fake delivery notification is indistinguishable from a real one on a small screen where the full URL is never visible"
flowchart TB
  A["SMS from 'FedEx': parcel held,<br/>short link included"] --> B["Short link expands to a<br/>lookalike domain"]
  B --> C["Mobile-friendly fake page<br/>asks for card or login"]
  C --> D["Details sent to the attacker"]
  E["Defense: open the courier's app or site yourself,<br/>never the link in the text"] -.- B
:::

:::notes
Smishing has grown dramatically as attackers recognize that mobile devices have outpaced desktops as the primary communication and authentication tool for most users. According to Proofpoint's 2023 State of the Phish report, 76% of organizations experienced smishing attacks in the prior year, a 10-percentage-point increase from 2022. The channel is effective for several converging reasons that deserve careful analysis.

First, the trust model for SMS is fundamentally different from email. Users apply much more skepticism to email (especially from unknown senders) than to text messages, which are psychologically associated with personal communication. When a message arrives claiming to be from FedEx about a package, it feels plausible, most people are expecting deliveries regularly, and the same companies do legitimately send SMS notifications.

Second, mobile browsers truncate long URLs. On a smartphone, a URL like `https://fedex-delivery-confirm.tracking-portal.ru/login?ref=XYZABC` may display as simply `fedex-delivery-confirm.track...`, with the malicious domain suffix completely hidden from view. This is a structural UI vulnerability that no amount of user training fully compensates for; users must develop the habit of actively tapping the address bar to expand the full URL before proceeding.

Third, there is no SMS equivalent of DMARC. Telephone numbers can be spoofed using VoIP services, and Sender ID (the name displayed above a text message) can be set arbitrarily by the sending party on many carrier networks. This means a smishing message can display "FedEx" or "Chase Bank" as its sender name with no technical authentication behind it.

FluBot (2021–2022) was an Android banking trojan spread by smishing. Once a phone was infected, it harvested the contact list and sent smishing messages to every contact from that device, making each victim an unwitting attacker of their own contacts. More than 11 million phones were targeted across Europe before Europol dismantled the infrastructure in May 2022.

NIST SP 800-187 (Guide to LTE Security) addresses SMS security limitations in the context of mobile network infrastructure. ISO/IEC 27001:2022 Annex A.6.8 (Information security event reporting) recommends organizations establish channels for employees to report suspected smishing messages, since corporate devices receiving smishing attempts may indicate targeted intelligence gathering against the organization. Defense recommendations include using SMS filtering apps, enabling operating system phishing protection (Google Safe Browsing on Android, Fraudulent Website Warning on iOS Safari), and never clicking links in unexpected SMS messages, navigating to the official app or website directly instead.
:::

%%%

---
unit: Deep Dive
code: VIS
title: Vishing, Social Engineering by Voice
---
:::callout style=soft
**Vishing** (voice phishing) uses phone calls, live human or automated (robocall/IVR), to impersonate trusted entities and extract sensitive information or manipulate victims into taking harmful actions in real time.
:::

:::table
| Vishing Scenario | Impersonated Entity | Target Action |
|---|---|---|
| IT Help Desk Impersonation | Internal IT support | Reveal password / install remote access tool |
| Bank Fraud Alert | Bank security department | "Confirm" account number and PIN |
| Government / IRS Call | IRS or Social Security Administration | Pay fake tax debt via gift cards |
| Tech Support Scam | Microsoft / Apple support | Grant remote desktop access |
| Executive Impersonation | CEO or COO | Authorize urgent wire transfer |
:::

:::list heading="Why Vishing is Uniquely Dangerous" style=plain
- **Real-time manipulation**: The attacker can adapt immediately to resistance or skepticism
- **Voice conveys authority**: Tone, confidence, and scripted expertise bypass cognitive scrutiny
- **Caller ID spoofing**: The displayed number can match the bank or company being impersonated (no technical barrier)
- **Artificial urgency**: "Your account will be locked in 10 minutes" is far more visceral spoken aloud than written
:::

:::code language=mermaid caption="Vishing attack scenarios: the unifying element is caller ID spoofing, the displayed number establishes false legitimacy before the first word is spoken"
flowchart LR
  A["<b>IT help desk</b><br/>lever: authority"] ~~~ B["<b>Bank fraud team</b><br/>lever: fear of loss"] ~~~ C["<b>Tax agency</b><br/>lever: threat of penalty"] ~~~ D["<b>Tech support</b><br/>lever: helpfulness"] ~~~ E["<b>Senior executive</b><br/>lever: hierarchy"]
:::

:::notes
Vishing combines the psychological power of human voice communication with technical deception (caller ID spoofing) to create an attack surface that most users are entirely unprepared for. Unlike phishing emails, which have been the subject of awareness training for two decades, vishing attacks catch users off-guard precisely because they involve a direct human interaction, a context where compliance and politeness are deeply conditioned responses.

Caller ID spoofing is technically trivial. VoIP services such as those built on the SIP protocol allow any calling party to set the "From" field of the SIP INVITE message, which maps to the displayed caller ID on the recipient's device. Services like SpoofCard make this available to anyone with a credit card. This means a vishing attacker can make a call appear to originate from a victim's own bank, their corporate IT help desk, or a government agency, with zero technical sophistication required. STIR/SHAKEN (Secure Telephone Identity Revisited / Signature-based Handling of Asserted information using toKENs) is a framework being deployed by US carriers (mandated by the FCC under the TRACED Act in 2021) to authenticate caller identity at the carrier level, but adoption is incomplete and international calls remain largely unauthenticated.

The 2020 Twitter hack is the canonical enterprise vishing case study. Attackers called Twitter employees, claiming to be from Twitter's internal IT team conducting a VPN credential migration during the COVID-19 remote work transition. Employees who "confirmed" their credentials on a fake internal portal provided the attackers with access to Twitter's administrative tools, which were then used to hijack the accounts of Barack Obama, Elon Musk, Apple, and others to run a Bitcoin scam. The attackers were teenagers, the sophistication was entirely social, not technical. MITRE ATT&CK classifies this under T1598.004 (Phishing for Information: Spearphishing Voice).

Pretext calls succeed even against people who know to expect them. The correct response to any unsolicited call asking for credentials or verification is to hang up and call back on a number obtained independently, such as from the company website, never a number the caller supplies.

NIST SP 800-63B section 6.1 (Authentication Assurance Levels) recommends that high-value authentication actions should never be performed over voice channels unless supplemented by a secondary out-of-band verification. ISO/IEC 27001:2022 Annex A.6.3 specifies that security awareness programs must cover social engineering via all channels, explicitly including voice. Organizations should also implement a verification protocol for IT support interactions, a shared secret or ticketing system reference number that legitimate support staff can provide, making impersonation detectable without requiring users to recognize the attack on their own.
:::

%%%

---
unit: Deep Dive
code: AIT
title: Bypassing MFA, Adversary-in-the-Middle Attacks
---
:::callout style=soft
When phishing campaigns encounter Multi-Factor Authentication, attackers do not give up, they proxy the authentication flow in real time, capturing both credentials **and** the session cookie that proves MFA was completed.
:::

:::flow
Victim visits phishing site
Phishing site forwards request to real site (reverse proxy)
Real site challenges for MFA
Victim completes MFA on phishing site
Session cookie transmitted to attacker
Attacker replays cookie, bypasses MFA entirely
:::

::::columns
::col::
:::list heading="AiTM Toolkit Examples" style=plain
- **Evilginx2**, Open-source reverse proxy phishing framework; captures session cookies with MITM technique (GitHub)
- **Modlishka**, Configurable reverse proxy phishing tool supporting any target site
- **Caffeine**, As-a-Service phishing platform sold on criminal forums; AiTM built in
- **Storm-1167**, Microsoft-tracked threat actor group using AiTM against Microsoft 365 since 2022
:::
::col::
:::list heading="Why Push-Based MFA Falls Short" style=plain
- SMS OTP: interceptable via SIM swap or real-time relay
- Authenticator app TOTP (30-second code): relayable in real time via proxy
- Push notification approval: susceptible to MFA fatigue / push bombing
- **What works**: FIDO2 hardware keys / passkeys, cryptographically bound to the originating domain, cannot be relayed
:::
::::

:::code language=mermaid caption="AiTM phishing renders push-based MFA ineffective by capturing the post-authentication session cookie, the only current defense is phishing-resistant FIDO2 authentication"
flowchart LR
  V["Victim's browser<br/>sees a real-looking sign-in page"] <-->|"credentials and MFA code"| P["Attacker's reverse proxy<br/>relays everything"]
  P <-->|"same traffic, forwarded"| L["Legitimate Microsoft 365"]
  L -->|"session cookie issued"| P
  P --> S["Attacker reuses the session cookie:<br/>MFA already satisfied"]
  D["Defense: phishing-resistant MFA (FIDO2),<br/>which is bound to the real domain"] -.- P
:::

:::notes
Adversary-in-the-Middle (AiTM) phishing, also known as real-time phishing or proxy-based phishing, represents the most important technical evolution in phishing over the past five years. Its emergence directly challenges the common belief that enabling MFA provides comprehensive protection against credential theft via phishing, a belief that led many organizations to consider phishing a "solved problem" after MFA deployment.

The mechanism works as follows: instead of presenting a static HTML clone of the target login page, the phishing site acts as a transparent reverse proxy. When the victim submits their username and password, the proxy forwards those credentials to the legitimate site in real time. The legitimate site then triggers its MFA challenge (push notification, TOTP code, SMS). The victim completes the MFA on what they believe is the real site, but is actually the attacker's proxy. The legitimate site then issues an authenticated session cookie. The proxy captures this session cookie before forwarding it to the victim. The attacker now possesses a valid authenticated session cookie that can be imported into their own browser using standard developer tools, granting full access to the victim's account with no need for the password or the MFA factor.

Microsoft's Detection and Response Team (DART) documented this technique being used by the threat actor group tracked as Storm-1167 (previously DEV-1167) in widespread campaigns against Microsoft 365 customers throughout 2022 and 2023. Microsoft reported that campaigns using this approach achieved post-MFA account takeover on tens of thousands of accounts. The Evilginx2 tool, released publicly on GitHub, implements this attack against virtually any web application that uses standard cookie-based session management, which is essentially all of them.

MFA is valuable but not complete. It defeats credential stuffing and most mass phishing, but adversary-in-the-middle (AiTM) campaigns that proxy the login session capture the session cookie after MFA succeeds.

The only currently effective defense against AiTM session cookie theft is phishing-resistant authentication using FIDO2 WebAuthn. In FIDO2, the cryptographic challenge-response is bound to the origin domain (the RP ID). A proxy attack fails because the challenge from `login.microsoft.com` will specify that domain as the RP ID, and the hardware key will sign a challenge bound to that domain, a signature that is valid only for that domain, not for `microsoft.secure-portal-login.net`. No relay can make this work. NIST SP 800-63B Digital Identity Guidelines (4th Edition draft, 2023) elevates phishing-resistant authenticators (FIDO2/WebAuthn and PIV smart cards) to Authenticator Assurance Level 3 (AAL3) and recommends their use for high-value accounts. CISA's 2022 advisory "Implementing Phishing-Resistant MFA" explicitly recommends organizations migrate away from SMS OTP and push notifications toward FIDO2 hardware keys for privileged accounts.
:::

%%%

---
unit: Tool Spotlight
code: TSP
title: Tool Spotlight, Evilginx2 & Phishing Frameworks
---
:::callout style=soft
Security teams use purpose-built phishing frameworks in authorized red team engagements to test whether controls and users would stop a real adversary. Understanding these tools is essential for defenders.
:::

:::table
| Tool | Type | Primary Use | Notable Feature |
|---|---|---|---|
| **Evilginx2** | Reverse-proxy phishing framework | AiTM credential + cookie capture | Captures session cookies; defeats MFA |
| **GoPhish** | Phishing simulation platform | Authorized awareness testing | Web UI; campaign analytics; open-source |
| **Modlishka** | Reverse proxy phishing | AiTM attacks on any site | Fully configurable; no static clones needed |
| **SEToolkit (SET)** | Social engineering toolkit | Phishing + pretexting + spear phishing | MITRE ATT&CK mapped; Metasploit integration |
| **PhishFlood** | Mass credential harvesting (criminal) | Malicious use only | Listed for awareness; not for use |
:::

:::list heading="Ethical and Legal Boundaries" style=plain
- **Always required**: Signed Rules of Engagement (ROE) and written authorization before any phishing simulation
- **Scope limits**: Test only against systems and users explicitly covered by the authorization
- **Prohibited**: Using these tools outside of authorized engagements is illegal under the Computer Fraud and Abuse Act (CFAA), Computer Misuse Act (UK), and equivalent laws worldwide
- **Red team goal**: Identify training gaps and control failures before a real adversary does
:::

:::notes
Understanding the tools used by attackers, and by authorized red teams simulating attackers, is a core competency for security practitioners. Phishing simulation frameworks have proliferated over the past decade, lowering the technical barrier for both legitimate security testing and malicious use. The same capabilities that allow a red team to test organizational resilience can be weaponized by adversaries; this dual-use nature demands that defenders understand how these tools work in order to detect their signatures and respond appropriately.

Evilginx2, created by security researcher Kuba Gretzky and published openly on GitHub, implements the AiTM architecture described in the previous slide. It uses a modified Nginx web server configured with "phishlets", YAML configuration files that define how to proxy a specific target site. Setting up a phishlet for Microsoft 365, Google Workspace, or GitHub takes a trained attacker approximately 30 minutes. The framework captures all cookies set by the target site post-authentication, including session cookies, and logs them in a structured database accessible to the attacker via a web interface. Defenders can detect Evilginx2 deployments by monitoring for newly registered domains with SSL certificates matching their brand, anomalous reverse-proxy server headers in phishing page responses, and session logins from geographically anomalous IP addresses immediately following authentication.

GoPhish is the most widely used open-source platform for authorized phishing awareness campaigns. It provides a web-based interface for building phishing email templates, defining target recipient lists, configuring landing pages, and generating detailed campaign analytics, including open rates, click rates, credential submission rates, and time-to-click distributions. The data produced by a GoPhish campaign is directly actionable: it identifies which departments, roles, or individuals are most vulnerable and allows security teams to target remediation training accordingly. NIST SP 800-50 (Building an Information Technology Security Awareness and Training Program) recommends phishing simulation as a core component of security awareness programs. ISO/IEC 27001:2022 Annex A.6.3 (Information security awareness) similarly emphasizes practical testing over passive training content.

Authorization is the line between penetration testing and crime. Every red-team engagement requires a written authorization letter, a scope document naming the systems and users in scope, and rules of engagement listing permitted actions. Phishing simulations against an organization's own staff serve to measure a baseline, target training and track improvement over time.
:::

%%%

---
unit: Case Study
code: CS1
title: Case Study, The 2016 Podesta Spear Phishing Attack
---
:::callout style=soft
In March 2016, a single spear phishing email gave Russian military intelligence (GRU) access to tens of thousands of emails that would shape the outcome of a U.S. presidential election, a defining illustration of what targeted credential theft can achieve.
:::

:::steps heading="Attack Timeline"
1. **March 19, 2016**, John Podesta (Clinton campaign chairman) receives email appearing to be from Google security, warning his Gmail account has been compromised from Ukraine
2. **The email contains a link to a credential harvesting page** disguised as a Google password reset form, a classic spear phishing page with Google branding
3. **An aide forwards the email to an IT staffer** who responds that it is "a legitimate email" (intending to type "illegitimate", a typo with historic consequences)
4. **Podesta follows the link and changes his password on the fake page**, delivering his Gmail credentials to APT28 (Fancy Bear / GRU Unit 26165)
5. **Approximately 50,000 emails are exfiltrated** from Podesta's Gmail account over the following months
6. **WikiLeaks begins publishing the emails in October 2016**, two months before the election
:::

:::table
| Attack Attribute | Detail |
|---|---|
| Threat Actor | APT28 (Fancy Bear), GRU Unit 26165 |
| MITRE Technique | T1566.002, Spearphishing Link |
| Target | Single high-value individual |
| Impact | 50,000 emails exfiltrated and published |
| Defense that would have stopped it | FIDO2 hardware key / passkey on Gmail account |
:::

:::code language=mermaid caption="Podesta attack timeline: one spear phishing link, one credential submission, 50,000 emails, the entire breach had no malware and left no forensic trace on Podesta's device"
flowchart TB
  A["March 19, 2016<br/>Fake Google security alert sent to Podesta's Gmail"] --> B["A staff reply calls it legitimate; password entered on the fake page"]
  B --> C["Tens of thousands of emails taken"]
  C --> D["October 2016<br/>Emails published during the election campaign"]
:::

:::notes
The 2016 Podesta email hack is perhaps the most consequential phishing attack in history from a geopolitical impact perspective, and it is instructive precisely because of its simplicity. There was no zero-day exploit, no advanced malware, no sophisticated intrusion, just a spoofed email, a convincing pretext, and a credential harvesting page. The attack succeeded entirely because of human factors.

The phishing email was crafted by GRU operators to appear as a Google security alert, a format many Gmail users recognize because Google does legitimately send such alerts. The email warned that someone from Ukraine had accessed Podesta's account and urged immediate action to secure it. This pretext is particularly effective because it activates loss aversion (protecting an existing valued asset), urgency (act now), and authority (a trusted service provider issuing a security warning) simultaneously.

The chain of human errors that compounded the initial attack is equally instructive. When the email was forwarded to IT staffer Charles Delevan for verification, he responded "This is a legitimate email", intending to indicate the opposite but never correcting the typo. This illustrates a communication failure that no technical control could have prevented: the human chain broke independently of the original technical deception.

The attack was later attributed to APT28 (Fancy Bear), GRU Unit 26165, through forensic analysis of the command-and-control infrastructure, bitly URL tracking pixel metadata, and TTP (tactics, techniques, and procedures) analysis matching known GRU operational patterns. The U.S. Department of Justice indicted 12 GRU officers in July 2018 (United States v. Netyksho et al.) with specific charges related to this campaign, providing a detailed public record of the attack methodology.

In the 2016 Podesta compromise, the target's privilege, not technical sophistication, determined the impact. A FIDO2 hardware security key would have stopped the attack: its cryptographic response is bound to the legitimate Google domain, so a credential-harvesting page on another domain receives nothing usable. Google's Titan Security Key, introduced in 2018, provides exactly this protection.
:::

%%%

---
unit: Case Study
code: CS2
title: Case Study, The 2022 Uber Breach via MFA Fatigue
---
:::callout style=soft
In September 2022, an 18-year-old attacker compromised Uber's internal systems using a combination of credential purchase, smishing, and MFA push bombing, reaching internal Slack, cloud infrastructure, and source code repositories within hours.
:::

:::steps heading="Attack Sequence"
1. Attacker purchases Uber contractor credentials from a dark web marketplace (previously harvested from a separate breach)
2. Login attempt triggers MFA push notification, contractor denies it repeatedly for over an hour
3. Attacker impersonates Uber IT support via WhatsApp message ("I'm from Uber IT security, you will keep receiving these MFA alerts; please approve one so we can investigate your account")
4. Contractor approves the MFA push, attacker gains authenticated session
5. Attacker explores internal systems and finds a PowerShell script on a network share containing hardcoded PAM (privileged access) credentials
6. Uses PAM credentials to access SentinelOne EDR console, G Suite admin, AWS, HackerOne vulnerability disclosure portal, and internal Slack workspace
:::

:::callout style=line
MFA fatigue (push bombing) exploits human compliance behavior, not a technical vulnerability. The attack succeeds when a user approves a push simply to make it stop.
:::

:::code language=mermaid caption="Uber 2022 breach: the initial MFA push bombing exploited human compliance under persistent pressure, the subsequent hardcoded credentials discovery enabled lateral movement across the entire estate"
flowchart TB
  A["Contractor credentials bought<br/>on a dark web market"] --> B["Repeated MFA push requests<br/>over about an hour"]
  B --> C["WhatsApp message posing as<br/>Uber IT: accept to make it stop"]
  C --> D["Push approved, VPN access gained"]
  D --> E["Admin credentials found in a<br/>network share script"]
  E --> F["Internal tools and cloud consoles accessed"]
:::

:::notes
The 2022 Uber breach is one of the most instructive modern case studies for demonstrating the intersection of several distinct attack techniques covered in this unit: social engineering, credential purchasing from breach marketplaces, MFA fatigue attacks, and the critical importance of secrets management (hardcoded credentials in scripts).

MFA fatigue, also termed push bombing, exploits a specific human behavioral pattern. When a user receives repeated MFA push notifications for logins they did not initiate, the experience is deeply stressful and disruptive. Most users understand that something is wrong, but the attacker counts on a subset of users eventually approving a push to make the interruptions stop, or because they convince themselves it might be a system error. The attack becomes far more effective when combined with a social engineering layer (the WhatsApp impersonation message) that provides a plausible explanation and explicit instruction to approve the notification.

The discovery of hardcoded PAM credentials in a PowerShell script illustrates a class of vulnerability that is entirely independent of phishing, secrets management failure. Once inside the network perimeter with a single authenticated session, the attacker found that internal scripts contained plaintext passwords with administrative privileges. This is classified under MITRE ATT&CK T1552 (Unsecured Credentials). The existence of those credentials in plaintext on a network share turned a single contractor account compromise into a full organizational breach reaching source code, vulnerability disclosures, and cloud infrastructure.

From a defensive standpoint, this incident motivated several specific control recommendations. CISA's advisory on MFA fatigue recommends implementing number matching in MFA push notifications, requiring the user to enter a code displayed on the login page into the approval app, rather than simply tapping "Approve." This makes real-time relay attacks far more difficult. Microsoft Authenticator and Google Authenticator both support number matching as of 2023. Additionally, Microsoft Entra ID (Azure AD) introduced additional context in MFA push notifications showing the geographic location and application requesting authentication, providing users with the information needed to detect anomalous requests. NIST SP 800-63B's forthcoming revision specifically addresses push bombing as a known weakness of simple push-based authenticators and recommends number matching or phishing-resistant alternatives for AAL2 and above.

FIDO2 hardware keys would have stopped the 2022 Uber breach at its first stage, because authentication is bound to the legitimate domain and stolen credentials would have been worthless. Issuing hardware keys to every contractor and temporary worker is logistically difficult, which is why number-matching push MFA is a practical intermediate step. Security choices trade assurance against operational feasibility.
:::

%%%

---
unit: Framework
code: IDN
title: Deep Dive, Homograph and IDN Attacks
---
:::callout style=soft
**Internationalized Domain Name (IDN) homograph attacks** exploit the visual similarity between characters from different Unicode scripts to register domains that are pixel-perfect impersonations of legitimate ones, invisible to users and sometimes to automated scanners.
:::

::::columns
::col::
:::list heading="How IDN Homograph Attacks Work" style=plain
- ICANN permitted non-ASCII characters in domain names (RFC 3492, Punycode) to support international languages
- Unicode contains thousands of characters visually identical or near-identical to common Latin letters
- Attackers register domains using these lookalike characters, encoded in Punycode (e.g., `xn--pple-43d.com` = `аpple.com` using Cyrillic `а`)
- The browser displays the rendered Unicode, the user sees `аpple.com` not `xn--pple-43d.com`
:::
::col::
:::table
| Visual Display | Actual Character | Unicode Code Point | Script |
|---|---|---|---|
| а | а (Cyrillic a) | U+0430 | Cyrillic |
| а | a (Latin a) | U+0061 | Latin |
| ο | ο (Greek omicron) | U+03BF | Greek |
| o | o (Latin o) | U+006F | Latin |
| і | і (Cyrillic i) | U+0456 | Cyrillic |
| i | i (Latin i) | U+0069 | Latin |
:::
::::

:::steps heading="IDN Homograph Attack Walkthrough"
1. Attacker identifies target domain (e.g., `paypal.com`)
2. Finds Cyrillic characters visually identical to Latin letters in the domain name (p, a, y, l)
3. Registers `раураl.com` (using Cyrillic `р`, `а`, `у`), Punycode: `xn--aypal-ova.com`
4. Obtains a free TLS certificate (Let's Encrypt does not validate visual similarity), the padlock appears in the browser
5. Deploys credential harvesting page with authentic PayPal branding
6. Sends phishing email pointing to `раураl.com`, visual inspection finds nothing wrong
:::

:::code language=mermaid caption="IDN homograph attack: both domains look identical in the address bar, only examining the Punycode representation or checking Unicode character details reveals the deception"
flowchart LR
  L["<b>Legitimate</b><br/>paypal.com<br/>all Latin letters"] ~~~ H["<b>Homograph</b><br/>pаypal.com<br/>second letter is Cyrillic а (U+0430)"]
  H --> P["Punycode form shows the trick:<br/>xn--pypal-4ve.com"]
  D["Defense: browsers show punycode for mixed scripts;<br/>password managers will not autofill"] -.- P
:::

:::notes
IDN homograph attacks were first publicly described by security researcher Evgeniy Gabrilovich and Shmuel Matias in a 2001 paper, but became practically weaponizable after ICANN introduced internationalized domain names to support non-Latin scripts in global internet addresses. The attack class exploits a fundamental tension between two design goals: making the internet accessible in all world languages, and making domain names visually unambiguous.

The Punycode encoding (RFC 3492) converts non-ASCII Unicode characters into ASCII-compatible encodings prefixed with `xn--`. So `аpple.com` (with Cyrillic `а` U+0430) encodes as `xn--pple-43d.com`. The DNS system operates purely on the Punycode form, it does not process or store Unicode. Browsers, however, decode Punycode back to Unicode for display, presenting users with the visually deceptive form. Modern browsers have partially mitigated this by displaying the Punycode form instead of Unicode when a domain contains mixed scripts, but single-script homographs (all Cyrillic, all Greek) may still display in Unicode form depending on the browser version and locale settings.

A landmark 2017 proof-of-concept by security researcher Xudong Zheng registered `xn--80ak6aa92e.com`, which displayed as `apple.com` with Cyrillic characters in fully updated Chrome and Firefox browsers at the time. The PoC included a valid TLS certificate obtained from Let's Encrypt, demonstrating that the padlock icon offers no protection against IDN homograph attacks, since certificate authorities verify domain ownership (control of DNS), not visual uniqueness.

The Cyrillic "а" and the Latin "a" are indistinguishable at normal display sizes, so people cannot be trained to spot IDN homograph domains by eye. Technical controls, browser IDN display policies and domain monitoring services, must replace human inspection here.

Defensive controls include: browser IDN display policies (Chrome displays Punycode for domains mixing Latin with non-Latin in the same domain component); organizational domain monitoring services that alert when lookalike domains (including Punycode variants) are newly registered mimicking the company name; and user education focused on verifying domain identity using browser security indicators beyond just the padlock (e.g., examining the full certificate Subject Alternative Name). NIST SP 800-177 Rev. 1 addresses this in the context of email sender domain verification, noting that visual domain inspection is insufficient and must be supplemented by technical authentication controls.
:::

%%%

---
unit: Framework
code: DMA
title: DMARC Deep Dive, From Monitor to Enforce
---
:::callout style=soft
DMARC is a policy framework, not just a technical check. Understanding how to move from `p=none` (monitoring only) to `p=reject` (full enforcement) is the difference between having DMARC and DMARC actually protecting your organization.
:::

:::table
| DMARC Policy | What Happens on Failure | Visibility Gained | Risk Level |
|---|---|---|---|
| `p=none` | Message delivered normally | Aggregate and forensic reports sent to domain owner | Zero (monitoring only) |
| `p=quarantine` | Message moved to spam/junk folder | Reports continue | Medium (some disruption if misconfigured) |
| `p=reject` | Message rejected by receiving server, never delivered | Reports continue | Full enforcement (misconfiguration blocks legitimate mail) |
:::

:::steps heading="The DMARC Deployment Journey"
1. **Publish SPF record**, list all legitimate sending IP addresses for your domain in a DNS TXT record
2. **Implement DKIM signing**, configure all legitimate email senders to cryptographically sign outgoing mail
3. **Publish DMARC record at p=none**, begin receiving aggregate reports (RUA) and forensic reports (RUF) without blocking any mail
4. **Analyze reports**, identify all legitimate mail streams (marketing platforms, CRMs, helpdesks) that need SPF/DKIM alignment
5. **Remediate gaps**, ensure every legitimate sending source passes SPF or DKIM alignment
6. **Escalate to p=quarantine**, failed messages go to spam; monitor for legitimate mail caught in quarantine
7. **Escalate to p=reject**, full enforcement; spoofed messages are rejected at the receiving server
:::

:::code language=mermaid caption="DMARC deployment is a journey, not a switch: premature enforcement without full alignment visibility blocks legitimate mail, the p=none monitoring phase is not optional"
flowchart TB
  subgraph PRE["Prerequisites"]
    direction LR
    S1["1 Inventory all senders"] --> S2["2 Publish SPF and DKIM"]
  end
  subgraph MON["Monitor and fix"]
    direction LR
    S3["3 p=none, read reports"] --> S4["4 Fix failing legitimate senders"]
  end
  subgraph ENF["Enforce"]
    direction LR
    S5["5 p=quarantine, rising percentage"] --> S6["6 p=reject"] --> S7["7 Ongoing report review"]
  end
  PRE --> MON --> ENF
:::

:::notes
DMARC (Domain-based Message Authentication, Reporting, and Conformance), defined in RFC 7489, is frequently misunderstood as a binary control, either you have it or you don't. In practice, the effectiveness of DMARC is entirely determined by which policy is enforced and whether all legitimate sending infrastructure is properly aligned before enforcement is activated. Many organizations publish DMARC records at `p=none` and then leave them there indefinitely, gaining the reporting visibility but none of the protection.

The alignment requirement is the core concept that makes DMARC meaningful. DMARC requires that the domain in the email's "From" header aligns with either the domain authenticated by SPF (the "envelope from" / Return-Path) or the domain signing the DKIM signature (the `d=` tag in the DKIM-Signature header). Without alignment, passing SPF or DKIM on its own does not constitute DMARC compliance, because an attacker can pass SPF on their own domain while spoofing your domain in the "From" header.

The DMARC aggregate report (tag `rua=`) is sent daily by receiving mail servers and contains XML data showing volume, sources, and authentication results for all mail claiming to come from your domain. Analyzing these reports, either manually or through a DMARC reporting tool such as Dmarcian, Valimail, or Agari, reveals sending sources that the domain owner may not be aware of (marketing platforms, transactional email services, third-party CRMs) that must be brought into alignment before enforcement is safe.

Moving DMARC from p=none to p=quarantine often reveals a legitimate sender, such as a cloud ERP system, a benefits provider or a partner sending on the domain's behalf, that was never configured for DKIM, so its mail starts going to spam. The p=none phase is best treated as an audit of every system that sends email under the domain, not a formality before enforcement.

NIST SP 800-177 Rev. 1 Section 4.6 provides comprehensive guidance on DMARC deployment, explicitly recommending the phased approach described here. The Cybersecurity and Infrastructure Security Agency (CISA) Binding Operational Directive 18-01 (updated as BOD 23-02 in 2023) mandated DMARC at `p=reject` for all U.S. federal executive branch domains, representing the most significant government endorsement of DMARC enforcement as a mandatory control. Organizations that have achieved `p=reject` see a near-total elimination of spoofed email impersonating their domain, since receiving servers worldwide that honor DMARC will reject the messages before they reach user inboxes.
:::

%%%

---
unit: Comparison
code: CMP
title: Phishing vs. Spear Phishing vs. Whaling, Choosing the Right Defense
---
:::callout style=soft
The appropriate defense strategy scales with the attack's precision: mass phishing requires bulk technical controls; spear phishing requires behavioral detection; whaling requires executive-specific process controls that no technical layer can fully substitute for.
:::

:::table
| Dimension | Mass Phishing | Spear Phishing | Whaling / BEC |
|---|---|---|---|
| **Target** | Anyone | Specific individual or role | C-suite / high-privilege executives |
| **Volume** | Millions of messages | Tens to hundreds | One to a handful |
| **Personalization** | None | High, references real context | Maximum, mimics known relationships |
| **Technical Sophistication** | Low | Medium | Low-Medium (often no malware) |
| **Success Rate per Message** | ~3% | Up to 70% | Very high when pretext is credible |
| **Primary Technical Defense** | Email filtering, DMARC, URL scanning | Behavioral analytics, OSINT monitoring | Out-of-band verification policy |
| **Primary Human Defense** | Awareness training, recognize generic indicators | Role-specific training, recognize OSINT-sourced lures | Executive briefing + strict wire transfer protocol |
| **MITRE ATT&CK ID** | T1566 | T1566.001 / T1566.002 | T1566.001 + T1534 (post-compromise) |
:::

:::callout style=line
No single control layer defends against all three variants. Effective programs deploy different controls at different layers targeting each variant's specific characteristics.
:::

:::code language=mermaid caption="Phishing defense matrix: each variant requires a distinct response layer, the same control that stops mass phishing is largely irrelevant against a targeted whaling attack"
flowchart LR
  M["<b>Mass phishing</b><br/>Scope: millions<br/>Personalization: generic<br/>Key defense: email filtering"] ~~~ S["<b>Spear phishing</b><br/>Scope: chosen people<br/>Personalization: researched<br/>Key defense: training, MFA"] ~~~ W["<b>Whaling</b><br/>Scope: one executive<br/>Personalization: deep<br/>Key defense: payment verification"]
:::

:::notes
One of the most persistent mistakes in organizational security programs is treating "phishing defense" as a single undifferentiated problem. Security awareness training that teaches users to look for generic indicators like spelling errors and urgent subject lines will produce almost no reduction in spear phishing or whaling success rates, because those attacks are specifically engineered to pass exactly those checks. Conversely, executive-level process controls like mandatory out-of-band wire transfer verification add significant operational friction for a control class that provides near-zero protection against mass phishing campaigns targeting lower-level employees.

Effective programs must map defenses to attack types. For mass phishing, the primary value is achieved through technical controls that scale: DMARC at `p=reject`, URL reputation filtering at the email gateway and browser level, attachment sandboxing, and general awareness training that addresses generic phishing indicators. These controls can filter out the vast majority of bulk phishing traffic before it reaches users. NIST SP 800-177 Rev. 1 provides the technical implementation framework for all of these email security controls.

For spear phishing, the defense emphasis shifts toward detection. Technical controls that examine sender reputation and message content against a baseline are valuable, but since spear phishing messages frequently originate from legitimate sending infrastructure (a compromised email account in the supply chain), content-based filtering is less reliable. Behavioral analytics that flag anomalies, an email referencing an internal project name from an external sender, an attachment file type unusual for the sender-recipient pair, become the primary detection layer. OSINT monitoring services that alert when information about executives or ongoing projects is newly indexed on public platforms provide proactive intelligence about reconnaissance activity.

For whaling and BEC specifically, process controls are the most effective mitigation. A mandatory policy requiring a phone call to a known, pre-registered number to verify any wire transfer, change to banking details, or request to bypass normal approval workflows, regardless of how legitimate the authorizing email appears, breaks the attack chain completely. No impersonation technique can survive a verification call to a number the attacker does not control. ISO/IEC 27001:2022 Annex A.5.19 (Information security in supplier relationships) and A.8.4 (Access to source code) both address process controls relevant to BEC prevention. NIST SP 800-53 control AC-3 (Access Enforcement) and AC-6 (Least Privilege) apply to limiting the blast radius when an executive account is compromised.
:::

%%%

---
unit: Mid-Lecture Checkpoint
code: CHK
title: Check Your Understanding, Phishing Fundamentals
---
:::callout style=soft
Take two minutes to answer these questions before we move on. If any are unclear, flag them now, the next section builds directly on these concepts.
:::

::::columns
::col::
:::list heading="Quick-Check Questions" style=plain
- What is the difference between phishing and spear phishing?
- Which protocol allows a domain owner to specify which IP addresses may send email on its behalf, SPF, DKIM, or DMARC?
- What does a DMARC `p=reject` policy instruct receiving mail servers to do?
- Name one technique attackers use to bypass SMS-based MFA in real time.
- What is the single most effective action a user should take within the first five minutes of realizing they submitted credentials to a phishing page?
:::
::col::
:::list heading="Concept Connections" style=plain
- Which phishing variant uses voice calls as its delivery channel?
- IDN homograph attacks exploit characters from which type of standard? (Hint: covers multilingual characters)
- In the Uber 2022 breach, what human behavior did the attacker exploit after obtaining credentials?
- A company's CFO receives an email from the CEO requesting an urgent wire transfer. What process control is the most effective defense?
- Name two MITRE ATT&CK technique IDs relevant to phishing-based initial access.
:::
::::

:::table
| Term | Brief Definition |
|---|---|
| Smishing | Phishing delivered via SMS |
| Vishing | Phishing delivered via voice call |
| AiTM | Adversary-in-the-Middle; captures session cookies via reverse proxy |
| DMARC | Email authentication policy that enforces SPF/DKIM and reports on failures |
| MFA Fatigue | Attacker spams MFA push approvals hoping victim will approve to stop the alerts |
:::

:::notes
This checkpoint slide is designed as an active recall moment, a retrieval practice exercise grounded in cognitive science research showing that testing recall (rather than re-reading) is the most effective method for encoding information into long-term memory (Roediger and Karpicke, 2006; NIST SP 800-50 cites similar principles for security training effectiveness).

Pause the lecture here and give students two minutes to write answers to the Quick-Check Questions without looking at their notes. After two minutes, work through the answers collectively.

Model answers for the Quick-Check Questions:
1. Phishing is sent broadly to many recipients with generic content; spear phishing is sent to a specific individual and uses personalized context gathered through reconnaissance.
2. SPF (Sender Policy Framework), defined in RFC 7208, allows domain owners to specify authorized sending IP addresses in DNS TXT records. DKIM provides cryptographic signing; DMARC provides policy enforcement using SPF and DKIM results.
3. DMARC `p=reject` instructs receiving mail servers to reject (not deliver and not quarantine) any message that fails DMARC alignment checks, the message is discarded before reaching the recipient's inbox.
4. AiTM (Adversary-in-the-Middle) proxy attack using tools like Evilginx2: the phishing site proxies the real MFA challenge to the victim in real time and captures the resulting session cookie after the victim completes MFA.
5. Change the compromised password from a clean, unaffected device, using the legitimate service's official website navigated to directly, not via any link, and then report the incident to the security team immediately.

Model answers for Concept Connections:
1. Vishing uses voice calls.
2. Unicode (ISO/IEC 10646), the international character encoding standard that includes characters from hundreds of world scripts, many of which are visually indistinguishable from Latin letters.
3. MFA fatigue / push bombing, after obtaining credentials via a smishing message, the attacker logged in repeatedly, flooding the contractor with MFA push notifications, then impersonated Uber IT support via WhatsApp to convince the contractor to approve a push.
4. Mandatory out-of-band phone verification to a pre-registered number, call the CEO back at a known number to confirm the request before any funds move.
5. T1566 (Phishing), T1566.001 (Spearphishing Attachment), T1566.002 (Spearphishing Link), T1566.003 (Spearphishing via Service), any two of these are correct.

:::

%%%

---
unit: Human Factors
code: COG
title: Cognitive Biases Exploited in Phishing
---
:::callout style=soft
Phishing does not defeat technical controls, it defeats human psychology. Understanding the specific cognitive biases targeted by phishing attacks is the first step toward building defenses that remain effective under pressure.
:::

:::table
| Cognitive Bias | Definition | How Phishing Exploits It | Example Phishing Phrase |
|---|---|---|---|
| **Authority Bias** | People comply with requests from authority figures | Impersonate executives, IT, banks, government | "This is a message from your IT department." |
| **Urgency / Scarcity** | Pressure of limited time suppresses deliberate analysis | Time-bound threats force hasty action | "Your account will be closed in 24 hours." |
| **Loss Aversion** | Fear of loss is twice as motivating as hope of gain | Frame action as preventing loss rather than gaining benefit | "Failure to verify will result in permanent account suspension." |
| **Social Proof** | People follow perceived majority behavior | Fake testimonials or claims about widespread impact | "Thousands of users have already secured their accounts." |
| **Reciprocity** | People feel obligated to return favors | Offer something (free gift, prize, reward) before requesting action | "You've been selected for a special security upgrade, click to claim." |
| **Familiarity / Liking** | People comply more readily with people or brands they like | Impersonate known brands, colleagues, or friends | "Your friend [Name] shared a document with you." |
:::

:::code language=mermaid caption="Six cognitive biases converge on the phishing hook: attackers select and combine these levers based on the target's role and context to maximize the probability of unverified compliance"
mindmap
  root((Phishing hook))
    Authority bias
      "This is the CEO, do it now"
    Urgency
      "Account closes in 24 hours"
    Scarcity
      "Only 3 bonus slots left"
    Social proof
      "Your whole team has signed"
    Reciprocity
      "Here is your free gift card"
    Familiarity
      "Hi, it's Sam from IT again"
:::

:::notes
Phishing is fundamentally an applied psychology problem. Attackers do not study computer science to craft effective phishing campaigns, they study human behavior. The most sophisticated phishing kits are not sophisticated in their technical construction; they are sophisticated in their selection and combination of psychological levers calibrated to the specific target population.

Psychologist Daniel Kahneman's dual-process theory, popularized in "Thinking, Fast and Slow" (2011), provides the foundational framework for understanding why phishing is so effective. System 1 thinking (fast, automatic, intuitive) handles the vast majority of daily decisions including routine email processing. System 2 thinking (slow, deliberate, analytical) is cognitively expensive and is suppressed under conditions of time pressure, stress, and cognitive load. Phishing specifically creates the conditions that keep the victim in System 1, time pressure (urgency), emotional arousal (fear of account closure), and authority cues (trusted brand recognition) all serve to suppress the transition to System 2 analytical evaluation.

Authority bias (Milgram, 1963) is particularly powerful in organizational contexts. Hierarchical structures condition employees to comply with directives from managers and executives without demanding detailed justification, a social norm that BEC and executive impersonation attacks exploit directly. The compliance rate for spoofed executive requests is higher among employees who have recently been praised by their managers, consistent with research on reciprocity and social bonding (Cialdini, "Influence," 1984).

Loss aversion, identified by Kahneman and Tversky (1979), explains why "your account will be closed" consistently outperforms "protect your account" as phishing call-to-action language. Prospect theory demonstrates that people are approximately twice as motivated to avoid a loss as they are to achieve an equivalent gain. Phishing copywriters exploit this asymmetry systematically.

Behavioral inoculation, or prebunking, exposes users to weakened forms of manipulation before they meet real attacks, by analogy with vaccination. Research by Basol, Roozenbeek and van der Linden (2021) found that prebunking significantly increases resistance to manipulation compared with conventional awareness training. Examples include SIFT training (Stop, Investigate, Find better sources, Trace claims) and the Cambridge Social Decision-Making Lab's "Go Viral" game, developed with WHO and UNICEF. ISO/IEC 27001:2022 control 6.3 expects awareness training to address psychological manipulation, not only technical indicators.
:::

%%%

---
unit: Controls
code: SIM
title: Phishing Simulation Programs, Measuring and Building Resilience
---
:::callout style=soft
A phishing simulation program systematically tests user susceptibility using controlled, authorized fake phishing campaigns, the results drive targeted training, measure improvement over time, and satisfy compliance requirements.
:::

::::columns
::col::
:::list heading="Phishing Simulation Program Components" style=plain
- **Baseline campaign**: Measure initial susceptibility rate before any targeted training
- **Difficulty tiers**: Escalate from generic phishing to spear phishing as the program matures
- **Immediate teachable moment**: Users who click see an educational message explaining what they missed, not a punishment notification
- **Metrics dashboard**: Track click rate, credential submission rate, reporting rate, and improvement trend over time
- **Targeted training**: Users who click receive role-specific micro-training rather than a blanket all-hands session
:::
::col::
:::list heading="Key Metrics to Track" style=plain
- **Click Rate**: % of recipients who clicked the simulated phishing link
- **Credential Submission Rate**: % who submitted simulated credentials
- **Report Rate**: % who used the "Report Phishing" button before clicking
- **Mean Time to Report**: How quickly employees report suspected phishing
- **Repeat Offender Rate**: % of employees who click across multiple simulation campaigns
:::
::::

:::table
| Simulation Tier | Difficulty | Personalization | Expected Click Rate (industry avg.) |
|---|---|---|---|
| Tier 1, Generic | Low | None | 15–25% |
| Tier 2, Brand Impersonation | Medium | Known brand + urgency | 10–20% |
| Tier 3, Spear Phishing | High | Role-specific context + colleague names | 5–15% |
| Tier 4, Targeted executive | Very High | Full OSINT-based pretext | Varies by individual |
:::

:::code language=mermaid caption="Phishing simulation program lifecycle: the value is in the trend over time, not any single campaign result, a mature program should show measurable reduction in susceptibility across simulation cycles"
flowchart LR
  A["Baseline campaign"] --> B["Immediate training<br/>at the moment of the click"]
  B --> C["Metrics analysis"]
  C --> D["Targeted follow-up<br/>for high-risk groups"]
  D --> E["Harder repeat campaign"]
  E --> C
:::

:::notes
Phishing simulation programs are among the most evidence-based interventions in security awareness training. Unlike passive training modules (videos, e-learning) which show modest and rapidly decaying effect sizes, simulation programs create a direct feedback loop: the user encounters a realistic phishing attempt in a safe environment, makes a decision, and immediately receives corrective feedback that is contextually tied to the specific mistake they made.

NIST SP 800-50 Rev. 1 (Building a Cybersecurity and Privacy Learning Program) explicitly endorses phishing simulations as a measurement tool for awareness program effectiveness, recommending that organizations track susceptibility rates over time and use the results to prioritize training investment. NIST SP 800-53 control AT-2 (Literacy Training and Awareness) and AT-3 (Role-Based Training) both align with the tiered simulation approach, different employee roles face different attack profiles and should receive training calibrated to those profiles.

The "teachable moment" design principle is critical. Research by Kumaraguru et al. (2007, Carnegie Mellon CyLab) demonstrated that embedding the phishing lesson at the moment of the click, when the user's attention is highest and their error is most salient, produces significantly better retention than equivalent training delivered at a later time. The message displayed to a user who clicks should immediately show the indicators they missed, explain why this was phishing, and provide one or two concrete detection tips they can apply going forward. It should NOT display a punitive message, their name on a list, or a threat of disciplinary action, blame-suppresses future reporting behavior and erodes the trust relationship between employees and the security team.

Phishing simulation programs can backfire. A first campaign that is too sophisticated causes mass failure and resentment rather than learning. Programs work better when they begin with generic, detectable simulations and announce in advance, without dates, that simulations will happen. ISO/IEC 27001:2022 control 6.3 frames awareness as a continuous-improvement process, consistent with this iterative design.

Organizations can run phishing simulations using open-source tools (GoPhish) or commercial platforms (KnowBe4, Proofpoint Security Awareness Training, Microsoft Attack Simulator). Commercial platforms offer pre-built simulation templates that mimic real-world phishing campaigns including replicas of actual observed phishing emails, current brand impersonations, and tiered difficulty libraries. The choice between open-source and commercial depends on team capacity: GoPhish requires more manual effort to manage template creation and reporting, while commercial platforms offer automated campaign management, reporting, and integration with HR systems for tracking training completion.
:::

%%%

---
unit: Controls
code: TEC
title: Technical Anti-Phishing Controls, A Layered Defense Stack
---
:::callout style=soft
No single technical control stops all phishing. Effective defense stacks controls at multiple layers so that failure of any one control does not result in a successful credential harvest.
:::

:::table
| Layer | Control | What It Stops | Limitation |
|---|---|---|---|
| **Email Gateway** | DMARC `p=reject` + SPF + DKIM | Spoofed sender addresses | Does not protect against compromised legitimate sender accounts |
| **Email Gateway** | Attachment sandboxing | Malicious attachments with zero-day exploits | Sandboxing evasion; time-delay payload activation |
| **Email Gateway** | URL reputation filtering | Known malicious links at time of click | Newly registered malicious domains bypass reputation checks initially |
| **Browser** | Safe Browsing / Phishing page detection | Known phishing URLs | Newly created phishing pages not yet indexed |
| **Browser** | HTTPS certificate validation | MITM certificate tampering | Does not validate domain identity, HTTPS ≠ safe |
| **Identity** | Phishing-resistant MFA (FIDO2) | Credential relay and AiTM cookie theft | Requires hardware key procurement and deployment |
| **Identity** | Conditional access policies | Login from anomalous location / device | Requires baseline of normal behavior; false positives |
| **Endpoint** | EDR / behavioral monitoring | Post-compromise malware execution | Does not address credential theft via web form |
| **Monitoring** | SIEM / authentication log alerting | Simultaneous logins from multiple geolocations | Requires baseline tuning; generates alert fatigue if uncalibrated |
:::

:::callout style=line
HTTPS padlock = the connection is encrypted. It does NOT mean the website is legitimate. Phishing sites routinely obtain valid TLS certificates, the padlock is visible on most phishing pages.
:::

:::code language=mermaid caption="Anti-phishing defense stack: each layer reduces attack probability independently, a phishing attempt that evades email filtering may still be blocked at URL scanning, and one that evades URL scanning may still fail at phishing-resistant MFA"
flowchart BT
  L1["SIEM monitoring"] --> L2["EDR on endpoints"] --> L3["Conditional access"] --> L4["FIDO2 MFA"] --> L5["Browser Safe Browsing"]
  L5 --> L6["Browser HTTPS validation"] --> L7["URL filtering"] --> L8["Attachment sandboxing"] --> L9["DMARC email authentication"]
:::

:::notes
Defense in depth, the practice of implementing multiple independent security controls so that no single point of failure results in a complete breach, is the organizing principle of effective anti-phishing architecture. Each control in the stack has a specific threat it addresses well and specific conditions under which it fails. Understanding both the capability and the limitation of each control is essential for designing a stack that remains effective across the range of phishing scenarios an organization is likely to encounter.

The most consequential misconception in user-facing phishing education is the persistent teaching that the HTTPS padlock indicates a safe website. Certificate authorities issue TLS certificates based on domain ownership validation, not legitimacy assessment. Let's Encrypt provides free DV (Domain Validation) certificates to any domain owner, including phishing sites, and it does so at scale and automatically. Google's Transparency Report data shows that the vast majority of phishing sites served in HTTPS have valid, browser-trusted TLS certificates. Teaching users "look for the padlock" as a phishing defense is actively harmful, it builds false confidence and causes users to dismiss warnings about credential forms on HTTPS-certified pages. NIST SP 800-177 Rev. 1 explicitly notes this limitation and recommends user training emphasize domain name scrutiny rather than padlock status.

URL reputation filtering, whether at the email gateway level, the web proxy level, or as a browser extension, is valuable but time-limited. Newly registered phishing domains typically enjoy a grace period of 24–72 hours during which they have not yet been detected and classified by threat intelligence feeds. Attackers exploit this window by deploying campaigns immediately after domain registration, before reputation services have had time to classify the domain. The "time-to-phish" metric (the interval between domain registration and first phishing use) averages under 24 hours for sophisticated campaigns. This means URL filtering alone is insufficient for fast-moving targeted campaigns.

Most of the email security stack fails against AiTM phishing. DMARC does not help when the attacker uses a look-alike domain with a valid certificate; URL filtering may miss a newly registered proxy domain; HTTPS checks pass because the proxy has a valid certificate; safe-browsing lists have not yet classified the domain. Only phishing-resistant FIDO2 MFA defeats it, because the key's cryptographic binding to the real origin prevents the proxy from relaying a valid authentication. This is why CISA recommends deploying FIDO2 to privileged accounts first.
:::

%%%

---
unit: Misconceptions
code: FAQ
title: Common Misconceptions About Phishing
---
:::callout style=soft
Security training often leaves students with oversimplified mental models. These misconceptions reduce defensive effectiveness by giving false confidence or directing attention to the wrong indicators.
:::

::::columns
::col::
:::list heading="Misconception 1, 'I can always spot phishing by looking for spelling errors'" style=plain
**Reality**: Modern phishing campaigns, especially spear phishing and BEC, are proofread and professionally written. AI-generated phishing can produce grammatically flawless, contextually accurate messages at scale. Spelling error detection is a useful first-pass heuristic for bulk phishing but provides zero protection against targeted attacks.
:::

:::list heading="Misconception 2, 'HTTPS padlock means the site is safe'" style=plain
**Reality**: TLS certificates authenticate domain ownership, not legitimacy. Free certificate authorities (Let's Encrypt) issue certificates automatically to any domain, including phishing sites. Over 80% of phishing sites now use HTTPS. The padlock means your connection to the site is encrypted, it says nothing about whether the site itself is malicious.
:::

::col::
:::list heading="Misconception 3, 'MFA means I'm protected against phishing'" style=plain
**Reality**: SMS OTP, authenticator app TOTP codes, and push notifications can all be intercepted or relayed in real time via AiTM proxy attacks. Only FIDO2/WebAuthn hardware keys or passkeys provide phishing-resistant authentication, because they are cryptographically bound to the legitimate domain and cannot be relayed.
:::

:::list heading="Misconception 4, 'Phishing only targets non-technical users'" style=plain
**Reality**: Phishing attacks are calibrated to their targets. Security professionals, developers, and IT administrators are targeted with technically sophisticated lures, fake GitHub pull request notifications, typosquatted npm package installation instructions, or fake CVE security advisories. Technical expertise reduces susceptibility to generic phishing but does not protect against well-crafted targeted attacks.
:::
::::

:::notes
Addressing misconceptions explicitly is more effective than simply providing accurate information, because incorrect mental models actively resist new information that conflicts with them. This phenomenon, known as the backfire effect in some earlier research, and more robustly as belief perseverance, means that if a student already believes "MFA means I'm protected from phishing," simply presenting correct information about AiTM attacks may be less effective than first surfacing and explicitly refuting the misconception. The four misconceptions on this slide represent the most consistently observed incorrect beliefs across security awareness programs.

Misconception 1 (spelling errors) is dangerous because it trains users to look for the wrong signals. As large language models become more accessible, generating culturally appropriate, syntactically correct, and contextually credible phishing messages at scale becomes trivial. IBM X-Force reported in 2023 that AI-assisted phishing campaigns produce a 40% increase in email open rates compared to traditional human-written campaigns, specifically because they eliminate the grammatical and spelling errors that users have been trained to look for. The correct message for users: no single visual cue is reliable; evaluate the overall communication, was it expected? Does the request make sense given your relationship with the purported sender? Does it create artificial urgency?

Misconception 2 (HTTPS padlock) stems from two decades of user training that conflated "secure connection" with "safe website." The transition of the web to HTTPS, driven by Google's SEO penalties for non-HTTPS sites and the availability of free certificates from Let's Encrypt, inadvertently created a new phishing-enablement surface. The padlock is now a meaningless trust signal for phishing detection. Browser vendors (Chrome, Firefox) have begun removing the padlock icon entirely, replacing it with a neutral information icon, precisely because research showed that displaying the padlock created false security expectations.

Technical users are not immune to phishing. Package typosquatting targets developers directly: the 2018 npm event-stream incident injected a malicious dependency into a popular library, and 2023 PyPI campaigns uploaded packages named after popular libraries with small misspellings, waiting for a mistyped pip install. Messages arriving through professional channels, such as GitHub notifications, registry emails and security mailing lists, often receive less scrutiny than personal email, a blind spot attackers exploit.
:::

%%%

---
unit: Controls
code: IRP
title: Organizational Incident Response to Phishing
---
:::callout style=soft
Individual response (change password, report) is only the first link in the chain. An effective organizational response to a phishing incident requires pre-planned playbooks, defined roles, and tested communication paths that activate within minutes of a report.
:::

:::steps heading="Organizational Phishing Incident Response Playbook"
1. **Detection**, Employee reports via phishing report button or security inbox; SIEM alert fires on anomalous authentication from new geolocation; email gateway quarantine queue flags suspicious campaign
2. **Triage (< 1 hour)**, Security analyst reviews reported email; determines if credential submission occurred; identifies all recipients of the same campaign in mail logs
3. **Containment (< 4 hours)**, Force password reset and session token revocation for all accounts that submitted credentials; block malicious URLs and sender domains across email gateway and web proxy; preserve email evidence for forensic analysis
4. **Eradication**, Confirm no persistence mechanisms were installed; review attacker activity in compromised accounts (mail rules, forwarding, OAuth app grants); revoke any unauthorized delegated access
5. **Recovery**, Restore access to affected users with new credentials; verify MFA enrollment is active on all affected accounts; confirm no data exfiltration occurred
6. **Post-Incident Review**, Document what worked and what failed; identify training gaps revealed by the incident; update phishing simulation scenarios to reflect the attack pattern encountered
:::

:::table
| Role | Responsibility During Phishing Incident |
|---|---|
| Security Analyst (Tier 1) | Triage reported email; categorize and escalate |
| Incident Responder (Tier 2) | Containment and eradication actions |
| IT Operations | Account lockdown, password reset, MFA enforcement |
| Legal / Compliance | Data breach notification assessment; regulatory reporting deadlines |
| Communications / PR | Internal and external communication if data was exfiltrated |
| Executive Leadership | Decision authority for external notifications and law enforcement engagement |
:::

:::code language=mermaid caption="Phishing incident response timeline: organizational response speed is the primary determinant of breach scope, credential revocation within four hours typically prevents lateral movement"
flowchart TB
  A["Detection<br/>user report or alert, SOC analyst, minutes"] --> B["Triage<br/>confirm phish, find all recipients"]
  B --> C["Containment<br/>purge emails, block domain, reset passwords"]
  C --> D["Eradication<br/>remove persistence, revoke sessions"]
  D --> E["Recovery<br/>restore access, watch for repeat"]
  E --> F["Post-incident review<br/>lessons learned within days"]
:::

:::notes
The individual response playbook (stop, reset password, report) is the user-facing component of a much larger organizational process. For organizations handling dozens to hundreds of phishing reports daily, an efficient triage and response workflow is essential for preventing individual incidents from escalating into full breach events. The key insight from incident response research is that time is the critical variable: the window between credential submission and attacker use of those credentials is measured in minutes for automated tools and hours for human operators, making rapid containment the highest-leverage intervention.

NIST SP 800-61 Rev. 2 (Computer Security Incident Handling Guide) provides the foundational framework for phishing incident response, organized around the Preparation, Detection, Analysis, Containment, Eradication, Recovery, and Post-Incident Activity lifecycle. ISO/IEC 27035-2:2023 (Guidelines to plan and prepare for incident response) specifies that organizations should develop written playbooks for specific incident scenarios including phishing, with clearly defined roles, responsibilities, and time targets for each response phase.

The containment phase deserves detailed attention because it contains the most operationally important, and most often delayed, action: session token revocation. Changing a user's password does not immediately invalidate active authenticated sessions in most web applications and identity providers. An attacker who captured a session cookie via AiTM phishing maintains access to the victim's account even after the password is changed, until the session is explicitly invalidated. Microsoft Entra ID (Azure Active Directory) provides a "Revoke all sessions" function that invalidates all active tokens for a user; Google Workspace provides equivalent session revocation. These must be part of the containment action for any confirmed credential submission incident, not just password reset.

Eradication often uncovers persistence created between the credential theft and its detection. In email account compromise, common mechanisms are mail-forwarding rules that send all incoming mail to an attacker's address, OAuth application grants that survive a password reset, and new recovery details or secondary credentials. Eradication must check every one of these, not just block the original phishing email. They map to ATT&CK T1114 (Email Collection), T1098 (Account Manipulation) and T1546 (Event Triggered Execution); Microsoft Secure Score and the Google Workspace security center both check for suspicious mail rules and OAuth grants.
:::

%%%

---
unit: Emerging Threats
code: AIP
title: AI-Powered Phishing, The Next Generation of the Threat
---
:::callout style=soft
Large language models (LLMs) have fundamentally altered the economics and scalability of phishing: crafting hundreds of personalized, culturally accurate, grammatically perfect spear phishing messages now takes seconds, not days.
:::

::::columns
::col::
:::list heading="How AI Changes Phishing" style=plain
- **Scale of personalization**: LLMs can generate unique, individually tailored phishing messages for every recipient in a target list, consuming OSINT data about each person as input
- **Language barrier removed**: Non-English-speaking threat actors can produce native-quality messages in any language, eliminating the grammatical errors previously used to detect foreign-origin phishing
- **Voice cloning**: AI voice synthesis can clone a person's voice from as little as three seconds of audio; used in vishing to impersonate executives (CFO impersonation audio in 2023 Hong Kong bank fraud case: $25M loss)
- **Deepfake video**: AI-generated video in real-time can impersonate executives in video calls; emerging but documented use in enterprise fraud
:::
::col::
:::list heading="Documented AI-Phishing Incidents" style=plain
- **2023, UK energy firm**: Attackers used AI voice cloning to mimic the CEO's voice and instructed a finance executive to transfer €220,000 to a fraudulent account; the voice clone was indistinguishable from the real CEO
- **2024, Hong Kong multinational**: A deepfake video call impersonating multiple company executives convinced a finance worker to wire $25 million USD
- **2023, WormGPT**: A ChatGPT-like LLM with no ethical guardrails advertised on criminal forums specifically for generating phishing and BEC emails at scale
- **2023, FraudGPT**: A subscription-based criminal AI service offering phishing email generation, credential harvesting page templates, and social engineering scripts
:::
::::

:::code language=mermaid caption="AI-powered phishing: the bottleneck of manual personalization is eliminated, an attacker who previously crafted ten spear phishing messages per day can now generate ten thousand, each individually tailored"
flowchart LR
  T["<b>Traditional</b><br/>Target research: hours<br/>Drafting: hours<br/>Translation: hours<br/>Proofreading: hours<br/>Deployment"] -->|"AI compresses each step"| A["<b>AI-assisted</b><br/>Research summaries: minutes<br/>Drafting: seconds<br/>Any language, fluent<br/>No tell-tale errors<br/>Deployment at scale"]
:::

:::notes
The emergence of capable large language models as publicly accessible tools represents one of the most significant threat landscape shifts in phishing's history. For the previous decade, spear phishing campaigns were constrained by the labor cost of personalization, crafting a convincing, individually tailored message required research time, cultural knowledge, and writing skill that limited the scale at which targeted campaigns could operate. LLMs eliminate this constraint entirely.

IBM X-Force's 2023 threat intelligence report documented a 40% increase in phishing email open rates for AI-generated messages compared to human-written equivalents in controlled testing, attributing the improvement primarily to the elimination of grammatical errors and improved cultural authenticity. This directly undermines the single most widely taught phishing detection heuristic, "look for spelling and grammar errors", at precisely the moment when that advice has already been inadequate for targeted attacks for years.

The criminal market has responded rapidly. WormGPT, FraudGPT, and a variety of similar tools began appearing on criminal forums (primarily Telegram-based markets and dark web forums) in mid-2023. These tools are LLMs fine-tuned on criminal use cases or jailbroken versions of existing models, specifically designed to generate phishing emails, BEC scripts, malware code, and credential harvesting page templates without the ethical refusals built into commercial AI systems. Subscription pricing as low as $75/month puts enterprise-quality phishing generation capability within reach of low-skill threat actors.

The voice cloning and deepfake video incidents represent a qualitative escalation beyond text-based phishing. The 2023 UK CEO voice clone case (Symantec threat intelligence report) demonstrated that AI voice synthesis has reached a quality threshold at which even individuals familiar with the target's voice cannot reliably distinguish synthetic audio from authentic recording. The 2024 Hong Kong deepfake video case, where a finance worker participated in what appeared to be a video conference with multiple known company executives before wiring $25 million, suggests that the "call your manager to verify unusual requests" defense advice will itself need to evolve for the deepfake era.

Voice and face cloning undermine the standard advice to verify a request out of band. More robust verification relies on pre-established passphrases that cannot be found in public sources, physical verification such as a hardware-key tap in person, or policies requiring in-person approval above financial thresholds. The defensive playbook here is less mature than the attack capability. NIST addresses AI-enabled threats in its AI Risk Management Framework (AI RMF 1.0, January 2023).
:::

%%%

---
unit: Summary
code: SUM2
title: Phishing Defense, Layering People, Process, and Technology
---
:::pullquote
Phishing cannot be stopped by any single control. It is defeated in depth, by combining technical layers that filter at machine scale with human resilience that detects what technology misses.
:::

::::columns
::col::
:::list heading="Technology Controls" style=plain
- DMARC `p=reject` + SPF + DKIM, email authentication
- URL reputation filtering at gateway and browser
- Attachment sandboxing
- FIDO2/WebAuthn phishing-resistant MFA
- Conditional access policies (anomalous login detection)
- SIEM authentication log monitoring
:::
::col::
:::list heading="Human Controls" style=plain
- Security awareness training incorporating bias education
- Role-specific spear phishing and whaling training
- Phishing simulation programs (tiered difficulty, teachable moments)
- Out-of-band wire transfer verification protocol
- Low-friction "Report Phishing" button in email clients
- Blame-free reporting culture
:::
::col::
:::list heading="Process Controls" style=plain
- Incident response playbook for phishing with defined time targets
- OSINT monitoring for lookalike domain registration
- DMARC report analysis and enforcement lifecycle management
- Supplier / vendor communication verification protocols
- Executive briefing on BEC and deepfake voice/video threats
- Regular post-simulation review and training adjustment
:::
::::

:::table
| Framework | Relevant Section | Phishing Control Addressed |
|---|---|---|
| NIST SP 800-177 Rev. 1 | Email Security | SPF, DKIM, DMARC deployment guidance |
| NIST SP 800-63B | Digital Identity | MFA assurance levels; phishing-resistant authenticators |
| NIST SP 800-61 Rev. 2 | Incident Handling | Phishing incident response lifecycle |
| ISO/IEC 27001:2022 | Annex A.6.3 | Security awareness and phishing simulation |
| MITRE ATT&CK | T1566, T1598, T1056, T1539 | Phishing technique taxonomy for detection mapping |
| CISA BOD 23-02 | Federal Email Security | DMARC `p=reject` mandate for federal domains |
:::

:::code language=mermaid caption="Phishing resilience triad: technology, human, and process controls are mutually reinforcing, gaps in any vertex are compensated by strength in the others, but all three must be present for sustained defense"
flowchart TB
  T["Technology"] ---|"MFA prompts that teach,<br/>report-phish button"| H["Human"]
  H ---|"clear reporting procedure,<br/>call-back verification"| P["Process"]
  P ---|"DMARC policy, automated<br/>email purge"| T
:::

:::notes
This closing summary synthesizes the architecture of a comprehensive phishing defense program. The key insight, which deserves emphasis because it contradicts how phishing is often presented in compliance-driven awareness training, is that no single control category is sufficient.

Organizations that invest heavily in technical controls (DMARC, email gateway, URL filtering) but neglect human training remain vulnerable to spear phishing and BEC attacks that are specifically engineered to pass technical filters. Conversely, organizations that invest in user awareness but neglect technical controls expose their well-trained users to a fire hose of bulk phishing that no awareness program can sustain defense against indefinitely, humans make errors, particularly under time pressure, and technical controls provide the safety net when human judgment fails. And both technical and human controls fail without the process infrastructure to detect incidents quickly, respond before attackers establish persistence, and continuously learn from simulations and real events.

The framework cross-reference table on this slide provides students with the authoritative sources for each control domain. These are the documents a security professional should cite when making the business case to an executive or board for phishing defense investments. NIST SP 800-177 Rev. 1 provides the email authentication technical implementation detail. NIST SP 800-63B provides the MFA assurance level framework that justifies the investment in FIDO2 over legacy OTP. NIST SP 800-61 Rev. 2 provides the incident response lifecycle framework. ISO/IEC 27001:2022 Annex A.6.3 provides the audit evidence for a comprehensive security awareness and simulation program. MITRE ATT&CK provides the threat intelligence taxonomy for mapping defenses to specific adversary techniques.

Phishing appeared in 36% of the breaches analyzed in the Verizon 2023 DBIR. After two decades of awareness training, email security investment and MFA deployment, it remains the dominant initial access vector because it adapts: generic phishing gave way to spear phishing as filters improved; defeated one-time codes gave way to MFA fatigue and AiTM; AI now removes the quality limits on personalized phishing. Security is a process of continuous adaptation, not a state that is reached.
:::
