from copy import deepcopy
import logging
from typing import Generator
from processing.Agent.agent import Agent
from DataFormatting.work_item import HyperParameterConfigurationClass
from processing.AgentBrain.agent_brain_factory import BrainFactory

def agent_generator(
    parents: list,
    
    instance_id: str,
    neural_network_config: HyperParameterConfigurationClass,
    environment: object,
    max_generation_size: int,
    current_generation_number: int,
) -> Generator:
    """ Generator for Agent
        Args:
            var: parents (List<BrainInstance>) 
            var: instance_id (string) - base learning instance ID
            var: brain_config (dict) - Configuration of the brain instances
            var: environment (obj) - Instance environtment
            var: max_generation_size (int) - Max number of generations
            var: current_generation_number (int) - current generation in the instance
        return:
            Generator (obj): yields a new agent when called
    """
    general_system_logger = logging.getLogger("general_system_logger")
    general_system_logger.info(f"GENERATOR - New Generator for generation : {current_generation_number} ")
        
    for instance_in_generation in range(int(max_generation_size)):
        # general_system_logger.info(f"GENERATOR - INISTANCE : {instance_in_generation} ")
        
        new_brain_type = "random_weighted_brain" if current_generation_number == 0 else "generational_weighted_brain"
        # general_system_logger.info(f"GENERATOR - Brain Type : {new_brain_type} ")
        
        new_brain_id = f"{instance_id}-{current_generation_number}-{instance_in_generation}"
        # general_system_logger.info(f"GENERATOR - Brain ID : {new_brain_id} ")

        agent_brain: object = BrainFactory.make_brain(
            neural_network_config = neural_network_config,
            brain_type = new_brain_type,
            brain_id = new_brain_id,
            parents=parents
        )
        
        
        
        agent: Agent = Agent(
             agent_brain = agent_brain, environment=deepcopy(environment)
        )
        
        
        yield agent