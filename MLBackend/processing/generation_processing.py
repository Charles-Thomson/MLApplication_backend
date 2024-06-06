import heapq

import logging
from typing import Generator
from functools import partial

from processing.agent_processing import ProcessAgent
from processing.AgentBrain.agent_brain import BrainInstance

from application_logging.logging_functions.logger_decorators import generation_instance_attribute_logger

from DataBase.ModelFunctions.agent_instance_functions import save_agent_to_DB
from DataBase.ModelFunctions.generation_instance_functions import add_empty_generation_Instance_to_data_base, update_generation_Instance


class ProcessGeneration:
    """
    Process a generation from a Generation Learning Instance
    """
    def __init__(self
                 , instanceId: str
                 ,agent_generator: Generator
                 , current_generation_number: int
                 , fitness_threshold: float
                 , logging_variables: dict
                 , instance_database_reference ):
        
        self.instanceId:str = instanceId
        
        self.logging_variables: dict = logging_variables
        self.agent_generator: Generator = agent_generator
        self.fitness_threshold: float = fitness_threshold
        self.current_generation_number: int  = current_generation_number
        
        self.generation_alpha_brain: BrainInstance = None 
        self.agent_brains_post_run: list[BrainInstance] = []
        self.generation_top_fitness_brains: heapq[BrainInstance] = []
        self.agent_fintess_values: list[float] = []
        
        self.number_of_agents: int = 0
        self.average_fitness_across_generation: float = 0.0
        
        self.general_system_logger = logging.getLogger("general_system_logger")
        
        self.is_generation_sucessful: bool = False
        
        self.generation_id: str = f"{instanceId}_{current_generation_number}"
        self.generation_database_reference = add_empty_generation_Instance_to_data_base(generation_id=self.generation_id, 
                                                                                        referance=instance_database_reference )
        
        
    @generation_instance_attribute_logger
    def process_generation(self, logging_variables: dict) -> None:
        """
        Process the gernation one agent at at a time, tacking highest fitness through the use of a heap
        """
        self.general_system_logger.info(f"PROCESSING GENERATION - Num : {self.current_generation_number} ")
        self.general_system_logger.info(f"PROCESSING GENERATION - Agent Generator: {next(self.agent_generator)} ")
        
        for agent in self.agent_generator:
            # self.general_system_logger.info(f"PROCESSING GENERATION - New agent from generator")
            
            processed_agent = ProcessAgent(agent=agent, logging_variables=self.logging_variables)
            # self.general_system_logger.info(f"New Agent Processing object created")
            
            
            processed_agent.process_agent(logging_variables=logging_variables)
            # self.general_system_logger.info(f"Agent Processed")
            
            self.agent_fintess_values.append(processed_agent.agent_brain_post_run.fitness)
            
            self.push_brain_to_heap(processed_agent.agent_brain_post_run)
            self.agent_brains_post_run.append(processed_agent.agent_brain_post_run)
            
        # self.general_system_logger.info(f"GENERATION Num : {self.current_generation_number} - Agent processing complete")
        
        self.number_of_agents = len(self.agent_brains_post_run)
        
        self.set_generation_top_fitness_brains()
        
        self.generation_alpha_brain = self.generation_top_fitness_brains[0]
        
        self.check_generation_success()
        self.save_agents_to_data_base()
        self.calculate_generation_average_fitness()
        
        update_generation_Instance(referance=self.generation_id, 
                                   number_of_agents=self.number_of_agents, 
                                   agent_fintess_values=self.agent_fintess_values,
                                   generation_average_fitness = self.average_fitness_across_generation
                                   )
        
        # self.general_system_logger.info(f"GENERATION Num : {self.current_generation_number} - Data Updated")
        
        
        
        
    def calculate_generation_average_fitness(self):
        """Calculate the avergae fitness across the generation
        """
        total_fitness = sum(agent.fitness for agent in self.agent_brains_post_run)
        self.average_fitness_across_generation = total_fitness / self.number_of_agents
        
        
    def save_agents_to_data_base(self):
        """Save the post run agent brains to the Database

        Args:
            generation_database_reference (_type_): The gernation the Agent Brains are associated with
            agent_brains_post_run (list[BrainInstance]): List of the Agent brains
        """
        self.general_system_logger.info(f"Saving Brain instances - Generation ref {self.generation_database_reference}")
        # partial_save_agent: callable = partial(save_agent_to_DB, generation_referance=self.generation_database_reference)
        # map(partial_save_agent, self.agent_brains_post_run)
        
        for x in self.agent_brains_post_run:
            self.general_system_logger.info(f"Agent Being Saved: {x.brain_id}")
            save_agent_to_DB(brain=x , generation_referance=self.generation_database_reference)
        
        
        
    def push_brain_to_heap(self, brain_instance: BrainInstance) -> None:
        """Push a new BrainINstance to the heap

        Args:
            post_run_agent_brain (BrainInstance): Newly processed BrainInstance
        """
        
        heapq.heappush(self.generation_top_fitness_brains, (brain_instance.fitness, brain_instance))
            
        if len(self.generation_top_fitness_brains) > 10:
            heapq.heappop(self.generation_top_fitness_brains)
            
    def set_generation_top_fitness_brains(self):
        """
        Set the generation_top_fitness_brains variable by ordering the remaining brains in the heap
        """
        self.generation_top_fitness_brains = [brain for _, brain in sorted(self.generation_top_fitness_brains, reverse=True)]
        
    def check_generation_success(self) -> None:
        """Check if a generation is sucessful
        """
        if self.generation_top_fitness_brains[-1].fitness >= float(self.fitness_threshold):
            self.is_generation_sucessful = True