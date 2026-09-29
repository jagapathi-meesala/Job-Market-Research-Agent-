from typing import Dict, Any
from contracts.tool_contract import ToolContract
import statistics

class CalculateJobMarketSummaryTool(ToolContract):
    @property
    def name(self) -> str:
        return "calculate-job-market-summary"
        
    @property
    def description(self) -> str:
        return "Produce a deterministic summary from supplied job-market records."
        
    def validate_input(self, input_data: Dict[str, Any]) -> bool:
        if "jobs" not in input_data or not isinstance(input_data["jobs"], list):
            raise ValueError("Input must contain a 'jobs' list.")
            
        for job in input_data["jobs"]:
            if not isinstance(job, dict):
                raise ValueError("Each job must be a dictionary.")
                
        return True

    def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        jobs = input_data["jobs"]
        total_jobs = len(jobs)
        
        unique_companies = set()
        unique_locations = set()
        common_skills = {}
        
        salaries = []
        
        work_mode_dist = {}
        emp_type_dist = {}
        exp_level_dist = {}
        
        for job in jobs:
            comp = job.get("company")
            if comp:
                unique_companies.add(comp.strip())
                
            loc = job.get("location")
            if loc:
                unique_locations.add(loc.strip())
                
            for skill in job.get("required_skills", []):
                common_skills[skill] = common_skills.get(skill, 0) + 1
                
            smin = job.get("salary_min")
            smax = job.get("salary_max")
            
            if smin is not None and smax is not None and smin <= smax:
                salaries.append((smin + smax) / 2)
            elif smin is not None:
                salaries.append(smin)
            elif smax is not None:
                salaries.append(smax)
                
            wm = job.get("work_mode", "Unknown")
            work_mode_dist[wm] = work_mode_dist.get(wm, 0) + 1
            
            et = job.get("employment_type", "Unknown")
            emp_type_dist[et] = emp_type_dist.get(et, 0) + 1
            
            el = job.get("experience_level", "Unknown")
            exp_level_dist[el] = exp_level_dist.get(el, 0) + 1
            
        top_skills = sorted(common_skills.items(), key=lambda x: x[1], reverse=True)[:10]
        
        salary_stats = {}
        if salaries:
            salary_stats = {
                "count": len(salaries),
                "min": min(salaries),
                "max": max(salaries),
                "average": sum(salaries) / len(salaries),
                "median": statistics.median(salaries)
            }
            
        return {
            "total_jobs": total_jobs,
            "unique_companies": len(unique_companies),
            "unique_locations": len(unique_locations),
            "common_skills": dict(top_skills),
            "salary_statistics": salary_stats,
            "work_mode_distribution": work_mode_dist,
            "employment_type_distribution": emp_type_dist,
            "experience_level_distribution": exp_level_dist,
            "major_descriptive_observations": [
                f"Analyzed {total_jobs} total jobs from the supplied dataset.",
                f"Found {len(unique_companies)} unique hiring entities.",
                f"Dataset spans {len(unique_locations)} unique locations.",
                f"Salary data was available for {len(salaries)} records."
            ],
            "limitations": "Every observation is strictly traceable to the supplied dataset. We do not produce unsupported predictions, forecast future market trends, or claim this represents the broader economy."
        }

def register(registry):
    registry.register(CalculateJobMarketSummaryTool())
