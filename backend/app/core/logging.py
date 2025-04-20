import logging
import sys
from typing import List
import os
from loguru import logger
from pydantic import BaseModel

# Create logs directory if it doesn't exist
os.makedirs("logs", exist_ok=True)

class LogConfig(BaseModel):
    """
    Logging configuration to be set for the application.
    """
    LOGGER_NAME: str = "og_production"
    LOG_FORMAT: str = "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>"
    LOG_LEVEL: str = "INFO"
    LOG_FILE_PATH: str = "logs/app.log"
    LOG_ROTATION: str = "10 MB"
    LOG_RETENTION: str = "1 month"

    # List of loggers to disable
    LOGGERS_TO_DISABLE: List[str] = [
        "uvicorn.asgi",
        "uvicorn.access",
    ]

def setup_logging():
    """
    Set up logging for the application.
    """
    log_config = LogConfig()
    
    # Configure loguru
    logger.remove()  # Remove default handler
    logger.add(sys.stderr, level=log_config.LOG_LEVEL, format=log_config.LOG_FORMAT)
    logger.add(
        log_config.LOG_FILE_PATH,
        level=log_config.LOG_LEVEL,
        format=log_config.LOG_FORMAT,
        rotation=log_config.LOG_ROTATION,
        retention=log_config.LOG_RETENTION,
    )
    
    # Disable loggers that are too noisy
    for logger_name in log_config.LOGGERS_TO_DISABLE:
        logging.getLogger(logger_name).handlers = []
        logging.getLogger(logger_name).propagate = False
        
    # Intercept standard logging messages
    class InterceptHandler(logging.Handler):
        def emit(self, record):
            # Get corresponding Loguru level
            try:
                level = logger.level(record.levelname).name
            except ValueError:
                level = record.levelno
            
            # Find caller from where the logged message originated
            frame, depth = logging.currentframe(), 2
            while frame.f_code.co_filename == logging.__file__:
                frame = frame.f_back
                depth += 1
                
            logger.opt(depth=depth, exception=record.exc_info).log(
                level, record.getMessage()
            )
    
    # Set up intercept handler
    logging.basicConfig(handlers=[InterceptHandler()], level=0)

    # Return configured logger
    return logger.bind(request_id=None, method=None)
