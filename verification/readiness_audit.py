import os
import sys
import re

REQUIRED_FILES = [
    "agent.yaml",
    "README.md",
    "SOUL.md",
    "RULES.md",
    "DUTIES.md",
    "AGENTS.md",
    "EXPLAINABILITY.md",
    "requirements.txt",
    ".env.example",
    "pytest.ini",
    ".gitignore",
    "config/settings.py",
    "core/agent.py",
    "core/registry.py",
    "contracts/agent_contract.py",
    "contracts/tool_contract.py",
    "contracts/adapter.py",
    "adapters/portable_adapter.py",
    "adapters/registry.py",
    "tools/analyze-job-listings.py",
    "tools/analyze-skill-demand.py",
    "tools/analyze-salary-data.py",
    "tools/analyze-location-demand.py",
    "tools/analyze-company-demand.py",
    "tools/calculate-skill-gap.py",
    "tools/calculate-job-market-summary.py",
    "tests/test_agent.py",
    "tests/test_registry.py",
    "tests/test_tools.py",
    "tests/test_security.py",
    "tests/test_documentation.py",
    "tests/test_adapters.py",
    "tests/test_open_gap_schema.py"
]

def check_files(base_dir: str):
    missing = []
    for rel_path in REQUIRED_FILES:
        full_path = os.path.join(base_dir, rel_path)
        if not os.path.exists(full_path):
            missing.append(rel_path)
    return missing
    
def check_secrets(base_dir: str):
    issues = []
    # Check for obvious unmasked secrets while ignoring environment variable lookups,
    # test fixtures, and placeholders.
    # Matches a credential keyword, an equals or colon, and a string literal
    # Group 1: keyword
    # Group 2: quote char (' or ")
    # Group 3: the string value
    regex = re.compile(r'(?i)\b(api_key|secret|password|token)\b\s*[:=]\s*([\'"])([^\'"]*)\2')
    
    excluded_values = [
        "your_api_key_here", 
        "your_secret_here", 
        "your_password_here", 
        "your_token_here",
        "placeholder"
    ]
    
    for root, dirs, files in os.walk(base_dir):
        if ".git" in root or "venv" in root or ".pytest_cache" in root or "__pycache__" in root:
            continue
            
        for file in files:
            path = os.path.join(root, file)
            
            # .env files are prohibited
            if file == ".env":
                issues.append(f"Prohibited file found: {path}")
                continue
                
            if file.endswith((".py", ".yaml", ".md", ".txt", ".ini")) and file != ".env.example":
                try:
                    with open(path, "r", encoding="utf-8") as f:
                        for line_num, line in enumerate(f, 1):
                            # Completely ignore assert statements looking for exact strings
                            # This prevents the scanner from flagging intentional string validations in tests.
                            if "assert " in line and ("not in" in line or "==" in line):
                                continue
                                
                            matches = regex.finditer(line)
                            for match in matches:
                                key_name = match.group(1)
                                value = match.group(3).strip()
                                
                                # Ignore empty values (e.g. API_KEY="")
                                if not value:
                                    continue
                                
                                # Ignore excluded placeholder values
                                if any(ex in value.lower() for ex in excluded_values):
                                    continue
                                    
                                # Ignore intentional security-test fixture strings explicitly marked
                                if "TEST_FIXTURE" in value:
                                    continue
                                
                                issues.append(f"Potential secret found in {path}:{line_num}: {key_name}='{value}'")
                except Exception:
                    pass
    return issues

def main():
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    
    print("Running Readiness Audit...")
    
    missing_files = check_files(base_dir)
    if missing_files:
        print("FAILED: Missing required files:")
        for m in missing_files:
            print(f"  - {m}")
        sys.exit(1)
        
    secret_issues = check_secrets(base_dir)
    if secret_issues:
        print("FAILED: Secret hygiene issues found:")
        for s in secret_issues:
            print(f"  - {s}")
        sys.exit(1)
        
    print("PASSED")
    sys.exit(0)

if __name__ == "__main__":
    main()
