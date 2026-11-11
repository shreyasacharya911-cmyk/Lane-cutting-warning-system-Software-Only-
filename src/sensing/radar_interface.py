from typing import Any, Dict, List
from src.security.input_validation import validate_radar_frame


class RadarInterface:
    """
    Acquires and validates raw radar frames from the side radar sensor.
    """

    def __init__(self, config: Dict[str, Any]) -> None:
        self.config = config
        self._frame_buffer: List[Dict[str, Any]] = []

    def get_latest_frames(self, side: str) -> List[Dict[str, Any]]:
        """
        Fetch radar frames for the active side.
        Returns a list of valid frame dictionaries.
        """
        valid_frames = []
        for frame in self._frame_buffer:
            if validate_radar_frame(frame):
                valid_frames.append(frame)

        # Clear after read (queue drain)
        self._frame_buffer = []
        return valid_frames

    def feed_simulated_data(self, frames: List[Dict[str, Any]]) -> None:
        """Inject radar frames for testing without physical radar hardware."""
        self._frame_buffer.extend(frames)
