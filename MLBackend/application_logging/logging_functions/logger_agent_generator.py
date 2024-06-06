import logging
def agent_generator_logger() -> None:
    """Generate a logger for the logging of agents produced by an agent generator
    """
    file_path = "application_logging/test_logs/generation_logs/" + "agent_generation_log"
    
    logger = logging.getLogger("agent_generator_logger")
    file_handler = logging.FileHandler(filename=file_path, mode="w")
    file_handler.setLevel(logging.DEBUG)
    logger.addHandler(file_handler)
    
    return logger