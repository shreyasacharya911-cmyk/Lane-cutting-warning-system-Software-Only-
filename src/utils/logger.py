import logging
import logging.config
import os
import yaml


def setup_logging() -> None:
    """Configure application logging from YAML config with a basic fallback."""
    project_root = os.path.abspath(
        os.path.join(os.path.dirname(__file__), "../..")
    )
    config_path = os.path.join(project_root, "config", "logging_config.yaml")
    try:
        with open(config_path, "r") as f:
            config = yaml.safe_load(f.read())

        file_handler = config.get("handlers", {}).get("file", {})
        log_filename = file_handler.get("filename")
        if log_filename:
            if not os.path.isabs(log_filename):
                log_filename = os.path.join(project_root, log_filename)
                file_handler["filename"] = log_filename
            log_dir = os.path.dirname(log_filename)
            if log_dir and not os.path.exists(log_dir):
                os.makedirs(log_dir, exist_ok=True)

        logging.config.dictConfig(config)
    except Exception as e:
        logging.basicConfig(level=logging.INFO)
        logging.warning(
            f"Failed to load logging config: {e}. Using basic config."
        )


def get_logger(name: str) -> logging.Logger:
    """Return a named logger instance."""
    return logging.getLogger(name)
