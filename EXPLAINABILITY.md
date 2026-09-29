# Job Market Research Agent Explainability

## Agent Purpose
The Job Market Research Agent is designed to process and analyze structured job-market datasets. Its primary purpose is to provide clear, deterministic, and explainable summaries (such as salary statistics and skill frequency distributions) without relying on unpredictable or opaque systems.

## Inputs
All inputs to the agent and its underlying tools are expected to be structured data payloads (exclusively JSON or Python dictionaries). The agent does NOT parse raw HTML, scrape live websites, or execute web requests.

## Decision/Process
The agent does not "decide" things using machine learning or a probabilistic AI model. Its process is purely calculative and deterministic. Decisions made by the agent are limited to validation logic (e.g., "Is this salary positive?", "Does the job object contain an ID?").

## Limits
- **No live access:** Cannot pull real-time data from the web.
- **No data transformation:** Cannot convert currencies automatically without external conversion rates being provided.
- **No forecasting:** Cannot guarantee job outcomes or predict future trends.
- **Scope limitation:** Statistics represent ONLY the isolated dataset provided, and do not reflect broader macroeconomic conditions.

## Output Contract
All outputs will be structured dictionaries containing standard primitive types (`int`, `float`, `list`, `dict`, `str`) representing descriptive statistics, along with a `success` boolean to indicate whether the operation completed without encountering validation errors.

## Complete Execution Lifecycle
1. Payload is received by the framework adapter.
2. The adapter validates and formats the payload into standard structures for the `AgentCore`.
3. `AgentCore` looks up and retrieves the requested tool from the `DynamicToolRegistry`.
4. The requested tool strictly validates the payload. If the payload is invalid, the tool immediately returns a structured error.
5. The tool performs standard, deterministic mathematical operations (e.g., aggregations, intersections).
6. The tool returns a structured response containing the calculated metrics.
7. The adapter translates the response back to the caller format.

## Tool-by-Tool Decision/Rule Transparency and Examples

### 1. analyze-job-listings
- **Agent purpose**: Count and aggregate overall listings.
- **Inputs**: `jobs` (array of objects).
- **Decision/process**: Simple frequency counting based on array length.
- **Limits**: Relies solely on the length and presence of fields in the `jobs` list.
- **Output contract**: Returns `total_jobs` (int).
- **Formula**: `total_jobs = len(jobs)`
- **Tool-by-tool example**: 
  - Input: `{"jobs": [{"job_id": "1", "title": "SE"}]}`
  - Output: `{"total_jobs": 1, ...}`
- **Explainability**: Output is exactly the number of valid dictionaries passed.

### 2. analyze-skill-demand
- **Agent purpose**: Calculate how often skills appear.
- **Inputs**: `jobs` (array of objects containing `required_skills` and `preferred_skills`).
- **Decision/process**: Iterates through each job and counts unique occurrences of skills.
- **Limits**: Case-sensitive if data is not normalized.
- **Output contract**: Returns counts and percentages for each skill.
- **Formula**: `percentage = (skill_count / total_jobs) * 100`
- **Tool-by-tool example**: 
  - Input: `{"jobs": [{"required_skills": ["Python"]}]}`
  - Output: `{"skill_percentages": {"Python": 100.0}, ...}`
- **Explainability**: Direct division of occurrences by total job array size.

### 3. analyze-salary-data
- **Agent purpose**: Compute salary statistics grouped by currency.
- **Inputs**: `jobs` (array of objects with `salary_min`, `salary_max`, `currency`).
- **Decision/process**: Sorts and averages salary data. Groups by currency.
- **Limits**: Ignores jobs without valid numeric salaries.
- **Output contract**: Min, max, average, median per currency.
- **Formula**: `average = sum(salaries) / count(salaries)`, `salary_midpoint = (salary_min + salary_max) / 2`
- **Tool-by-tool example**:
  - Input: `{"jobs": [{"salary_min": 100, "salary_max": 200, "currency": "USD"}]}`
  - Output: `{"currencies": {"USD": {"average_salary": 150.0}}, ...}`
- **Explainability**: Standard statistical aggregations strictly mapped to the provided numbers.

### 4. analyze-location-demand
- **Agent purpose**: Group jobs by geographical location or work mode.
- **Inputs**: `jobs` (array of objects).
- **Decision/process**: Groups exact string matches of the `location` field.
- **Limits**: Does not perform geographical mapping (e.g., "NY" and "New York" are separate).
- **Output contract**: Counts per location string.
- **Formula**: `location_count = sum(1 for job in jobs if job.location == X)`
- **Tool-by-tool example**:
  - Input: `{"jobs": [{"location": "Remote"}]}`
  - Output: `{"locations": {"Remote": 1}, ...}`
- **Explainability**: Simple key-value frequency dictionary.

### 5. analyze-company-demand
- **Agent purpose**: Evaluate the presence of employers in the dataset.
- **Inputs**: `jobs` (array of objects).
- **Decision/process**: Counts occurrences of the `company` field.
- **Limits**: Does not rank employer quality, only volume of listings.
- **Output contract**: Job count per company.
- **Formula**: `company_count = sum(1 for job in jobs if job.company == X)`
- **Tool-by-tool example**:
  - Input: `{"jobs": [{"company": "Tech Corp"}]}`
  - Output: `{"jobs_per_company": {"Tech Corp": 1}, ...}`
- **Explainability**: Output is a direct sum of occurrences in the input list.

