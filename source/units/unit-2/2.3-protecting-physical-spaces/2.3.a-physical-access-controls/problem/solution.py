"""Reference solution for 2.3.a. MUST pass 100% of tests.py.
Also the default 'blackbox' implementation students can swap out (see blackbox.yaml)."""
def solve(data: dict[str, bool]) -> list[str]:
    gaps = []
    
    # - If keyed lock is absent AND badge reader is absent: gap "no_key_control"
    if not data.get("keyed_lock", False) and not data.get("badge_reader", False):
        gaps.append("no_key_control")
        
    # - If badge reader is absent AND biometric is absent: gap "no_electronic_access"
    if not data.get("badge_reader", False) and not data.get("biometric_reader", False):
        gaps.append("no_electronic_access")
        
    # - If mantrap is absent: gap "no_tailgating_prevention"
    if not data.get("mantrap", False):
        gaps.append("no_tailgating_prevention")
        
    # - If CCTV is absent: gap "no_visual_monitoring"
    if not data.get("cctv", False):
        gaps.append("no_visual_monitoring")
        
    # - If security guard is absent AND biometric is absent: gap "no_identity_verification"
    if not data.get("security_guard", False) and not data.get("biometric_reader", False):
        gaps.append("no_identity_verification")
        
    return sorted(gaps)
