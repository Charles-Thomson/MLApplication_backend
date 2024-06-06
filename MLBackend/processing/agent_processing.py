import logging
from processing.Agent.agent import Agent
from processing.AgentBrain.agent_brain import BrainInstance

from application_logging.logging_functions.logger_decorators import agent_instance_attribute_logger


class ProcessAgent:
    """Process an Agent Instance
    """
    
    def __init__(self, agent:Agent, logging_variables: dict):
        self.agent: Agent = agent
        self.agent_brain_post_run: BrainInstance = None
        
        
    @agent_instance_attribute_logger
    def process_agent(self, logging_variables) -> None:
        
        self.agent.run_agent()
        
        self.agent_brain_post_run = self.agent.brain