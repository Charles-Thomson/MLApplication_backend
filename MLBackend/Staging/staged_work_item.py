"""Doc string """
from typing import Generator
from dataclasses import dataclass
from DataFormatting.work_item import EnvironmentConfigurationClass


@dataclass
class StagedWorkItem:
    """A staged work Item that is ready for processing"""

    instance_id: str = None
    with_logging: bool = False
    partial_agent_generator: Generator = None
    environment_config: EnvironmentConfigurationClass = None
    
    _maximum_number_of_genrations: int = None
    _maximum_generation_size: int = None
    _starting_fitness_threshold: float = None
    _start_new_generation_threshold: int = None
    _generation_failure_threshold: int = None
    
    

