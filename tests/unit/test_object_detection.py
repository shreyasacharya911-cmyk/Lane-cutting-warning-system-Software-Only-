from src.processing.object_detection import ObjectDetector
from src.processing.object_tracking import ObjectTracker
from src.security.input_validation import validate_radar_frame


def test_valid_radar_frame() -> None:
    frame = {
        "id": 1,
        "distance": 10.0,
        "relative_speed": -5.0,
        "angle": 30.0,
        "timestamp": 123456,
    }
    assert validate_radar_frame(frame)


def test_missing_keys() -> None:
    frame = {"id": 1, "distance": 10.0}
    assert not validate_radar_frame(frame)


def test_out_of_bounds_distance() -> None:
    frame = {
        "id": 1,
        "distance": 250.0,
        "relative_speed": -5.0,
        "angle": 30.0,
        "timestamp": 123456,
    }
    assert not validate_radar_frame(frame)

    frame2 = {
        "id": 1,
        "distance": -5.0,
        "relative_speed": -5.0,
        "angle": 30.0,
        "timestamp": 123456,
    }
    assert not validate_radar_frame(frame2)


def test_out_of_bounds_angle() -> None:
    frame = {
        "id": 1,
        "distance": 15.0,
        "relative_speed": 5.0,
        "angle": 185.0,
        "timestamp": 123456,
    }
    assert not validate_radar_frame(frame)


def test_object_detector_and_tracker_stale_cleanup() -> None:
    detector = ObjectDetector()
    tracker = ObjectTracker()
    frame1 = {
        "id": 1,
        "distance": 15.0,
        "relative_speed": 5.0,
        "angle": -4.0,
        "timestamp": 1,
    }
    frame2 = {
        "id": 2,
        "distance": 25.0,
        "relative_speed": 2.0,
        "angle": -10.0,
        "timestamp": 1,
    }
    tracks = tracker.update_tracks(detector.detect_objects([frame1, frame2]))
    assert len(tracks) == 2

    # Sensor drops track 2 on next frame
    tracks = tracker.update_tracks(detector.detect_objects([frame1]))
    assert len(tracks) == 1
    assert tracks[0].id == 1
