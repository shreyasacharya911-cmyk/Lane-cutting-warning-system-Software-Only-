import os


class AccessControl:
    """Enforces least-privilege runtime permission checks."""

    def __init__(self) -> None:
        pass

    def check_permissions(self) -> bool:
        """Ensure the process is running as a non-root user on POSIX."""
        if hasattr(os, "geteuid"):
            if os.geteuid() == 0:
                print("SECURITY WARNING: Running as root!")
                return False
        return True
