## 6. Work the queue before you hand over

Your shift had ten alerts, and the night shift left a note that says "nothing major". Give every alert a disposition and a one-line reason. Some belong to the incident; some are ordinary noise and should be closed so the next shift isn't chasing them.

The alert queue sorts by severity, then time. Pick an alert, choose a disposition, and write why.

- [ ] Every alert gets a disposition: nothing left "Not triaged"
- [ ] Each reason is one line a stranger could check
- [ ] Write the notes for the next shift in the box under the queue
- [ ] Download the handover the queue writes for you

> Hint: AL-2202's "Singapore" address is the company VPN exit: read the detail line. AL-2206 retried and worked at 09:25.

```tool alerts
{"file": "case/alerts.json", "d": {"AL-2201": "escalate", "AL-2202": "benign", "AL-2203": "escalate", "AL-2204": "escalate", "AL-2205": "escalate", "AL-2210": "escalate", "AL-2206": "benign", "AL-2209": "benign", "AL-2208": "escalate", "AL-2207": "escalate"}, "n": 7, "blank": ["d"]}
```

?> Which alert ID is the sign-in from the company VPN exit? :: AL-2202

?> Which local account did the attacker create on hr-pc07? :: support_svc
