from django.test import TestCase
from DataBase.ModelFunctions.generational_learning_instance_functions import add_empty_Generational_Learning_Instance_to_data_base, get_Generational_Learning_Instance_from_data_base, get_Generational_Learning_Instance_referanced_environment_and_alpha
from DataBase.ModelFunctions.generation_instance_functions import add_empty_generation_Instance_to_data_base, get_generation_from_data_base_by_id, update_generation_Instance
from DataBase.ModelFunctions.agent_instance_functions import save_agent_to_DB, add_alpha_to_generation_instance, add_alpha_to_leanring_instance
from DataBase.models import GenerationalLearningInstanceDataBaseModel, GenerationInstanceDataBaseModel, GenerationalLearningInstanceEnvironmentDataBaseModel, InstanceAlphaBrainDataBaseModel
from processing.AgentBrain.agent_brain import BrainInstance
import pytest
from DataFormatting.work_item import EnvironmentConfigurationClass
from DataBase.ModelFunctions.environment_instance_functions import add_environment_to_DB
import numpy as np

@pytest.mark.django_db
def test_adding_and_getting_learning_instance():
    test_id: str = "test_instance"
    model_ref = add_empty_Generational_Learning_Instance_to_data_base(instance_id=test_id)
    result = get_Generational_Learning_Instance_from_data_base(instance_id=test_id)
    assert isinstance(result, GenerationalLearningInstanceDataBaseModel)
    
    
@pytest.fixture
def generate_learning_instance_referance():
    test_id: str = "fixture_learning_instance"
    learning_instance_referance: GenerationalLearningInstanceDataBaseModel = add_empty_Generational_Learning_Instance_to_data_base(instance_id=test_id)
    return learning_instance_referance


@pytest.mark.django_db
def test_adding_and_getting_generation_instance(generate_learning_instance_referance):
    
    test_id: str = "test_generation"
    model_ref = add_empty_generation_Instance_to_data_base(generation_id=test_id, referance=generate_learning_instance_referance)
    model_result = get_generation_from_data_base_by_id(generation_id = test_id, instance_ref = generate_learning_instance_referance)



@pytest.fixture
def generate_generation_instance_referance():
    learning_instance_test_id: str = "fixture_learning_instance"
    generation_instance_test_id: str = "fixture_generation_instance"
    
    learning_instance_referance: GenerationalLearningInstanceDataBaseModel = add_empty_Generational_Learning_Instance_to_data_base(instance_id=learning_instance_test_id)
    generation_instance_referance: GenerationInstanceDataBaseModel = add_empty_generation_Instance_to_data_base(generation_id = generation_instance_test_id, referance = learning_instance_referance )
    
    return generation_instance_referance



@pytest.fixture
def dummy_agent_brain() -> BrainInstance:
    """
    Generate a dummy agent brain for testing
    """
    test_brain = BrainInstance(
        brain_id = "test_agent",
        fitness = 1.0,
        brain_type = "test_brain",
        traversed_path = [],
        fitness_by_step = [],
        current_generation_number = 0,
        hidden_weights = np.empty((2,2)),
        output_weights = np.empty((2,2)),
        hidden_layer_activation_function = None,
        output_layer_activation_function = None
    )
    return test_brain


@pytest.fixture
def dummy_environment() -> EnvironmentConfigurationClass:
    """Generate a dummy environmnet for testing
    """
    
    test_environment = EnvironmentConfigurationClass(
        _environment_map =  [1, 2, 3, 4],
        _environment_map_dimensions= 2,
        _environment_start_coordinates= [1, 1],
        _environment_maximum_action_count = 10
    ) 
    
    return test_environment


@pytest.mark.django_db
def test_add_agent_to_data_base(generate_generation_instance_referance, dummy_agent_brain):
    """
    Adda Agent to the Databse using a given genreation referance

    Args:
        generate_generation_instance_referance (GenerationalLearningInstanceDataBaseModel,GenerationInstanceDataBaseModel ): Generation Referance
    """
    save_agent_to_DB(brain = dummy_agent_brain , generation_referance = generate_generation_instance_referance)
    
    
    
@pytest.mark.django_db
def test_add_alpha_to_genertion_instance(dummy_agent_brain, generate_generation_instance_referance ) -> None:
    """
    Add a barin instance as an Alpha to a Generation Instance
    """
    add_alpha_to_generation_instance(alpha_brain=dummy_agent_brain, generation_referance=generate_generation_instance_referance)
    
    
@pytest.mark.django_db
def test_add_alpha_to_learning_instance(dummy_agent_brain, generate_learning_instance_referance ) -> None:
    """
    Add a barin instance as an Alpha to a Learning Instance
    """
    
    add_alpha_to_leanring_instance(alpha_brain= dummy_agent_brain, learning_instance_referance=generate_learning_instance_referance)

    
@pytest.mark.django_db
def test_add_environment_to_db(generate_learning_instance_referance, dummy_environment):
    """Add an environment instance to the Database

    Args:
        generate_learning_instance_referance (GenerationalLearningInstanceDataBaseModel): Learning instance referance 
        dummy_environment (EnvironmentConfigurationClass): Environment for testing
    """
    
    add_environment_to_DB(environment_data = dummy_environment, learning_instance_referance = generate_learning_instance_referance)
    
@pytest.mark.django_db
def test_adding_and_getting_enviornmnet_and_alpha_from_instance(generate_learning_instance_referance, dummy_environment,dummy_agent_brain ):
    """
    Associate a Environment and Instance alpha with an instance, then get back via the learning instance ref

    Args:
        generate_learning_instance_referance (_type_): _description_
    """
    add_environment_to_DB(environment_data=dummy_environment, learning_instance_referance=generate_learning_instance_referance)
    add_alpha_to_leanring_instance(alpha_brain=dummy_agent_brain, learning_instance_referance=generate_learning_instance_referance)
    instance_data = get_Generational_Learning_Instance_referanced_environment_and_alpha(instance_id=generate_learning_instance_referance.instance_id)
    assert(isinstance(instance_data.instance_alpha, InstanceAlphaBrainDataBaseModel))
    assert(isinstance(instance_data.instance_environment, GenerationalLearningInstanceEnvironmentDataBaseModel))
    
    
@pytest.mark.django_db
def test_updating_database_generation_instance(generate_generation_instance_referance):
    """Test the updating of a generation instance in the database
    """
    
    update_generation_Instance(referance="fixture_generation_instance", number_of_agents=22)
    
    