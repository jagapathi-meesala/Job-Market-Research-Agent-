import os

def test_documentation_presence():
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    required_docs = [
        "README.md",
        "SOUL.md",
        "RULES.md",
        "DUTIES.md",
        "AGENTS.md",
        "EXPLAINABILITY.md",
        "agent.yaml"
    ]
    for doc in required_docs:
        assert os.path.exists(os.path.join(base_dir, doc)), f"Missing {doc}"
