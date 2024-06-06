import pytest
from DataFormatting.work_item_data_formatting import format_work_item_json_to_work_item

from DataFormatting.work_item import WorkItem
import json

from DataBase.models import GenerationalLearningInstanceDataBaseModel
from Staging.staged_work_item import StagedWorkItem
from Staging.staging import stage_work_item_for_processing


from processing.instance_processing import ProcessInstance

@pytest.fixture
def new_dummy_work_item_json() -> json:
    """
    Dummy JSON for testing
    """
    
    return """{
    "instance_id": "instance_5",
    "environment_configuration": {
        "_environment_map": [1,1,1,1,1,3,1,2,3,1,1,1,2,1,1,3,1,2,3,3,3,1,3,1,3],
        "_environment_map_dimensions": 5,
        "_environment_start_coordinates": [1, 1],
        "_environment_maximum_action_count": 10
    },
    "hyper_parameter_configuration": {
        "_maximum_number_of_genrations": 20,
        "_maximum_generation_size": 100,
        "_starting_fitness_threshold": 1.2,
        "_start_new_generation_threshold": 10,
        "_generation_failure_threshold": 2.0
    },
    "neural_network_configuration": {
        "_weight_init_huristic": "he_weight",
        "_hidden_activation_function_ref": "linear_activation_function",
        "_output_activation_function_ref": "argmax_activation",
        "_new_generation_creation_function_ref": "crossover_weights_average",
        "_input_to_hidden_connections": [24, 9],
        "_hidden_to_output_connections": [9, 9]
    }
    }"""

@pytest.fixture
def new_dummy_work_item(new_dummy_work_item_json) -> WorkItem:
    """Work item with data assigned
    """
    work_item = format_work_item_json_to_work_item(work_item_configuration=new_dummy_work_item_json)
    return work_item

@pytest.fixture
def dummy_staged_work_item(new_dummy_work_item)-> StagedWorkItem:
    """Stage a dummy work item

    Args:
        new_dummy_work_item (work_item): Formatted work_item ready to be staged

    Returns:
        StagedWorkItem: Staged work item
    """
    
    dummy_staged_work_item = stage_work_item_for_processing(work_item = new_dummy_work_item)
    return dummy_staged_work_item
    

@pytest.mark.django_db
def test_full_instance_run(dummy_staged_work_item):
    """
    Test running a full instance
    """
    
    testing_instance = ProcessInstance(staged_work_item = dummy_staged_work_item)
    
    # Get the environment and Instance Alpha 
    ref = testing_instance.instance_database_reference
    instance = GenerationalLearningInstanceDataBaseModel.objects.prefetch_related(
            "instance_alpha", "instance_environment"
        ).get(instance_id=ref.instance_id)
    
    