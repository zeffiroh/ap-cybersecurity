## 6. Work the queue before you hand over

Your shift had eleven alerts, and the night shift left "quiet night". Give every alert a disposition and one line of reason a stranger could check. Read each detail line before you decide.

- [ ] Every alert gets a disposition: nothing left "Not triaged"
- [ ] Each reason is one line a stranger could check
- [ ] Write the notes for the next shift in the box under the queue
- [ ] Download the handover the queue writes for you

```tool alerts
{"file": "alerts.json", "d": {"AL-3301": "escalate", "AL-3302": "benign", "AL-3303": "escalate", "AL-3304": "escalate", "AL-3305": "escalate", "AL-3306": "benign", "AL-3307": "escalate", "AL-3308": "benign", "AL-3309": "escalate", "AL-3310": "escalate", "AL-3311": "escalate"}, "n": 8, "blank": ["d"]}
```

?> Which alert ID is the sign-in from the company's cloud VPN gateway? :: AL-3302

?> How many alerts belong to the incident and get escalated? :: 8

?> Which outside IP address appears in both proxy.log and the failed VPN logons? :: 198.51.100.77
