## 1. How the search program works

Before you hunt, learn the program. A SIEM (security information and event management system) does four things with every log file it is given:

1. **Reads** each file and splits it into **events**, usually one line or one JSON record each.
2. **Stamps** every event with a time, `_time`, so events from different files line up on one clock.
3. **Recognises the format** and records it as the `sourcetype`: `syslog` for Linux logs, `access_combined` for web server logs, `json` for Windows events.
4. **Extracts fields** such as `src_ip`, `user`, `status` or `EventID`, so you can search on them instead of on raw text.

On screen you have a search box with a language switch (SPL or KQL), **Run**, a chart of **events over time**, the **field list** on the left (click a field to see its values and add one to your search), and the results as events or as a statistics table. **Help** lists the commands this teaching version knows.

The SIEM here is the company's: Chandni Textiles in Surat, a fabric shop that also sells online. Four logs from Monday 9 November have been loaded. Read `README.txt` first.

- [ ] Run the first search: what did the program make of each file?
- [ ] Run the second search: which programs wrote to auth.log?
- [ ] Click the field `src_ip` in the field list and read its values

> Hint: `*` means every event. `stats count by source sourcetype` makes one row per file and format, with the number of events in each.

```tool siem
{"q": "* | stats count by source sourcetype", "n": 4, "files": ["auth.log", "access.log", "lookbook_access.log", "eventlogs/Security.jsonl"], "blank": ["q"]}
```

```tool siem
{"q": "sourcetype=syslog | stats count by process", "n": 3, "files": ["auth.log"], "blank": ["q"]}
```

?> How many events does the program hold across the four files? :: 163

?> Which sourcetype did the program give auth.log? :: syslog
