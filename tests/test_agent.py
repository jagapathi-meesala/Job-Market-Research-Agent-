import pytest
from core.agent import AgentCore

def test_agent_initialization():
    agent = AgentCore()
    assert agent is not None
    assert agent.registry is not None
    
def test_agent_metadata():
    agent = AgentCore()
    meta = agent.get_metadata()
    assert isinstance(meta, dict)
    assert "name" in meta
    assert meta["name"] == "job-market-research-agent"
    assert "version" in meta
    
def test_agent_tool_listing():
    agent = AgentCore()
    tools = agent.list_tools()
    assert isinstance(tools, list)
    assert "analyze-job-listings" in tools
    assert "analyze-skill-demand" in tools
    assert "analyze-salary-data" in tools
    assert "analyze-location-demand" in tools
    assert "analyze-company-demand" in tools
    assert "calculate-skill-gap" in tools
    assert "calculate-job-market-summary" in tools
