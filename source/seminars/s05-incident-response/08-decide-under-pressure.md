## 8. Decide under pressure

Responders make calls before they have all the facts. Play the tabletop as the incident lead. Each choice costs time; the debrief at the end says what good looks like.

```tool tabletop
{"file": "tabletop-garnet-ransomware.json", "path": [{"node": "t1", "c": 0, "label": "Pull the network cable, cut the VPN session, keep the machines powered on"}, {"node": "t2", "c": 0, "label": "Don't pay; restore from the Thursday tape; get legal advice on the customer contracts"}, {"node": "t3", "c": 0, "label": "File with CERT-In by 06:31 UTC with what we know, and update later"}, {"node": "t4", "c": 0, "label": "Turn on MFA for every VPN account and reset s.kale and adm.rjoshi before bringing fs02 back"}, {"node": "t5", "c": 0, "label": "Tell staff and the affected customer plainly what happened and what you are doing"}], "n": 10, "blank": ["path"]}
```

- [ ] Play it once as the incident lead
- [ ] Play it again as the managing director: which call is hardest from that seat?
- [ ] For each decision, one line on why

> Hint: Isolate, don't power off: memory is evidence. And the six-hour CERT-In clock starts when you noticed, not when you finish investigating.

?> What is the best score you can get in the tabletop? :: 10
