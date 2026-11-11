from src.processing.decision_logic import DecisionLogic


def test_hysteresis() -> None:
    decision = DecisionLogic({"hysteresis_frames": 3})

    assert not decision.process("HIGH")
    assert not decision.process("HIGH")
    assert decision.process("HIGH")

    assert decision.process("LOW")
    assert decision.process("LOW")
    assert not decision.process("LOW")


def test_reset() -> None:
    decision = DecisionLogic({"hysteresis_frames": 2})
    assert not decision.process("HIGH")
    assert decision.process("HIGH")

    decision.reset()
    assert not decision.warning_active
    assert decision.high_risk_counter == 0
