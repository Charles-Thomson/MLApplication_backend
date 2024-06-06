import numpy as np
from Staging.Environment.Environment_Observation import environment_observation
from DataFormatting.work_item import EnvironmentConfigurationClass
import logging

class Enviroment:
    """Environment the agent operates within
    
    Args: 
        map_data (dict) : Data relating to the maze size, duration ect
    
    
    """
    
    def __init__(self, environment_config: EnvironmentConfigurationClass):
        self.current_step: int = 0
        self.path: list[tuple[int, int]] = []

        self.environment_map: np.array = environment_config.environment_map
        self.max_step_count: int = environment_config.environment_maximum_action_count
        self.current_coords: tuple[int, int] = environment_config.environment_start_coordinates
        
        self.general_system_logger = logging.getLogger("general_system_logger")

    def get_env_type(self) -> str:
        """
        Return the type of the environement
        rtn: The type of the environement
        """
        return "Static_State"

    def get_environment_observation(self) -> np.array:
        """ Get the distance of objects  in each direction from a point in the Enviromnet

        Returns:
            np.array: Array containing distance from objects 
        """

        return environment_observation(self.current_coords, self.environment_map)

    def step(self, action: int) -> tuple[int, float, bool]:
        """ Carry out an action/step
        
            Args: 
                action (int): Int value relating to an action

            return:
                current_coords (int) : new location in the enviroment after action
                termination (bool) : If the action resulted in termination
                reward (float) : Value gained from taking the action
        
        """

        reward: float = self.calculate_reward(self.current_coords)
        new_state_x, new_state_y = self.process_action(action)
        termination: bool = self.termination_check(new_state_x, new_state_y)

        self.path.append(self.current_coords)

        self.current_coords = (new_state_x, new_state_y)

        self.current_step += 1

        return self.current_coords, termination, reward

    def remove_goal(self, current_state_x: int, current_state_y: int):
        """Remove a gola node from the Environment when reached by Agent

        Args:
            current_state_x (int): Curent location in the Environmnet X-axis
            current_state_y (int): Curent location in the Environmnet Y-axis
        """
        
        self.environment_map[current_state_x, current_state_y] = 1

    def calculate_reward(self, current_coords: tuple[int]) -> float:
        """Calculate the reawrd given for an action take in the enviroment
           Reward is calculated based on the type of node the action leads to
           

        Args:
            current_coords (tuple[int]): The current coordinates of the Agent in the Enviromnet

        Returns:
            float: The reward given based o nthe new state in the Enviroment
        """

        current_state_x, current_state_y = current_coords

        value_at_new_state = self.get_location_value(
            self.environment_map, (current_state_x, current_state_y)
        )

        if (current_state_x, current_state_y) in self.path:
            return 0.0

        match value_at_new_state:
            case 0:  # Open Tile
                return 0.15

            case 1: # goal
                self.remove_goal(current_state_x, current_state_y)
                return 3.0
                

            case 2:  # Obstical
                return 0.0

    def termination_check(self, new_state_x: int, new_state_y: int) -> bool:
        """ Check if the Agent has breached any of the terminetion conditions

        Args:
            new_state_x (int): Curent location in the Environmnet X-axis
            new_state_y (int): Curent location in the Environmnet Y-axis

        Returns:
            bool: If the agent is to be terminated
        """

        termination_conditions: list = [
            new_state_x < 0,
            new_state_y < 0,
            self.current_step >= self.max_step_count,
            self.get_location_value(self.environment_map, (new_state_x, new_state_y))
            == 2,
        ]

        if any(termination_conditions):
            return True

        return False

    def process_action(self, action: int) -> tuple[int]:
        """ Process the given action 

        Args:
            action (int): Int value relating to a corisponding action 

        Returns:
            tuple[int]: The new x,y coordinates of the Agent after taking the action
        """

        hrow, hcol = self.current_coords

        match action:
            case 0:  # Up + Left
                hrow -= 1
                hcol -= 1

            case 1:  # Up
                hrow -= 1

            case 2:  # Up + Right
                hrow -= 1
                hcol += 1

            case 3:  # left
                hcol -= 1

            case 4:  # No Move
                pass

            case 5:  # Right
                hcol += 1

            case 6:  # Down + Left
                hrow += 1
                hcol -= 1

            case 7:  # Down
                hrow += 1

            case 8:  # Down + Right
                hcol += 1
                hrow += 1

        return (hrow, hcol)

    def get_location_value(self, env_map: np.array, coords: tuple):
        """ Get the value of a node at a specified location in the Environment

        Args:
            
            env_map (np.array): Map of the Environment 
            coords (tuple): The coordinates of the desired node value

        Returns:
            int: Value of the node at the given coordinates 
            "2" indicates an obstical or out of bounds
        """
        try:
            value = env_map[coords[0]][coords[1]]
            return value
        except IndexError:
            return 2  # Termination condition
    