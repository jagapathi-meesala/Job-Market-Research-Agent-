from typing import Dict, Any, List
from contracts.agent_contract import AgentContract
from core.registry import DynamicToolRegistry
import importlib
import yaml
import os

class AgentCore(AgentContract):
    """
    The core Job Market Research Agent.
    Orchestrates tool loading and execution.
    """
    
    def __init__(self, manifest_path: str = "agent.yaml"):
        self.registry = DynamicToolRegistry()
        self.metadata = {}
        self._load_manifest(manifest_path)
        self._load_tools()
        
    def _load_manifest(self, manifest_path: str):
        if not os.path.exists(manifest_path):
            self.metadata = {
                "name": "job-market-research-agent",
                "version": "1.0.0",
                "description": "Fallback metadata when manifest is missing."
            }
            return
            
        with open(manifest_path, "r", encoding="utf-8") as f:
            try:
                self.metadata = yaml.safe_load(f)
            except yaml.YAMLError:
                self.metadata = {
                    "name": "job-market-research-agent",
                    "error": "Failed to parse manifest."
                }
                
    def _load_tools(self):
        """
        Dynamically load tools declared in the manifest.
        For security, this only loads from the known local `tools` package.
        """
        tools_list = self.metadata.get("tools", [])
        for tool_entry in tools_list:
            # Handle list of strings or list of dicts based on standard manifests
            tool_name = tool_entry if isinstance(tool_entry, str) else tool_entry.get("name")
            if not tool_name:
                continue
                
            # Safely resolve module name based on tool name pattern.
            # Example: "analyze-job-listings" -> "tools.analyze_job_listings"
            # Note: User explicitly asked for hyphenated tool files e.g. analyze-job-listings.py
            module_name = f"tools.{tool_name.replace('.py', '')}"
            try:
                # We use importlib to dynamically load the tool module.
                # In each tool module, we expect a `register(registry)` function.
                module = importlib.import_module(module_name)
                if hasattr(module, "register"):
                    module.register(self.registry)
            except Exception as e:
                # We ignore failed imports in production, but could log them.
                pass
                
    def get_metadata(self) -> Dict[str, Any]:
        return self.metadata
        
    def list_tools(self) -> List[str]:
        return self.registry.list_tools()
        
    def execute_tool(self, tool_name: str, input_data: Dict[str, Any]) -> Dict[str, Any]:
        return self.registry.execute(tool_name, input_data)
