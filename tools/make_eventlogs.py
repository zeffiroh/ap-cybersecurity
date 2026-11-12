import csv
import json
import random
import re
from datetime import datetime, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CASES = ROOT / "source" / "static" / "assets" / "linux" / "cases"
SEC = "Security-Auditing"
LOGON_TYPES = {2: "Interactive", 3: "Network", 5: "Service", 7: "Unlock", 11: "CachedInteractive"}


class Log:
    def __init__(self, host, start):
        self.host = host
        self.rec = start
        self.rows = []

    def add(self, when, eid, provider, task, message, data, level="Information", keywords=None):
        self.rec += 1
        row = {"TimeCreated": when.strftime("%Y-%m-%dT%H:%M:%SZ"), "EventID": eid, "Level": level}
        if keywords:
            row["Keywords"] = keywords
        row.update({"Provider": provider, "Task": task, "Computer": self.host, "RecordID": self.rec, "Message": message, "Data": data})
        self.rows.append(row)

    def write(self, path):
        self.rows.sort(key=lambda r: (r["TimeCreated"], r["RecordID"]))
        for i, r in enumerate(self.rows):
            r["RecordID"] = self.rows[0]["RecordID"] + i
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in self.rows), encoding="utf-8")


def logon(log, when, user, domain, ltype, ip="-", logon_id="0x0"):
    log.add(when, 4624, SEC, "Logon",
            f"An account was successfully logged on.\n\nLogon Information:\n\tLogon Type:\t\t{ltype}\n\nNew Logon:\n\tAccount Name:\t\t{user}\n"
            f"\tAccount Domain:\t\t{domain}\n\tLogon ID:\t\t{logon_id}\n\nNetwork Information:\n\tSource Network Address:\t{ip}",
            {"TargetUserName": user, "TargetDomainName": domain, "LogonType": str(ltype), "TargetLogonId": logon_id, "IpAddress": ip,
             "LogonProcessName": "User32" if ltype in (2, 7, 11) else "Advapi", "AuthenticationPackageName": "Negotiate"},
            keywords="Audit Success")


def logoff(log, when, user, domain, ltype, logon_id):
    log.add(when, 4634, SEC, "Logoff", f"An account was logged off.\n\nSubject:\n\tAccount Name:\t\t{user}\n\tAccount Domain:\t\t{domain}\n\tLogon ID:\t\t{logon_id}\n\nLogon Type:\t\t\t{ltype}",
            {"TargetUserName": user, "TargetDomainName": domain, "TargetLogonId": logon_id, "LogonType": str(ltype)}, keywords="Audit Success")


def process(log, when, user, domain, logon_id, pid, image, cmd, ppid, parent):
    log.add(when, 4688, SEC, "Process Creation",
            f"A new process has been created.\n\nCreator Subject:\n\tAccount Name:\t\t{user}\n\tAccount Domain:\t\t{domain}\n\tLogon ID:\t\t{logon_id}\n\n"
            f"Process Information:\n\tNew Process ID:\t\t{hex(pid)}\n\tNew Process Name:\t{image}\n\tCreator Process ID:\t{hex(ppid)}\n"
            f"\tCreator Process Name:\t{parent}\n\tProcess Command Line:\t{cmd}",
            {"SubjectUserName": user, "SubjectDomainName": domain, "SubjectLogonId": logon_id, "NewProcessId": hex(pid), "NewProcessName": image,
             "ProcessId": hex(ppid), "ParentProcessName": parent, "CommandLine": cmd}, keywords="Audit Success")


def noise(log, start, end, rnd, every=(9, 25)):
    t = start
    while t < end:
        logon(log, t, "SYSTEM", "NT AUTHORITY", 5, logon_id="0x3e7")
        t += timedelta(minutes=rnd.randint(*every), seconds=rnd.randint(0, 59))


def system_boot(log, when):
    log.add(when, 6005, "EventLog", "None", "The Event log service was started.", {})
    log.add(when + timedelta(seconds=2), 7036, "Service Control Manager", "None", "The DHCP Client service entered the running state.", {"param1": "DHCP Client", "param2": "running"})
    log.add(when + timedelta(seconds=5), 7036, "Service Control Manager", "None", "The Windows Update service entered the running state.", {"param1": "Windows Update", "param2": "running"})


