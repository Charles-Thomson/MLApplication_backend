"""Brain generation in the form of a factory"""
from __future__ import annotations
from copy import deepcopy
import logging
import random
import numpy as np
from dataclasses import dataclass
# from MLBackend.processing.AgentBrain.agent_brain_old import BrainInstance
from DataFormatting.work_item import NeuralNetworkConfigurationClass


from NeuralNetwork.HiddenLayerActivationFunctions.hidden_layer_activation_functions_factory import HiddenLayerActvaitionFactory
from NeuralNetwork.OutputLayerActivationFunctions.output_layer_activation_functions_factory import OutputLayerActvaitionFactory
from NeuralNetwork.GenerationCreation.generation_creation_functions_factory import GenerationalFunctionsFactory

from NeuralNetwork.WeightInitHuristics.weight_init_huristics_factory import WeightHuristicsFactory

from processing.AgentBrain.agent_brain import BrainInstance

class BrainFactory:
    
    """Factory for the creation of Agent brains

    Returns:
        callable: New Agent brain
    """

    brain_types = {}

    @classmethod
    def make_brain(
        cls,
        neural_network_config: NeuralNetworkConfigurationClass,
        brain_type: str,
        brain_id: str,
        parents: list[BrainInstance] = None,
    ):
        """Generate the brain based of given type"""
        general_system_logger = logging.getLogger("general_system_logger")
        
        try:
            retreval = cls.brain_types[brain_type]

        except KeyError as err:
            
            raise NotImplementedError(f"{brain_type} Not implemented") from err

        return retreval(neural_network_config=neural_network_config, brain_id = brain_id, parents=parents)

    @classmethod
    def register(cls, type_name):
        """Register an brain enerator to the factory"""

        def deco(deco_cls):
            cls.brain_types[type_name] = deco_cls
            return deco_cls

        return deco


# @BrainFactory.register("base_brain_instance")
# def base_brain_instance(neural_network_config: NeuralNetworkConfigurationClass, brain_id: str, parents=None) -> BrainInstance:
#     """
#     Populate a new BrainInstance with pre existing formatted data
#     - Converting a models.Model back to a BrainInstance
    
#     Args:
#         neural_network_config (obj)- the config file of the brain instance
#         parents - not used
        
#     return: 
#         BrainInstance: A new Brain Instance 
#     """
    
#     return BrainInstance(
#         neural_network_config=neural_network_config,
#         brain_id = brain_id
#     )


@BrainFactory.register("generational_weighted_brain")
def new_generational_weighted_brain(
    neural_network_config: NeuralNetworkConfigurationClass,
    brain_id: str,
    parents: list[BrainInstance]
) -> BrainInstance:
    """
    Generate a new generationally weighted brain
    - Uased when a new generation is created
    
    Args:
        neural_network_config (dict): the config file of the brain instance
        parents (List[BrainInstance]): parent brain instances used to generate new instance
        
        return:
            BrainInstance: New generationally weighted  BrainInstance
    """
    general_system_logger = logging.getLogger("general_system_logger")
    general_system_logger.info(f"GENERATIONAL WEIGHTED BRAIN")

    new_brain_instance: BrainInstance = BrainInstance()
    
    # general_system_logger.info(f"GENERATIONAL WEIGHTED BRAIN - New brain Instance")
    new_brain_instance.brain_id = brain_id
    
    mutation_threshold: int = 50

    new_generation_function = GenerationalFunctionsFactory.get_generation_func(neural_network_config._new_generation_creation_function_ref)
    
    # general_system_logger.info(f"GENERATIONAL WEIGHTED BRAIN - New generation Function set")
    
    val: int = len(parents)
    weightings: list[float] = tuple(val / i for i in range(1, val + 1))

    parent_a, parent_b = random.choices(parents, weights=weightings, k=2)

    # general_system_logger.info(f"GENERATIONAL WEIGHTED BRAIN - Parents selected")

    parent_a: BrainInstance = deepcopy(parent_a)
    parent_b: BrainInstance = deepcopy(parent_b)

    new_input_to_hidden_weight: np.array = new_generation_function(
        parent_a.hidden_weights, parent_b.hidden_weights
    )

    new_hidden_to_output_weights: np.array = new_generation_function(
        parent_a.output_weights, parent_b.output_weights
    )
    
    # general_system_logger.info(f"GENERATIONAL WEIGHTED BRAIN - Weights calculated")

    if random.randint(0, 100) > mutation_threshold:
        random_selection = random.randint(0, 1)
        if random_selection == 0:
            new_input_to_hidden_weight = apply_mutation(new_input_to_hidden_weight)

        if random_selection == 1:
            new_hidden_to_output_weights = apply_mutation(new_hidden_to_output_weights)

    new_brain_instance.hidden_weights = new_input_to_hidden_weight
    new_brain_instance.output_weights = new_hidden_to_output_weights
    
    # general_system_logger.info(f"GENERATIONAL WEIGHTED BRAIN - Weights set")

    set_brain_activation_functions(brain_instance=new_brain_instance, neural_network_config=neural_network_config)
    
    # general_system_logger.info(f"GENERATIONAL WEIGHTED BRAIN - Activation Functions set")

    return new_brain_instance
    

