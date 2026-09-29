"""
Registry for framework adapters (stub for potential multiple adapter support).
"""
from adapters.portable_adapter import PortableAdapter

def get_adapter(agent_core, adapter_type: str = "portable"):
    if adapter_type == "portable":
        return PortableAdapter(agent_core)
    raise ValueError(f"Unknown adapter type: {adapter_type}")
