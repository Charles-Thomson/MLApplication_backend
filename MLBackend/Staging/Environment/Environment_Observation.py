from itertools import chain
import numpy as np


def environment_observation(observation_point: int, env_map: np.array) -> list[float]:
    """ 
        Observe the environment for a given node

        Args:
            observation_point (int) : The location of the agent in the environment / the observation point
            env_map (np.array) : The map of the Environment
            
            
        return: 
            observation_data (List<float>) : The float representation of each object type, in each direction,
                                            from the observation point

    """

    loc_row, loc_col = observation_point

    up_right: list = np.diagonal(env_map[loc_row::-1, loc_col:])[1:]
    down_right: list = np.diagonal(env_map[loc_row:, loc_col:])[1:]
    down: list = env_map[loc_row + 1 :, loc_col]
    down_left: list = np.diagonal(env_map[loc_row:, loc_col::-1])[1:]
    right = env_map[loc_row, loc_col + 1 :]
    up_left: list = np.diagonal(env_map[loc_row::-1, loc_col::-1])[1:]
    left: list = env_map[loc_row, loc_col - 1 :: -1]
    up: list = env_map[loc_row - 1 :: -1, loc_col]

    # Handle the case where loc row/col == 0 
    left = [] if loc_col == 0 else left 
    up = [] if loc_row == 0 else up 

    sight_lines = [
        up,
        up_right,
        right,
        down_right,
        down,
        down_left,
        left,
        up_left,
    ]

    observation_data = [check_sight_line(line) for line in sight_lines]
    observation_data = list(chain(*observation_data))
    return observation_data


def check_sight_line(sight_line: list) -> list[float, float, float]:
    """ Check along a given range of values for each node type

    Args:
        sight_line (list): The values to be checked

    Returns:
        list[float, float, float]: List of values representing the distance of each object type along
                                   the sight line.
    """
    rtn_data = []
    for distance, value in enumerate(sight_line):
        if value == 1:
            rtn_data = [0.1 * (distance + 1), 0.0, 0.0]
        if value == 2:
            return [round(0.1 * distance, 3), 1 / (distance + 1), 0.0]
        if value == 3:
            return [round(0.1 * distance, 3), 0.0, 1 / (distance + 1)]

    # if no data aka out of bounds
    if not rtn_data:
        return [0.0, 0.0, 0.0]

    return rtn_data
