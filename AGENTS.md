# AGENTS Architecture

This agent is built to be modular, portable, and framework-agnostic. 

## Architecture Layers

### AgentCore
The `AgentCore` serves as the primary instantiation point for the agent logic. It initializes the `DynamicToolRegistry` and exposes metadata about the agent's capabilities. It does not contain domain-specific job market logic.

### DynamicToolRegistry
The `DynamicToolRegistry` dynamically manages tools at runtime. It avoids monolithic dispatch functions and instead dynamically registers tools ensuring that their class signatures respect the `ToolContract`. Duplicate registrations or missing tools are handled deterministically through structured error payloads.

### Contracts
Abstract base classes (`ToolContract`, `AgentContract`) enforce structural guarantees. Tools must adhere to an input schema, an output schema, and an `execute` function.

### Tools
The pure business logic of the agent. Tools execute strict mathematical formulas on valid input payloads. They lack system access, network access, or side-effect capabilities.

### Adapters
The `adapters/` directory holds translation boundaries. The `portable_adapter.py` allows standard frameworks (like OpenGAP or CrewAI) to treat this highly deterministic engine as a standard agent without polluting the core logic with external framework dependencies.

### Validation
Each tool validates its inputs against explicit rules. Missing fields, mismatched types, or logically invalid data (e.g., negative salaries) are rejected safely.

### Security
The agent operates in a closed environment:
- No `eval()`
- No `subprocess`
- No dynamic imports governed by untrusted user data.
- No direct file read/write unless absolutely required (none required currently).

### Extension Mechanism
To extend this agent, simply create a new Python file in the `tools/` directory inheriting from `ToolContract`, and add it to the `agent.yaml`.

### Portability Strategy
Because the agent does not import LangChain, CrewAI, AutoGen, or the OpenAI SDK natively in its `core/` or `tools/` modules, it can run as an isolated Python microservice, an OpenGAP worker, or an AWS Lambda function trivially via the `portable_adapter`.
