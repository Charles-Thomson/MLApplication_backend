
import logging


class Agent:
    """ 
    The agent class 
    
    """
    
    def __init__(self, environment: object, agent_brain: object):
        self.fitness: float = 0.0
        self.termination: bool = False
        self.brain: object = agent_brain
        self.environment: object = environment
        self.fitness_by_step: list[tuple] = []
        self.path: list[int, int] = [self.environment.current_coords]
        
        
    def run_agent(self) -> None:
        """
        Run the agent throught the environment
        """
        
        while self.termination is False:
            observation_data = self.environment.get_environment_observation()
            action = self.brain.determin_action(observation_data)
            new_coords, termination_status, reward = self.environment.step(action)
            self.fitness += reward
            self.path.append(new_coords)
            self.termination = termination_status
            self.fitness_by_step.append(self.fitness)

        self.brain.fitness = self.fitness
        self.brain.traversed_path = self.path
        self.brain.fitness_by_step = self.fitness_by_step

    