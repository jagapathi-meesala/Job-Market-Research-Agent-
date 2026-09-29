# Job Market Research Agent Explainability

## analyze-job-listings

### Decision
This tool determines the total volume of job listings by executing a straightforward iteration over the `jobs` array. It calculates the final total by evaluating the strict length of the validated list.

### Inputs
The input for this tool is derived strictly from the provided YAML schema which expects an object containing a `jobs` array. Every element within this array must be a dictionary representing a single job listing to be valid.

### Limits
The tool is strictly limited to parsing the provided array length without performing any semantic natural language processing on the job titles. Because of this limitation, it cannot distinguish between high-quality listings and spam listings.

## analyze-skill-demand

### Decision
The agent decides the relative frequency of each skill by iterating through the listings and accumulating unique string occurrences into a frequency map. It then determines the final percentage by dividing the accumulated count by the total number of jobs.

### Inputs
The tool requires an input payload containing a `jobs` array, where each job dictionary may optionally contain `required_skills` and `preferred_skills` string arrays. The data must be structured explicitly in this format for the skills to be successfully extracted.

### Limits
The analysis is constrained to the exact spelling of the skills explicitly provided in the data. The tool does not use machine learning to infer related skills, meaning it will treat 'ReactJS' and 'React.js' as entirely separate entities unless pre-normalized.

## analyze-salary-data

### Decision
The agent groups the validated salary records by their currency string to ensure accurate, isolated mathematical calculations. It then applies standard statistical formulas to calculate the average, median, minimum, and maximum salary bands per currency.

### Inputs
The required input is a `jobs` array containing objects with numeric `salary_min` and `salary_max` fields alongside a string `currency` code. The tool strictly validates that these numerical ranges are well-formed and non-negative.

### Limits
The tool only processes numeric salaries and intentionally ignores records that omit salary information or contain contradictory bounds. It does not perform live foreign exchange currency conversions, meaning disparate currencies cannot be aggregated together.

## analyze-location-demand

### Decision
The execution logic processes the dataset by grouping job records according to strict string matching of the location field. The frequency map is populated by incrementing a counter every time an identical location string is encountered.

### Inputs
The tool ingests a `jobs` array containing objects with a `location` string field. The data source is solely the user-supplied payload, and no external geographical databases are queried.

### Limits
This analysis relies purely on exact textual matching and lacks spatial awareness. Consequently, it cannot infer that a remote job posted in 'New York, NY' belongs to the broader 'New York State' geographical region.

## analyze-company-demand

### Decision
The agent computes employer prevalence by mapping exact company string matches to an integer frequency counter. It processes the entire array sequentially to determine the total listing count attributed to each unique company string.

### Inputs
The expected input structure is a `jobs` array where individual listings contain a `company` string field representing the employer. The tool expects standard string data and safely ignores listings where the company name is omitted.

### Limits
The tool is limited to quantifying the volume of job listings without assessing employer reputation or listing quality. It does not access corporate registries to verify if two slightly differently spelled companies are actually the same corporate entity.

## calculate-skill-gap

### Decision
The tool calculates skill overlap by performing strict set intersection operations between the candidate's skills and the job's requirement sets. It computes the final match percentage by dividing the intersection size by the total number of required skills.

### Inputs
The YAML input schema mandates three arrays of strings: `candidate_skills`, `required_skills`, and an optional `preferred_skills` list. The tool relies exclusively on this localized structured data to perform its comparisons.

### Limits
The calculation uses case-insensitive string equality and does not employ semantic similarity matching. It cannot deduce that a candidate who knows 'Python' is implicitly qualified for general 'Programming' requirements.

## calculate-job-market-summary

### Decision
The agent generates the summary by orchestrating deterministic distinct-count operations across the extracted fields like companies, locations, and skills. It determines the final top-level metrics by aggregating the lengths of these unique deduplicated sets.

### Inputs
The tool accepts a master `jobs` array containing comprehensively structured job listings. The input must conform to the established standard dictionary schema for all underlying metrics to be accurately calculated.

### Limits
The generated summary is mathematically bounded by the provided dataset and reflects only that specific sample. It does not represent macroeconomic truths and cannot forecast broader labor market trends.

