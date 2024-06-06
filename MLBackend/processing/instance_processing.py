
import logging
from typing import Generator

from Staging.staged_work_item import StagedWorkItem

from processing.AgentBrain.agent_brain import BrainInstance
from processing.generation_processing import ProcessGeneration

from application_logging.logging_functions.logger_generator_class import LoggerGeneratorClass
from application_logging.logging_functions.logger_decorators import learning_instance_attribute_logger, with_process_Instance_logging

from DataBase.ModelFunctions.environment_instance_functions import add_environment_to_DB

from DataBase.ModelFunctions.generational_learning_instance_functions import add_empty_Generational_Learning_Instance_to_data_base, update_generational_learning_instance
from DataBase.ModelFunctions.agent_instance_functions import add_new_alpha_brain



class ProcessInstance:
    """
    Process the generation learning instance 
    """
    
    def __init__(self, staged_work_item: StagedWorkItem):
        self.staged_work_item = staged_work_item
        self.work_item = staged_work_item
        self.instance_id = staged_work_item.instance_id
        self.logging_variables = [self.instance_id, 
                                  staged_work_item.with_logging
                                  ]
        
        self.sucessful_generations_count: int = 0
        self.instance_alpha_brain: BrainInstance = None 
        self.next_generation_parents : list[BrainInstance] = []
        self.fitness_threshold: float = self.work_item._starting_fitness_threshold
        
        self.generation_average_fitness_values: list[float] = []
        
        if staged_work_item.with_logging:
            _ = LoggerGeneratorClass(instance_id=self.instance_id)

        self.instance_database_reference = None
        
        self.general_system_logger = logging.getLogger("general_system_logger")
        
        
    def AddBaseLearningInstanceToDB(self):
        self.instance_database_reference = add_empty_Generational_Learning_Instance_to_data_base(self.instance_id)
        
        
        
        
    def AddEnvironmentToDB(self):
        add_environment_to_DB(environment_data=self.staged_work_item.environment_config, learning_instance_referance=self.instance_database_reference)
        
        
        
    @with_process_Instance_logging
    def process_instance(self, logging_variables) -> None:
        """Process the learning Instance

        Args:
            logging_variables (dict): Variable relating to data logging
        """
        self.general_system_logger.info(f"Start Of Processing Function ")
        self.AddBaseLearningInstanceToDB()
        self.AddEnvironmentToDB()
        
        self.general_system_logger.info(f"Starting Processing : ")
        self.general_system_logger.info(f"max num generations type {type(self.work_item._maximum_number_of_genrations)}")
        
        for current_generation_number in range(int(self.work_item._maximum_number_of_genrations)):
            self.general_system_logger.info(f"INSATNCE PROCESSING - NEW GENERATION - {current_generation_number}")
            
            agent_generator: Generator = self.get_agent_generator(next_generation_parents=self.next_generation_parents,
                                    current_generation_number=current_generation_number)
            
            self.general_system_logger.info(f"INSATNCE PROCESSING - Agent Generator {next(agent_generator)}")
            
            
            generation_instance = ProcessGeneration(
                            instanceId=self.instance_id,
                            agent_generator=agent_generator,
                            current_generation_number=current_generation_number,
                            fitness_threshold=self.fitness_threshold, 
                            logging_variables=self.logging_variables, 
                            instance_database_reference=self.instance_database_reference )
            
            self.general_system_logger.info(f"NEW GENERATION : Num : {current_generation_number}")
            
            generation_instance.process_generation(logging_variables=logging_variables)
            
            self.general_system_logger.info(f"Generation Instance Finished Processing")
            
            generation_alpha_brain = generation_instance.generation_alpha_brain
            
            add_new_alpha_brain(alpha_brain=generation_instance.generation_alpha_brain,
                                generation_referance = generation_instance.generation_database_reference,
                                instance_relation = self.instance_database_reference)
            
            self.update_instance_alpha_brain(potential_alpha_brain=generation_alpha_brain)
            
            if generation_instance.is_generation_sucessful is False:
                break
            
            self.sucessful_generations_count += 1
            self.next_generation_parents = generation_instance.generation_top_fitness_brains
            self.fitness_threshold = self.generate_new_fitness_threshold(self.next_generation_parents)
            self.generation_average_fitness_values.append(generation_instance.average_fitness_across_generation)
       
       
        # add_alpha_to_leanring_instance(alpha_brain=self.instance_alpha_brain, 
        #                                learning_instance_referance=self.instance_database_reference)
        
        
        update_generational_learning_instance(instance_id=self.instance_id, 
                                              number_of_sucessful_generations = self.sucessful_generations_count,
                                              generation_average_fitness_values=self.generation_average_fitness_values)
        
        
    
        
    def update_instance_alpha_brain(self, potential_alpha_brain: BrainInstance) -> None:
        """Determine if a new brain is a more appropriate Instance Alpha based on the Fitness attribute
    
        Args:
            alpha_brain (): Potential new alpha brain 
        """
        if self.instance_alpha_brain is None or potential_alpha_brain.fitness > self.instance_alpha_brain.fitness:
                self.instance_alpha_brain = potential_alpha_brain
        
    def get_agent_generator(self, next_generation_parents: list[BrainInstance], current_generation_number: int) -> Generator:
        """Return the completed agent generator

        Args:
            parents (list[BrainInstance]): Highest achiving BrainINstance From previous generation
            current_generation_number (int): Current generation
            
        Return:
            agent_generator (Generator): Complete generator for Agent Objects
        """
        agent_generator: Generator = self.work_item.partial_agent_generator(
                instance_id = self.instance_id,
                parents = next_generation_parents,
                max_generation_size = self.work_item._maximum_generation_size,
                current_generation_number = current_generation_number,
            )
        return agent_generator
    
    def generate_new_fitness_threshold(self, next_generation_parents: list[BrainInstance]) -> float:
        """
        Generatre a new fitness threshold based on the avergae fitness of 
        a given set of BrainInstances. Average fitness is taken then 10% is added.

        Args:
            next_generation_parents (list[BrainInstance]): List of Brain Instances
            
        return:
            new_fitness_threshold (float): The new fitness threshold
        """
        
        if not next_generation_parents:
            return 0.0
        
        average_fitness: float = sum(instance.fitness for instance in next_generation_parents) / len(next_generation_parents)
       
        return average_fitness + (average_fitness / 100) * 10
    
    
    
