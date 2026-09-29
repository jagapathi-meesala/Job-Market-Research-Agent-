from typing import Dict, Any
from contracts.tool_contract import ToolContract

class AnalyzeLocationDemandTool(ToolContract):
    @property
    def name(self) -> str:
        return "analyze-location-demand"
        
    @property
    def description(self) -> str:
        return "Analyze job distribution by location."
        
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
        
        location_counts = {}
        work_mode_counts = {}
        
        for job in jobs:
            loc = job.get("location", "")
            if not loc or not isinstance(loc, str) or loc.strip() == "":
                loc = "Unknown/Missing"
            else:
                loc = loc.strip()
                
            location_counts[loc] = location_counts.get(loc, 0) + 1
            
            wm = job.get("work_mode")
            if wm:
                work_mode_counts[wm] = work_mode_counts.get(wm, 0) + 1
                
        percentages = {loc: (count / total_jobs * 100) for loc, count in location_counts.items()} if total_jobs > 0 else {}
        
        top_locations = sorted(location_counts.items(), key=lambda x: x[1], reverse=True)[:10]
        
        return {
            "total_jobs": total_jobs,
            "job_counts_by_location": location_counts,
            "percentages_by_location": percentages,
            "remote_hybrid_onsite_distribution": work_mode_counts,
            "top_locations": dict(top_locations),
            "limitations": "These are descriptive statistics of the dataset only. Frequency does not imply a location is objectively better."
        }

def register(registry):
    registry.register(AnalyzeLocationDemandTool())
