"""Proves the stealth scenario is solvable + the toolkit is correct against the synthetic world.
This is the scenario's acceptance gate. Run from source/capstone/:  python -m pytest tests -q
"""
import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]      # source/capstone/
sys.path.insert(0, str(ROOT))

from toolkit import tools, world   # noqa: E402

STAGES = json.loads((ROOT / "stages" / "stages.json").read_text(encoding="utf-8"))


def test_world_present():
    assert world.load("employees") and world.load("network") and world.load("emails")


def test_stage1_recon_finds_expected_hosts():
    found = {h["name"] for h in tools.recon(world.load("network"))}
    for expected in STAGES["stages"][0]["expected_hosts"]:
        assert expected in found, f"recon missed {expected}"
    # the legacy clinical host must be flagged for telnet
    pacs = [h for h in tools.recon(world.load("network")) if h["name"] == "pacs"][0]
    assert "telnet" in pacs["risky_services"]


def test_stage1_password_spray_detected():
    spray = tools.detect_spray(world.load("auth_logs"))
    assert spray, "no spray detected"
    top = spray[0]
    assert top["src_ip"] == world.load("_meta")["spray_ip"]
    assert top["users"] >= 5 and top["fails"] >= 20


def test_stage2_phish_identified():
    phish = tools.find_phish(world.load("emails"))
    breach = [m for m in phish if m["id"] == STAGES["stages"][1]["expected_email"]]
    assert breach, "breach email M999 not flagged"
    assert breach[0]["indicators"] == STAGES["stages"][1]["expected_indicators"]


def test_ir_timeline_reconstructs_breach():
    ir = tools.ir_timeline(world.load("emails"), world.load("auth_logs"), world.load("_meta"))
    assert ir["victim"] == world.load("_meta")["victim"]
    assert ir["entry_email"] == "M999"
    assert ir["compromised_login_src"] == world.load("_meta")["spray_ip"]
    assert "enable MFA" in ir["recommendation"]


def test_stage4_lateral_movement_traced():
    meta = world.load("_meta")
    chain = tools.find_lateral_movement(world.load("network_logs"), meta)
    dsts = [h["dst_ip"] for h in chain]
    assert "10.20.1.25" in dsts and "10.20.1.10" in dsts
    fileserver_hop = [h for h in chain if h["dst_ip"] == "10.20.1.25"][0]
    assert fileserver_hop["service"] == "smb"
    dc_hop = [h for h in chain if h["dst_ip"] == "10.20.1.10"][0]
    assert dc_hop["service"] == "ldap"


def test_stage5_ioc_detected_on_compromised_host():
    meta = world.load("_meta")
    matches = tools.detect_ioc(world.load("device_logs"), meta)
    assert any(m["host"] == "ws-nguyen" and m["hash"] == meta["ioc_hash"] for m in matches)


def test_stage6_exfil_detected():
    meta = world.load("_meta")
    hits = tools.detect_exfil(world.load("app_logs"), meta)
    assert hits and hits[0]["dst_ip"] == meta["exfil_dst_ip"]
    assert hits[0]["bytes_out"] >= meta["exfil_bytes_threshold"]


def test_stage7_full_report_ties_stages_together():
    meta = world.load("_meta")
    report = tools.full_incident_report(
        world.load("emails"), world.load("auth_logs"), world.load("network_logs"),
        world.load("device_logs"), world.load("app_logs"), meta)
    assert report["ir_timeline"]["victim"] == meta["victim"]
    assert report["lateral_movement"]
    assert report["ioc_matches"]
    assert report["exfiltration"]
    assert "isolate ws-nguyen" in report["recommendation"]
