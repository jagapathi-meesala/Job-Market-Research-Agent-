from typing import Dict, Any, List
from contracts.tool_contract import ToolContract

class DynamicToolRegistry:
    """
    Manages available tools dynamically.
    Enforces contract validation without executing arbitrary code.
    """
    
    def __init__(self):
        self._tools: Dict[str, ToolContract] = {}
        
    def register(self, tool: ToolContract) -> None:
        """Register a tool instance."""
        if not isinstance(tool, ToolContract):
            raise TypeError("Tool must implement ToolContract")
            
        if tool.name in self._tools:
            raise ValueError(f"Tool with name '{tool.name}' is already registered.")
            
        self._tools[tool.name] = tool
        
    def get(self, tool_name: str) -> ToolContract:
        """Retrieve a tool by name."""
        if tool_name not in self._tools:
            raise KeyError(f"Tool '{tool_name}' not found in registry.")
        return self._tools[tool_name]
        
    def list_tools(self) -> List[str]:
        """List all registered tool names."""
        return list(self._tools.keys())
        
    def execute(self, tool_name: str, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute a registered tool.
        Returns a structured dictionary, trapping standard errors.
        """
        try:
            tool = self.get(tool_name)
            return tool.run(input_data)
        except Exception as e:
            return {
                "success": False,
                "error_type": type(e).__name__,
                "message": str(e)
            }
