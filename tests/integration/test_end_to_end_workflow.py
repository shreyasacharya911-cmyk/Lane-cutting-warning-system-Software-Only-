from src.driver_input.indicator_reader import IndicatorReader
from src.processing.decision_logic import DecisionLogic
from src.processing.lane_cut_detector import LaneCutDetector
from src.processing.object_detection import ObjectDetector
from src.processing.object_tracking import ObjectTracker
from src.processing.risk_calculator import RiskCalculator
from src.sensing.radar_interface import RadarInterface


def _run_step(
    indicator_side: str,
    radar: RadarInterface,
    detector: ObjectDetector,
    tracker: ObjectTracker,
    lane_cutter: LaneCutDetector,
    risk_calc: RiskCalculator,
    decision: DecisionLogic,
) -> bool:
    frames = radar.get_latest_frames(indicator_side)
    tracks = tracker.update_tracks(detector.detect_objects(frames))

    max_risk = "LOW"
    for track in tracks:
        if lane_cutter.is_cutting_lane(track, indicator_side):
            ttc = risk_calc.calculate_ttc(track)
            risk = risk_calc.evaluate_risk(ttc)
            if risk == "HIGH":
                max_risk = "HIGH"
            elif risk == "MEDIUM" and max_risk != "HIGH":
                max_risk = "MEDIUM"

    return decision.process(max_risk)


def test_full_workflow() -> None:
    config = {
        "lca": {
            "lane_width_m": 3.5,
            "lateral_warning_distance_m": 1.0,
            "ttc_high_risk_threshold_s": 1.5,
            "ttc_medium_risk_threshold_s": 2.5,
            "hysteresis_frames": 2,
        }
    }

    indicator = IndicatorReader()
    radar = RadarInterface({})
    detector = ObjectDetector()
    tracker = ObjectTracker()
    lane_cutter = LaneCutDetector(config["lca"])
    risk_calc = RiskCalculator(config["lca"])
    decision = DecisionLogic(config["lca"])

    # 1. System idle
    assert indicator.read_status() == "OFF"

    # 2. Indicator ON
    indicator.set_simulation_status("LEFT")
    side = indicator.read_status()

    # 3. Frame 1: approaching at TTC = 2.0s (MEDIUM)
    radar.feed_simulated_data(
        [
            {
                "id": 1,
                "distance": 20.0,
                "relative_speed": 10.0,
                "angle": 0.0,
                "timestamp": 1,
            }
        ]
    )
    assert not _run_step(
        side, radar, detector, tracker, lane_cutter, risk_calc, decision
    )

    # Frame 2: closer at TTC = 1.0s (HIGH), hysteresis counter = 1
    radar.feed_simulated_data(
        [
            {
                "id": 1,
                "distance": 10.0,
                "relative_speed": 10.0,
                "angle": 0.0,
                "timestamp": 2,
            }
        ]
    )
    assert not _run_step(
        side, radar, detector, tracker, lane_cutter, risk_calc, decision
    )

    # Frame 3: TTC = 0.5s (HIGH), hysteresis reached -> warning active
    radar.feed_simulated_data(
        [
            {
                "id": 1,
                "distance": 5.0,
                "relative_speed": 10.0,
                "angle": 0.0,
                "timestamp": 3,
            }
        ]
    )
    assert _run_step(
        side, radar, detector, tracker, lane_cutter, risk_calc, decision
    )

    # 4. Sensor dropout mid-warning: hysteresis decays on empty frames
    assert _run_step(
        side, radar, detector, tracker, lane_cutter, risk_calc, decision
    )
    assert not _run_step(
        side, radar, detector, tracker, lane_cutter, risk_calc, decision
    )

    # 5. Indicator toggled OFF mid-warning clears state immediately
    radar.feed_simulated_data(
        [
            {
                "id": 1,
                "distance": 5.0,
                "relative_speed": 10.0,
                "angle": 0.0,
                "timestamp": 4,
            }
        ]
    )
    _run_step(side, radar, detector, tracker, lane_cutter, risk_calc, decision)
    radar.feed_simulated_data(
        [
            {
                "id": 1,
                "distance": 4.0,
                "relative_speed": 10.0,
                "angle": 0.0,
                "timestamp": 5,
            }
        ]
    )
    assert _run_step(
        side, radar, detector, tracker, lane_cutter, risk_calc, decision
    )

    indicator.set_simulation_status("OFF")
    decision.reset()
    assert not decision.warning_active
