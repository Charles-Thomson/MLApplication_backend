import logging
from django.db import models

class Teacher(models.Model):
    name = models.CharField(max_length=80)
    age = models.IntegerField()


class GenerationalLearningInstanceDataBaseModel(models.Model):
    """ The top level model for a Generational Learning Instance

    Args:
        models (Model): base django models type
        
    Attr:
        instance_id (string): The ID of the Instance 
        number_of_generations (JSON(int)): The number of generation instances relating to the instance 
        
    """
    instance_id = models.CharField(max_length = 200)
    generation_average_fitness_results = models.JSONField(null=True)
    number_of_sucessful_generations = models.IntegerField()
    
    
class GenerationInstanceDataBaseModel(models.Model):
    """Model to store data realting to a generaiton 

    Args:
        models (Model): base django models type
    
    Attr:
        generation_id (string): The ID of the Generation 
        number_of_agents (JSON(int)): The number of agents within the generation
        instance_relation (Obj(GenerationalLearningInstanceDataBaseModel)): The Instance the GenerationInstance belongs to 
    """
    generation_id = models.CharField(max_length = 300)
    number_of_agents = models.IntegerField()
    all_agents_fitness_results = models.JSONField(null=True)
    generation_average_fitness = models.JSONField(null=True)
    relation = models.ForeignKey(GenerationalLearningInstanceDataBaseModel, on_delete=models.CASCADE, related_name="generation_instance")


class BrainInstanceDataBaseModel(models.Model):
    """Model to store data relating to an agent

    Args:
        models (Model): base django models type
        
    Attr:
        brain_id (string): The ID of the Generation
        brain_fitness (float): The Fitness of the brain
        brain_path (JSON(List<(float,float)>)): The path of the brain throung an environment
        brain_fitness_by_step (JSON(List<Float>)): The progression of the fitness per step taken by the brain in the environment
        generation_relation (Obj(GenerationInstance)): The GeneratationInstance the brain belongs to
    """
    brain_id = models.CharField(max_length = 200)
    brain_fitness = models.CharField(max_length = 100)
    brain_path = models.JSONField()
    brain_fitness_by_step = models.JSONField()
    brain_hidden_weights = models.JSONField()
    brain_output_weights = models.JSONField()
    # Need to save the weights
    
    relation = models.ForeignKey(GenerationInstanceDataBaseModel, on_delete=models.CASCADE, related_name="brain_instance")
    
class AlphaBrainInstanceDataBaseModel(models.Model):
    """Model to store data relating to an Alpha agent

    Args:
        models (Model): base django models type
        
    Attr:
        brain_id (string): The ID of the Generation
        brain_fitness (float): The Fitness of the brain
        brain_path (JSON(List<(float,float)>)): The path of the brain throung an environment
        brain_fitness_by_step (JSON(List<Float>)): The progression of the fitness per step taken by the brain in the environment
        generation_relation (Obj(GenerationInstance)): The GeneratationInstance the brain belongs to
    """
    
    brain_id = models.CharField(max_length = 200)
    brain_fitness = models.CharField(max_length = 100)
    brain_path = models.JSONField()
    brain_fitness_by_step = models.JSONField()
    brain_hidden_weights = models.JSONField()
    brain_output_weights = models.JSONField()
    
    generation_relation = models.ForeignKey(GenerationInstanceDataBaseModel, on_delete=models.CASCADE, related_name="generation_relation", null=True)
    instance_relation = models.ForeignKey(GenerationalLearningInstanceDataBaseModel, on_delete=models.CASCADE, related_name="instance_relation", null=True)
    
    
# class InstanceAlphaBrainDataBaseModel(models.Model):
#     """Model to store the Alpha agent of a given GenerationalLearningInstanceDataBaseModel or GenerationInstance 
        

#     Args:
#         models (Model): base django models type
        
#     agent_id (string): The ID of the Generation
#         agent_fitness (float): The Fitness of the agent
#         agent_path (JSON(List<(float,float)>)): The path of the agent throung an environment
#         agent_fitness_by_step (JSON(List<Float>)): The progression of the fitness per step taken by the agent in the environment
#         relation (Obj(GenerationalLearningInstanceDataBaseModel)): The realtion to the GenerationalLearningInstanceDataBaseModel
#     """
#     brain_id = models.CharField(max_length = 200)
#     brain_fitness = models.CharField(max_length = 100)    
#     brain_fitness_by_step = models.JSONField()
#     brain_path = models.JSONField()
#     brain_hidden_weights = models.JSONField()
#     brain_output_weights = models.JSONField()
#     instance_relation = models.OneToOneField("GenerationalLearningInstanceDataBaseModel", on_delete=models.CASCADE,related_name="instance_alpha")
    

# class GenerationAlpahBrainDataBaseModel(models.Model):
#     """Model to store the Alpha agent of a given GenerationalLearningInstanceDataBaseModel or GenerationInstance 
        

#     Args:
#         models (Model): base django models type
        
#         brain_id (string): The ID of the Generation
#         brain_fitness (float): The Fitness of the brain 
#         brain_path (JSON(List<(float,float)>)): The path of the brain throung an environment
#         brain_fitness_by_step (JSON(List<Float>)): The progression of the fitness per step taken by the brain in the environment
#         relation (Obj(GenerationInstance)): The realtion to the GenerationInstance
#     """
#     brain_id = models.CharField(max_length = 200)
#     brain_fitness = models.CharField(max_length = 100)    
#     brain_fitness_by_step = models.JSONField()
#     brain_path = models.JSONField()
#     brain_hidden_weights = models.JSONField()
#     brain_output_weights = models.JSONField()
#     relation = models.OneToOneField("GenerationInstanceDataBaseModel", on_delete=models.CASCADE,related_name="generation_alpha")
#     instance_relation = models.ForeignKey(GenerationalLearningInstanceDataBaseModel, on_delete=models.CASCADE, related_name="alpha_instance", null=True)
    
class GenerationalLearningInstanceEnvironmentDataBaseModel(models.Model):
    """The enviroment of a GenerationalLearningInstanceDataBaseModel

    Args:
        models (Model): base django models type
    Attr: 
        obsticals (JSON(List<(int,int)>)): The location of obsticals in the Environment
        goals (JSON(List<(int,int)>)): The location of goals in the Environment
        start (JSON((int,int))): The start location of the agent in the environment
        environment_map_dimensions (JSON( (int,int))): The size of the enviromnet - as x,y max 
        instance_relation (Obj(GenerationalLearningInstanceDataBaseModel)): The GenerationalLearningInstanceDataBaseModel the environment relates to 
    """
    environment_map = models.JSONField()
    environment_map_dimensions = models.IntegerField(default=0)
    environment_start_coordinates = models.JSONField()
    environment_maximum_action_count = models.IntegerField(default=0)
    relation = models.OneToOneField("GenerationalLearningInstanceDataBaseModel", on_delete=models.CASCADE,related_name="instance_environment")   

    