def insider():
    rnd = random.Random(57)
    host, dom, user = "eng-ws57.halcyon.lan", "HALCYON", "r.menon"
    sec, sys_ = Log(host, 77100), Log(host, 5100)
    rows = list(csv.DictReader((CASES / "insider" / "case" / "ws_events.csv").open(encoding="utf-8")))
    noise(sec, datetime(2026, 11, 2, 8, 30), datetime(2026, 11, 3, 9, 30), rnd, (40, 90))
    system_boot(sys_, datetime(2026, 11, 2, 8, 31, 2))
    ids = {}
    for r in rows:
        t = datetime.strptime(r["time"], "%Y-%m-%d %H:%M:%S")
        if r["event"] == "logon":
            lid = hex(0x5a0000 + len(ids) * 0x1f3)
            ids[r["time"][:10]] = lid
            logon(sec, t, user, dom, 2, logon_id=lid)
            process(sec, t + timedelta(seconds=6), user, dom, lid, 0x1a20 + len(ids), "C:\\Windows\\explorer.exe", "C:\\Windows\\Explorer.EXE", 0x2c4, "C:\\Windows\\System32\\userinit.exe")
        elif r["event"] == "logoff":
            logoff(sec, t, user, dom, 2, ids.get(r["time"][:10], "0x5a0000"))
    night = ids.get("2026-11-03", "0x5a01f3")
    t = datetime(2026, 11, 3, 2, 5, 41)
    sec.add(t, 6416, SEC, "Plug and Play Events",
            "A new external device was recognized by the system.\n\nDevice ID:\tUSBSTOR\\Disk&Ven_SanDisk&Prod_Ultra&Rev_1.00\\4C530001230918112345\nDevice Name:\tSanDisk Ultra USB 3.0\nClass Name:\tDiskDrive",
            {"SubjectUserName": "ENG-WS57$", "DeviceId": "USBSTOR\\Disk&Ven_SanDisk&Prod_Ultra&Rev_1.00\\4C530001230918112345", "DeviceDescription": "SanDisk Ultra USB 3.0",
             "ClassName": "DiskDrive", "VendorIds": "USB\\VID_0781&PID_5581"}, keywords="Audit Success")
    sys_.add(t + timedelta(seconds=1), 20001, "UserPnp", "None", "Driver Management concluded the process to install driver disk.inf for Device Instance ID USBSTOR\\DISK&VEN_SANDISK&PROD_ULTRA&REV_1.00\\4C530001230918112345 with status 0x0.",
             {"DeviceInstanceID": "USBSTOR\\DISK&VEN_SANDISK&PROD_ULTRA&REV_1.00\\4C530001230918112345", "DriverName": "disk.inf", "Status": "0x0"})
    sys_.add(t + timedelta(seconds=2), 98, "Ntfs", "None", "Volume E: (\\Device\\HarddiskVolume7) is healthy. No action is needed.", {"DriveName": "E:", "DeviceName": "\\Device\\HarddiskVolume7"})
    process(sec, datetime(2026, 11, 3, 2, 6, 8), user, dom, night, 0x2f14, "C:\\Windows\\System32\\Robocopy.exe",
            "robocopy C:\\Users\\r.menon\\repos E:\\work /E /R:0 /W:0 /NP /NFL /NDL", 0x1b38, "C:\\Windows\\System32\\cmd.exe")
    process(sec, datetime(2026, 11, 3, 2, 5, 58), user, dom, night, 0x1b38, "C:\\Windows\\System32\\cmd.exe", "\"C:\\Windows\\system32\\cmd.exe\"", 0x1a22, "C:\\Windows\\explorer.exe")
    for i, folder in enumerate(["halcyon-rotor-firmware", "halcyon-test-rigs", "customer-configs", "pricing-models"]):
        sec.add(datetime(2026, 11, 3, 2, 7 + i * 8, 14 + i), 4663, SEC, "Removable Storage",
                f"An attempt was made to access an object.\n\nSubject:\n\tAccount Name:\t\t{user}\n\nObject:\n\tObject Type:\t\tFile\n\tObject Name:\t\tE:\\work\\{folder}\n\nAccess Request Information:\n\tAccesses:\t\tWriteData (or AddFile)",
                {"SubjectUserName": user, "SubjectDomainName": dom, "ObjectType": "File", "ObjectName": f"E:\\work\\{folder}", "AccessMask": "0x2",
                 "ProcessName": "C:\\Windows\\System32\\Robocopy.exe"}, keywords="Audit Success")
    process(sec, datetime(2026, 11, 3, 2, 52, 30), user, dom, night, 0x3310, "C:\\Windows\\System32\\cmd.exe",
            "cmd.exe /c del /q %APPDATA%\\Microsoft\\Windows\\Recent\\*.lnk", 0x1a22, "C:\\Windows\\explorer.exe")
    sys_.add(datetime(2026, 11, 3, 2, 58, 3), 225, "Kernel-PnP", "None", "The application System with process id 4 stopped the removal or ejection for the device USBSTOR\\Disk&Ven_SanDisk&Prod_Ultra&Rev_1.00\\4C530001230918112345.",
             {"DeviceInstance": "USBSTOR\\Disk&Ven_SanDisk&Prod_Ultra&Rev_1.00\\4C530001230918112345", "ProcessId": "4"}, level="Warning")
    sec.add(datetime(2026, 11, 3, 3, 5, 30), 1102, "Eventlog", "Log clear", "The audit log was cleared.\n\nSubject:\n\tAccount Name:\t\tr.menon",
            {"SubjectUserName": user, "SubjectDomainName": dom}, keywords="Audit Success")
    sec.write(CASES / "insider" / "case" / "eventlogs" / "Security.jsonl")
    sys_.write(CASES / "insider" / "case" / "eventlogs" / "System.jsonl")


