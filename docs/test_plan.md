# Test Plan

## Unit Tests
- `test_object_detection`: Invalid/out-of-bound radar data rejection.
- `test_lane_cut_detector`: Objects moving parallel vs cutting the lane.
- `test_risk_calculator`: TTC accuracy, handling dividing by zero.
- `test_decision_logic`: Hysteresis logic, proper state changes.

## Integration Tests
- Simulate full event loop: Indicator ON -> radar detects vehicle -> TTC drops -> Risk goes HIGH -> Warning activated -> Indicator OFF -> Warning cleared.

## Edge Cases Covered
- Sensor dropout mid-detection.
- Indicator toggled mid-warning.
- Watchdog failure simulating hung process.
