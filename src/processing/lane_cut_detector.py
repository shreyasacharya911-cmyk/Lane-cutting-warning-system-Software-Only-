import math
from typing import Any, Dict

from src.processing.object_tracking import TrackedObject


class LaneCutDetector:
    """Detects whether a tracked object trajectory cuts into the ego lane."""

    def __init__(self, config: Dict[str, Any]) -> None:
        self.lane_width = config.get("lane_width_m", 3.5)
        self.lateral_warning_distance = config.get(
            "lateral_warning_distance_m", 1.0
        )

    def is_cutting_lane(self, track: TrackedObject, side: str) -> bool:
        """
        Determine if the object trajectory intersects our lane.
        Checks active turn side and whether lateral distance is within
        the warning corridor (0 deg = directly behind, - left, + right).
        """
        if not track.history:
            return False

        latest = track.history[-1]
        angle = latest["angle"]

        # Ignore objects on the opposite side
        if side == "LEFT" and angle > 0:
            return False
        if side == "RIGHT" and angle < 0:
            return False

        lateral_dist = abs(
            latest["distance"] * math.sin(math.radians(angle))
        )

        return bool(lateral_dist < self.lateral_warning_distance)
