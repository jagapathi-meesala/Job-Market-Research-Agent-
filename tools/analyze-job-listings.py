from typing import Dict, Any, List
from contracts.tool_contract import ToolContract

class AnalyzeJobListingsTool(ToolContract):
    @property
    def name(self) -> str:
        return "analyze-job-listings"
        
    @property
    def description(self) -> str:
        return "Analyze a structured collection of job listings."
        
    def validate_input(self, input_data: Dict[str, Any]) -> bool:
        if "jobs" not in input_data or not isinstance(input_data["jobs"], list):
            raise ValueError("Input must contain a 'jobs' list.")
            
        seen_ids = set()
        for job in input_data["jobs"]:
            if not isinstance(job, dict):
                raise ValueError("Each job must be a dictionary.")
            
            job_id = job.get("job_id")
            title = job.get("title")
            
            if not job_id:
                raise ValueError("All jobs must have a 'job_id'.")
            if not title:
                raise ValueError(f"Job {job_id} must have a 'title'.")
            
            if job_id in seen_ids:
                raise ValueError(f"Duplicate job_id detected: {job_id}")
            seen_ids.add(job_id)
            
            # Numeric validation
            sal_min = job.get("salary_min")
            sal_max = job.get("salary_max")
            
            if sal_min is not None and not isinstance(sal_min, (int, float)):
                raise ValueError(f"Job {job_id} has invalid salary_min type.")
            if sal_max is not None and not isinstance(sal_max, (int, float)):
                raise ValueError(f"Job {job_id} has invalid salary_max type.")
                
            if sal_min is not None and sal_min < 0:
                raise ValueError(f"Job {job_id} has negative salary_min.")
            if sal_max is not None and sal_max < 0:
                raise ValueError(f"Job {job_id} has negative salary_max.")
            if sal_min is not None and sal_max is not None and sal_min > sal_max:
                raise ValueError(f"Job {job_id} has salary_min > salary_max.")
                
            exp_min = job.get("experience_min")
            exp_max = job.get("experience_max")
            
            if exp_min is not None and not isinstance(exp_min, (int, float)):
                raise ValueError(f"Job {job_id} has invalid experience_min type.")
            if exp_max is not None and not isinstance(exp_max, (int, float)):
                raise ValueError(f"Job {job_id} has invalid experience_max type.")
            if exp_min is not None and exp_min < 0:
                raise ValueError(f"Job {job_id} has negative experience_min.")
            if exp_max is not None and exp_max < 0:
                raise ValueError(f"Job {job_id} has negative experience_max.")
            if exp_min is not None and exp_max is not None and exp_min > exp_max:
                raise ValueError(f"Job {job_id} has experience_min > experience_max.")
                
            req_skills = job.get("required_skills")
            if req_skills is not None and not isinstance(req_skills, list):
                raise ValueError(f"Job {job_id} has malformed required_skills list.")
                
        return True

    def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        jobs = input_data["jobs"]
        
        total_jobs = len(jobs)
        emp_type_counts = {}
        work_mode_counts = {}
        location_counts = {}
        company_counts = {}
        title_counts = {}
        
        total_exp_min = 0
        exp_min_count = 0
        
        sal_provided_count = 0
        
        all_skills = {}
        
        for job in jobs:
            emp_type = job.get("employment_type", "Unknown")
            emp_type_counts[emp_type] = emp_type_counts.get(emp_type, 0) + 1
            
            work_mode = job.get("work_mode", "Unknown")
            work_mode_counts[work_mode] = work_mode_counts.get(work_mode, 0) + 1
            
            loc = job.get("location", "Unknown")
            location_counts[loc] = location_counts.get(loc, 0) + 1
            
            comp = job.get("company", "Unknown")
            company_counts[comp] = company_counts.get(comp, 0) + 1
            
            title = job.get("title")
            title_counts[title] = title_counts.get(title, 0) + 1
            
            exp_min = job.get("experience_min")
            if exp_min is not None:
                total_exp_min += exp_min
                exp_min_count += 1
                
            if job.get("salary_min") is not None or job.get("salary_max") is not None:
                sal_provided_count += 1
                
            for skill in job.get("required_skills", []):
                all_skills[skill] = all_skills.get(skill, 0) + 1
                
        avg_exp = total_exp_min / exp_min_count if exp_min_count > 0 else None
        
        common_titles = sorted(title_counts.items(), key=lambda x: x[1], reverse=True)[:5]
        common_titles_dict = {k: v for k, v in common_titles}
        
        common_skills_list = sorted(all_skills.items(), key=lambda x: x[1], reverse=True)[:10]
        common_skills_dict = {k: v for k, v in common_skills_list}
        
        return {
            "total_jobs": total_jobs,
            "jobs_by_employment_type": emp_type_counts,
            "jobs_by_work_mode": work_mode_counts,
            "jobs_by_location": location_counts,
            "jobs_by_company": company_counts,
            "common_titles": common_titles_dict,
            "average_experience_requirement": avg_exp,
            "salary_availability_statistics": {
                "provided_count": sal_provided_count,
                "provided_percentage": (sal_provided_count / total_jobs * 100) if total_jobs > 0 else 0
            },
            "common_skills": common_skills_dict,
            "structured_findings": "Analysis completed deterministically based on supplied records."
        }

def register(registry):
    registry.register(AnalyzeJobListingsTool())
