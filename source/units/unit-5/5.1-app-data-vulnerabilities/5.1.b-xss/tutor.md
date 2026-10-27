# 5.1.b tutor notes

Notes for the pre- and post-lecture tutor posts.

## The intuition to hold onto
The mental model to bring into this lecture: XSS is SQL injection's twin, just aimed at the browser instead of the database. In both cases the root failure is identical, data and code sharing one channel, so a program that expected to receive text ends up executing instructions instead. Once you already understand that a database can't tell apart "the string admin'--" from "a SQL comment," it should feel natural that a browser can't tell apart "the string `<script>`" from "an instruction to run JavaScript." The specific fix differs, escaping output for HTML instead of parameterizing a query, but the diagnosis is the same question asked in a new context: where did code and data get mixed?

## The big picture
The detail worth remembering longest here is that the three XSS variants are really differentiated by one question: does the malicious payload have to survive a trip to the server, or not? Reflected XSS needs the victim to click something, because the payload lives only in that one request. Stored XSS is scarier precisely because it removes that requirement, once it's saved in a comment or profile field, every visitor including an administrator is compromised just by loading the page, no phishing step needed. DOM-based XSS removes the server from the picture entirely, which is exactly why a server-side filter can look completely clean while the page is still vulnerable. That's the exam trap: students who memorize "XSS = unescaped input" without sorting by *where* the unescaped step happens will misclassify DOM-based cases as safe because the server-side log shows nothing wrong.
