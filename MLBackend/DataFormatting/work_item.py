from dataclasses import dataclass, field
import logging 
import numpy as np 

general_system_logger = logging.getLogger("general_system_logger")

    

@dataclass
class EnvironmentConfigurationClass:
    """Data attaining to the configuration of the environment of a work instance."""

    _environment_map: np.array = None
    _environment_map_dimensions: int = None
    _environment_start_coordinates: tuple[int, int] = None
    _environment_maximum_action_count: int = None
    general_system_logger.info(f"Environment Configuration Class Created")
    
    # Should call for all setters to use the ValueError checking ?
    def __post_init__(self):
        if self._environment_map is not None:
            self.environment_map = self._environment_map
        if self._environment_start_coordinates is not None:
            self.environment_start_coordinates = self._environment_start_coordinates

    

    @property
    def environment_map(self):
        return self._environment_map

    @environment_map.setter
    def environment_map(self, value):
        general_system_logger.info(f"environment_map")
        
        if not isinstance(value, list):
            raise ValueError("Environment map must be a numpy array.")
        new_array = np.array(value).reshape(int(self.environment_map_dimensions), -1)
        self._environment_map = new_array
        
        general_system_logger.info(f"environment_map Complete ")
        
    @property
    def environment_map_dimensions(self):
        return int(self._environment_map_dimensions)

    @environment_map_dimensions.setter
    def environment_map_dimensions(self, value):
        general_system_logger.info(f"environment_map_dimensions")
        
        if not isinstance(value, int) or value <= 0:
            raise ValueError("Environment map dimensions must be a positive integer.")
        self._environment_map_dimensions = int(value)

    
    
    @property
    def environment_start_coordinates(self):
        return self._environment_start_coordinates

    @environment_start_coordinates.setter
    def environment_start_coordinates(self, value):
        general_system_logger.info(f"environment_start_coordinates")
        
        
        if not isinstance(value, int) or value < 0:
            raise ValueError("Environment start state must be a positive integer")
        
        if value == 0:
            
            self._environment_start_coordinates = (0, 0)
            return
        x_dimension = (int(self.environment_map_dimensions) / value)
        y_dimension = (int(self.environment_map_dimensions) % value)
    
        self._environment_start_coordinates = (x_dimension, y_dimension)
        
        general_system_logger.info(f"environment_start_coordinates Complete")

    @property
    def environment_maximum_action_count(self):
        return int(self._environment_maximum_action_count)

    @environment_maximum_action_count.setter
    def environment_maximum_action_count(self, value):
        general_system_logger.info(f"environment_maximum_action_count")
        if not isinstance(value, int) or value <= 0:
            raise ValueError("Environment maximum action count must be a positive integer.")
        self._environment_maximum_action_count = int(value)
        
    def __str__(self):
        return f"{self._environment_map} \n {self.environment_map_dimensions} \n {self._environment_start_coordinates} \n {self._environment_maximum_action_count}"
        
               
@dataclass
class HyperParameterConfigurationClass:
    """Data attaining to the hyper parameter configuaration of a work instance 
    """
    _maximum_number_of_genrations: int = None
    _maximum_generation_size: int = None
    _starting_fitness_threshold: float = None
    _start_new_generation_threshold: int = None
    _generation_failure_threshold: int = None
    
    
    @property
    def maximum_number_of_genrations(self):
        return int(self._maximum_number_of_genrations)
    
    @maximum_number_of_genrations.setter
    def maximum_number_of_genrations(self, value):
        if not isinstance(value, int) or value <= 0:
            raise ValueError(f"maximum_number_of_genrations must be greater then 0")
        self._maximum_number_of_genrations = int(value)
    
    
    @property
    def maximum_generation_size(self):
        return self._maximum_generation_size
    
    @maximum_generation_size.setter
    def maximum_generation_size(self, value):
        
        if not isinstance(value, int) or value <= 0:
            raise ValueError(f"maximum_generation_size must be greater then 0")
        self._maximum_generation_size = value
        
    @property
    def starting_fitness_threshold(self):
        return self._starting_fitness_threshold
    
    @starting_fitness_threshold.setter
    def starting_fitness_threshold(self, value):
        
        if not isinstance(value, float) or value <= 0.0:
            raise ValueError(f"_starting_fitness_threshold must be greater then 0")
        self._starting_fitness_threshold = value
    
    @property
    def start_new_generation_threshold(self):
        return self._start_new_generation_threshold
    
    @start_new_generation_threshold.setter
    def start_new_generation_threshold(self, value):
        if not isinstance(value, int) or value <= 0:
            raise ValueError(f"start_new_generation_threshold must be greater then 0")
        self._start_new_generation_threshold = value
    
    @property
    def generation_failure_threshold(self):
        return self._generation_failure_threshold
    
    @generation_failure_threshold.setter
    def generation_failure_threshold(self, value):
        if not isinstance(value, int) or value <= 0:
            raise ValueError(f"generation_failure_threshold must be greater then 0")
        self._generation_failure_threshold = value
    
    
    def __str__(self):
        return f"{self.maximum_number_of_genrations} \n {self.maximum_generation_size} \n {self.starting_fitness_threshold} \n {self.start_new_generation_threshold} \n {self.generation_failure_threshold}"
    
        
