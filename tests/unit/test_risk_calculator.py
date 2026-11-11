from src.processing.object_tracking import TrackedObject
from src.processing.risk_calculator import RiskCalculator


def test_ttc_calculation_approaching() -> None:
    calc = RiskCalculator(
        {"ttc_high_risk_threshold_s": 1.5, "ttc_medium_risk_threshold_s": 2.5}
    )
    track = TrackedObject(1)
    # distance 10, speed 10 -> TTC = 1.0
    track.update({"distance": 10.0, "relative_speed": 10.0})
    assert calc.calculate_ttc(track) == 1.0


def test_ttc_calculation_receding_and_zero_speed() -> None:
    calc = RiskCalculator({"ttc_high_risk_threshold_s": 1.5})
    track = TrackedObject(1)
    track.update({"distance": 10.0, "relative_speed": -5.0})
    assert calc.calculate_ttc(track) == float("inf")

    track.update({"distance": 10.0, "relative_speed": 0.0})
    assert calc.calculate_ttc(track) == float("inf")

    empty_track = TrackedObject(2)
    assert calc.calculate_ttc(empty_track) == float("inf")


def test_risk_evaluation() -> None:
    calc = RiskCalculator(
        {"ttc_high_risk_threshold_s": 1.5, "ttc_medium_risk_threshold_s": 2.5}
    )
    assert calc.evaluate_risk(1.0) == "HIGH"
    assert calc.evaluate_risk(2.0) == "MEDIUM"
    assert calc.evaluate_risk(5.0) == "LOW"
