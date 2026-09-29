import pytest
import yaml
import os

def test_opengap_manifest_parsable():
    manifest_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "agent.yaml"))
    assert os.path.exists(manifest_path)
    
    with open(manifest_path, "r") as f:
        data = yaml.safe_load(f)
        
    assert isinstance(data, dict)
    assert "name" in data
    assert "version" in data
    assert "tools" in data
    assert isinstance(data["tools"], list)
    
    # Normally we would use jsonschema and the official OpenGAP schema here.
    # Because of execution environment constraints preventing retrieval of the live 
    # OpenGAP schema during build, this test verifies structural integrity against
    # generic expected YAML standard keys rather than pretending to use the official schema.
