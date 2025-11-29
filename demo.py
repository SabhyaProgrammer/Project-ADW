import json
import os
import sys
from typing import List
from sage import Sage
from models import Option, Scenario

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_header():
    print("="*60)
    print("   THE ORACLE - Contextual Reasoning Engine")
    print("="*60)
    print()

def load_scenarios(path: str = "data/oracle_scenarios.json") -> List[Scenario]:
    try:
        with open(path, 'r') as f:
            data = json.load(f)
            scenarios = []
            for item in data:
                # Convert options dicts to Option objects
                opts = [Option(**o) for o in item['options']]
                # Create Scenario object
                scen = Scenario(
                    id=item['id'],
                    description=item['description'],
                    options=opts,
                    context=item.get('context', {}),
                    goals=item.get('goals', {})
                )
                scenarios.append(scen)
            return scenarios
    except FileNotFoundError:
        print(f"Error: Could not load scenarios from {path}.")
        return []
    except Exception as e:
        print(f"Error loading scenarios: {e}")
        return []

def run_demo():
    sage = Sage()
    scenarios = load_scenarios()
    
    while True:
        clear_screen()
        print_header()
        print("Available Scenarios:")
        for i, s in enumerate(scenarios):
            print(f"{i+1}. {s.id}: {s.description}")
        print(f"{len(scenarios)+1}. [CUSTOM] Create your own scenario")
        print("Q. Quit")
        
        choice = input("\nSelect a scenario to analyze: ").strip().lower()
        
        if choice == 'q':
            print("\nOracle: Terminating session.")
            break
            
        try:
            idx = int(choice) - 1
            if 0 <= idx < len(scenarios):
                handle_scenario(sage, scenarios[idx])
            elif idx == len(scenarios):
                handle_custom_scenario(sage)
            else:
                input("Invalid selection. Press Enter to try again.")
        except ValueError:
            input("Invalid input. Press Enter to try again.")

def handle_custom_scenario(sage: Sage):
    clear_screen()
    print_header()
    print("=== Custom Scenario Input ===\n")
    
    # 1. Context Variables
    print("Enter context variables (key=value, comma-separated):")
    print("Example: fatigue=0.7, deadline_pressure=0.4")
    context_str = input("> ").strip()
    context = {}
    if context_str:
        for item in context_str.split(','):
            if '=' in item:
                k, v = item.split('=', 1)
                try:
                    context[k.strip()] = float(v.strip())
                except ValueError:
                    context[k.strip()] = v.strip()
    
    # 2. Available Options
    print("\nEnter available options (comma-separated):")
    options_str = input("> ").strip()
    options = []
    if options_str:
        for i, opt_name in enumerate(options_str.split(',')):
            name = opt_name.strip()
            if name:
                # For custom scenarios, we don't have explicit feature values for options unless we ask.
                # To keep it usable, we'll ask for a quick rating of each option against the priorities later,
                # OR we infer/randomize for the demo. 
                # BETTER: Ask for features for each option? Too tedious.
                # COMPROMISE: We will assume the options have features that match the priorities roughly, 
                # or we ask the user to rate them. 
                # Let's ask for a simplified feature set or just use the name and infer?
                # The prompt says "Your engine will evaluate EACH option using its reasoning rules."
                # Reasoning rules need features. 
                # Let's ask for 1-2 key feature values for each option.
                print(f"  Define features for '{name}' (key=value, e.g. cost=0.5, utility=0.9):")
                feats_str = input("  > ").strip()
                features = {}
                if feats_str:
                    for f_item in feats_str.split(','):
                        if '=' in f_item:
                            k, v = f_item.split('=', 1)
                            try:
                                features[k.strip()] = float(v.strip())
                            except ValueError:
                                pass
                options.append(Option(id=f"custom_opt_{i}", name=name, domain="custom", features=features))
    
    if not options:
        print("Error: No options provided.")
        input("Press Enter to return...")
        return

    # 3. Objectives & Priorities
    print("\nEnter priorities/objectives (key=value, 0-1):")
    print("Example: health=0.8, productivity=0.5")
    goals_str = input("> ").strip()
    goals = {}
    if goals_str:
        for item in goals_str.split(','):
            if '=' in item:
                k, v = item.split('=', 1)
                try:
                    goals[k.strip()] = float(v.strip())
                except ValueError:
                    pass
                    
    # 4. Constraints
    print("\nEnter constraints (comma-separated) or 'none':")
    constraints_str = input("> ").strip()
    # We store constraints in context for now as the model doesn't have a separate field yet
    if constraints_str and constraints_str.lower() != 'none':
        context['constraints'] = [c.strip() for c in constraints_str.split(',')]

    # 5. Uncertainty
    print("\nEnter uncertainty (0-1):")
    try:
        unc_str = input("> ").strip()
        uncertainty = float(unc_str) if unc_str else 0.0
        context['uncertainty'] = uncertainty
    except ValueError:
        context['uncertainty'] = 0.0

    # Create Scenario
    scenario = Scenario(
        id="custom_scen_" + str(len(context)), # simple unique id
        description="User generated custom scenario",
        options=options,
        context=context,
        goals=goals
    )
    
    # Run the standard handler
    handle_scenario(sage, scenario)

def handle_scenario(sage: Sage, scenario: Scenario):
    clear_screen()
    print_header()
    print(f"Analyzing Scenario: {scenario.id}")
    print(f"Description: {scenario.description}")
    print(f"Context: {scenario.context}")
    print(f"Goals: {scenario.goals}")
    print("\nOptions:")
    for opt in scenario.options:
        print(f"- {opt.name}: {opt.description}")
    print("-" * 60)
    
    # Make decision
    print("\n... Oracle is reasoning ...\n")
    decision = sage.make_decision(scenario)
    
    print(">>> ORACLE DECISION <<<")
    # Find selected option name for display
    selected_name = next((o.name for o in scenario.options if o.id == decision.selected_option_id), "Unknown")
    print(f"Selected: {selected_name}")
    print("\n>>> JUSTIFICATION <<<")
    print(decision.reasoning)
    print("-" * 60)
    
    # Get feedback
    print("\nProvide Feedback to the Oracle:")
    print("Enter a reward score (0.0 to 1.0), where 1.0 is perfect and 0.0 is terrible.")
    
    while True:
        fb = input("Reward (0.0 - 1.0): ").strip()
        try:
            reward = float(fb)
            if 0.0 <= reward <= 1.0:
                reflection = sage.provide_feedback(decision.id, reward)
                print(f"\n>>> INTERNAL REFLECTION <<<")
                print(reflection)
                input("\nPress Enter to continue...")
                break
            else:
                print("Please enter a value between 0.0 and 1.0")
        except ValueError:
            print("Invalid input. Please enter a number.")

if __name__ == "__main__":
    run_demo()
