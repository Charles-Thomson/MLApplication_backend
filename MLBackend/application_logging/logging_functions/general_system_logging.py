import logging

# Basic logging config
logging.root.setLevel(logging.NOTSET)
logging.basicConfig(level=logging.NOTSET)

DEFAULT_FORMAT = "%(levelname)s :: %(funcName)s :: %(message)s"

def general_system_logger_generator() -> None:
    """Generate the logger for general use in the system
    """
    
    general_system_logging_file_path = "application_logging/logs/system_logs/general_system"
    general_system_logger_name = "general_system_logger"
    
    logger = logging.getLogger(general_system_logger_name)
    file_handler = logging.FileHandler(general_system_logging_file_path)
    file_handler.setLevel(logging.DEBUG)  
    formatter = logging.Formatter(DEFAULT_FORMAT)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)