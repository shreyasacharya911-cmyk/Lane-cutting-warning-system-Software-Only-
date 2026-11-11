from typing import Any, Dict


class SecureCANInterface:
    """Provides authenticated CAN bus messaging abstraction."""

    def __init__(self) -> None:
        pass

    def send_message(self, topic: str, payload: Dict[str, Any]) -> bool:
        """Send an authenticated CAN message (CRC/MAC hook for target)."""
        return True
