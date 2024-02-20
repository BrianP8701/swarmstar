from abc import ABC, abstractmethod
from typing import List, Dict

from swarmstar.swarm.types import SwarmConfig, SwarmOperation, SwarmNode, SwarmState

class BaseAction(ABC):
    '''
    All actions should subclass this class.
    '''    
    def __init__(self, swarm: SwarmConfig, node: SwarmNode):
        self.swarm = swarm
        self.node = node
    
    @abstractmethod
    def main(self, **kwargs) -> SwarmOperation:
        pass
    
    def save_node_report(self, report: str):
        self.node.report = report
        swarm_state = SwarmState(swarm=self.swarm)
        swarm_state.update_node(self.node)
        
    def update_termination_policy(self, termination_policy: str):
        self.node.termination_policy = termination_policy
        swarm_state = SwarmState(swarm=self.swarm)
        swarm_state.update_node(self.node)
        
    def messages(self, messages: List[List[str, str]]) -> List[Dict[str, str]]:
        '''
        Convert a list of messages: 
            [[role, content], [role, content]] 
        to a list of dictionaries: 
            [{'role': role, 'content': content}, {'role': role, 'content': content}
        '''
        messages_dict = []
        for message in messages:
            messages_dict.append({'role': message[0], 'content': message[1]})
        return messages_dict
    
    