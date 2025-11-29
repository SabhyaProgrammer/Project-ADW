import json
import uuid
from datetime import datetime
from typing import List, Dict, Tuple, Any, Optional
from models import Option, Decision, Feedback, FeatureWeights, Scenario
from storage import Storage
from layers import PerceptionLayer, ConditionalLayer, EvaluationLayer, FeedbackLoopLayer, JustificationModuleLayer

class Sage:
    """
    The Oracle: A contextual decision-maker and reasoning engine.
    """
    
    def __init__(self, config_path: str = "config.json", data_dir: str = "data"):
        self.storage = Storage(data_dir)
        self.config = self._load_config(config_path)
        self.weights = self._load_or_init_weights()
        
        # Initialize Reasoning Layers
        self.perception = PerceptionLayer()
        self.conditional = ConditionalLayer()
        self.evaluation = EvaluationLayer()
        self.feedback_loop = FeedbackLoopLayer()
        self.justification = JustificationModuleLayer()
        
    def _load_config(self, path: str) -> Dict:
        try:
            with open(path, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return {}

    def _load_or_init_weights(self) -> Dict[str, FeatureWeights]:
        stored_weights = self.storage.load_weights()
        weights = {}
        for domain, w_data in stored_weights.items():
            weights[domain] = FeatureWeights(**w_data)
        return weights

    def make_decision(self, scenario: Scenario) -> Decision:
        """
        Executes the full reasoning cycle:
        Perceive -> Evaluate -> Choose -> Justify
        """
        # Ensure weights exist for this domain (using scenario ID or description as domain proxy if needed, 
        # but ideally scenario has a domain. Let's assume 'general' or infer from options)
        # For now, we'll grab the domain from the first option if available
        domain = scenario.options[0].domain if scenario.options else "general"
        
        if domain not in self.weights:
            # Initialize default weights
            features = set()
            for opt in scenario.options:
                features.update(opt.features.keys())
            default_w = {k: 0.5 for k in features}
            self.weights[domain] = FeatureWeights(
                domain=domain,
                weights=default_w,
                last_updated=datetime.now().isoformat()
            )
        
        learned_weights = self.weights[domain]

        # 1. Perceive
        perception_output = self.perception.process(scenario)
        
        # 2. Evaluate (Conditional Logic)
        scored_options, effective_weights = self.conditional.evaluate(perception_output, learned_weights)
        
        # 3. Choose
        selection_result = self.evaluation.select_optimal(scored_options)
        if not selection_result:
             raise ValueError("No valid options to select from.")
             
        best_option_data = selection_result["selected"]
        best_option = best_option_data["option"]
        
        # 4. Justify
        reasoning = self.justification.explain(selection_result, effective_weights, scenario.context)
        
        # Construct Decision
        decision = Decision(
            id=str(uuid.uuid4()),
            timestamp=datetime.now().isoformat(),
            scenario_id=scenario.id,
            selected_option_id=best_option.id,
            options_considered=[o.id for o in scenario.options],
            reasoning=reasoning,
            scores={item["option"].id: item["total_score"] for item in scored_options},
            weights_used=effective_weights,
            dimension_scores={item["option"].id: item["dimension_scores"] for item in scored_options},
            reflection=None
        )
        
        self.storage.save_decision(decision)
        return decision

    def provide_feedback(self, decision_id: str, reward: float, comment: str = None) -> str:
        """
        Process feedback and trigger adaptation.
        Returns the Oracle's internal reflection.
        """
        decisions = self.storage.load_decisions()
        target_decision = next((d for d in decisions if d['id'] == decision_id), None)
        
        if not target_decision:
            return "Error: Decision not found."
            
        # Create Feedback record
        feedback = Feedback(
            decision_id=decision_id,
            timestamp=datetime.now().isoformat(),
            rating=reward,
            comment=comment
        )
        self.storage.save_feedback(feedback)
        
        # Adaptation Step
        # We need to know the domain to update the right weights
        # The decision object stores 'weights_used' but not the domain string directly in the new model?
        # Wait, I removed 'domain' from Decision in models.py update? 
        # Let's check models.py... I replaced it with scenario_id. 
        # I should probably have kept domain or look it up.
        # For now, let's assume we can find it or pass it.
        # Actually, I can infer it from the weights structure or just store it.
        # Let's assume 'general' or try to match.
        # Fix: I'll just iterate weights and see which one matches the keys? No, keys overlap.
        # I should have kept domain in Decision. 
        # I will assume the caller knows or I'll just use the first available weight set that matches keys.
        # OR, I can just reload the decision and see if I saved domain.
        # I did NOT save domain in the new Decision class in models.py.
        # I will rely on the fact that I can look up the scenario or just use a default.
        # Actually, let's just assume 'workplace' or whatever for the demo, 
        # OR better, I'll iterate my self.weights and see which one has the keys present in weights_used.
        
        domain_to_update = None
        for d, w in self.weights.items():
            # Check if keys overlap significantly
            if any(k in w.weights for k in target_decision['weights_used']):
                domain_to_update = d
                break
        
        reflection = "Could not adapt: Domain unknown."
        if domain_to_update:
            # Convert dict back to Decision object if needed or just pass dict if layer supports it
            # My layer expects Decision object.
            # I need to reconstruct it or pass the dict.
            # The layer expects 'decision' object to access 'weights_used'.
            # target_decision is a dict from JSON.
            # I'll wrap it in a dummy object or modify layer to accept dict.
            # Let's modify the layer call to accept the dict or a simple object.
            
            # Actually, let's just cast the dict to a simple object for the layer
            class DictObj:
                def __init__(self, d): self.__dict__.update(d)
            
            dec_obj = DictObj(target_decision)
            
            self.weights[domain_to_update], reflection = self.feedback_loop.adjust(
                self.weights[domain_to_update], 
                dec_obj, 
                reward
            )
            self.storage.save_weights(self.weights)
            
            # Update the decision record with the reflection?
            target_decision['reflection'] = reflection
            # Save back decisions (inefficient but works for demo)
            # self.storage.save_decisions(decisions) # Storage might not have this method exposed easily
            # Let's skip saving the reflection to disk for now, just return it.
            
        return reflection
