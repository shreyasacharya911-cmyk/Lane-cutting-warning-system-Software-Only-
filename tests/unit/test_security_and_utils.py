import time

from src.security.input_validation import sanitize_indicator_status
from src.security.watchdog import Watchdog
from src.utils.diagnostics import Diagnostics


def test_watchdog_triggers_fail_safe_on_timeout() -> None:
    triggered = []

    def fail_safe() -> None:
        triggered.append(True)

    watchdog = Watchdog(timeout_s=0.02, fail_safe_cb=fail_safe)
    watchdog.check()
    assert not triggered

    time.sleep(0.05)
    watchdog.check()
    assert triggered == [True]
    assert watchdog.faulted

    watchdog.heartbeat()
    assert not watchdog.faulted


def test_diagnostics_fault_lifecycle() -> None:
    diag = Diagnostics()
    assert not diag.has_faults()

    diag.report_fault("radar", "Sensor timeout")
    assert diag.has_faults()

    diag.clear_fault("radar")
    assert not diag.has_faults()


def test_sanitize_indicator_status() -> None:
    assert sanitize_indicator_status("left") == "LEFT"
    assert sanitize_indicator_status("RIGHT") == "RIGHT"
    assert sanitize_indicator_status("invalid") == "OFF"
    assert sanitize_indicator_status(None) == "OFF"
