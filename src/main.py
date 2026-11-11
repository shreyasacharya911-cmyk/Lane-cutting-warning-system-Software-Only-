import os
import sys
import time
import yaml

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from src.driver_input.indicator_reader import IndicatorReader  # noqa: E402
from src.processing.decision_logic import DecisionLogic  # noqa: E402
from src.processing.lane_cut_detector import LaneCutDetector  # noqa: E402
from src.processing.object_detection import ObjectDetector  # noqa: E402
from src.processing.object_tracking import ObjectTracker  # noqa: E402
from src.processing.risk_calculator import RiskCalculator  # noqa: E402
from src.security.access_control import AccessControl  # noqa: E402
from src.security.watchdog import Watchdog  # noqa: E402
from src.sensing.radar_interface import RadarInterface  # noqa: E402
from src.system_status.instrument_cluster_publisher import (  # noqa: E402
    InstrumentClusterPublisher,
)
from src.utils.diagnostics import Diagnostics  # noqa: E402
from src.utils.logger import get_logger, setup_logging  # noqa: E402
from src.warning_output.audible_warning import AudibleWarning  # noqa: E402
from src.warning_output.visual_warning import VisualWarning  # noqa: E402


def main() -> None:
    """Initialize and run the Lane Cut Assist (LCA) main control loop."""
    setup_logging()
    logger = get_logger("LCASystem")
    logger.info("Initializing LCA System...")

    config_path = os.path.join(PROJECT_ROOT, "config", "system_config.yaml")
    with open(config_path, "r") as f:
        config = yaml.safe_load(f) or {}

    sys_config = config.get("system", {})
    lca_config = config.get("lca", {})
    radar_config = config.get("radar", {})

    diagnostics = Diagnostics()
    access_control = AccessControl()
    if not access_control.check_permissions():
        logger.warning("Running with elevated privileges.")
        diagnostics.report_fault("security", "Process running as root")

    indicator_reader = IndicatorReader()
    radar = RadarInterface(radar_config)
    detector = ObjectDetector()
    tracker = ObjectTracker()
    lane_cutter = LaneCutDetector(lca_config)
    risk_calc = RiskCalculator(lca_config)
    decision = DecisionLogic(lca_config)
    vis_warn = VisualWarning()
    aud_warn = AudibleWarning()
    cluster = InstrumentClusterPublisher()

    def fail_safe() -> None:
        logger.error("Watchdog timeout! Engaging fail-safe.")
        diagnostics.report_fault("watchdog", "Loop timeout exceeded")
        vis_warn.deactivate()
        aud_warn.deactivate()
        cluster.publish(0.0, "OFF", False, False)

    timeout_s = float(sys_config.get("timeout_ms", 100)) / 1000.0
    watchdog = Watchdog(timeout_s=timeout_s, fail_safe_cb=fail_safe)
    loop_rate_hz = max(1.0, float(sys_config.get("loop_rate_hz", 20)))

    logger.info("System initialized. Starting main loop...")

    # Nominal vehicle speed (km/h) pending CAN speed signal integration
    speed = 40.0
    watchdog.heartbeat()

    try:
        while True:
            watchdog.check()
            watchdog.heartbeat()

            indicator = indicator_reader.read_status()

            if indicator in ["LEFT", "RIGHT"]:
                lca_on = True
                frames = radar.get_latest_frames(side=indicator)
                objects = detector.detect_objects(frames)
                tracks = tracker.update_tracks(objects)

                max_risk = "LOW"

                for track in tracks:
                    if lane_cutter.is_cutting_lane(track, indicator):
                        ttc = risk_calc.calculate_ttc(track)
                        risk = risk_calc.evaluate_risk(ttc)
                        if risk == "HIGH":
                            max_risk = "HIGH"
                        elif risk == "MEDIUM" and max_risk != "HIGH":
                            max_risk = "MEDIUM"

                warning_trigger = decision.process(max_risk)

                if warning_trigger:
                    vis_warn.activate()
                    aud_warn.activate()
                else:
                    vis_warn.deactivate()
                    aud_warn.deactivate()
            else:
                lca_on = False
                decision.reset()
                vis_warn.deactivate()
                aud_warn.deactivate()

            cluster.publish(speed, indicator, lca_on, decision.warning_active)
            time.sleep(1.0 / loop_rate_hz)

    except KeyboardInterrupt:
        logger.info("System shutdown requested.")
        vis_warn.deactivate()
        aud_warn.deactivate()


if __name__ == "__main__":
    main()