### 6. calculate-skill-gap
- **Agent purpose**: Identify matches between a candidate and a job.
- **Inputs**: `candidate_skills` (list of strings), `required_skills` (list of strings), `preferred_skills` (list of strings).
- **Decision/process**: Performs set intersection between candidate skills and required/preferred skills. Case-insensitive matching.
- **Limits**: Cannot infer skills (e.g., knowing "React" does not automatically grant "JavaScript").
- **Output contract**: Match percentages and missing skill lists.
- **Formula**: `required_match_percentage = matched_required_skills / total_required_skills * 100`
- **Tool-by-tool example**:
  - Input: `{"candidate_skills": ["Python"], "required_skills": ["Python", "AWS"]}`
  - Output: `{"required_skill_match_percentage": 50.0, "missing_required_skills": ["AWS"], ...}`
- **Explainability**: Set intersection size divided by required set size.

### 7. calculate-job-market-summary
- **Agent purpose**: High-level market overview.
- **Inputs**: `jobs` (array of objects).
- **Decision/process**: Aggregates total jobs, unique companies, unique locations, and global top skills.
- **Limits**: Summary applies exclusively to the supplied dataset.
- **Output contract**: Total counts, salary statistics, and categorical distributions.
- **Formula**: Combination of `len()` operations across unique sets.
- **Tool-by-tool example**:
  - Input: `{"jobs": [{"company": "A", "location": "B", "required_skills": ["C"]}]}`
  - Output: `{"unique_companies": 1, "unique_locations": 1, ...}`
- **Explainability**: Values strictly equal to the length of deduplicated sets extracted from the payload.

## Explainability of Calculated Results
Every number generated by this agent can be manually verified by reviewing the source payload and applying the documented formulas. Calculations are fully transparent. There are no black-box weights, no probabilistic inferences, and no non-deterministic AI processes involved in the core metrics.

## Provenance
- **Source**: Exclusively user-supplied structured data payloads.
- **Derived**: All metrics, percentages, medians, and averages are deterministically derived from the source payload.
- **External**: The agent utilizes no external APIs, databases, or third-party dependencies to retrieve information.

## Failure Handling
In the event of anomalous or missing data:
1. Missing optional fields (e.g., `preferred_skills`) are handled safely and treated as empty collections.
2. Missing required fields (e.g., `jobs` list) result in an immediate, explicit `ValueError` that is gracefully caught by the tool wrapper.
3. The wrapper returns `{ "success": false, "error_type": "ValueError", "message": "..." }` preventing runtime panics.

## Validation Behavior
All tools execute a strict `validate_input` method prior to running business logic.
- Type enforcement: Ensures `jobs` is a list, and individual elements are dictionaries.
- Mathematical safety: Ensures division operations never divide by zero (e.g., when calculating match percentages against empty requirements).

## Security Boundaries
- **No execution**: The agent absolutely prohibits the use of `eval()`, `exec()`, or `subprocess` commands.
- **No environment leak**: The agent never reads environment variables except for explicit, secure configurations.
- **Data isolation**: Tool executions are completely stateless.

## Deterministic Behavior
The agent guarantees identical output for identical input. Re-running the agent with the exact same payload will unconditionally result in the exact same mathematical summary. 

## Data Assumptions
- Salaries represent annual values if not explicitly marked.
- Deduplication relies on exact string matching (case-insensitive for skills, but exact for locations and companies unless standardized by the caller).
- Empty strings are treated as valid missing data ("Unknown").

## How Inputs Become Outputs
Input JSON lists are iterated sequentially in memory. Fields are extracted into Python primitives (sets, dictionaries, lists) for counting and statistical mapping. The final state of these primitives is serialized directly back into the output JSON dictionary. 

## What the Agent Does NOT Do
- The agent **does NOT** require or utilize an LLM (Large Language Model) to execute its core mathematical functionality.
- The agent **does NOT** use external APIs to enrich data.
- The agent **does NOT** perform autonomous machine-learning predictions or forecasts.
- The agent **does NOT** guarantee hiring success.
- The agent **does NOT** feature unstructured natural language reasoning; all inputs and outputs must strictly conform to schemas.

## Checkpoint 2 Self-Audit

| Requirement | Present? | Exact section | Evidence |
|-------------|----------|---------------|----------|
| Agent purpose | PASS | Agent Purpose | Clearly defines deterministic analysis purpose. |
| Inputs | PASS | Inputs | Defines inputs as structured data payloads exclusively. |
| Decision/process | PASS | Decision/Process | Explains decisions are purely validation/math logic. |
| Limits | PASS | Limits | Lists 4 explicit limits regarding scope and data capabilities. |
| Output contract | PASS | Output Contract | Details structured primitive dictionary returns. |
| Complete execution lifecycle | PASS | Complete Execution Lifecycle | 7-step breakdown from payload to return. |
| Tool-by-tool decision/rule transparency | PASS | Tool-by-Tool Decision/Rule... | Rules and formulas listed for all 7 tools. |
| Tool-by-tool examples | PASS | Tool-by-Tool Decision/Rule... | Example I/O provided for all 7 tools. |
| Explainability of calculated results | PASS | Explainability of Calculated Results | States absence of black boxes; manual verification possible. |
| Provenance | PASS | Provenance | Traces origins exclusively to user data. |
| Failure handling | PASS | Failure Handling | Documents safe error catching and JSON error returns. |
| Validation behavior | PASS | Validation Behavior | Details type enforcement and math safety checks. |
| Security boundaries | PASS | Security Boundaries | Verifies prohibition of eval/exec/subprocess. |
| Deterministic behavior | PASS | Deterministic Behavior | Guarantees identical output for identical input. |
| Data assumptions | PASS | Data Assumptions | Details case-sensitivity and deduplication rules. |
| How inputs become outputs | PASS | How Inputs Become Outputs | Traces JSON list ingestion to memory to output JSON. |
| What the agent does NOT do | PASS | What the Agent Does NOT Do | Explicitly denies LLM usage, API calls, and forecasting. |
