from typing import Dict, Any, List
from contracts.tool_contract import ToolContract

class CalculateSkillGapTool(ToolContract):
    @property
    def name(self) -> str:
        return "calculate-skill-gap"
        
    @property
    def description(self) -> str:
        return "Compare a candidate's supplied skills with required and preferred skills."
        
    def validate_input(self, input_data: Dict[str, Any]) -> bool:
        cand_skills = input_data.get("candidate_skills")
        req_skills = input_data.get("required_skills")
        pref_skills = input_data.get("preferred_skills")
        
        if cand_skills is None or not isinstance(cand_skills, list):
            raise ValueError("Input must contain a 'candidate_skills' list.")
            
        if req_skills is None or not isinstance(req_skills, list):
            raise ValueError("Input must contain a 'required_skills' list.")
            
        if pref_skills is not None and not isinstance(pref_skills, list):
            raise ValueError("If provided, 'preferred_skills' must be a list.")
            
        return True

    def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        cand_skills = set(s.lower().strip() for s in input_data["candidate_skills"])
        
        req_skills_raw = input_data["required_skills"]
        req_skills = set(s.lower().strip() for s in req_skills_raw)
        
        pref_skills_raw = input_data.get("preferred_skills", [])
        pref_skills = set(s.lower().strip() for s in pref_skills_raw)
        
        matched_required = req_skills.intersection(cand_skills)
        missing_required = req_skills.difference(cand_skills)
        
        matched_preferred = pref_skills.intersection(cand_skills)
        missing_preferred = pref_skills.difference(cand_skills)
        
        total_req = len(req_skills)
        if total_req == 0:
            req_match_pct = None
            req_pct_message = "Percentage cannot be meaningfully calculated because there are zero required skills."
        else:
            req_match_pct = (len(matched_required) / total_req) * 100
            req_pct_message = "Successfully calculated."
            
        total_pref = len(pref_skills)
        if total_pref == 0:
            pref_match_pct = None
        else:
            pref_match_pct = (len(matched_preferred) / total_pref) * 100
            
        # Map lowercased sets back to original casing where possible for output
        # For missing ones, we know the original casing from the raw list.
        # For matched ones, we use the raw list to keep the job's casing convention.
        
        def restore_case(skill_set, original_list):
            return [orig for orig in original_list if orig.lower().strip() in skill_set]
            
        return {
            "matched_required_skills": restore_case(matched_required, req_skills_raw),
            "missing_required_skills": restore_case(missing_required, req_skills_raw),
            "matched_preferred_skills": restore_case(matched_preferred, pref_skills_raw),
            "missing_preferred_skills": restore_case(missing_preferred, pref_skills_raw),
            "required_skill_match_percentage": req_match_pct,
            "required_skill_message": req_pct_message,
            "preferred_skill_match_percentage": pref_match_pct,
            "transparent_calculation": "required_match_percentage = matched_required_skills / total_required_skills * 100",
            "limitations": "These are strictly deterministic match calculations. We do not make hiring predictions, claim the candidate will get the job, infer personal characteristics, or fabricate skills."
        }

def register(registry):
    registry.register(CalculateSkillGapTool())
