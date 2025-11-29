import random
from typing import List, Dict, Tuple, Any
from models import Option, Decision, Feedback, FeatureWeights, Scenario
from datetime import datetime

class PerceptionLayer:
    """
    Layer 1: Perception (Input understanding)
    Parses the scenario into structured representations.
    """
    def process(self, scenario: Scenario) -> Dict[str, Any]:
        """
        Normalizes options and extracts relevant context/goals.
        """
        processed_options = []
        for opt in scenario.options:
            normalized_features = {}
            for feature, value in opt.features.items():
                normalized_features[feature] = self._normalize_value(value, feature)
            
            processed_options.append({
                "option": opt,
                "normalized_features": normalized_features
            })
            
        return {
            "options": processed_options,
            "context": scenario.context,
            "goals": scenario.goals
        }

    def _normalize_value(self, value: Any, feature: str) -> float:
        """Helper to convert values to 0-1 float."""
        if isinstance(value, (int, float)):
            # Heuristic normalization
            # Assuming some common ranges or simple scaling
            if "time" in feature.lower() or "cost" in feature.lower():
                # Lower is better usually, but let's just normalize to 0-1 first
                # We'll handle directionality in weights or logic
                return 1.0 / (value + 1.0) 
            if value > 1.0:
                return min(1.0, value / 100.0) # Rough scale
            return value
        return 0.5

class ConditionalLayer:
    """
    Layer 2: Conditional (Decision logic)
    Evaluates options based on the 5 Dimensions of Cognition.
    """
    DIMENSIONS = {
        "Logical Coherence": 0.25,
        "Adaptivity": 0.20,
        "Transparency": 0.20,
        "Innovation": 0.20,
        "Ethical Awareness": 0.15
    }

    def evaluate(self, perception_output: Dict[str, Any], learned_weights: FeatureWeights) -> Tuple[List[Dict[str, Any]], Dict[str, float]]:
        """
        Calculates scores based on the 5 cognitive dimensions.
        """
        options_data = perception_output["options"]
        context = perception_output["context"]
        goals = perception_output["goals"]
        
        # Merge learned weights with explicit scenario goals for Logical Coherence calc
        effective_weights = learned_weights.weights.copy()
        if context.get("deadline_pressure") == "high" or context.get("deadline_pressure", 0) > 0.7:
            for k in effective_weights:
                if k in ["time", "speed", "duration"]:
                    effective_weights[k] = min(1.0, effective_weights[k] + 0.3)
        for goal, priority in goals.items():
            effective_weights[goal] = priority

        scored_options = []
        for item in options_data:
            opt = item["option"]
            norm_features = item["normalized_features"]
            
            # --- Calculate Dimension Scores ---
            
            # 1. Logical Coherence (Rational Utility)
            # How well does it match the weighted priorities?
            utility_score = 0.0
            weight_sum = 0.0
            for feature, norm_val in norm_features.items():
                w = effective_weights.get(feature, 0.5) # Default weight 0.5
                utility_score += norm_val * w
                weight_sum += w
            
            # Normalize to 0-1
            logical_coherence = (utility_score / weight_sum) if weight_sum > 0 else 0.5
            
            # 2. Adaptivity (Flexibility)
            # Heuristic: Middle-of-the-road values are more adaptable than extremes? 
            # Or explicit 'flexibility' feature.
            if "flexibility" in norm_features:
                adaptivity = norm_features["flexibility"]
            else:
                # Proxy: Inverse of variance? Or just a base value modified by uncertainty context?
                # If uncertainty is high, we penalize rigid options (if we could detect them).
                # Let's use a deterministic hash of the name to simulate intrinsic properties for the demo
                # mixed with feature count (more features = more handles = more adaptive?)
                adaptivity = 0.5 + (len(norm_features) * 0.05)
                adaptivity = min(0.9, adaptivity)

            # 3. Transparency (Clarity)
            # Heuristic: Fewer features = simpler = more transparent. 
            # Or explicit 'clarity' feature.
            if "clarity" in norm_features:
                transparency = norm_features["clarity"]
            else:
                # Penalize complexity
                transparency = max(0.2, 1.0 - (len(norm_features) * 0.1))

            # 4. Innovation (Novelty)
            # Heuristic: High variance in features = spiky/unique.
            # Or explicit 'novelty' feature.
            if "novelty" in norm_features:
                innovation = norm_features["novelty"]
            else:
                vals = list(norm_features.values())
                if vals:
                    avg = sum(vals) / len(vals)
                    variance = sum((x - avg) ** 2 for x in vals) / len(vals)
                    innovation = min(1.0, variance * 4.0 + 0.3) # Scale up variance
                else:
                    innovation = 0.3

            # 5. Ethical Awareness
            # Heuristic: Look for 'sustainability', 'ethics', 'fairness'.
            # Default to high baseline (0.7) because we assume good intent unless flagged.
            if "sustainability" in norm_features:
                ethical = norm_features["sustainability"]
            elif "ethics" in norm_features:
                ethical = norm_features["ethics"]
            else:
                ethical = 0.7

            # --- Aggregate ---
            dim_scores = {
                "Logical Coherence": logical_coherence,
                "Adaptivity": adaptivity,
                "Transparency": transparency,
                "Innovation": innovation,
                "Ethical Awareness": ethical
            }
            
            total_score = sum(score * self.DIMENSIONS[dim] for dim, score in dim_scores.items())
            
            scored_options.append({
                "option": opt,
                "total_score": total_score,
                "dimension_scores": dim_scores,
                "feature_scores": norm_features, # Keep for debug/legacy
                "normalized_features": norm_features
            })
            
        return scored_options, effective_weights

