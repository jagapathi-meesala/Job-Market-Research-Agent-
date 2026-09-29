from typing import Dict, Any, List
from contracts.tool_contract import ToolContract

class AnalyzeSkillDemandTool(ToolContract):
    @property
    def name(self) -> str:
        return "analyze-skill-demand"
        
    @property
    def description(self) -> str:
        return "Determine the frequency of skills across supplied job listings."
        
    def validate_input(self, input_data: Dict[str, Any]) -> bool:
        if "jobs" not in input_data or not isinstance(input_data["jobs"], list):
            raise ValueError("Input must contain a 'jobs' list.")
            
        for job in input_data["jobs"]:
            if not isinstance(job, dict):
                raise ValueError("Each job must be a dictionary.")
            
            req_skills = job.get("required_skills")
            pref_skills = job.get("preferred_skills")
            
            if req_skills is not None and not isinstance(req_skills, list):
                raise ValueError("required_skills must be a list.")
            if pref_skills is not None and not isinstance(pref_skills, list):
                raise ValueError("preferred_skills must be a list.")
                
        return True

    def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        jobs = input_data["jobs"]
        total_jobs = len(jobs)
        
        req_freq = {}
        pref_freq = {}
        overall_freq = {}
        
        for job in jobs:
            job_skills = set()
            
            for skill in job.get("required_skills", []):
                req_freq[skill] = req_freq.get(skill, 0) + 1
                job_skills.add(skill)
                
            for skill in job.get("preferred_skills", []):
                pref_freq[skill] = pref_freq.get(skill, 0) + 1
                job_skills.add(skill)
                
            for skill in job_skills:
                overall_freq[skill] = overall_freq.get(skill, 0) + 1
                
        percentages = {}
        for skill, count in overall_freq.items():
            percentages[skill] = (count / total_jobs * 100) if total_jobs > 0 else 0
            
        top_skills = sorted(overall_freq.keys(), key=lambda k: overall_freq[k], reverse=True)
        
        return {
            "total_jobs_analyzed": total_jobs,
            "skill_frequency": overall_freq,
            "required_skill_frequency": req_freq,
            "preferred_skill_frequency": pref_freq,
            "skill_percentages": percentages,
            "top_skills": top_skills[:20], # Return top 20 for brevity
            "supporting_counts": overall_freq,
            "limitations": "Results represent ONLY the supplied dataset and should not be construed as industry-wide demand unless the dataset captures the entire industry."
        }

def register(registry):
    registry.register(AnalyzeSkillDemandTool())
