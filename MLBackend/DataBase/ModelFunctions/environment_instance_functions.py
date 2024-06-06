import json
import logging
from DataBase.models import GenerationalLearningInstanceEnvironmentDataBaseModel, GenerationalLearningInstanceDataBaseModel
from DataFormatting.work_item import EnvironmentConfigurationClass



def add_environment_to_DB(environment_data: EnvironmentConfigurationClass, learning_instance_referance: GenerationalLearningInstanceDataBaseModel) -> None:
    """Add the Environment to the database 

    Args:
        environment_data (_type_): The environment data
        learning_instance_referance () : THe leraning instance the Environment is associated with
    """
    
    general_system_logger = logging.getLogger("general_system_logger")
    general_system_logger.info(f"GENERATIONAL WEIGHTED BRAIN")
    
    new_model: GenerationalLearningInstanceEnvironmentDataBaseModel = GenerationalLearningInstanceEnvironmentDataBaseModel(
        environment_map = environment_data.environment_map.tolist(),
        environment_map_dimensions = environment_data.environment_map_dimensions,
        environment_start_coordinates = environment_data.environment_start_coordinates,
        environment_maximum_action_count = environment_data.environment_maximum_action_count,
        relation = learning_instance_referance
    )
    
    general_system_logger = logging.getLogger("general_system_logger")
    general_system_logger.info(f" ****** SAVING ENV START COORDS AS {json.dumps(environment_data.environment_map_dimensions)} ******")
    
    new_model.save()