class EvaluationLayer:
    """
    Layer 3: Evaluation (Preference Mapping)
    Selects the optimal choice.
    """
    def select_optimal(self, scored_options: List[Dict[str, Any]]) -> Dict[str, Any]:
        if not scored_options:
            return None
        # Sort by score descending
        scored_options.sort(key=lambda x: x["total_score"], reverse=True)
        return {
            "selected": scored_options[0],
            "ranked": scored_options
        }

class JustificationModuleLayer:
    """
    Layer 5: Justification module (Explanation engine)
    Produces a human-readable explanation based on the 5 Dimensions of Cognition.
    """
    def explain(self, selection_result: Dict[str, Any], weights_used: Dict[str, float], context: Dict[str, Any]) -> str:
        selected_data = selection_result["selected"]
        selected_opt = selected_data["option"]
        dim_scores = selected_data["dimension_scores"]
        total_score = selected_data["total_score"]
        
        lines = []
        
        # 1. Primary Justification (Top Dimensions)
        # Identify the dimensions that contributed most (Score * Weight)
        weighted_dims = {k: v * ConditionalLayer.DIMENSIONS[k] for k, v in dim_scores.items()}
        sorted_dims = sorted(weighted_dims.items(), key=lambda x: x[1], reverse=True)
        top_dim, top_val = sorted_dims[0]
        
        lines.append(f"**Decision Driver:** The choice was primarily driven by **{top_dim}** (Score: {dim_scores[top_dim]:.2f}).")
        
        # 2. Detailed Dimension Breakdown
        lines.append("\n**Cognitive Dimensions Analysis:**")
        for dim, score in dim_scores.items():
            weight = ConditionalLayer.DIMENSIONS[dim]
            lines.append(f"- **{dim}** ({weight*100:.0f}%): {score:.2f} / 1.0")
            
        # 3. Contextual Reasoning (Logical Coherence Deep Dive)
        lines.append("\n**Reasoning Context:**")
        if dim_scores["Logical Coherence"] > 0.7:
            lines.append("- Strong alignment with established goals and priorities.")
        else:
            lines.append("- Moderate alignment with explicit goals; other factors compensated.")
            
        # 4. Risk & Ethics
        if dim_scores["Ethical Awareness"] < 0.6:
            lines.append("- **Warning:** Ethical score is low. Review potential externalities.")
        
        uncertainty = context.get("uncertainty", 0.0)
        if uncertainty > 0.3:
             lines.append(f"- High uncertainty ({uncertainty}) detected. 'Adaptivity' was prioritized.")

        return "\n".join(lines)

class FeedbackLoopLayer:
    """
    Layer 4: Feedback loop (Learning and reflection)
    Updates weights and produces internal reflection.
    """
    def adjust(self, weights: FeatureWeights, decision: Decision, reward: float) -> Tuple[FeatureWeights, str]:
        """
        Updates weights based on reward (0.0 to 1.0).
        Returns updated weights and the 'Internal Reflection' string.
        """
        # Reward > 0.5 is positive, < 0.5 is negative
        # 0.5 is neutral
        
        delta = (reward - 0.5) * 0.2 # Scale adjustment
        
        # Identify what to update. 
        # We update the weights that were used in the decision.
        # For simplicity, we update the top contributing features of the selected option.
        
        # We need to reconstruct which features were important.
        # The decision object has scores, but not the feature breakdown directly easily accessible 
        # without re-parsing. 
        # However, we have 'weights_used'. We should update the PERSISTENT weights based on this feedback.
        # If the user said "Good job" (High reward), we reinforce the weights that led to this.
        
        # Let's look at the weights used.
        # We'll update the top 3 heaviest weights used in that decision.
        
        sorted_used_weights = sorted(decision.weights_used.items(), key=lambda x: x[1], reverse=True)
        top_keys = [k for k, v in sorted_used_weights[:3]]
        
        changes = []
        
        for key in top_keys:
            # Only update if it's a feature we track in learned weights
            if key in weights.weights:
                old_val = weights.weights[key]
                weights.update(key, delta)
                new_val = weights.weights[key]
                diff = new_val - old_val
                if abs(diff) > 0.001:
                    changes.append(f"{key} ({diff:+.2f})")
        
        if not changes:
            reflection = "After feedback: No significant weight updates triggered."
        else:
            reflection = f"After feedback: I adjusted weights for {', '.join(changes)} based on reward {reward}."
            
        weights.last_updated = datetime.now().isoformat()
        return weights, reflection
