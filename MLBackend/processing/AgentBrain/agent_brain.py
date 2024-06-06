from dataclasses import dataclass, field
import numpy as np
from DataFormatting.work_item import NeuralNetworkConfigurationClass

@dataclass(order=True)
class BrainInstance:
    """
    Agent Brain
    Stores neural network related information along 
    with data relating to the state of the Agent/agents performance
    """
    
    
    brain_id: str = None
    fitness: float = 0.0
    brain_type: str = None
    traversed_path: list[tuple[int,int]] = field(default_factory=list[tuple[int,int]])
    
    fitness_by_step: list[float] = field(default_factory=list[float])
    current_generation_number: int = None
    
    hidden_weights: np.array = None
    output_weights: np.array = None
    
    hidden_layer_activation_function: callable = None
    output_layer_activation_function: callable = None
    
    
    def determin_action(self, sight_data: np.array) -> int:
        """
        Determin best action based on given data/activation
        Args: 
            sight_data (np.array) - Activation data from envrironment
        retrun: 
           (int) Determined action based on input data
        """

        hidden_layer_dot_product = np.dot(sight_data, self.hidden_weights)
        vectorize_func = np.vectorize(self.hidden_layer_activation_function)
        hidden_layer_activation = vectorize_func(hidden_layer_dot_product)
        output_layer_dot_product = np.dot(hidden_layer_activation, self.output_weights)

        return self.output_layer_activation_function(output_layer_dot_product)

    
    