def solve(data: dict[str, bool]) -> list[str]:
    gaps = []
    
    if not data.get("keyed_lock", False) and not data.get("badge_reader", False):
        gaps.append("no_key_control")
        
    if not data.get("badge_reader", False) and not data.get("biometric_reader", False):
        gaps.append("no_electronic_access")
        
    if not data.get("mantrap", False):
        gaps.append("no_tailgating_prevention")
        
    if not data.get("cctv", False):
        gaps.append("no_visual_monitoring")
        
    if not data.get("security_guard", False) and not data.get("biometric_reader", False):
        gaps.append("no_identity_verification")
        
    return sorted(gaps)
