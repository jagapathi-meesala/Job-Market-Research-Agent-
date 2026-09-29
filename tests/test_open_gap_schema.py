import pytest
import yaml
import os
import json
import jsonschema

def test_opengap_manifest_parsable():
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    manifest_path = os.path.join(base_dir, "agent.yaml")
    assert os.path.exists(manifest_path)

    with open(manifest_path, "r") as f:
        data = yaml.safe_load(f)

    assert isinstance(data, dict)
    assert "name" in data
    assert "version" in data
    assert "tools" in data
    assert isinstance(data["tools"], list)

    schema_path = os.path.join(base_dir, "verification", "schemas", "agent-yaml.schema.json")
    if os.path.exists(schema_path):
        with open(schema_path, "r") as f:
            schema = json.load(f)
        jsonschema.validate(instance=data, schema=schema)

def test_opengap_tools_parsable():
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    manifest_path = os.path.join(base_dir, "agent.yaml")
    with open(manifest_path, "r") as f:
        data = yaml.safe_load(f)
        
    schema_path = os.path.join(base_dir, "verification", "schemas", "tool.schema.json")
    schema = None
    if os.path.exists(schema_path):
        with open(schema_path, "r") as f:
            schema = json.load(f)

    for tool_name in data.get("tools", []):
        tool_yaml_path = os.path.join(base_dir, "tools", f"{tool_name}.yaml")
        assert os.path.exists(tool_yaml_path), f"Missing tool YAML definition for {tool_name}"
        
        with open(tool_yaml_path, "r") as f:
            tool_data = yaml.safe_load(f)
            
        assert isinstance(tool_data, dict)
        assert tool_data.get("name") == tool_name
        
        if schema:
            jsonschema.validate(instance=tool_data, schema=schema)
