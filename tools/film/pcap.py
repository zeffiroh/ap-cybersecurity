import re
import sys
from datetime import datetime, timezone

from scapy.all import DNS, DNSQR, DNSRR, IP, TCP, UDP, Raw, wrpcap
from scapy.layers.tls.all import TLS, TLSClientHello, TLS_Ext_ServerName, ServerName, TLSApplicationData

MONTHS = "Jan Feb Mar Apr May Jun Jul Aug Sep Oct Nov Dec".split()
UDP_PROTOS = {"DNS", "NTP", "DHCP", "SNMP", "SYSLOG", "QUIC"}


def start_of(title):
    m = re.search(r"(\d{1,2})(?:-\d{1,2})? (\w{3}) (\d{4}) from (\d\d):(\d\d)(?::(\d\d))?", title)
    if not m:
        return datetime(2026, 11, 1, tzinfo=timezone.utc).timestamp()
    d, mon, y, hh, mm, ss = m.groups()
    return datetime(int(y), MONTHS.index(mon[:3].title()) + 1, int(d), int(hh), int(mm), int(ss or 0), tzinfo=timezone.utc).timestamp()


def flags_of(info):
    m = re.search(r"\[([A-Z, ]+)\]", info)
    if not m:
        return "PA"
    names = {"SYN": "S", "ACK": "A", "FIN": "F", "RST": "R", "PSH": "P"}
    return "".join(names[f.strip()] for f in m.group(1).split(",") if f.strip() in names) or "A"


def pad(n, used):
    return b"\x00" * max(0, n - used)


def packet(f):
    t, src, sp, dst, dp, proto, ln, info = f[:8]
    method, uri, host, ua, qname = (f + [""] * 13)[8:13]
    ln = int(ln or 60)
    sp, dp = int(sp or 0), int(dp or 0)
    ip = IP(src=src, dst=dst)
    up = proto.upper()
    if up == "DNS":
        m = re.search(r"Standard query(?: response)? 0x([0-9a-f]+) (\w+) (\S+)", info)
        qid = int(m.group(1), 16) if m else 1
        qtype = m.group(2) if m else "A"
        name = qname or (m.group(3) if m else "example")
        dns = DNS(id=qid, rd=1, qd=DNSQR(qname=name, qtype=qtype))
        if "response" in info:
            dns.qr, dns.ra = 1, 1
            a = re.search(r"\b(A|AAAA|TXT|CNAME) (\S+)$", info)
            if a and a.group(1) == "A" and re.match(r"^\d+\.\d+\.\d+\.\d+$", a.group(2)):
                dns.an, dns.ancount = DNSRR(rrname=name, type="A", ttl=300, rdata=a.group(2)), 1
            elif qtype == "TXT":
                dns.an, dns.ancount = DNSRR(rrname=name, type="TXT", ttl=60, rdata="ok"), 1
        return ip / UDP(sport=sp, dport=dp) / dns
    if up in UDP_PROTOS:
        return ip / UDP(sport=sp, dport=dp) / Raw(pad(ln, 28) or b"\x00")
    if proto == "ICMP":
        from scapy.all import ICMP
        return ip / ICMP() / Raw(pad(ln, 28))
    tcp = TCP(sport=sp, dport=dp, flags=flags_of(info) if up == "TCP" else "PA", seq=1000, ack=1000)
    if up == "TCP":
        return ip / tcp
    if up == "HTTP":
        if method:
            body = f"{method} {uri or '/'} HTTP/1.1\r\nHost: {host}\r\nUser-Agent: {ua}\r\nAccept: */*\r\n\r\n".encode()
        else:
            status = re.match(r"(HTTP/1\.[01] \d{3}[^(]*)", info)
            line = (status.group(1).strip() if status else "HTTP/1.1 200 OK")
            body = (line + "\r\nContent-Type: application/octet-stream\r\nContent-Length: 0\r\n\r\n").encode()
        return ip / tcp / Raw(body)
    if up.startswith("TLS"):
        sni = re.search(r"SNI=([^)\s]+)", info)
        if sni:
            hello = TLS(msg=[TLSClientHello(ext=[TLS_Ext_ServerName(servernames=[ServerName(servername=sni.group(1).encode())])])])
            return ip / tcp / hello
        return ip / tcp / TLS(type=23, msg=[TLSApplicationData(data=pad(min(ln, 1460), 66))])
    return ip / tcp / Raw(pad(ln, 54) or b"\x00")


def convert(src, dst):
    lines = open(src, encoding="utf-8").read().splitlines()
    title = next((l for l in lines if l.startswith("#")), "")
    base = start_of(title)
    pkts = []
    for line in lines:
        if not line or line.startswith("#"):
            continue
        f = line.split("|")
        if len(f) < 8:
            continue
        p = packet(f)
        p.time = base + float(f[0])
        pkts.append(p)
    wrpcap(dst, pkts)
    return len(pkts)


if __name__ == "__main__":
    print(convert(sys.argv[1], sys.argv[2]))
