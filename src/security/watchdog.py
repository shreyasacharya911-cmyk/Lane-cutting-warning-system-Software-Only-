import time
from typing import Callable


class Watchdog:
    """
    Monitors process health. If heartbeat isn't called within timeout,
    triggers a fail-safe callback.
    """

    def __init__(
        self, timeout_s: float, fail_safe_cb: Callable[[], None]
    ) -> None:
        self.timeout_s = timeout_s
        self.fail_safe_cb = fail_safe_cb
        self.last_heartbeat = time.time()
        self.faulted = False

    def heartbeat(self) -> None:
        self.last_heartbeat = time.time()
        self.faulted = False

    def check(self) -> None:
        elapsed = time.time() - self.last_heartbeat
        if not self.faulted and elapsed > self.timeout_s:
            self.faulted = True
            self.fail_safe_cb()
