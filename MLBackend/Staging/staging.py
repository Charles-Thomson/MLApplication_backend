""""""
from functools import partial
from typing import Generator
from DataFormatting.work_item import WorkItem
from Staging.staged_work_item import StagedWorkItem
from Staging.Environment.Environment_Class import Enviroment

from processing.Agent.agent_generator import agent_generator

# This will eventually work along side a stack of work items to do 

def stage_work_item_for_processing(work_item: WorkItem) -> StagedWorkItem:
    """
    Stage a work item for processing

    Args:
        work_item (WorkItem): A pre formatted work item
    """
    
    new_environment: Enviroment = Enviroment(
        environment_config=work_item.enviroment_config
    ) 
    
    partial_agent_generator: Generator = partial(
        agent_generator,
        neural_network_config=work_item.neural_network_config,
        environment=new_environment,
    )
    
    new_staged_work_item: StagedWorkItem = StagedWorkItem(
        instance_id=work_item.instance_id,
        with_logging=work_item.with_logging,
        partial_agent_generator=partial_agent_generator,
        environment_config = work_item.enviroment_config,
        **work_item.hyper_parameter_config.__dict__
    )
    
    
    
    return new_staged_work_item
