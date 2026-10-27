#!/usr/bin/env python3
"""mhsec — CLI front-end for the Meridian Health toolkit. Offline.
Run from source/capstone/:
  python -m toolkit.mhsec scan
  python -m toolkit.mhsec loganalyze
  python -m toolkit.mhsec phish
  python -m toolkit.mhsec ir
  python -m toolkit.mhsec pivot
  python -m toolkit.mhsec iocscan
  python -m toolkit.mhsec exfil
  python -m toolkit.mhsec report
"""
import json
import sys

from . import tools, world


def main(argv=None):
    argv = argv if argv is not None else sys.argv[1:]
    if not argv:
        print("usage: mhsec {scan|loganalyze|phish|ir}")
        return 2
    cmd = argv[0]
    if cmd == "scan":
        out = tools.recon(world.load("network"))
    elif cmd == "loganalyze":
        out = tools.detect_spray(world.load("auth_logs"))
    elif cmd == "phish":
        out = tools.find_phish(world.load("emails"))
    elif cmd == "ir":
        out = tools.ir_timeline(world.load("emails"), world.load("auth_logs"), world.load("_meta"))
    elif cmd == "pivot":
        out = tools.find_lateral_movement(world.load("network_logs"), world.load("_meta"))
    elif cmd == "iocscan":
        out = tools.detect_ioc(world.load("device_logs"), world.load("_meta"))
    elif cmd == "exfil":
        out = tools.detect_exfil(world.load("app_logs"), world.load("_meta"))
    elif cmd == "report":
        out = tools.full_incident_report(
            world.load("emails"), world.load("auth_logs"), world.load("network_logs"),
            world.load("device_logs"), world.load("app_logs"), world.load("_meta"))
    else:
        print(f"unknown tool: {cmd}")
        return 2
    print(json.dumps(out, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
