# import pytest
# import json

# from DataFormatting.work_item_data_formatting import format_work_item_json_to_work_item

# from DataFormatting.work_item import WorkItem

# from Staging.staged_work_item import StagedWorkItem
# from Staging.staging import stage_work_item_for_processing

# @pytest.fixture
# def new_dummy_work_item_json() -> json:
#     """
#     Dummy JSON for testing
#     """
    
#     return """{
#     "instance_id": "instance_4",
#     "environment_configuration": {
#         "_environment_map": [1, 2, 3, 4],
#         "_environment_map_dimensions": 2,
#         "_environment_start_coordinates": [1, 1],
#         "_environment_maximum_action_count": 10
#     },
#     "hyper_parameter_configuration": {
#         "_maximum_number_of_genrations": 1,
#         "_maximum_generation_size": 1,
#         "_starting_fitness_threshold": 1.2,
#         "_start_new_generation_threshold": 1,
#         "_generation_failure_threshold": 1
#     },
#     "neural_network_configuration": {
#         "_weight_init_huristic": "a",
#         "_hidden_activation_function_ref": "a",
#         "_output_activation_function_ref": "a",
#         "_new_generation_creation_function_ref": "a",
#         "_input_to_hidden_connections": [1, 1],
#         "_hidden_to_output_connections": [2, 2]
#     }
#     }"""

     
# @pytest.fixture
# def new_dummy_work_item(new_dummy_work_item_json) -> WorkItem:
#     """Work item with data assigned
#     """
#     work_item = format_work_item_json_to_work_item(work_item_configuration=new_dummy_work_item_json)
#     return work_item


# @pytest.fixture
# def dummy_staged_work_item(new_dummy_work_item)-> StagedWorkItem:
#     """Stage a dummy work item

#     Args:
#         new_dummy_work_item (work_item): Formatted work_item ready to be staged

#     Returns:
#         StagedWorkItem: Staged work item
#     """
    
#     dummy_staged_work_item = stage_work_item_for_processing(work_item = new_dummy_work_item)
#     return dummy_staged_work_item
    