from typing import Dict


class Diagnostics:
    """Tracks active module-level faults across the LCA system."""

    def __init__(self) -> None:
        self.faults: Dict[str, str] = {}

    def report_fault(self, module: str, error: str) -> None:
        self.faults[module] = error

    def clear_fault(self, module: str) -> None:
        if module in self.faults:
            del self.faults[module]

    def has_faults(self) -> bool:
        return len(self.faults) > 0
