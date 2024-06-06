import logging
import datetime
import os

# Basic logging config
logging.root.setLevel(logging.NOTSET)
logging.basicConfig(level=logging.NOTSET)

DEFAULT_FORMAT = "%(levelname)s :: %(funcName)s :: %(message)s"

class LoggerGeneratorClass:
    """
    Class for the generation of loggers 
    
    Args:
        instace_id (str): The insatnce the loggers are being generated for
    
    """
    
    def __init__(self, instance_id: str):
        self.instance_id = instance_id
        self.base_file_path = self.generate_base_file_path()
        self.generate_file_structure()
        self.generate_loggers()
        
    
    def generate_base_file_path(self) -> str:
        """Genertae the path to the file location where logs will be stored 

        Args:
            instance_id (str): Instance id

        Returns:
            (str): File path to logs
        """
        return "application_logging/logs/instance_logging/" + self.instance_id + "_logs"
        
    def generate_file_structure(self) -> None:
        """
        Generate the file structure for the loggs, this will be a dir containing the instance_id
        """
        directroys: list[str] = ["/instance_data", "/generation_data", "/agents_by_generation_data", "/run_time"]
    
        if not os.path.exists(self.base_file_path):
            os.mkdir(self.base_file_path)
            
        for directroy in directroys:
            full_file_path: str = self.base_file_path + directroy
            if not os.path.exists(full_file_path):
                os.makedirs(full_file_path)
        
    def generate_loggers(self):
        """
        Generate loggers
        """
        
        instance_logger_file_path =  self.base_file_path + "/instance_data/" + self.instance_id
        generation_logger_file_path = self.base_file_path + "/generation_data/" + self.instance_id
        agent_logger_file_path = self.base_file_path + "/agents_by_generation_data/" + self.instance_id
        run_time_logger_file_path = self.base_file_path + "/run_time/" + self.instance_id
        
        instance_logger_name = self.instance_id + "_instance_logger"
        generation_logger_name = self.instance_id + "_generation_logger"
        run_time_logger_name = self.instance_id + "_run_time_logger"
        agent_logger_name = self.instance_id + "_agent_logger"
        
        to_be_generated: list[tuple[str, str]] = [
        (instance_logger_file_path, instance_logger_name),
        (generation_logger_file_path, generation_logger_name),
        (run_time_logger_file_path, run_time_logger_name),
        (agent_logger_file_path, agent_logger_name)
    ]
        
        for item in to_be_generated:
            logger = logging.getLogger(item[1])
            file_handler = logging.FileHandler(item[0], mode="w")
            file_handler.setLevel(logging.DEBUG)  
            formatter = logging.Formatter(DEFAULT_FORMAT)
            file_handler.setFormatter(formatter)
            logger.addHandler(file_handler)
            
            
            
            
            
        