class InstrumentClusterPublisher:
    """Publishes LCA system state to the scooter instrument cluster."""

    def publish(
        self,
        speed: float,
        indicator: str,
        lca_on: bool,
        warning_active: bool,
    ) -> None:
        """Publish the current system status summary."""
        status_msg = (
            f"[CLUSTER] Speed: {speed} km/h | "
            f"Indicator: {indicator} | "
            f"LCA: {'ON' if lca_on else 'OFF'} | "
            f"WARNING: {'ACTIVE' if warning_active else 'NONE'}"
        )
        print(status_msg)
