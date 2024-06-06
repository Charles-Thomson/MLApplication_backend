import logging
from DataBase.models import  GenerationInstanceDataBaseModel,  BrainInstanceDataBaseModel, AlphaBrainInstanceDataBaseModel
from processing.AgentBrain.agent_brain import BrainInstance
import json


def save_agent_to_DB(brain: BrainInstance, generation_referance: GenerationInstanceDataBaseModel):
    """Ad a agent instance to the Data base with the FK referance of a GenerationModel

    Args:
        generation_referance (GenerationInstanceDataBaseModel - Forign Key): The generation the Agent belongs to 
    """
    
    new_model: BrainInstanceDataBaseModel = BrainInstanceDataBaseModel(
            brain_id = brain.brain_id,
            brain_fitness = brain.fitness,
            brain_path = brain.traversed_path,
            brain_fitness_by_step = brain.fitness_by_step,
            brain_hidden_weights = json.dumps(brain.hidden_weights.tolist()),
            brain_output_weights = json.dumps(brain.output_weights.tolist()),
            relation = generation_referance
    )
    
    new_model.save()
    

    
def add_new_alpha_brain(alpha_brain: BrainInstance, generation_referance: GenerationInstanceDataBaseModel, instance_relation: GenerationInstanceDataBaseModel):
    """
    Add a new alpha brain with the given generation and instance relations 

    Args:
        alpha_brain (BrainInstance): The highest fitness brain of the gernation
        generation_referance (GenerationInstanceDataBaseModel): The referance to the generation
    """
    general_system_logger = logging.getLogger("general_system_logger")
    general_system_logger.info(f"ADDING NEW ALPHA BRAIN")
    new_model: AlphaBrainInstanceDataBaseModel = AlphaBrainInstanceDataBaseModel(
            brain_id = alpha_brain.brain_id,
            brain_fitness = alpha_brain.fitness,
            brain_path = alpha_brain.traversed_path,
            brain_fitness_by_step = alpha_brain.fitness_by_step,
            brain_hidden_weights = json.dumps(alpha_brain.hidden_weights.tolist()),
            brain_output_weights = json.dumps(alpha_brain.output_weights.tolist()),
            generation_relation = generation_referance,
            instance_relation = instance_relation
    )
    
    new_model.save()
