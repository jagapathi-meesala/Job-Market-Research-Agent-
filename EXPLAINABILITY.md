# Job Market Research Agent Explainability

## analyze-job-listings

### Agent purpose
Analyze structured job listings to extract basic frequencies.

### Inputs
YAML schema expects an object with a `jobs` array containing job objects. Required: `jobs`.

### Decision/process
Iterates the `jobs` array to compute total count and extracts basic fields if valid.

### Limits
Does not perform NLP analysis on titles. Relies strictly on the array length and structure.

### Output contract
Dictionary containing `total_jobs` (int) and `success` (bool) plus a `message`.

### Complete execution lifecycle
Input adapter -> validate_input(jobs list exists) -> execute() counts list length -> return standard dict.

### Tool-by-tool decision/rule transparency
Formula: total_jobs = len(jobs). Rejects any non-list `jobs` payload.

### Tool-by-tool examples
Input: {"jobs": [{"job_id": "1", "title": "SE"}]}
Output: {"total_jobs": 1, "success": true, "message": "Successfully counted 1 jobs."}

### Explainability of calculated results
The output value `total_jobs` is exactly the length of the valid `jobs` array provided.

### Provenance
All data originates directly and exclusively from the user-supplied `jobs` payload.

### Failure handling
Raises ValueError if `jobs` is missing or not a list, or if a job lacks `job_id` or `title`.

### Validation behavior
Strictly type-checks that `jobs` is a list, and iterates to ensure every item is a dictionary.

### Security boundaries
Stateless execution. No eval, exec, or subprocess calls are made.

### Deterministic behavior
Given the exact same `jobs` list, the `len(jobs)` operation will inherently always return the exact same integer.

### Data assumptions
Assumes every job dictionary represents exactly one job listing.

### How inputs become outputs
The raw JSON array is loaded into a Python list, measured with `len()`, and serialized back to JSON.

### What the agent does NOT do
Does NOT fetch job listings from the internet. Does NOT guess titles.

## analyze-skill-demand

### Agent purpose
Analyze the demand for specific skills in job listings.

### Inputs
YAML schema expects a `jobs` array. Each job object may optionally contain `required_skills` and `preferred_skills` arrays. Required: `jobs`.

### Decision/process
Iterates jobs to count occurrences of strings in `required_skills` and `preferred_skills`, then calculates percentages.

### Limits
Only analyzes the skills explicitly provided. Case-sensitive depending on the input normalization.

### Output contract
Dictionary containing `total_jobs_analyzed`, `skill_frequency`, `skill_percentages`, etc.

### Complete execution lifecycle
Input adapter -> validate_input() -> execute() aggregates lists into sets and frequencies -> calculation of percentages -> return dict.

### Tool-by-tool decision/rule transparency
Formula: percentage = (skill_count / total_jobs) * 100.

### Tool-by-tool examples
Input: {"jobs": [{"required_skills": ["Python"]}]}
Output: {"total_jobs_analyzed": 1, "skill_frequency": {"Python": 1}, "skill_percentages": {"Python": 100.0}}

### Explainability of calculated results
Percentages are simple division of the frequency count by the total jobs parsed, multiplied by 100.

### Provenance
Skills are extracted purely from the `required_skills` and `preferred_skills` fields of the input.

### Failure handling
Raises ValueError if `jobs` is not a list or if `required_skills` is provided but is not a list.

### Validation behavior
Type-checks the `jobs` key and verifies nested skill fields are strictly list types if present.

### Security boundaries
Stateless map-reduce aggregation in memory with no external side effects.

### Deterministic behavior
Exact same input arrays will yield the exact same frequency dictionaries and percentages.

### Data assumptions
Assumes provided skills are correctly spelled. Treats 'Python' and 'python' as identical if normalized prior to input.

### How inputs become outputs
Iterates job dictionaries, populates Python `dict` with counts, divides by length of jobs list, and returns standard dictionary.

### What the agent does NOT do
Does NOT infer skills (e.g., seeing 'React' does not add 'JavaScript').

## analyze-salary-data

### Agent purpose
Analyze salary statistics from job listings.

