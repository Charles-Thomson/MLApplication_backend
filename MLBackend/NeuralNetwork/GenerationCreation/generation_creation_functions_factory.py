"""generational functions factory"""
import logging
import numpy as np
import random


class GenerationalFunctionsFactory:
    """Factory for the Generation Functions

    Returns:
        callable: New Generation Function 
    """

    generational_functions = {}
    
    general_system_logger = logging.getLogger("general_system_logger")
    

    @classmethod
    def get_generation_func(cls, generational_funcation):
        """Generate the brain based of given type"""
        cls.general_system_logger.info(f"GETIING Generation func {generational_funcation}")
        try:
            retreval = cls.generational_functions[generational_funcation]

        except KeyError as err:
            raise NotImplementedError(
                f"{generational_funcation} Not implemented"
            ) from err

        return retreval

    @classmethod
    def register(cls, type_name):
        """Register an brain enerator to the factory"""

        def deco(deco_cls):
            cls.generational_functions[type_name] = deco_cls
            return deco_cls

        return deco


@GenerationalFunctionsFactory.register("crossover_weights_average")
def crossover_weights_average(
    weight_set_a: np.array, weight_set_b: np.array
) -> np.array:
    """Take the average of two "parent" weight sets and return the average for each weight

    Args:
        weight_set_a (np.array): Parent weight set A
        weight_set_b (np.array): Parent weight set B

    Returns:
        np.array: New weight set, the average of both parents
    """
    
    
    new_weight_set_sum: np.array = np.add(weight_set_a, weight_set_b)
    new_weight_set: np.array = np.divide(new_weight_set_sum, 2)
    return new_weight_set


@GenerationalFunctionsFactory.register("crossover_weights_mergining")
def crossover_weights_mergining(
    weight_set_a: np.array, weight_set_b: np.array
) -> np.array:
    """Take weeights randomly from two parents and create anew weight set

    Args:
        weight_set_a (np.array): Parent weight set A
        weight_set_b (np.array): Parent weight set B

    Returns:
        np.array: New weight set, randomly selected weights
    """

    new_weights = weight_set_a
    for index_x, weights in enumerate(weight_set_a):
        for index_y, _ in enumerate(weights):
            selection_chance = random.randrange(1, 100)
            if selection_chance > 50:
                new_weights[index_x][index_y] = weight_set_b[index_x][index_y]

    new_weights = np.array(new_weights)

    return new_weights