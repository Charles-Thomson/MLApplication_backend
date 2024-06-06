import json

import jsonpickle

from DataBase.models import GenerationalLearningInstanceDataBaseModel
from django.core.exceptions import ObjectDoesNotExist




def add_Generational_Learning_Instance_to_data_base():
    """
    Create and add a GenerationalLearningInstanceDataBaseModel to the Database
    """

    new_model: GenerationalLearningInstanceDataBaseModel = GenerationalLearningInstanceDataBaseModel(
        instance_id = "saved_instance_3",
        number_of_sucessful_generations = 0
    )
    
    new_model.save()
    
    print("Model Saved")
    
    get_Generational_Learning_Instance_from_data_base()
    
    return new_model # Need to get the referance



def add_empty_Generational_Learning_Instance_to_data_base(instance_id: str) -> GenerationalLearningInstanceDataBaseModel:
    """
    Create and add a GenerationalLearningInstanceDataBaseModel to the Database
    """

    new_model: GenerationalLearningInstanceDataBaseModel = GenerationalLearningInstanceDataBaseModel(
        instance_id = instance_id,
        number_of_sucessful_generations = 0
    )
    
    new_model.save()
    
    return new_model 


def get_Generational_Learning_Instance_from_data_base(instance_id: str):
    """
        Get the model from the DB 
    """
    
    learing_instance_model: GenerationalLearningInstanceDataBaseModel = GenerationalLearningInstanceDataBaseModel.objects.get(
        instance_id=instance_id
    )
    
    return learing_instance_model

def get_Generational_Learning_Instance_referanced_environment_and_alpha(instance_id: str):
    """Gthe the Environment and Instance Alpha Brain for a Learning instance for the DB 

    Args:
        instance_id (str): ID of the learning instance

    Returns:
        instance (GenerationalLearningInstanceDataBaseModel): The learning instance with the Environment and Alpha Brain
    """
    instance = GenerationalLearningInstanceDataBaseModel.objects.prefetch_related(
            "instance_alpha", "instance_environment"
        ).get(instance_id=instance_id)

    return instance

def update_generational_learning_instance(instance_id: str, number_of_sucessful_generations: int, generation_average_fitness_values: list[float]):
    """Update the learning instance with the number of sucessful generations

    Args:
        instance_id (str): The id of the Instance
        number_of_sucessful_generations (int): NUmber of "Sucessful" generations in the instance
    """
    try:
        learning_instance = GenerationalLearningInstanceDataBaseModel.objects.get(instance_id=instance_id)
        
    except ObjectDoesNotExist:
        return  ObjectDoesNotExist(f"Learning instance with reference ID {instance_id} not found.")
    
    learning_instance.number_of_sucessful_generations = number_of_sucessful_generations
    learning_instance.generation_average_fitness_results = generation_average_fitness_values
    
    
    learning_instance.save(update_fields=["number_of_sucessful_generations","generation_average_fitness_results"])