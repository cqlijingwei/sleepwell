from abc import ABC, abstractmethod

class BaseAgent(ABC):
    def __init__(self, config):
        self.config = config
        self.is_enabled = self._check_enabled()
    
    def _check_enabled(self):
        agent_name = self.__class__.__name__.lower().replace('agent', '')
        return self.config['agents'].get(agent_name, {}).get('enabled', False)
    
    @abstractmethod
    def process_query(self, query, context=None):
        pass
    
    def format_response(self, response):
        if not self.is_enabled:
            return "I'm sorry, but I am unable to assist with this type of request right now. Please try again later!"
        return response