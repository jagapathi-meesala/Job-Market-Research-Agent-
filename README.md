# Job Market Research Agent

## Overview
The Job Market Research Agent is a framework-independent, deterministic AI agent designed to analyze structured job-market information without relying on an LLM or live web scraping. It evaluates job listings, skill demands, salary datasets, location data, and company hiring trends from provided datasets to generate reproducible, explainable insights.

## Features
- **Deterministic Analysis**: Calculations (averages, frequencies) run on supplied dataset parameters instead of relying on unpredictable LLM outputs.
- **Skill Gap Calculation**: Evaluates candidate skills against specific job requirements and preferred skills.
- **Dataset Summaries**: Analyzes market demand, location distribution, and salary ranges.
- **Secure by Design**: Executes no user-supplied code or shell commands. Rejects malformed input structures safely.
- **Portable Architecture**: Core components are cleanly separated from agent framework adapters.

## Architecture
The agent is built on a clear modular structure:
- **AgentCore**: Handles initialization, validation, and tool execution orchestration.
- **DynamicToolRegistry**: Manages tool registration securely, avoiding arbitrary evaluation.
- **ToolContracts**: Enforce input/output schemas and deterministic behaviors for every tool.
- **Adapters**: Provide framework-agnostic interoperability endpoints (e.g., portable_adapter.py).

## Tools
1. **analyze-job-listings**: Summarizes statistics of a job listing dataset.
2. **analyze-skill-demand**: Measures skill frequencies across job listings.
3. **analyze-salary-data**: Computes min, max, average, and median salary info.
4. **analyze-location-demand**: Distributes job counts across geographical constraints.
5. **analyze-company-demand**: Summarizes company presence in a dataset.
6. **calculate-skill-gap**: Compares candidate skills against job requirements.
7. **calculate-job-market-summary**: Returns an aggregate descriptive view of the overall job market subset.

## Input/Output Examples
**Input (analyze-salary-data):**
```json
{
  "jobs": [
    {"job_id": "1", "salary_min": 60000, "salary_max": 80000, "currency": "USD"},
    {"job_id": "2", "salary_min": 75000, "salary_max": 95000, "currency": "USD"}
  ]
}
```
**Output:**
```json
{
  "success": true,
  "number_of_records": 2,
  "minimum_salary": 60000,
  "maximum_salary": 95000,
  "average_salary": 77500,
  "median_salary": 77500
}
```

## Installation
```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Configuration
All configuration variables are securely handled via environment constraints. See `.env.example` for details. Do not commit actual secrets.

## Running Tests
Ensure `pytest` is installed and run from the repository root:
```bash
pytest -q
```

## Validation
A Readiness Audit is included to verify structure and safety protocols. Run:
```bash
python -m verification.readiness_audit
```

## Security
- The agent does not execute user strings as code (`eval` and `exec` are avoided).
- Shell commands and subprocess bindings are strictly prohibited.
- Malformed data structures yield safe structured errors instead of exceptions or stack trace leaks.
- API secrets or access tokens are not hardcoded.

## Portability
Through its adapter layer (`contracts/adapter.py`), this agent can easily be hooked into OpenGAP compliant frameworks or adapted to crewAI, LangChain, and other runners without touching core logic.

## OpenGAP Compliance
This agent strives to comply with the OpenGAP git-native standard. Due to dynamic execution constraints during development, the schema validation against the live specification could not be officially certified on the current build runner.

## Limitations
- **No Live Scraping**: Requires pre-structured JSON-like job data.
- **No Exchange Rate Inference**: Multiple currencies without conversion inputs are handled independently.
- **No Guarantees**: Does not output deterministic "hireability" scores, only raw matching descriptive statistics.

## Project Structure
- `config/`: Environment configuration.
- `core/`: Agent orchestration and registry.
- `contracts/`: Data schemas and abstract classes.
- `tools/`: Deterministic business logic.
- `adapters/`: Interoperability layer.
- `tests/`: Pytest suite.
- `verification/`: Auditing scripts.

## Extension Guide
To add a new tool:
1. Create `tools/your-tool-name.py`
2. Extend `ToolContract` and implement `execute()`.
3. Add it to the test suite and update `agent.yaml`.
