# validate_hackathon_requirements.py
"""
Validator for OpenEnv Email Triage Hackathon Requirements.
Checks all pre-submission validation criteria.
"""

import yaml
import os
import json
import subprocess

def check_openenv_yaml():
    """Check if openenv.yaml exists and is valid."""
    print("\n[1] Checking openenv.yaml...")
    if not os.path.exists("openenv.yaml"):
        print("  ✗ openenv.yaml not found")
        return False
    
    try:
        with open("openenv.yaml") as f:
            config = yaml.safe_load(f)
        
        required_fields = ["name", "version", "entrypoint", "observation_model", "action_model", "reward_model", "tasks"]
        missing = [f for f in required_fields if f not in config]
        
        if missing:
            print(f"  ✗ Missing fields in openenv.yaml: {missing}")
            return False
        
        if len(config["tasks"]) < 3:
            print(f"  ✗ Less than 3 tasks defined (found {len(config['tasks'])})")
            return False
        
        print(f"  ✓ openenv.yaml valid with {len(config['tasks'])} tasks")
        return True
    except Exception as e:
        print(f"  ✗ Error reading openenv.yaml: {e}")
        return False


def check_typed_models():
    """Check if typed models are defined."""
    print("\n[2] Checking typed models...")
    try:
        from env.models import Observation, Action, Reward, Email
        print(f"  ✓ Observation model defined")
        print(f"  ✓ Action model defined")
        print(f"  ✓ Reward model defined")
        print(f"  ✓ Email model defined")
        return True
    except Exception as e:
        print(f"  ✗ Error importing models: {e}")
        return False


def check_environment_api():
    """Check if environment implements step/reset/state."""
    print("\n[3] Checking environment API...")
    try:
        from env.environment import EmailEnv
        from env.tasks import EasyTask
        
        env = EmailEnv(EasyTask())
        
        # Check reset
        obs = env.reset()
        print(f"  ✓ reset() works")
        
        # Check state
        state = env.state()
        print(f"  ✓ state() works")
        
        return True
    except Exception as e:
        print(f"  ✗ Error with environment API: {e}")
        return False


def check_tasks_and_graders():
    """Check if 3+ tasks exist with graders."""
    print("\n[4] Checking tasks and graders...")
    try:
        from env.tasks import EasyTask, MediumTask, HardTask
        
        tasks = [EasyTask(), MediumTask(), HardTask()]
        print(f"  ✓ Found {len(tasks)} tasks")
        
        for task in tasks:
            if not hasattr(task, 'get_expected_actions'):
                print(f"  ✗ Task {task.__class__.__name__} missing get_expected_actions()")
                return False
            
            expected = task.get_expected_actions()
            if not isinstance(expected, dict) or not expected:
                print(f"  ✗ Task {task.__class__.__name__} grader not working")
                return False
            
            print(f"  ✓ {task.__class__.__name__} with grader (expects {len(expected)} emails)")
        
        return True
    except Exception as e:
        print(f"  ✗ Error checking tasks: {e}")
        return False


def check_dockerfile():
    """Check if Dockerfile exists."""
    print("\n[5] Checking Dockerfile...")
    if not os.path.exists("Dockerfile"):
        print("  ✗ Dockerfile not found")
        return False
    
    try:
        with open("Dockerfile") as f:
            content = f.read()
        
        required = ["FROM", "WORKDIR", "COPY", "RUN", "CMD"]
        missing = [r for r in required if r not in content]
        
        if missing:
            print(f"  ✗ Dockerfile missing: {missing}")
            return False
        
        if "uvicorn" not in content and "fastapi" not in content:
            print("  ✗ Dockerfile doesn't mention FastAPI/uvicorn")
            return False
        
        print("  ✓ Dockerfile valid")
        return True
    except Exception as e:
        print(f"  ✗ Error reading Dockerfile: {e}")
        return False


