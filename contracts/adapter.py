from abc import ABC, abstractmethod
from typing import Dict, Any

class FrameworkAdapter(ABC):
    """
    Base contract for framework adapters.
    Adapters translate external framework requests into AgentCore inputs.
    """
    
    @abstractmethod
    def invoke(self, request_payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Receive a payload from an external system, translate it, 
        invoke the core, and return the response.
        """
        pass