@dataclass
class NeuralNetworkConfigurationClass:
    """Data attaining to neural network configuaration of a work instance 
    """
    _weight_init_huristic: str = None
    _hidden_activation_function_ref : str = None
    _output_activation_function_ref: str = None
    _new_generation_creation_function_ref: str = None
    _input_to_hidden_connections: tuple[int,int] = None
    _hidden_to_output_connections: tuple[int, int] = None
    
    
    def __post_init__(self):
        if self._input_to_hidden_connections is not None:
            self.input_to_hidden_connections = self._input_to_hidden_connections
        if self._hidden_to_output_connections is not None:
            self.hidden_to_output_connections = self._hidden_to_output_connections
        
        
    @property
    def weight_init_huristic(self):
        return self._weight_init_huristic
    
    @weight_init_huristic.setter
    def weight_init_huristic(self, value):
        if not isinstance(value, str) or value == None:
            raise ValueError(f"weight_init_huristic must be given as a tring and can not be null")
        self._weight_init_huristic = value
        
    @property
    def hidden_activation_function(self):
        return self._hidden_activation_function_ref
    
    @hidden_activation_function.setter
    def hidden_activation_function(self, value):
        if not isinstance(value, str) or value == None:
            raise ValueError(f"hidden_activation_function must be given as a tring and can not be null")
        self._hidden_activation_function_ref = value
    
    
    @property
    def output_activation_function(self):
        return self._output_activation_function_ref
    
    @output_activation_function.setter
    def output_activation_function(self, value):
        if not isinstance(value, str) or value == None:
            raise ValueError(f"output_activation_function must be given as a tring and can not be null")
        self._output_activation_function_ref = value
    
    @property
    def new_generation_creation_function(self):
        return self._new_generation_creation_function_ref
    
    @new_generation_creation_function.setter
    def new_generation_creation_function(self, value):
        if not isinstance(value, str) or value == None:
            raise ValueError(f"new_generation_creation_function must be given as a tring and can not be null")
        self._new_generation_creation_function_ref = value
    
    @property
    def input_to_hidden_connections(self):
        return self._input_to_hidden_connections

    @input_to_hidden_connections.setter
    def input_to_hidden_connections(self, value):
        if not isinstance(value, list) or len(value) != 2 or not all(isinstance(x, int) for x in value):
            
            raise ValueError("input_to_hidden_connections must be a tuple of two integers.")
        self._input_to_hidden_connections = (value[0], value[1])
        
    @property
    def hidden_to_output_connections(self):
        return self._hidden_to_output_connections

    @hidden_to_output_connections.setter
    def hidden_to_output_connections(self, value):
        if not isinstance(value, list) or len(value) != 2 or not all(isinstance(x, int) for x in value):
            
            raise ValueError("hidden_to_output_connections must be a tuple of two integers.")
        self._hidden_to_output_connections = (value[0], value[1])
    
    def __str__(self):
        return f"{self.weight_init_huristic} \n {self.hidden_activation_function} \n {self.output_activation_function} \n {self.new_generation_creation_function} \n {self.input_to_hidden_connections} \n {self.hidden_to_output_connections}"
    
    
    
@dataclass
class WorkItem:
    """ An item of work that needs to be completed
    
    """
    instance_id: str
    enviroment_config: EnvironmentConfigurationClass
    hyper_parameter_config: HyperParameterConfigurationClass
    neural_network_config: NeuralNetworkConfigurationClass
    with_logging: bool = True
    
    def __str__(self):
        return f"{self.instance_id} \n {self.enviroment_config} \n {self.hyper_parameter_config} \n {self.neural_network_config}"
    