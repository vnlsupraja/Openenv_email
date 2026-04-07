# test_environment.py
"""
Test script to validate the OpenEnv Email Triage environment without requiring API calls.
This ensures all components work correctly before deployment.
"""

from env.environment import EmailEnv
from env.tasks import EasyTask, MediumTask, HardTask
from env.models import Action
from env.graders import grade

def test_task(task_class, num_actions):
    """Test a single task."""
    print(f"\n{'='*60}")
    print(f"Testing: {task_class.__name__}")
    print(f"{'='*60}")
    
    try:
        task = task_class()
        env = EmailEnv(task)
        
        # Reset environment
        obs = env.reset()
        print(f"✓ Environment reset successfully")
        print(f"  Initial inbox size: {len(obs.inbox)}")
        
        # Get expected actions
        expected_map = task.get_expected_actions()
        print(f"  Expected emails: {list(expected_map.keys())}")
        
        # Simulate some actions
        total_reward = 0
        for i, email in enumerate(obs.inbox[:num_actions]):
            expected_steps = expected_map.get(email.id, [])
            if expected_steps:
                expected_action = expected_steps[0]
                
                # Create action matching expectation
                action = Action(
                    type=expected_action["type"],
                    email_id=email.id,
                    content=expected_action.get("content", None)
                )
                
                obs, reward, done, info = env.step(action)
                total_reward += reward.value
                
                print(f"  Action {i+1}: {action.type} on email {email.id}")
                print(f"    Reward: {reward.value:.2f} ({reward.reason})")
                print(f"    Score: {info['score']:.2f}")
                
                if done:
                    print(f"  ✓ Task completed!")
                    break
        
        print(f"\n✓ {task_class.__name__} test PASSED")
        print(f"  Final Score: {info['score']:.2f}")
        print(f"  Total Reward: {total_reward:.2f}")
        return True
        
    except Exception as e:
        print(f"\n✗ {task_class.__name__} test FAILED")
        print(f"  Error: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    print("\n" + "="*60)
    print("OpenEnv Email Triage - Environment Validation Test")
    print("="*60)
    
    results = {
        "EasyTask": test_task(EasyTask, 2),
        "MediumTask": test_task(MediumTask, 4),
        "HardTask": test_task(HardTask, 6),
    }
    
    print(f"\n\n{'='*60}")
    print("TEST SUMMARY")
    print(f"{'='*60}")
    
    passed = sum(1 for v in results.values() if v)
    total = len(results)
    
    for task_name, result in results.items():
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{task_name}: {status}")
    
    print(f"\nOverall: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n✓ All tests passed! Environment is ready for deployment.")
    else:
        print(f"\n✗ {total - passed} test(s) failed. Please fix issues before deployment.")
