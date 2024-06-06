import json
from DataBase.models import GenerationInstanceDataBaseModel, GenerationalLearningInstanceDataBaseModel
from django.core.exceptions import ObjectDoesNotExist


def add_generation_instance_to_DB(referance: GenerationalLearningInstanceDataBaseModel):
    
    new_model: GenerationInstanceDataBaseModel = GenerationInstanceDataBaseModel(generation_id = "genneration_0",
                                                                                 number_of_agents = 1, 
                                                                                 relation =  referance)
    
    
    new_model.save()
    
    print("Generation saved")
    
    
def add_empty_generation_Instance_to_data_base(generation_id: str, referance: GenerationalLearningInstanceDataBaseModel) -> GenerationalLearningInstanceDataBaseModel:
    """
    Create and add a GenerationalLearningInstanceDataBaseModel to the Database
    """

    new_model: GenerationInstanceDataBaseModel = GenerationInstanceDataBaseModel(
        generation_id = generation_id,
        number_of_agents = 0,
        relation = referance
    )
    
    new_model.save()
    
    return new_model

def update_generation_Instance(referance: str, number_of_agents: int, agent_fintess_values: list[float] ,generation_average_fitness: float):
    """Update the number_of_agents field of a given generation instances

    Args:
        referance (GenerationInstanceDataBaseModel): The Generation INstance to be updated
        number_of_agents (int): The number of agents 
    """
    try:
        generation_instance = GenerationInstanceDataBaseModel.objects.get(generation_id=referance)
        
    except ObjectDoesNotExist:
        return  ObjectDoesNotExist(f"Generation instance with reference ID {referance} not found.")
    
    
    generation_instance.number_of_agents = number_of_agents
    generation_instance.all_agents_fitness_results = agent_fintess_values
    generation_instance.generation_average_fitness = generation_average_fitness
    generation_instance.save(update_fields=["number_of_agents","all_agents_fitness_results", "generation_average_fitness"])
    
    
def get_generation_from_data_base_by_id(generation_id: object, instance_ref: object):
    """Get a generation instance form the database using a given ID

    Args:
        instance_id (str): Learning Instance ID
        generation_id (str): Generation Instance ID
    """
    
    full_instance = GenerationalLearningInstanceDataBaseModel.objects.get(
            instance_id= instance_ref.instance_id
        )
    
    generation = full_instance.generation_instance.get(generation_id= generation_id)
    return generation

