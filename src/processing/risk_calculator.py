from typing import Any, Dict

from src.processing.object_tracking import TrackedObject


class RiskCalculator:
    """Computes Time To Collision (TTC) and maps it to discrete risk."""

    def __init__(self, config: Dict[str, Any]) -> None:
        self.ttc_high = config.get("ttc_high_risk_threshold_s", 1.5)
        self.ttc_medium = config.get("ttc_medium_risk_threshold_s", 2.5)

    def calculate_ttc(self, track: TrackedObject) -> float:
        """
        Calculate TTC = distance / relative_closing_speed.
        If relative_closing_speed <= 0 (receding or stationary), return inf.
        """
        if not track.history:
            return float("inf")

        latest = track.history[-1]
        distance = float(latest["distance"])
        rel_speed = float(latest["relative_speed"])

        if rel_speed <= 0:
            return float("inf")

        return distance / rel_speed

    def evaluate_risk(self, ttc: float) -> str:
        if ttc <= self.ttc_high:
            return "HIGH"
        elif ttc <= self.ttc_medium:
            return "MEDIUM"
        return "LOW"
