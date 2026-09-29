from abc import ABC, abstractmethod
from typing import Dict, Any, List

class AgentContract(ABC):
    """
    Base contract for the Agent Core.
    Ensures that any agent implementation exposes metadata and a standard execution interface.
    """
    
    @abstractmethod
    def get_metadata(self) -> Dict[str, Any]:
        """Return metadata about the agent."""
        pass
        
    @abstractmethod
    def execute_tool(self, tool_name: str, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a tool by name with the given input data."""
        pass

    @abstractmethod
    def list_tools(self) -> List[str]:
        """Return a list of available tool names."""
        pass
