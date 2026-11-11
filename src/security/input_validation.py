from typing import Any, Dict


def validate_radar_frame(frame: Dict[str, Any]) -> bool:
    """
    Validate that a radar frame has required keys and logical bounds.
    Returns True if valid, False otherwise.
    """
    required_keys = ["id", "distance", "relative_speed", "angle", "timestamp"]
    for key in required_keys:
        if key not in frame:
            return False

    try:
        if frame["distance"] < 0 or frame["distance"] > 200:
            return False
        if frame["angle"] < -180 or frame["angle"] > 180:
            return False
    except TypeError:
        return False

    return True


def sanitize_indicator_status(status: Any) -> str:
    """Ensure turn indicator status is a known safe state."""
    valid_states = ["OFF", "LEFT", "RIGHT"]
    if isinstance(status, str) and status.upper() in valid_states:
        return status.upper()
    return "OFF"
