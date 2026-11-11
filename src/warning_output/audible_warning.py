class AudibleWarning:
    """Controls audible buzzer output for lane-cut warnings."""

    def __init__(self) -> None:
        self.active = False

    def activate(self) -> None:
        if not self.active:
            print("[BUZZER]: BEEP BEEP BEEP!")
            self.active = True

    def deactivate(self) -> None:
        if self.active:
            print("[BUZZER]: Off.")
            self.active = False
