# System Architecture

## Core Modules

- **Driver Input (`src/driver_input/`)**: Reads the L/R indicator status to determine if the system should be active.
- **Sensing (`src/sensing/`)**: Interacts with the side radar, reading raw frames and bounds-checking them.
- **Processing (`src/processing/`)**:
  - `object_detection.py`: Validates radar frames.
  - `object_tracking.py`: Maintains history of detected objects.
  - `lane_cut_detector.py`: Predicts if object trajectory intersects the ego lane.
  - `risk_calculator.py`: Calculates Time To Collision (TTC).
  - `decision_logic.py`: Compares risk to thresholds and triggers warnings.
- **Warning Output (`src/warning_output/`)**: Triggers visual (HMI) and audible (buzzer) feedback.
- **System Status (`src/system_status/`)**: Publishes current speed, state, and warning flags.
- **Security (`src/security/`)**: Validates input, prevents spoofing, and handles the heartbeat watchdog.
