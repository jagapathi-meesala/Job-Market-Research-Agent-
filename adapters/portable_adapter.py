from typing import Dict, Any
from contracts.adapter import FrameworkAdapter
from core.agent import AgentCore

class PortableAdapter(FrameworkAdapter):
    """
    A portable adapter that translates generic framework requests 
    into standard AgentCore tool executions.
    """
    
    def __init__(self, agent_core: AgentCore):
        self.agent = agent_core
        
    def invoke(self, request_payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Expected payload format:
        {
            "action": "execute_tool",
            "tool_name": "...",
            "input_data": {...}
        }
        """
        action = request_payload.get("action")
        
        if action == "execute_tool":
            tool_name = request_payload.get("tool_name")
            input_data = request_payload.get("input_data", {})
            if not tool_name:
                return {"success": False, "error_type": "MissingToolName", "message": "tool_name is required."}
                
            return self.agent.execute_tool(tool_name, input_data)
            
        elif action == "get_metadata":
            return {"success": True, "metadata": self.agent.get_metadata()}
            
        elif action == "list_tools":
            return {"success": True, "tools": self.agent.list_tools()}
            
        return {
            "success": False, 
            "error_type": "UnknownAction", 
            "message": f"Action '{action}' is not supported by PortableAdapter."
        }
