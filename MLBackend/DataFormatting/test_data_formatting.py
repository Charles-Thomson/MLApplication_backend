import pytest 
import json
# Create your tests here.
from DataFormatting.work_item import EnvironmentConfigurationClass, WorkItem, HyperParameterConfigurationClass, NeuralNetworkConfigurationClass
from DataFormatting.work_item_data_formatting import format_work_item_json_to_work_item

@pytest.fixture
def dummy_work_item_json() -> json:
    """
    Dummy JSON for testing
    """
    
    return """{
    "instance_id": "instance_4",
    "environment_configuration": {
        "_environment_map": [1, 2, 3, 4],
        "_environment_map_dimensions": 2,
        "_environment_start_coordinates": 0,
        "_environment_maximum_action_count": 10
    },
    "hyper_parameter_configuration": {
        "_maximum_number_of_genrations": 1,
        "_maximum_generation_size": 1,
        "_starting_fitness_threshold": 1.2,
        "_start_new_generation_threshold": 1,
        "_generation_failure_threshold": 1
    },
    "neural_network_configuration": {
        "_weight_init_huristic": "a",
        "_hidden_activation_function_ref": "a",
        "_output_activation_function_ref": "a",
        "_new_generation_creation_function_ref": "a",
        "_input_to_hidden_connections": [1, 1],
        "_hidden_to_output_connections": [2, 2]
    }
    }"""
    
@pytest.fixture
def dummy_work_item(dummy_work_item_json) -> WorkItem:
    """Work item with data assigned
    """
    work_item = format_work_item_json_to_work_item(work_item_configuration=dummy_work_item_json)
    return work_item

def test_work_item_class_types(dummy_work_item: WorkItem):
    """
    Test the setting of the environment Config Class
    """
    assert(isinstance(dummy_work_item.enviroment_config, EnvironmentConfigurationClass))
    assert(isinstance(dummy_work_item.hyper_parameter_config, HyperParameterConfigurationClass))
    assert(isinstance(dummy_work_item.neural_network_config, NeuralNetworkConfigurationClass))