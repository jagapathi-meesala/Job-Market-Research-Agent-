from abc import ABC, abstractmethod
from typing import Dict, Any

class ToolContract(ABC):
    """
    Base contract for all tools.
    Enforces deterministic behavior and safe execution structures.
    """
    
    @property
    @abstractmethod
    def name(self) -> str:
        """The canonical name of the tool."""
        pass
        
    @property
    @abstractmethod
    def description(self) -> str:
        """A brief description of what the tool does."""
        pass
        
    @abstractmethod
    def validate_input(self, input_data: Dict[str, Any]) -> bool:
        """
        Validate that the input matches expected schemas.
        Should raise ValueError or return False if invalid, 
        depending on implementation preference (raising allows better error messages).
        """
        pass
        
    @abstractmethod
    def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        The core deterministic logic of the tool.
        Must not evaluate arbitrary code or run shell commands.
        """
        pass

    def run(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Standard execution wrapper that includes validation and safe error handling.
        """
        try:
            self.validate_input(input_data)
            result = self.execute(input_data)
            
            # Ensure the result has a success flag if not already present
            if "success" not in result:
                result["success"] = True
                
            return result
        except Exception as e:
            # Deterministic error response structure
            return {
                "success": False,
                "error_type": type(e).__name__,
                "message": str(e)
            }
