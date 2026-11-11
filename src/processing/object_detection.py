from typing import Any, Dict, List


class ObjectDetector:
    """Extracts structured object detections from validated radar frames."""

    def __init__(self) -> None:
        pass

    def detect_objects(
        self, frames: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """
        In a real system, might run clustering or filtering.
        Here, we pass through valid frames as detected objects.
        """
        objects = []
        for frame in frames:
            objects.append(
                {
                    "id": frame["id"],
                    "distance": frame["distance"],
                    "relative_speed": frame["relative_speed"],
                    "angle": frame["angle"],
                    "timestamp": frame["timestamp"],
                }
            )
        return objects
