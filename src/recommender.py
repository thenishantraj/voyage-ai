"""
Confidence Scoring Engine
Calculates weighted geometric mean for destination recommendations
"""

import numpy as np
from typing import Dict, List, Any
from datetime import datetime

class ConfidenceEngine:
    """Engine for calculating confidence scores"""
    
    def __init__(self):
        self.weights = {
            "budget_score": 0.25,
            "dna_match": 0.25,
            "weather_score": 0.20,
            "crowd_score": 0.15,
            "interest_score": 0.15
        }
        
        self.category_mapping = {
            "Adventure": ["Adventure", "Mountains", "Hiking", "Extreme", "Thrill"],
            "Cultural": ["History", "Culture", "Museums", "Temples", "Heritage"],
            "Luxury": ["Luxury", "Shopping", "Fine Dining", "Resort", "Premium"],
            "Nature": ["Nature", "Wildlife", "Beaches", "Mountains", "Forest"],
            "Urban": ["Cities", "Nightlife", "Urban", "Metropolitan"],
            "Beach": ["Beaches", "Relaxation", "Water", "Ocean"],
            "Wellness": ["Wellness", "Spa", "Relaxation", "Yoga", "Retreat"]
        }
    
    def calculate_recommendations(self, destinations: List[Dict], user_prefs: Dict) -> List[Dict]:
        """Calculate confidence-scored recommendations"""
        recommendations = []
        
        for dest in destinations:
            scores = self._calculate_component_scores(dest, user_prefs)
            confidence = self._weighted_geometric_mean(scores)
            
            rec = dest.copy()
            rec.update({
                "confidence_score": round(min(100, confidence), 1),
                "budget_score": round(scores.get("budget_score", 0), 1),
                "weather_score": round(scores.get("weather_score", 0), 1),
                "crowd_score": round(scores.get("crowd_score", 0), 1),
                "dna_match": round(scores.get("dna_match", 0), 1),
                "interest_score": round(scores.get("interest_score", 0), 1)
            })
            
            recommendations.append(rec)
        
        # Sort by confidence score descending
        recommendations.sort(key=lambda x: x["confidence_score"], reverse=True)
        return recommendations
    
    def _calculate_component_scores(self, dest: Dict, prefs: Dict) -> Dict[str, float]:
    """Calculate individual component scores (0-10 scale) - FIXED VERSION"""
    scores = {}
    
    # Budget Score (0-10)
    dest_cost = dest.get("average_cost", 3000)
    budget_min = prefs.get("budget_min", 1000)
    budget_max = prefs.get("budget_max", 5000)
    
    if dest_cost <= budget_min:
        scores["budget_score"] = 10.0
    elif dest_cost <= budget_max:
        ratio = (dest_cost - budget_min) / (budget_max - budget_min) if budget_max > budget_min else 0
        scores["budget_score"] = 10.0 - (ratio * 4.0)  # 10 to 6
    else:
        penalty = (dest_cost - budget_max) / budget_max if budget_max > 0 else 1
        scores["budget_score"] = max(1, 6.0 - (penalty * 5.0))
    
    # Weather Score
    dest_weather = dest.get("weather_score", 7.0)
    weather_priority = prefs.get("weather_priority", 5) / 10.0
    scores["weather_score"] = dest_weather * (0.7 + 0.3 * weather_priority)
    
    # Crowd Score
    dest_crowd = dest.get("crowd_score", 5.0)
    user_tolerance = prefs.get("crowd_tolerance", 5) / 10.0
    
    if user_tolerance <= 0.4:  # Prefers quiet
        ideal = 10.0 - dest_crowd
        scores["crowd_score"] = ideal * 1.2
    elif user_tolerance >= 0.7:  # Likes crowds
        scores["crowd_score"] = dest_crowd * 1.2
    else:  # Balanced
        ideal = 10.0 - abs(dest_crowd - 5.0)
        scores["crowd_score"] = ideal
    
    scores["crowd_score"] = min(10, max(1, scores["crowd_score"]))
    
    # FIXED: DNA Match Score - Better error handling
    scores["dna_match"] = 7.0  # Default
    
    user_dna = prefs.get("travel_dna")
    
    if user_dna and isinstance(user_dna, dict):
        # Try to get dimensions from different possible structures
        dna_dims = user_dna.get("dimensions", {})
        
        # If no dimensions, try to use the profile directly
        if not dna_dims and "adventure" in user_dna:
            dna_dims = user_dna
        
        dest_dna = dest.get("dna_affinity", {})
        
        if dna_dims and dest_dna:
            total = 0
            count = 0
            for dim in ["adventure", "comfort", "culture", "luxury", "nature", "urban", "social"]:
                if dim in dna_dims and dim in dest_dna:
                    # Normalize both to 0-10 scale
                    user_val = float(dna_dims[dim])
                    dest_val = float(dest_dna[dim])
                    diff = abs(user_val - dest_val)
                    total += (10 - diff)
                    count += 1
            
            if count > 0:
                scores["dna_match"] = total / count
    
    # Interest Score
    user_interests = prefs.get("interests", [])
    dest_category = dest.get("category", "")
    category_keywords = self.category_mapping.get(dest_category, [])
    
    if user_interests and category_keywords:
        matches = sum(1 for interest in user_interests 
                     if any(keyword.lower() in interest.lower() 
                           for keyword in category_keywords))
        scores["interest_score"] = (matches / len(user_interests)) * 10 if user_interests else 7.0
    else:
        scores["interest_score"] = 7.0
    
    return scores
    
    def _weighted_geometric_mean(self, scores: Dict[str, float]) -> float:
        """Calculate weighted geometric mean"""
        log_sum = 0
        weight_sum = 0
        
        for key, weight in self.weights.items():
            score = max(0.1, scores.get(key, 5.0))
            log_sum += weight * np.log(score)
            weight_sum += weight
        
        if weight_sum == 0:
            return 70.0
        
        geometric_mean = np.exp(log_sum / weight_sum)
        return geometric_mean * 10
