import os
import tempfile
from verification.readiness_audit import check_secrets

def test_no_hardcoded_secrets():
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "core"))
    for root, _, files in os.walk(base_dir):
        for file in files:
            if file.endswith(".py"):
                with open(os.path.join(root, file), "r") as f:
                    content = f.read()
                    assert "API_KEY=" not in content
                    assert "SECRET=" not in content

def test_no_eval_exec():
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "tools"))
    for root, _, files in os.walk(base_dir):
        for file in files:
            if file.endswith(".py"):
                with open(os.path.join(root, file), "r") as f:
                    content = f.read()
                    assert "eval(" not in content
                    assert "exec(" not in content
                    assert "subprocess" not in content

def test_scanner_detects_realistic_secret():
    """Test that a realistic hardcoded secret IS detected."""
    with tempfile.TemporaryDirectory() as tmpdir:
        test_file = os.path.join(tmpdir, "bad_file.py")
        with open(test_file, "w") as f:
            f.write("API_" + "KEY = 'sk-live-123456789'\n")
        
        issues = check_secrets(tmpdir)
        assert len(issues) == 1
        assert "Potential secret found" in issues[0]
        assert "sk-live-123456789" in issues[0]

def test_scanner_ignores_placeholders():
    """Test that documentation placeholders and environment fetches are ignored."""
    with tempfile.TemporaryDirectory() as tmpdir:
        test_file = os.path.join(tmpdir, "ok_file.py")
        with open(test_file, "w") as f:
            f.write("API_" + "KEY = 'your_api_key_here'\n")
            f.write("API_" + "KEY = os.environ.get('API_KEY')\n")
        
        issues = check_secrets(tmpdir)
        assert len(issues) == 0

def test_scanner_ignores_test_fixtures():
    """Test that intentional security-test fixtures are ignored."""
    with tempfile.TemporaryDirectory() as tmpdir:
        test_file = os.path.join(tmpdir, "test_ok_file.py")
        with open(test_file, "w") as f:
            f.write("API_" + "KEY = 'TEST_FIXTURE_123'\n")
            f.write("assert \"API_KEY=\" not in content\n")
            
        issues = check_secrets(tmpdir)
        assert len(issues) == 0

def test_scanner_prohibits_env_file():
    """Test that .env files are prohibited."""
    with tempfile.TemporaryDirectory() as tmpdir:
        env_file = os.path.join(tmpdir, ".env")
        with open(env_file, "w") as f:
            f.write("API_" + "KEY=xyz\n")
            
        issues = check_secrets(tmpdir)
        assert len(issues) == 1
        assert "Prohibited file found" in issues[0]
