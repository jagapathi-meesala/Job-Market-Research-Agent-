import pytest
from core.agent import AgentCore

@pytest.fixture
def agent():
    return AgentCore()
    
def test_analyze_job_listings_valid(agent):
    data = {
        "jobs": [
            {"job_id": "1", "title": "SE", "salary_min": 50000, "salary_max": 70000}
        ]
    }
    res = agent.execute_tool("analyze-job-listings", data)
    assert res["success"] is True
    assert res["total_jobs"] == 1
    
def test_analyze_job_listings_missing_id(agent):
    data = {"jobs": [{"title": "SE"}]}
    res = agent.execute_tool("analyze-job-listings", data)
    assert res["success"] is False
    
def test_analyze_job_listings_negative_salary(agent):
    data = {"jobs": [{"job_id": "1", "title": "SE", "salary_min": -500}]}
    res = agent.execute_tool("analyze-job-listings", data)
    assert res["success"] is False
    
def test_analyze_skill_demand(agent):
    data = {
        "jobs": [
            {"required_skills": ["Python", "AWS"], "preferred_skills": ["Docker"]}
        ]
    }
    res = agent.execute_tool("analyze-skill-demand", data)
    assert res["success"] is True
    assert res["total_jobs_analyzed"] == 1
    assert "Python" in res["skill_frequency"]

def test_analyze_salary_data(agent):
    data = {
        "jobs": [
            {"job_id": "1", "salary_min": 100, "salary_max": 200, "currency": "USD"}
        ]
    }
    res = agent.execute_tool("analyze-salary-data", data)
    assert res["success"] is True
    assert res["currencies"]["USD"]["average_salary"] == 150

def test_calculate_skill_gap(agent):
    data = {
        "candidate_skills": ["Python", "AWS", "Git"],
        "required_skills": ["Python", "AWS", "Docker"],
        "preferred_skills": ["Git", "Linux"]
    }
    res = agent.execute_tool("calculate-skill-gap", data)
    assert res["success"] is True
    assert "Python" in res["matched_required_skills"]
    assert "Docker" in res["missing_required_skills"]
    # 2 matched out of 3 required
    assert round(res["required_skill_match_percentage"], 2) == 66.67
    
def test_calculate_job_market_summary(agent):
    data = {
        "jobs": [
            {"company": "Tech Corp", "location": "NY"}
        ]
    }
    res = agent.execute_tool("calculate-job-market-summary", data)
    assert res["success"] is True
    assert res["total_jobs"] == 1
    assert res["unique_companies"] == 1