def check_baseline_script():
    """Check if inference.py exists and imports correctly."""
    print("\n[6] Checking baseline inference script...")
    if not os.path.exists("inference.py"):
        print("  ✗ inference.py not found")
        return False
    
    try:
        with open("inference.py") as f:
            content = f.read()
        
        required = ["EasyTask", "MediumTask", "HardTask", "OpenAI"]
        missing = [r for r in required if r not in content]
        
        if missing:
            print(f"  ✗ inference.py missing: {missing}")
            return False
        
        print("  ✓ inference.py structure valid")
        return True
    except Exception as e:
        print(f"  ✗ Error reading inference.py: {e}")
        return False


def check_env_config():
    """Check if environment variables are properly configured."""
    print("\n[7] Checking environment configuration...")
    try:
        from env.config import validate_config
        
        # Check that validate_config function exists
        print("  ✓ env.config module has validate_config()")
        
        # Check .env.example
        if not os.path.exists(".env.example"):
            print("  ✗ .env.example not found")
            return False
        print("  ✓ .env.example found")
        
        return True
    except Exception as e:
        print(f"  ✗ Error with environment config: {e}")
        return False


def check_readme():
    """Check if README exists with setup instructions."""
    print("\n[8] Checking README...")
    if not os.path.exists("readme.md"):
        print("  ✗ readme.md not found")
        return False
    
    try:
        with open("readme.md") as f:
            content = f.read().lower()
        
        required = ["setup", "install", "task"]
        missing = [r for r in required if r not in content]
        
        if missing:
            print(f"  ✗ README missing sections: {missing}")
            return False
        
        print("  ✓ README has required sections")
        return True
    except Exception as e:
        print(f"  ✗ Error reading README: {e}")
        return False


def check_requirements():
    """Check if requirements.txt exists."""
    print("\n[9] Checking requirements.txt...")
    if not os.path.exists("requirements.txt"):
        print("  ✗ requirements.txt not found")
        return False
    
    try:
        with open("requirements.txt") as f:
            packages = f.read()
        
        required = ["fastapi", "pydantic", "openai"]
        missing = [p for p in required if p not in packages]
        
        if missing:
            print(f"  ✗ requirements.txt missing: {missing}")
            return False
        
        print("  ✓ requirements.txt has all dependencies")
        return True
    except Exception as e:
        print(f"  ✗ Error reading requirements.txt: {e}")
        return False


def check_data():
    """Check if data files exist."""
    print("\n[10] Checking data files...")
    if not os.path.exists("data/emails.json"):
        print("  ✗ data/emails.json not found")
        return False
    
    try:
        with open("data/emails.json") as f:
            emails = json.load(f)
        
        if not isinstance(emails, list) or len(emails) < 12:
            print(f"  ✗ emails.json should have at least 12 emails (has {len(emails)})")
            return False
        
        print(f"  ✓ data/emails.json valid with {len(emails)} emails")
        return True
    except Exception as e:
        print(f"  ✗ Error reading data files: {e}")
        return False


if __name__ == "__main__":
    print("=" * 70)
    print("OpenEnv Email Triage - Hackathon Pre-Submission Validator")
    print("=" * 70)
    
    checks = [
        ("OpenEnv Spec (openenv.yaml)", check_openenv_yaml),
        ("Typed Models", check_typed_models),
        ("Environment API", check_environment_api),
        ("Tasks & Graders", check_tasks_and_graders),
        ("Dockerfile", check_dockerfile),
        ("Baseline Script", check_baseline_script),
        ("Environment Config", check_env_config),
        ("README", check_readme),
        ("Requirements", check_requirements),
        ("Data Files", check_data),
    ]
    
    results = {}
    for name, check_func in checks:
        try:
            results[name] = check_func()
        except Exception as e:
            print(f"  ✗ Unexpected error: {e}")
            results[name] = False
    
    print("\n" + "=" * 70)
    print("VALIDATION SUMMARY")
    print("=" * 70)
    
    passed = sum(1 for v in results.values() if v)
    total = len(results)
    
    for name, result in results.items():
        status = "✓" if result else "✗"
        print(f"{status} {name}")
    
    print(f"\n{passed}/{total} checks passed")
    
    if passed == total:
        print("\n✓ ALL CHECKS PASSED - Ready for hackathon submission!")
    else:
        print(f"\n✗ {total - passed} check(s) failed - Please fix before submission")
