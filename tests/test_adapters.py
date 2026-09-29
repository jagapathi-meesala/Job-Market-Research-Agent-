import pytest
from adapters.registry import get_adapter
from core.agent import AgentCore

def test_portable_adapter_invocation():
    agent = AgentCore()
    adapter = get_adapter(agent, "portable")
    
    # Test valid action
    res = adapter.invoke({"action": "get_metadata"})
    assert res["success"] is True
    assert "metadata" in res
    
    # Test tool execution via adapter
    res = adapter.invoke({
        "action": "execute_tool",
        "tool_name": "analyze-job-listings",
        "input_data": {"jobs": []}
    })
    assert res["success"] is True
    assert res["total_jobs"] == 0
    
    # Test invalid action
    res = adapter.invoke({"action": "unknown"})
    assert res["success"] is False