### Inputs
YAML schema expects a `jobs` array. Jobs may have `salary_min`, `salary_max`, and `currency`. Required: `jobs`.

### Decision/process
Groups salaries by currency and calculates min, max, average, and median per currency group.

### Limits
Ignores jobs without valid numeric salaries or currency codes.

### Output contract
Dictionary of currencies containing `min`, `max`, `average`, `median`, and `count`.

### Complete execution lifecycle
Input adapter -> validate_input() -> execute() groups values -> standard math operations on groups -> return stats dictionary.

### Tool-by-tool decision/rule transparency
Formulas: average = sum(salaries)/len(salaries). Midpoint = (min+max)/2.

### Tool-by-tool examples
Input: {"jobs": [{"salary_min": 100, "salary_max": 200, "currency": "USD"}]}
Output: {"USD": {"average": 150.0, "min": 100, "max": 200}}

### Explainability of calculated results
The results are strict textbook statistical functions applied to the collected salary values.

### Provenance
Extracts explicitly provided `salary_min` and `salary_max` from the input payload.

### Failure handling
Raises ValueError if `salary_min` > `salary_max` or if salaries are negative.

### Validation behavior
Ensures `jobs` is a list and performs logical boundary checks on numerical salary values.

### Security boundaries
Math operations are standard Python float/int operations, protected from overflow attacks by framework limits.

### Deterministic behavior
Mathematical statistics on a static list are mathematically proven to be identical every run.

### Data assumptions
Assumes salaries represent annual values unless normalized differently by caller. No automatic currency conversion.

### How inputs become outputs
Numerical values are mapped into lists partitioned by string currency keys, processed by `sum()` and `len()`, and mapped to output keys.

### What the agent does NOT do
Does NOT perform real-time FX currency conversions.

## analyze-location-demand

### Agent purpose
Analyze location demand distribution (remote, hybrid, physical).

### Inputs
YAML schema expects a `jobs` array. Required: `jobs`.

### Decision/process
Groups jobs strictly by string matching the `location` field.

### Limits
Does not understand geographic hierarchy (e.g. 'NYC' is entirely distinct from 'New York').

### Output contract
Dictionary with location names as keys and integer frequencies as values.

### Complete execution lifecycle
Input adapter -> validate_input() -> execute() iterates to populate frequency dictionary -> return.

### Tool-by-tool decision/rule transparency
Formula: location_count = sum(1 for job in jobs if job.location == X).

### Tool-by-tool examples
Input: {"jobs": [{"location": "Remote"}, {"location": "Remote"}]}
Output: {"locations": {"Remote": 2}}

### Explainability of calculated results
It is a 1-to-1 reflection of how many times a given location string appeared in the array.

### Provenance
Locations are read directly from the `location` key of the job object.

### Failure handling
Raises ValueError for invalid payload structures.

### Validation behavior
Ensures `jobs` is a list of dicts. Safely ignores missing `location` fields or groups them as 'unknown'.

### Security boundaries
Executes entirely in memory with no external I/O.

### Deterministic behavior
String matching frequency counts on static data are mathematically deterministic.

### Data assumptions
Assumes the caller has standardized spelling if deduplication is expected.

### How inputs become outputs
Input list is traversed, strings are extracted, and a hash map (dictionary) accumulates the occurrences.

### What the agent does NOT do
Does NOT use mapping APIs to resolve coordinates or zip codes.

## analyze-company-demand

### Agent purpose
Analyze structured job listings for company demand.

### Inputs
YAML schema expects a `jobs` array. Required: `jobs`.

### Decision/process
Groups jobs strictly by string matching the `company` field.

### Limits
Only counts volume of listings, does not assess company quality.

### Output contract
Dictionary containing `jobs_per_company` with company names as keys and integers as values.

### Complete execution lifecycle
Input adapter -> validate_input() -> execute() iterates to populate frequency dictionary -> return.

### Tool-by-tool decision/rule transparency
Formula: company_count = sum(1 for job in jobs if job.company == X).

### Tool-by-tool examples
Input: {"jobs": [{"company": "TechCorp"}]}
Output: {"jobs_per_company": {"TechCorp": 1}}

