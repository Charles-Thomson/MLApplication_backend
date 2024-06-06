"""Output layer functions factory"""
import numpy as np


class OutputLayerActvaitionFactory:
    """Factory for the Output Layer activation Functions

    Returns:
        callable: New Output Layer activation Function 
    """

    output_layer_activation_functions = {}

    @classmethod
    def get_output_activation_func(cls, activation_function):
        """Generate the brain based of given type"""
        try:
            retreval = cls.output_layer_activation_functions[activation_function]

        except KeyError as err:
            raise NotImplementedError(f"{activation_function} Not implemented") from err

        return retreval

    @classmethod
    def register(cls, type_name):
        """Register an brain enerator to the factory"""

        def deco(deco_cls):
            cls.output_layer_activation_functions[type_name] = deco_cls
            return deco_cls

        return deco


@OutputLayerActvaitionFactory.register("argmax_activation")
def argmax_activation(vector: np.array) -> int:
    
    """ArgMax - Convert highest value in vectror to 1, sets all others to 0
    
    Args:
        vector: Input np.array

    Returns:
        int: Index of highest value
    """
    return np.argmax(vector)


@OutputLayerActvaitionFactory.register("soft_argmax_activation")
def soft_argmax_activation(vector: np.array) -> int:
    
    """SoftMax - each value is given a probabilitry of occuring

    Returns:
        int: index of highest chance to occur 
    """
    vector_exp = np.exp(vector)
    vector_sum = vector_exp / vector_exp.sum()
    return np.argmax(vector_sum)
