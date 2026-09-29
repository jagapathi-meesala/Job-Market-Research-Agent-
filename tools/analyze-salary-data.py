from typing import Dict, Any
from contracts.tool_contract import ToolContract
import statistics

class AnalyzeSalaryDataTool(ToolContract):
    @property
    def name(self) -> str:
        return "analyze-salary-data"
        
    @property
    def description(self) -> str:
        return "Analyze salary data from structured job salary records."
        
    def validate_input(self, input_data: Dict[str, Any]) -> bool:
        if "jobs" not in input_data or not isinstance(input_data["jobs"], list):
            raise ValueError("Input must contain a 'jobs' list.")
            
        for job in input_data["jobs"]:
            if not isinstance(job, dict):
                raise ValueError("Each job must be a dictionary.")
                
            sal_min = job.get("salary_min")
            sal_max = job.get("salary_max")
            
            if sal_min is not None and not isinstance(sal_min, (int, float)):
                raise ValueError("salary_min must be a number.")
            if sal_max is not None and not isinstance(sal_max, (int, float)):
                raise ValueError("salary_max must be a number.")
                
            if sal_min is not None and sal_min < 0:
                raise ValueError("Negative salary not allowed.")
            if sal_max is not None and sal_max < 0:
                raise ValueError("Negative salary not allowed.")
            if sal_min is not None and sal_max is not None and sal_min > sal_max:
                raise ValueError("salary_min cannot be greater than salary_max.")
                
        return True

    def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        jobs = input_data["jobs"]
        
        # Group by currency
        # Since we cannot convert currencies automatically, we evaluate them separately
        currency_groups = {}
        
        for job in jobs:
            sal_min = job.get("salary_min")
            sal_max = job.get("salary_max")
            
            if sal_min is None and sal_max is None:
                continue
                
            currency = job.get("currency", "UNKNOWN")
            loc = job.get("location", "UNKNOWN")
            exp = job.get("experience_level", "UNKNOWN")
            
            midpoint = None
            if sal_min is not None and sal_max is not None:
                midpoint = (sal_min + sal_max) / 2
            elif sal_min is not None:
                midpoint = sal_min
            elif sal_max is not None:
                midpoint = sal_max
                
            if currency not in currency_groups:
                currency_groups[currency] = {
                    "salaries": [],
                    "by_location": {},
                    "by_experience": {}
                }
                
            group = currency_groups[currency]
            group["salaries"].append(midpoint)
            
            if loc not in group["by_location"]:
                group["by_location"][loc] = []
            group["by_location"][loc].append(midpoint)
            
            if exp not in group["by_experience"]:
                group["by_experience"][exp] = []
            group["by_experience"][exp].append(midpoint)
            
        results = {}
        
        for curr, data in currency_groups.items():
            sals = data["salaries"]
            if not sals:
                continue
                
            results[curr] = {
                "number_of_records": len(sals),
                "minimum_salary": min(sals),
                "maximum_salary": max(sals),
                "average_salary": sum(sals) / len(sals),
                "median_salary": statistics.median(sals),
                "salary_range_statistics": {
                    "spread": max(sals) - min(sals)
                },
                "statistics_by_location": {
                    l: sum(v)/len(v) for l, v in data["by_location"].items() if v
                },
                "statistics_by_experience": {
                    e: sum(v)/len(v) for e, v in data["by_experience"].items() if v
                }
            }
            
        return {
            "currencies": results,
            "total_records_processed": len(jobs),
            "limitations": "Salaries are not real-world current market values unless the dataset itself contains real-world current market values. Currency conversion is not performed."
        }

def register(registry):
    registry.register(AnalyzeSalaryDataTool())
