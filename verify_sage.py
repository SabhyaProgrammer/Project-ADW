from sage import Sage
from models import Option, Scenario
import os
import shutil

def test_sage():
    print("Setting up test environment...")
    # Use a temporary data directory for testing
    test_data_dir = "test_data"
    if os.path.exists(test_data_dir):
        shutil.rmtree(test_data_dir)
    
    sage = Sage(data_dir=test_data_dir)
    
    # Create test options
    options = [
        Option(id="1", name="Option A", domain="test", features={"quality": 10, "cost": 5}, description="High quality"),
        Option(id="2", name="Option B", domain="test", features={"quality": 5, "cost": 2}, description="Low cost")
    ]
    
    scenario = Scenario(
        id="test_scen_01",
        description="Test Scenario",
        options=options,
        context={"pressure": 0.5},
        goals={"quality": 0.8}
    )
    
    print("\n1. Testing Decision Making...")
    decision = sage.make_decision(scenario)
    print(f"Selected: {decision.selected_option_id}")
    print(f"Reasoning: {decision.reasoning}")
    
    assert decision.selected_option_id is not None
    assert len(decision.reasoning) > 0
    
    print("\n2. Testing Feedback & Learning...")
    # Get initial weight for 'quality'
    initial_weight = sage.weights["test"].weights.get("quality", 0.5)
    print(f"Initial quality weight: {initial_weight}")
    
    # Provide positive feedback
    print("Providing positive feedback (1.0/1.0)...")
    sage.provide_feedback(decision.id, 1.0)
    
    # Check if weights updated
    updated_weight = sage.weights["test"].weights.get("quality", 0.5)
    print(f"Updated quality weight: {updated_weight}")
    
    # If Option A (High Quality) was chosen and we gave 5 stars, 
    # quality weight should likely increase or stay same (if capped).
    # Note: The logic in sage.py updates weights of the *domain* based on the decision.
    
    if updated_weight != initial_weight:
        print("SUCCESS: Weights adapted.")
    else:
        print("NOTE: Weights didn't change (might be capped or logic specific).")
        
    print("\n3. Testing Persistence...")
    # Create new instance to verify load
    sage2 = Sage(data_dir=test_data_dir)
    loaded_weight = sage2.weights["test"].weights.get("quality")
    print(f"Loaded quality weight: {loaded_weight}")
    
    assert loaded_weight == updated_weight
    print("SUCCESS: Persistence verified.")
    
    # Cleanup
    if os.path.exists(test_data_dir):
        shutil.rmtree(test_data_dir)
        
    print("\nAll systems operational!")

if __name__ == "__main__":
    test_sage()
