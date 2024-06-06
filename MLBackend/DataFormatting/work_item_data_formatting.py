import json
import logging

import numpy as np
from DataFormatting.work_item import EnvironmentConfigurationClass, HyperParameterConfigurationClass, NeuralNetworkConfigurationClass, WorkItem

def format_work_item_json_to_work_item(work_item_configuration: json):
    """Format the work_item_configuration into the defined work item class structure

    Args:
        work_item_configuration (json): new work item raw config data from API
    """
    
    general_system_logger = logging.getLogger("general_system_logger")
    general_system_logger.info(f"In the data formatting")
    
    unpacked_work_item_configuration = json.loads(work_item_configuration)
    general_system_logger.info(f"JSON LOADED")
    
    environment_config_dict: dict = unpacked_work_item_configuration["environment_configuration"]
    general_system_logger.info(f"Environment Unpacked")
    
    hyper_parameter_config_dict: dict = unpacked_work_item_configuration["hyper_parameter_configuration"]
    general_system_logger.info(f"Hyper Parameters Unpckacked")
    
    neural_network_config_dict: dict = unpacked_work_item_configuration["neural_network_configuration"]
    general_system_logger.info(f"Neural Network Unpacked")
    
    
    environment_config = EnvironmentConfigurationClass(**environment_config_dict)
    general_system_logger.info(f"Environment config assigned")
    
    hyper_parameter_config = HyperParameterConfigurationClass(**hyper_parameter_config_dict)
    general_system_logger.info(f"Hyper Paramter config assigned")
    
    neural_network_config = NeuralNetworkConfigurationClass(**neural_network_config_dict)
    general_system_logger.info(f"Neural Network config assigned")
    general_system_logger.info(f"NEURAL NETWORK CONFIG - New Generationfunc {neural_network_config.new_generation_creation_function} ")
    
    general_system_logger.info(f"Assigned to classes")
   
    new_work_item: WorkItem = WorkItem(
        instance_id=unpacked_work_item_configuration["instance_id"],
        enviroment_config=environment_config,
        hyper_parameter_config=hyper_parameter_config,
        neural_network_config=neural_network_config
        )
    general_system_logger.info(f"Work Item Created ")
    
    return new_work_item
    