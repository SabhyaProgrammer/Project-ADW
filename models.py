from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any
from datetime import datetime
import uuid

@dataclass
class Option:
    """Represents a choice available to the user."""
    id: str
    name: str
    domain: str
    features: Dict[str, Any]  # e.g., {"time": 5, "accuracy": 0.9}
    description: Optional[str] = None

@dataclass
class Scenario:
    """
    A packet of information describing a situation requiring a choice.
    Contains options, context (state), and goals (priorities).
    """
    id: str
    description: str
    options: List[Option]
    context: Dict[str, Any] = field(default_factory=dict) # e.g. {"fatigue": 0.75, "pressure": "medium"}
    goals: Dict[str, float] = field(default_factory=dict) # e.g. {"health": 0.6, "productivity": 0.4}

@dataclass
class Decision:
    """Represents a decision made by the Oracle."""
    id: str
    timestamp: str
    scenario_id: str
    selected_option_id: str
    options_considered: List[str]
    reasoning: str
    scores: Dict[str, float]
    weights_used: Dict[str, float]
    dimension_scores: Dict[str, Dict[str, float]] = field(default_factory=dict) # OptionID -> {Dimension: Score}
    reflection: Optional[str] = None # Populated after feedback

@dataclass
class Feedback:
    """Represents user feedback on a decision."""
    decision_id: str
    timestamp: str
    rating: float  # 0.0 to 1.0
    comment: Optional[str] = None

@dataclass
class FeatureWeights:
    """Stores learned weights for features/goals."""
    domain: str # loosely maps to scenario types
    weights: Dict[str, float]
    last_updated: str
    learning_rate: float = 0.1
    
    def update(self, feature: str, delta: float):
        """Update weight for a feature."""
        current = self.weights.get(feature, 0.5)
        # Clamp between 0.0 and 1.0 (allowing 0 as per user implies flexible weights)
        self.weights[feature] = max(0.0, min(1.0, current + delta))