### Explainability of calculated results
The results simply reflect the count of listings associated with that company string.

### Provenance
The company name is extracted directly from the user-supplied job object.

### Failure handling
Standard payload validation errors.

### Validation behavior
Validates list format. Handles missing company names safely.

### Security boundaries
Pure in-memory string comparison.

### Deterministic behavior
Hash map aggregation ensures exact identical outputs for identical inputs.

### Data assumptions
Assumes 'TechCorp' and 'Tech Corp' are different companies unless normalized by the caller.

### How inputs become outputs
Extracts the `company` field to serve as dictionary keys, incrementing their integer values.

### What the agent does NOT do
Does NOT search the internet to verify the company exists.

## calculate-skill-gap

### Agent purpose
Compare a candidate's supplied skills with required and preferred skills.

### Inputs
YAML schema expects `candidate_skills` (array of strings), `required_skills` (array of strings), and optional `preferred_skills` (array of strings). Required: `candidate_skills`, `required_skills`.

### Decision/process
Performs set intersections and differences between candidate skills and job skills.

### Limits
Matches are exact text representations (usually lowercased and stripped of whitespace). No semantic similarity matching.

### Output contract
Dictionary with match percentages, missing required skills, and missing preferred skills.

### Complete execution lifecycle
Input adapter -> validate_input() -> execute() generates sets -> calculates intersection/difference -> computes percentages -> returns.

### Tool-by-tool decision/rule transparency
Formula: required_match_percentage = (matched_required_skills / total_required_skills) * 100.

### Tool-by-tool examples
Input: {"candidate_skills": ["Python"], "required_skills": ["Python", "AWS"]}
Output: {"required_skill_match_percentage": 50.0, "missing_required_skills": ["AWS"]}

### Explainability of calculated results
The percentage is calculated by taking the length of the set intersection over the length of the required set.

### Provenance
Both the candidate skills and the required skills are supplied entirely by the input payload.

### Failure handling
Raises ValueError if required skills are missing (cannot calculate percentage).

### Validation behavior
Validates that all three skill fields are list types.

### Security boundaries
Standard Python set operations with no external risks.

### Deterministic behavior
Set mathematics guarantee the same intersections every run.

### Data assumptions
Assumes skills are directly comparable via string equality. Normalizes to lowercase for comparison.

### How inputs become outputs
Converts input lists to lowercase sets, applies `.intersection()` and `.difference()`, and maps results to output.

### What the agent does NOT do
Does NOT guess what a candidate might know based on their current skills.

## calculate-job-market-summary

### Agent purpose
Produce a deterministic summary from supplied job-market records.

### Inputs
YAML schema expects a `jobs` array. Required: `jobs`.

### Decision/process
Aggregates findings from the other analytical tools (companies, locations, skills) into a high-level summary overview.

### Limits
The summary is bounded strictly by the provided dataset and does not represent macroeconomic truths.

### Output contract
Dictionary containing unique counts and top-level summary metrics.

### Complete execution lifecycle
Input adapter -> validate_input() -> execute() aggregates data from all fields -> return dictionary.

### Tool-by-tool decision/rule transparency
Formulas: combinations of unique sets via `len(set(items))`.

### Tool-by-tool examples
Input: {"jobs": [{"company": "A", "location": "B", "required_skills": ["C"]}]}
Output: {"unique_companies": 1, "unique_locations": 1, "total_jobs": 1}

### Explainability of calculated results
Metrics are simple distinct counts (length of sets) from the payload.

### Provenance
All summary metrics are strictly aggregated from the provided job array.

### Failure handling
Standard payload validation errors if the array is missing or malformed.

### Validation behavior
Ensures the input is a valid list of dictionaries.

### Security boundaries
Operates fully in memory.

### Deterministic behavior
Aggregating a static array into a set yields a mathematically deterministic size.

### Data assumptions
Empty strings or missing fields are omitted from unique counts.

### How inputs become outputs
Extracts fields, adds them to unique `set` objects, and returns their `.length`.

### What the agent does NOT do
Does NOT write summary reports using a Large Language Model.

