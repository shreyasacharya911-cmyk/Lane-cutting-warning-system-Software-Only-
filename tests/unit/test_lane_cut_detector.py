from src.processing.lane_cut_detector import LaneCutDetector
from src.processing.object_tracking import TrackedObject


def test_lane_cut_positive() -> None:
    detector = LaneCutDetector({"lateral_warning_distance_m": 1.0})
    track = TrackedObject(1)
    # distance 10, angle 0 -> lateral distance = 0 < 1.0 -> True
    track.update(
        {
            "id": 1,
            "distance": 10.0,
            "relative_speed": 5.0,
            "angle": 0.0,
            "timestamp": 1,
        }
    )
    assert detector.is_cutting_lane(track, "LEFT")


def test_lane_cut_negative() -> None:
    detector = LaneCutDetector({"lateral_warning_distance_m": 1.0})
    track = TrackedObject(1)
    # distance 10, angle 30 (right side) while LEFT indicator active -> False
    track.update(
        {
            "id": 1,
            "distance": 10.0,
            "relative_speed": 5.0,
            "angle": 30.0,
            "timestamp": 1,
        }
    )
    assert not detector.is_cutting_lane(track, "LEFT")


def test_lane_cut_working_scenario() -> None:
    detector = LaneCutDetector({"lateral_warning_distance_m": 1.0})
    track = TrackedObject(2)
    # distance 10, angle -5 (left side) -> lateral ~0.87 < 1.0 -> True
    track.update(
        {
            "id": 2,
            "distance": 10.0,
            "relative_speed": 5.0,
            "angle": -5.0,
            "timestamp": 2,
        }
    )
    assert detector.is_cutting_lane(track, "LEFT")
    assert not detector.is_cutting_lane(track, "RIGHT")


def test_lane_cut_right_side_and_empty_history() -> None:
    detector = LaneCutDetector({"lateral_warning_distance_m": 1.0})
    empty_track = TrackedObject(3)
    assert not detector.is_cutting_lane(empty_track, "RIGHT")

    right_track = TrackedObject(4)
    right_track.update(
        {
            "id": 4,
            "distance": 10.0,
            "relative_speed": 5.0,
            "angle": 5.0,
            "timestamp": 3,
        }
    )
    assert detector.is_cutting_lane(right_track, "RIGHT")
    assert not detector.is_cutting_lane(right_track, "LEFT")
