from loguru import logger
import sys
import os
from pathlib import Path

from src.config.settings import settings

def configure_logging():
    """Configure Loguru logging for the application."""
    
    # Remove default logger
    logger.remove()
    
    # Console logging with colors
    logger.add(
        sys.stderr,
        format=(
            "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
            "<level>{level: <8}</level> | "
            "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - "
            "<level>{message}</level>"
        ),
        level=settings.log_level,
        colorize=True,
        backtrace=True,
        diagnose=True,
    )
    
    # File logging for persistence
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)
    
    logger.add(
        log_dir / "cadpilot.log",
        rotation="10 MB",
        retention="1 month",
        compression="zip",
        level="DEBUG",  # More verbose in files
        format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}",
        backtrace=True,
        diagnose=True,
    )
    
    logger.info("Logging configured successfully")
    logger.debug(f"Log level set to: {settings.log_level}")

# Configure logging immediately when imported
configure_logging()