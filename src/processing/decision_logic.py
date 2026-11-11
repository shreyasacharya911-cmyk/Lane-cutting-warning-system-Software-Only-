from typing import Any, Dict


class DecisionLogic:
    """Applies frame hysteresis to risk levels to prevent warning flicker."""

    def __init__(self, config: Dict[str, Any]) -> None:
        self.hysteresis_frames = config.get("hysteresis_frames", 3)
        self.high_risk_counter = 0
        self.warning_active = False

    def process(self, max_risk_level: str) -> bool:
        """
        Evaluate risk level and apply hysteresis to trigger warning.
        Returns True if warning should be active.
        """
        if max_risk_level == "HIGH":
            self.high_risk_counter += 1
        else:
            self.high_risk_counter = max(0, self.high_risk_counter - 1)

        if self.high_risk_counter >= self.hysteresis_frames:
            self.warning_active = True
        elif self.high_risk_counter == 0:
            self.warning_active = False

        return self.warning_active

    def reset(self) -> None:
        self.high_risk_counter = 0
        self.warning_active = False
