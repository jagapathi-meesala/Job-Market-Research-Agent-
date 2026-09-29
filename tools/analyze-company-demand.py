from typing import Dict, Any
from contracts.tool_contract import ToolContract

class AnalyzeCompanyDemandTool(ToolContract):
    @property
    def name(self) -> str:
        return "analyze-company-demand"
        
    @property
    def description(self) -> str:
        return "Analyze structured job listings for company demand."
        
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
        
        company_counts = {}
        company_titles = {}
        
        for job in jobs:
            comp = job.get("company", "")
            if not comp or not isinstance(comp, str) or comp.strip() == "":
                comp = "Unknown/Missing"
            else:
                comp = comp.strip()
                
            title = job.get("title", "Unknown Role")
            
            company_counts[comp] = company_counts.get(comp, 0) + 1
            
            if comp not in company_titles:
                company_titles[comp] = set()
            company_titles[comp].add(title)
            
        unique_companies = len(company_counts)
        repeated_hiring_presence = sum(1 for c, count in company_counts.items() if count > 1)
        
        # Convert sets to lists for JSON serialization
        company_titles_list = {k: list(v) for k, v in company_titles.items()}
        
        # Sort companies by job count descending
        sorted_companies = sorted(company_counts.items(), key=lambda x: x[1], reverse=True)
        
        return {
            "total_jobs": total_jobs,
            "unique_companies": unique_companies,
            "jobs_per_company": dict(sorted_companies),
            "company_distribution": {
                comp: (count / total_jobs * 100) if total_jobs > 0 else 0 
                for comp, count in sorted_companies
            },
            "repeated_hiring_presence": repeated_hiring_presence,
            "company_title_combinations": company_titles_list,
            "limitations": "Statistics only reflect the provided dataset. We do NOT rank companies as 'best' or infer employer quality from listing frequency."
        }

def register(registry):
    registry.register(AnalyzeCompanyDemandTool())
