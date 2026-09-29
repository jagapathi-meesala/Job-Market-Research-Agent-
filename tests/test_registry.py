import pytest
from core.registry import DynamicToolRegistry
from contracts.tool_contract import ToolContract
from typing import Dict, Any

class DummyTool(ToolContract):
    @property
    def name(self) -> str: return "dummy-tool"
    @property
    def description(self) -> str: return "Dummy"
    def validate_input(self, data: Dict[str, Any]) -> bool: return True
    def execute(self, data: Dict[str, Any]) -> Dict[str, Any]: return {"result": "success"}

def test_registry_registration():
    registry = DynamicToolRegistry()
    registry.register(DummyTool())
    
    assert "dummy-tool" in registry.list_tools()
    
def test_registry_duplicate_registration():
    registry = DynamicToolRegistry()
    registry.register(DummyTool())
    
    with pytest.raises(ValueError):
        registry.register(DummyTool())
        
def test_missing_tool():
    registry = DynamicToolRegistry()
    with pytest.raises(KeyError):
        registry.get("non-existent-tool")

def test_execution_through_registry():
    registry = DynamicToolRegistry()
    registry.register(DummyTool())
    
    result = registry.execute("dummy-tool", {})
    assert result.get("success") is True
    assert result.get("result") == "success"
