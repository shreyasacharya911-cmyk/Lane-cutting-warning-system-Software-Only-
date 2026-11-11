class VisualWarning:
    """Controls visual HMI indicator output for lane-cut warnings."""

    def __init__(self) -> None:
        self.active = False

    def activate(self) -> None:
        if not self.active:
            print("[HMI DISPLAY]: Vehicle in Blind Spot - Lane Cut Risk!")
            self.active = True

    def deactivate(self) -> None:
        if self.active:
            print("[HMI DISPLAY]: Cleared.")
            self.active = False
