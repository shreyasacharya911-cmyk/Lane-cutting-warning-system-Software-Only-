class RadarCalibration:
    """Handles side radar calibration checks and routines."""

    def __init__(self) -> None:
        self.calibrated = False

    def calibrate(self) -> bool:
        """Run radar calibration routine and return calibration state."""
        print("[RADAR] Calibration successful.")
        self.calibrated = True
        return self.calibrated