def apply_mutation(weight_set: np.array) -> np.array:
    """
    Apply a mutation to a weighting to give variance
    +/- 1-10% mutation 
    
    Args:
        weight_set(np.array): set of given weights to be mutated
        
    return:
        weight_set(np.array): weight_set post mutation
    """

    weight_set_shape: tuple = weight_set.shape

    # select random weight from set

    x_loc: int = random.randrange(weight_set_shape[0])
    y_loc: int = random.randrange(weight_set_shape[1])

    weight_to_mutate: float = weight_set[x_loc][y_loc]

    mutation_amount: int = random.randint(1, 10)
    positive_mutation: float = weight_to_mutate - (weight_to_mutate / mutation_amount)
    negitive_mutation: float = weight_to_mutate + (weight_to_mutate / mutation_amount)

    mutation: float = random.choice((positive_mutation, negitive_mutation))

    weight_set[x_loc][y_loc] = mutation

    return weight_set


@BrainFactory.register("random_weighted_brain")
def new_random_weighted_brain(
    neural_network_config: NeuralNetworkConfigurationClass,
    brain_id: str, 
    parents: list[BrainInstance]) -> BrainInstance:
    """
    Generate a randomly weighted brain
    Used in generation 0 - when there are no "parent" BrainInstances
    
    Args:
        brain_config(): the config file of the brain instance
        parents(list[BrainInstance]): default given as unused
        
    return: 
        BrainInstance - A new randomly weight BrainInstance
    """

    new_brain_instance: BrainInstance = BrainInstance()
    new_brain_instance.brain_id = brain_id
    
    
    weight_initilization_huristic: callable = WeightHuristicsFactory.get_huristic(neural_network_config.weight_init_huristic)

    hidden_weights: np.array = initialize_weights(
        layer_connections=neural_network_config.input_to_hidden_connections,
        weight_heuristic_func=weight_initilization_huristic
    )

    output_weights: np.array = initialize_weights(
        layer_connections=neural_network_config.hidden_to_output_connections,
        weight_heuristic_func=weight_initilization_huristic
    )

    new_brain_instance.hidden_weights = hidden_weights
    new_brain_instance.output_weights = output_weights
    
    set_brain_activation_functions(brain_instance=new_brain_instance, neural_network_config=neural_network_config)

    return new_brain_instance
 

def initialize_weights(
    layer_connections: tuple[int, int], weight_heuristic_func: callable
) -> np.array:
    """
    Generate random weigths between to layers of a specified sizes
    
    Args:
        layer_connections(tuple[int,int]): The number of connections between two layers
        weight_heuristic_func(callable): The init huristic of the weights
        
    return:
        rand_weights(np.array): Generated weights
    """
    get_weight = weight_heuristic_func(layer_connections)

    sending_layer, reciving_layer = layer_connections
    rand_weights: np.array = np.array(
        [
            [next(get_weight) for i in range(reciving_layer)]
            for i in range(sending_layer)
        ]
    )

    return rand_weights

def set_brain_activation_functions(brain_instance: BrainInstance, neural_network_config: NeuralNetworkConfigurationClass) -> None:
    """
    Set the activation functions of a brain instance using based on referance 
    given in the newual network config

    Args:
        brain_instance (BrainInstance): THe brain instance to have functions set
        neural_network_config (NeuralNetworkConfigurationClass): The configuration for the Brain Instance
    """
    
    brain_instance.hidden_layer_activation_function = HiddenLayerActvaitionFactory.get_hidden_activation_func(neural_network_config._hidden_activation_function_ref)
    brain_instance.output_layer_activation_function = OutputLayerActvaitionFactory.get_output_activation_func(neural_network_config._output_activation_function_ref)