def quietdns():
    rnd = random.Random(44)
    host, dom, user = "fin-lt04.harbourline.lan", "HARBOUR", "m.devlin"
    sec, sys_, sm = Log(host, 210400), Log(host, 8800), Log(host, 33000)
    lid = "0x9b31a0"
    noise(sec, datetime(2026, 11, 5, 10, 40), datetime(2026, 11, 5, 11, 50), rnd)
    system_boot(sys_, datetime(2026, 11, 5, 10, 41, 10))
    logon(sec, datetime(2026, 11, 5, 10, 58, 40), user, dom, 2, logon_id=lid)
    procs = list(csv.DictReader((CASES / "quietdns" / "case" / "process.csv").open(encoding="utf-8")))
    images = {}
    for p in procs:
        images[p["pid"]] = p["image"]
    for p in procs:
        t = datetime.strptime(p["time"], "%Y-%m-%d %H:%M:%S")
        u, d = (p["user"].split("\\", 1) + [""])[:2][::-1] if "\\" in p["user"] else (p["user"], "")
        parent = images.get(p["ppid"], "C:\\Windows\\explorer.exe")
        process(sec, t, u, d, lid if u == user else "0x3e7", int(p["pid"]), p["image"], p["command_line"], int(p["ppid"]), parent)
        sm.add(t, 1, "Sysmon", "Process Create (rule: ProcessCreate)",
               f"Process Create:\nUtcTime: {t:%Y-%m-%d %H:%M:%S}.000\nProcessId: {p['pid']}\nImage: {p['image']}\nCommandLine: {p['command_line']}\nUser: {p['user']}\nParentProcessId: {p['ppid']}\nParentImage: {parent}",
               {"UtcTime": f"{t:%Y-%m-%d %H:%M:%S}.000", "ProcessId": p["pid"], "Image": p["image"], "CommandLine": p["command_line"], "User": p["user"],
                "ParentProcessId": p["ppid"], "ParentImage": parent, "IntegrityLevel": "System" if "SYSTEM" in p["user"] else "Medium"})
    task = datetime(2026, 11, 5, 11, 4, 11)
    sec.add(task, 4698, SEC, "Other Object Access Events",
            f"A scheduled task was created.\n\nSubject:\n\tAccount Name:\t\t{user}\n\tAccount Domain:\t\t{dom}\n\nTask Information:\n\tTask Name:\t\t\\TeamsUpdateCheck\n"
            "\tAction:\t\t\tC:\\Users\\m.devlin\\AppData\\Roaming\\Microsoft\\Teams\\msteams-update.exe\n\tTrigger:\t\tAt log on",
            {"SubjectUserName": user, "SubjectDomainName": dom, "TaskName": "\\TeamsUpdateCheck", "Action": "C:\\Users\\m.devlin\\AppData\\Roaming\\Microsoft\\Teams\\msteams-update.exe",
             "Trigger": "At log on"}, keywords="Audit Success")
    bad = "C:\\Users\\m.devlin\\AppData\\Roaming\\Microsoft\\Teams\\msteams-update.exe"
    pat = re.compile(r"^(\d\d-\w{3}-\d{4} \d\d:\d\d:\d\d)\.(\d+) queries: client ([\d.]+)#\d+: query: (\S+) IN (\w+)")
    for line in (CASES / "quietdns" / "case" / "dns.log").read_text(encoding="utf-8").splitlines():
        m = pat.match(line)
        if not m or m.group(3) != "10.70.0.44":
            continue
        t = datetime.strptime(m.group(1), "%d-%b-%Y %H:%M:%S")
        name = m.group(4)
        image = bad if name.endswith("cloudmetric.example") else ("C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe" if not name.endswith(".lan") else "C:\\Windows\\System32\\svchost.exe")
        sm.add(t, 22, "Sysmon", "Dns query (rule: DnsQuery)", f"Dns query:\nUtcTime: {t:%Y-%m-%d %H:%M:%S}.{m.group(2)}\nQueryName: {name}\nQueryStatus: 0\nImage: {image}",
               {"UtcTime": f"{t:%Y-%m-%d %H:%M:%S}.{m.group(2)}", "QueryName": name, "QueryType": m.group(5), "QueryStatus": "0", "Image": image, "User": f"{dom}\\{user}"})
    sec.write(CASES / "quietdns" / "case" / "eventlogs" / "Security.jsonl")
    sys_.write(CASES / "quietdns" / "case" / "eventlogs" / "System.jsonl")
    sm.write(CASES / "quietdns" / "case" / "eventlogs" / "Sysmon.jsonl")


if __name__ == "__main__":
    insider()
    quietdns()
    for case in ("insider", "quietdns"):
        for f in sorted((CASES / case / "case" / "eventlogs").glob("*.jsonl")):
            print(case, f.name, sum(1 for _ in f.open(encoding="utf-8")))
