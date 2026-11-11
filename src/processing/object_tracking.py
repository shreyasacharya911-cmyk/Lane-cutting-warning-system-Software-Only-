from typing import Any, Dict, List


class TrackedObject:
    """Maintains bounded frame history for a single tracked object."""

    def __init__(self, obj_id: int) -> None:
        self.id = obj_id
        self.history: List[Dict[str, Any]] = []

    def update(self, data: Dict[str, Any]) -> None:
        self.history.append(data)
        # Keep last 10 frames
        if len(self.history) > 10:
            self.history.pop(0)


class ObjectTracker:
    """Associates detections by ID and prunes stale tracks."""

    def __init__(self) -> None:
        self.tracks: Dict[int, TrackedObject] = {}

    def update_tracks(
        self, detections: List[Dict[str, Any]]
    ) -> List[TrackedObject]:
        seen_ids = set()

        for det in detections:
            obj_id = det["id"]
            if obj_id not in self.tracks:
                self.tracks[obj_id] = TrackedObject(obj_id)
            self.tracks[obj_id].update(det)
            seen_ids.add(obj_id)

        # Clean up stale tracks
        stale_ids = set(self.tracks.keys()) - seen_ids
        for stale in stale_ids:
            del self.tracks[stale]

        return list(self.tracks.values())
