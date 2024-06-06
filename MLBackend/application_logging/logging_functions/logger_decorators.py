import datetime
from functools import wraps
import logging
import time
from datetime import datetime, timedelta

def learning_instance_attribute_logger(func):
    
    
    @wraps(func)
    def process_instance_wrapper(*args, **kwargs ):
        instance = args[0]
        logging_variables = kwargs.get("logging_variables")
        instance_id, with_logging = logging_variables
        if with_logging:
            run_time_logger = logging.getLogger(instance_id + "_run_time_logger")
            
            start_time = datetime.now()
            
            run_time_logger.info(f"Instance: {instance_id} - Start Time: {start_time}")
            
            func(*args, **kwargs)
            
            end_time = datetime.now()
            
            run_time_logger.info(f"Instance: {instance_id} - Completion Time: {end_time} - Total run Time: {end_time - start_time}")
            
            sucessful_generations_count = instance.sucessful_generations_count
            alpha_brain = instance.instance_alpha_brain
        
            logger = logging.getLogger(instance_id + "_instance_logger")
            logger.info(f"Class: {instance_id}, Generations: {sucessful_generations_count} Alpha ID: {alpha_brain.brain_id}")
            
        else: 
            func(*args, **kwargs)
            
    return process_instance_wrapper

def generation_instance_attribute_logger(func):
    @wraps(func)
    def process_generation_wrapper(*args, **kwargs ):
        
        instance = args[0]
        logging_variables = kwargs.get("logging_variables")
        instance_id, with_logging = logging_variables
        
        if with_logging :
            start_time = datetime.now()
            func(*args, **kwargs)
            end_time = datetime.now()
            
            logger = logging.getLogger(instance_id + "_generation_logger")
            run_time_logger = logging.getLogger(instance_id + "_run_time_logger")
            
            generation_id = instance.generation_id
            current_generation_number = instance.current_generation_number
            is_generation_sucessful = instance.is_generation_sucessful
            fitness_threshold = instance.fitness_threshold
            number_of_agents = instance.number_of_agents
            average_fitness_across_generation = instance.average_fitness_across_generation
            
            generation_alpha_brain = instance.generation_alpha_brain
            
            logger.info(f"Generation ID: {generation_id} - Generation Number: {current_generation_number} - Total Agents: {number_of_agents} - Generation Sucessful: {is_generation_sucessful} - Average Fitness: {average_fitness_across_generation} - Fitness Threshold: {fitness_threshold}")
            
            run_time_logger.info(f"Generation: {generation_id} - Total run Time: {end_time - start_time} - Start Time: {start_time} - Completion Time: {end_time}")
        else:
            func(*args, **kwargs)
            
    return process_generation_wrapper

def agent_instance_attribute_logger(func):
    @wraps(func)
    def process_agent_wrapper(*args, **kwargs ):
        instance = args[0]
        logging_variables = kwargs.get("logging_variables")
        instance_id, with_logging = logging_variables
        
        func(*args, **kwargs)
        
        if with_logging :
            logger = logging.getLogger(instance_id + "_agent_logger")
            
            agent = instance.agent
            agent_brain_post_run = instance.agent_brain_post_run
            
            logger.info(f"Agent/Brain ID: {agent_brain_post_run.brain_id}, From Generation: {agent_brain_post_run.current_generation_number} Fitness: {agent_brain_post_run.fitness}, Traversed Path: {agent_brain_post_run.traversed_path}")
            
    return process_agent_wrapper


with_process_Instance_logging = learning_instance_attribute_logger
with_process_generation_logging = generation_instance_attribute_logger
with_process_agent_logging = agent_instance_attribute_logger

# def learning_instance_logging_factory():
    
#     def deco_function(func) -> callable:
#         @wraps(func)
#         def wrapper(*args, **kwargs):
            
#             logging_variables = kwargs.get("logging_variables")
            
#             if logging_variables is None:
#                 raise ValueError("logging_variables must be provided")
            
#             instance_id, with_logging = logging_variables
            
#             logger = logging.getLogger(instance_id + "_instance_logger")
#             logger.debug(f"Instance: {instance_id} --- Started at: {datetime.datetime.now()}")
            
#             func(*args, **kwargs)
            
#             logger.debug(f"Instance: {instance_id} --- Completed at: {datetime.datetime.now()}")
            
#         return wrapper
    
#     return deco_function


# def generation_instance_logging_factory():
    
#     def deco_function(func):
        
#         @wraps(func)
#         def wrapper(*args, **kwargs):
            
#             logging_variables = kwargs.get("logging_variables")
            
#             if logging_variables is None:
#                 raise ValueError("logging_variables must be provided")
            
#             instance_id, with_logging = logging_variables
            
#             logger = logging.getLogger(instance_id + "_generation_logger")
            
            
#             generation_alpha_brain, generation_top_fitness_brains,agent_brains_post_run, is_generation_sucessful, generation_id = func(*args, **kwargs)
            
#             logger.debug(f"The genration number: {generation_id} Sucessful: {is_generation_sucessful}")
#             logger.debug(f"Generation Alpha: {generation_alpha_brain.fitness} Path: {generation_alpha_brain.traversed_path}")
            
#             logger.debug(f"Next Generation Parents:")
#             for brain in generation_top_fitness_brains:
#                 logger.debug(f"Future Parent: {brain.fitness} Path: {brain.traversed_path}")
            
#             logger.debug(f"All Brains:")
#             for brain in agent_brains_post_run:
#                 logger.debug(f"Brain Instance: {brain.fitness} Path: {brain.traversed_path}")
            
#             return generation_alpha_brain, generation_top_fitness_brains,agent_brains_post_run, is_generation_sucessful, generation_id
#         return wrapper
    
#     return deco_function


# def agent_instance_logging_factory():
    
#     def deco_function(func):
        
#         @wraps(func)
#         def wrapper(*args, **kwargs):
            
#             logging_variables = kwargs.get("logging_variables")
            
#             if logging_variables is None:
#                 raise ValueError("logging_variables must be provided")
            
#             instance_id, with_logging = logging_variables
            
#             logger = logging.getLogger(instance_id + "_agent_logger")
            
            
#             agent_brain = func(*args, **kwargs)
            
#             logger.debug(agent_brain)
            
#             return agent_brain
        
#         return wrapper
    
#     return deco_function


# process_instance_with_logging = learning_instance_logging_factory()
# process_generation_with_logging = generation_instance_logging_factory()
# process_agent_with_logging = agent_instance_logging_factory()