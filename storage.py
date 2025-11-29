import json
import os
from typing import List, Dict, Optional
from models import Decision, Feedback, FeatureWeights

class Storage:
    """Handles persistence of data using JSON files."""
    
    def __init__(self, data_dir: str = "data"):
        self.data_dir = data_dir
        self._ensure_data_dir()
        
        self.decisions_file = os.path.join(data_dir, "decisions.json")
        self.feedback_file = os.path.join(data_dir, "feedback.json")
        self.weights_file = os.path.join(data_dir, "weights.json")

    def _ensure_data_dir(self):
        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir)

    def save_decision(self, decision: Decision):
        decisions = self.load_decisions()
        # Convert dataclass to dict
        decision_dict = decision.__dict__
        decisions.append(decision_dict)
        with open(self.decisions_file, 'w') as f:
            json.dump(decisions, f, indent=2)

    def load_decisions(self) -> List[Dict]:
        if not os.path.exists(self.decisions_file):
            return []
        try:
            with open(self.decisions_file, 'r') as f:
                return json.load(f)
        except json.JSONDecodeError:
            return []

    def save_feedback(self, feedback: Feedback):
        feedbacks = self.load_feedback()
        feedbacks.append(feedback.__dict__)
        with open(self.feedback_file, 'w') as f:
            json.dump(feedbacks, f, indent=2)

    def load_feedback(self) -> List[Dict]:
        if not os.path.exists(self.feedback_file):
            return []
        try:
            with open(self.feedback_file, 'r') as f:
                return json.load(f)
        except json.JSONDecodeError:
            return []

    def save_weights(self, weights: Dict[str, FeatureWeights]):
        # Convert dict of FeatureWeights to dict of dicts
        weights_dict = {domain: fw.__dict__ for domain, fw in weights.items()}
        with open(self.weights_file, 'w') as f:
            json.dump(weights_dict, f, indent=2)

    def load_weights(self) -> Dict[str, Dict]:
        if not os.path.exists(self.weights_file):
            return {}
        try:
            with open(self.weights_file, 'r') as f:
                return json.load(f)
        except json.JSONDecodeError:
            return {}
