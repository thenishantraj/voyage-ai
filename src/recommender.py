"""
Confidence Scoring Engine
Calculates weighted geometric mean for destination recommendations
"""

import numpy as np
from typing import Dict, List, Any

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
            
            # Fix: Calculate confidence score properly
            if scores:
                confidence = self._weighted_geometric_mean(scores)
                
                rec = dest.copy()
                rec.update({
                    "confidence_score": round(min(100, confidence), 1),
                    "budget_score": round(scores.get("budget_score", 7), 1),
                    "weather_score": round(scores.get("weather_score", 7), 1),
                    "crowd_score": round(scores.get("crowd_score", 7), 1),
                    "dna_match": round(scores.get("dna_match", 7), 1),
                    "interest_score": round(scores.get("interest_score", 7), 1)
                })
                
                recommendations.append(rec)
        
        # Sort by confidence score descending
        recommendations.sort(key=lambda x: x["confidence_score"], reverse=True)
        return recommendations
    
    def _calculate_component_scores(self, dest: Dict, prefs: Dict) -> Dict[str, float]:
        """Calculate individual component scores (0-10 scale)"""
        scores = {}
        
        # 1. BUDGET SCORE (0-10)
        dest_cost = dest.get("average_cost", 3000)
        budget_min = prefs.get("budget_min", 1000)
        budget_max = prefs.get("budget_max", 5000)
        
        if dest_cost <= budget_min:
            scores["budget_score"] = 10.0
        elif dest_cost <= budget_max:
            if budget_max > budget_min:
                # Calculate how well it fits in the range
                range_size = budget_max - budget_min
                position = (dest_cost - budget_min) / range_size
                # 10 to 8 based on position
                scores["budget_score"] = 10.0 - (position * 2.0)
            else:
                scores["budget_score"] = 8.0
        else:
            # Over budget - penalty
            over_by = dest_cost - budget_max
            if budget_max > 0:
                penalty_ratio = min(1.0, over_by / budget_max)
                scores["budget_score"] = max(3.0, 8.0 - (penalty_ratio * 5.0))
            else:
                scores["budget_score"] = 5.0
        
        # 2. WEATHER SCORE (0-10)
        dest_weather = dest.get("weather_score", 7.0)
        weather_priority = prefs.get("weather_priority", 5) / 10.0
        scores["weather_score"] = dest_weather * (0.5 + 0.5 * weather_priority)
        scores["weather_score"] = min(10, max(1, scores["weather_score"]))
        
        # 3. CROWD SCORE (0-10)
        dest_crowd = dest.get("crowd_score", 5.0)
        user_tolerance = prefs.get("crowd_tolerance", 5) / 10.0
        
        # Calculate how well destination matches user's crowd preference
        if user_tolerance <= 0.3:  # Wants low crowds
            # Prefer destinations with low crowd scores
            scores["crowd_score"] = 10.0 - dest_crowd
        elif user_tolerance >= 0.7:  # Likes crowds
            # Prefer destinations with high crowd scores
            scores["crowd_score"] = dest_crowd
        else:  # Neutral
            # Prefer medium crowd scores
            scores["crowd_score"] = 10.0 - abs(dest_crowd - 5.0)
        
        scores["crowd_score"] = min(10, max(1, scores["crowd_score"]))
        
        # 4. DNA MATCH SCORE (0-10)
        scores["dna_match"] = 7.0  # Default
        
        user_dna = prefs.get("travel_dna")
        
        if user_dna and isinstance(user_dna, dict):
            # Get dimensions from profile
            dna_dims = user_dna.get("dimensions", {})
            
            # If no dimensions but has direct keys
            if not dna_dims and any(k in user_dna for k in ["adventure", "comfort"]):
                dna_dims = user_dna
            
            dest_dna = dest.get("dna_affinity", {})
            
            if dna_dims and dest_dna:
                total = 0
                count = 0
                for dim in ["adventure", "comfort", "culture", "luxury", "nature", "urban", "social"]:
                    if dim in dna_dims and dim in dest_dna:
                        try:
                            user_val = float(dna_dims[dim])
                            dest_val = float(dest_dna[dim])
                            # Calculate similarity (10 - difference)
                            similarity = 10 - abs(user_val - dest_val)
                            total += similarity
                            count += 1
                        except (ValueError, TypeError):
                            continue
                
                if count > 0:
                    scores["dna_match"] = total / count
        
        # 5. INTEREST SCORE (0-10)
        user_interests = prefs.get("interests", [])
        dest_category = dest.get("category", "")
        
        if user_interests and dest_category:
            match_count = 0
            for interest in user_interests:
                # Check if interest matches category
                if interest.lower() in dest_category.lower():
                    match_count += 1
                # Check category mapping
                elif dest_category in self.category_mapping:
                    category_keywords = self.category_mapping[dest_category]
                    if any(keyword.lower() in interest.lower() for keyword in category_keywords):
                        match_count += 1
            
            # Calculate score based on matches
            if match_count > 0:
                scores["interest_score"] = min(10, 5 + (match_count * 2.5))
            else:
                scores["interest_score"] = 5.0
        else:
            scores["interest_score"] = 7.0
        
        scores["interest_score"] = min(10, max(1, scores["interest_score"]))
        
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
