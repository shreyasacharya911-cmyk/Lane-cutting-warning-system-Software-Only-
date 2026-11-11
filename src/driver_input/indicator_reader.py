from src.security.input_validation import sanitize_indicator_status


class IndicatorReader:
    """
    Provides the left/right turn indicator status.
    In production, this interfaces with the vehicle CAN bus or GPIO.
    """

    def __init__(self) -> None:
        self._current_status = "OFF"

    def read_status(self) -> str:
        """Return sanitized indicator status: 'OFF', 'LEFT', or 'RIGHT'."""
        return sanitize_indicator_status(self._current_status)

    def set_simulation_status(self, status: str) -> None:
        """Set indicator state for hardware-free testing and mocking."""
        self._current_status = status
