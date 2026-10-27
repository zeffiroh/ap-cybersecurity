"""Test suite for 2.3.d — the blackbox acceptance contract.
Imports the implementation under test via IMPL env var so the SAME tests grade:
  - solution.py   (reference, must be green)
  - starter.py    (must be red until completed)
Default target is solution.py.
"""
import importlib.util
import os
import pathlib

_HERE = pathlib.Path(__file__).parent
_TARGET = os.environ.get("IMPL", str(_HERE / "solution.py"))


def _load(path):
    spec = importlib.util.spec_from_file_location("impl", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


impl = _load(_TARGET)

# ---------------------------------------------------------------------------
# Shared fixtures — seeded, deterministic policy and zone data
# ---------------------------------------------------------------------------
POLICY = {
    "server": {
        "require_ups": True,
        "min_hvac_redundancy": 1,
        "allowed_suppression": ["clean_agent"],
        "require_leak_sensor": True,
    },
    "closet": {
        "require_ups": True,
        "allowed_suppression": ["clean_agent", "none"],
    },
    "office": {
        "allowed_suppression": ["water", "clean_agent"],
    },
}


def _zone(name, room_type, has_ups, hvac_redundancy, suppression, has_leak_sensor):
    return {
        "name": name,
        "room_type": room_type,
        "has_ups": has_ups,
        "hvac_redundancy": hvac_redundancy,
        "suppression": suppression,
        "has_leak_sensor": has_leak_sensor,
    }


# ---- visible cases -------------------------------------------------------

def test_fully_compliant_server_room():
    zones = [_zone("server-room-a", "server", True, 1, "clean_agent", True)]
    assert impl.solve(zones, POLICY) == []


def test_server_room_missing_ups():
    zones = [_zone("server-room-b", "server", False, 1, "clean_agent", True)]
    assert impl.solve(zones, POLICY) == ["server-room-b"]


def test_server_room_water_suppression_noncompliant():
    zones = [_zone("server-room-c", "server", True, 1, "water", True)]
    assert impl.solve(zones, POLICY) == ["server-room-c"]


def test_server_room_no_hvac_redundancy():
    zones = [_zone("server-room-d", "server", True, 0, "clean_agent", True)]
    assert impl.solve(zones, POLICY) == ["server-room-d"]


def test_server_room_missing_leak_sensor():
    zones = [_zone("server-room-e", "server", True, 1, "clean_agent", False)]
    assert impl.solve(zones, POLICY) == ["server-room-e"]


def test_office_water_suppression_is_compliant():
    zones = [_zone("office-1", "office", False, 0, "water", False)]
    assert impl.solve(zones, POLICY) == []


def test_office_no_suppression_is_noncompliant():
    zones = [_zone("office-2", "office", False, 0, "none", False)]
    assert impl.solve(zones, POLICY) == ["office-2"]


def test_unknown_room_type_always_compliant():
    zones = [_zone("lobby-1", "lobby", False, 0, "none", False)]
    assert impl.solve(zones, POLICY) == []


def test_empty_zones():
    assert impl.solve([], POLICY) == []


def test_multiple_zones_mixed_compliance():
    zones = [
        _zone("server-room-a", "server", True, 1, "clean_agent", True),
        _zone("server-room-b", "server", False, 1, "clean_agent", True),
        _zone("closet-1", "closet", True, 0, "clean_agent", False),
        _zone("closet-2", "closet", False, 0, "none", False),
        _zone("office-1", "office", False, 0, "water", False),
    ]
    result = impl.solve(zones, POLICY)
    assert result == ["closet-2", "server-room-b"]


# ---- hidden / edge cases -------------------------------------------------

def test_closet_water_suppression_noncompliant():
    """closet policy only allows clean_agent or none, not water."""
    zones = [_zone("closet-3", "closet", True, 0, "water", False)]
    assert impl.solve(zones, POLICY) == ["closet-3"]


def test_hvac_redundancy_exact_boundary():
    """hvac_redundancy exactly equal to min_hvac_redundancy is compliant."""
    zones = [_zone("server-room-f", "server", True, 1, "clean_agent", True)]
    assert impl.solve(zones, POLICY) == []


def test_hvac_redundancy_above_minimum_is_compliant():
    zones = [_zone("server-room-g", "server", True, 3, "clean_agent", True)]
    assert impl.solve(zones, POLICY) == []


def test_multiple_failures_zone_reported_once():
    """A zone failing multiple rules still appears only once in the output."""
    zones = [_zone("server-room-h", "server", False, 0, "water", False)]
    assert impl.solve(zones, POLICY) == ["server-room-h"]


def test_output_sorted_and_deduplicated_order():
    zones = [
        _zone("z-server-3", "server", False, 0, "water", False),
        _zone("a-server-1", "server", False, 0, "water", False),
        _zone("m-server-2", "server", False, 0, "water", False),
    ]
    result = impl.solve(zones, POLICY)
    assert result == sorted(result)
    assert result == ["a-server-1", "m-server-2", "z-server-3"]


def test_empty_policy_means_no_zone_ever_fails():
    zones = [_zone("server-room-z", "server", False, 0, "water", False)]
    assert impl.solve(zones, {}) == []


def test_room_type_entry_with_no_keys_always_compliant():
    """A room_type present in policy but with an empty requirements dict has no requirements."""
    policy = {"vault": {}}
    zones = [_zone("vault-1", "vault", False, 0, "none", False)]
    assert impl.solve(zones, policy) == []
