"""
Travel DNA Profiling System
Psychological profiling for travel personality classification
"""

from typing import Dict, List, Any
import numpy as np

# Travel Personality Definitions
TRAVEL_PERSONALITIES = {
    "Adventure Seeker": {
        "traits": "Thrill-seeking, Spontaneous, Risk-tolerant",
        "style": "Active exploration, off-the-beaten-path, physical challenges",
        "perfect_for": "Extreme sports, remote destinations, unpredictable itineraries",
        "emoji": "🏔️",
        "color": "#ffa502"
    },
    "Culture Connoisseur": {
        "traits": "Intellectual, Curious, Historically-minded",
        "style": "Museum-hopping, local immersion, culinary exploration",
        "perfect_for": "Historical sites, artistic hubs, traditional experiences",
        "emoji": "🏛️",
        "color": "#4834d4"
    },
    "Luxury Escapist": {
        "traits": "Comfort-oriented, Quality-focused, Service-expecting",
        "style": "Premium accommodations, exclusive access, pampering services",
        "perfect_for": "5-star resorts, private tours, gourmet dining",
        "emoji": "✨",
        "color": "#f6b93b"
    },
    "Nature Immerser": {
        "traits": "Eco-conscious, Peace-seeking, Nature-connected",
        "style": "Outdoor activities, wildlife watching, sustainable travel",
        "perfect_for": "National parks, eco-lodges, wilderness retreats",
        "emoji": "🌲",
        "color": "#6ab04c"
    },
    "Urban Explorer": {
        "traits": "Energy-seeking, Social, Trend-aware",
        "style": "City hopping, nightlife, modern architecture",
        "perfect_for": "Metropolitan cities, tech hubs, contemporary art scenes",
        "emoji": "🌆",
        "color": "#ff6b6b"
    },
    "Relaxation Chaser": {
        "traits": "Calm, Rejuvenation-focused, Slow-paced",
        "style": "Beach lounging, spa retreats, minimal planning",
        "perfect_for": "Beach resorts, wellness retreats, countryside escapes",
        "emoji": "🧘",
        "color": "#00d4ff"
    },
    "Social Connector": {
        "traits": "People-oriented, Communicative, Experience-sharing",
        "style": "Group tours, local interactions, social experiences",
        "perfect_for": "Festivals, community stays, shared accommodations",
        "emoji": "🎉",
        "color": "#e84342"
    }
}

class TravelDNAProfiler:
    """Psychological profiling engine for travel personalities"""
    
    def __init__(self):
        self.questions = self._initialize_questions()
        self.personality_centroids = self._initialize_centroids()
    
    def _initialize_questions(self) -> List[Dict]:
        """Initialize the quiz questions"""
        return [
            {
                "id": "q1",
                "question": "When you hear 'vacation', what's your first instinct?",
                "type": "multiple_choice",
                "options": [
                    "Find the most thrilling activity",
                    "Research historical and cultural sites",
                    "Book the most luxurious accommodation",
                    "Look for natural landscapes",
                    "Explore city attractions",
                    "Find the most relaxing spot",
                    "Plan activities to meet new people"
                ]
            },
            {
                "id": "q2",
                "question": "How do you typically allocate your travel budget?",
                "type": "multiple_choice",
                "options": [
                    "Experiences and adventures",
                    "Museums and cultural tours",
                    "Premium accommodations",
                    "Outdoor activities",
                    "Urban attractions",
                    "Relaxation services",
                    "Social experiences"
                ]
            },
            {
                "id": "q3",
                "question": "What pace feels most natural for your travels?",
                "type": "slider",
                "range": [1, 10],
                "labels": ["Slow & Relaxed", "Fast & Energetic"]
            },
            {
                "id": "q4",
                "question": "Your ideal accommodation is...",
                "type": "multiple_choice",
                "options": [
                    "A base camp for adventures",
                    "Centrally located for cultural access",
                    "A 5-star resort with amenities",
                    "An eco-lodge in nature",
                    "A trendy city hotel",
                    "A quiet spa retreat",
                    "A social hostel or guesthouse"
                ]
            },
            {
                "id": "q5",
                "question": "How structured do you prefer your itinerary?",
                "type": "slider",
                "range": [1, 10],
                "labels": ["Completely Spontaneous", "Fully Planned"]
            },
            {
                "id": "q6",
                "question": "Which activities excite you most?",
                "type": "multiple_choice",
                "options": [
                    "Hiking and extreme sports",
                    "Museum visits and historical tours",
                    "Fine dining and luxury shopping",
                    "Wildlife safaris and nature walks",
                    "City tours and architecture",
                    "Spa and beach lounging",
                    "Local festivals and events"
                ]
            },
            {
                "id": "q7",
                "question": "How important are social interactions during travel?",
                "type": "slider",
                "range": [1, 10],
                "labels": ["Solo Time", "Meet Everyone"]
            },
            {
                "id": "q8",
                "question": "What do you want to bring home from your travels?",
                "type": "multiple_choice",
                "options": [
                    "Adrenaline-filled memories",
                    "Cultural understanding",
                    "Luxury experiences",
                    "Connection with nature",
                    "Urban experiences",
                    "Complete relaxation",
                    "New friendships"
                ]
            }
        ]
    
    def _initialize_centroids(self) -> Dict[str, Dict[str, float]]:
        """Initialize personality centroids for matching"""
        return {
            "Adventure Seeker": {
                "adventure": 9.5, "comfort": 2.0, "culture": 3.0,
                "luxury": 1.5, "nature": 7.0, "urban": 3.0, "social": 5.0
            },
            "Culture Connoisseur": {
                "adventure": 3.0, "comfort": 5.0, "culture": 9.5,
                "luxury": 4.0, "nature": 4.0, "urban": 7.0, "social": 6.0
            },
            "Luxury Escapist": {
                "adventure": 1.5, "comfort": 9.5, "culture": 4.0,
                "luxury": 9.5, "nature": 3.0, "urban": 5.0, "social": 4.0
            },
            "Nature Immerser": {
                "adventure": 6.0, "comfort": 4.0, "culture": 3.0,
                "luxury": 2.0, "nature": 9.5, "urban": 1.5, "social": 3.0
            },
            "Urban Explorer": {
                "adventure": 4.0, "comfort": 6.0, "culture": 7.0,
                "luxury": 5.0, "nature": 2.0, "urban": 9.5, "social": 7.0
            },
            "Relaxation Chaser": {
                "adventure": 1.5, "comfort": 9.5, "culture": 3.0,
                "luxury": 7.0, "nature": 6.0, "urban": 2.0, "social": 2.0
            },
            "Social Connector": {
                "adventure": 5.0, "comfort": 5.0, "culture": 6.0,
                "luxury": 3.0, "nature": 4.0, "urban": 7.0, "social": 9.5
            }
        }
    
    def get_quiz_questions(self) -> List[Dict]:
        """Return quiz questions"""
        return self.questions
    
    def analyze_responses(self, responses: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze responses and determine travel DNA profile"""
        
        # Map multiple choice answers to dimensions
        option_to_dim = {
            0: "adventure", 1: "culture", 2: "luxury", 
            3: "nature", 4: "urban", 5: "comfort", 6: "social"
        }
        
        dimension_scores = {
            "adventure": 0, "comfort": 0, "culture": 0,
            "luxury": 0, "nature": 0, "urban": 0, "social": 0
        }
        
        count = {dim: 0 for dim in dimension_scores}
        
        for q_id, response in responses.items():
            if not q_id.startswith("q"):
                continue
                
            try:
                q_num = int(q_id.replace("q", ""))
            except:
                continue
            
            if q_num in [1, 2, 4, 6, 8]:  # Multiple choice questions
                try:
                    # Find index of selected option
                    q = next(q for q in self.questions if q["id"] == q_id)
                    idx = q["options"].index(response)
                    dim = option_to_dim.get(idx % 7, "adventure")
                    dimension_scores[dim] += 9
                    count[dim] += 1
                except:
                    pass
            
            elif q_num in [3, 5, 7]:  # Slider questions
                try:
                    score = int(response)
                    
                    if q_num == 3:  # Pace: adventure vs comfort
                        dimension_scores["adventure"] += score
                        dimension_scores["comfort"] += (10 - score)
                        count["adventure"] += 1
                        count["comfort"] += 1
                    elif q_num == 5:  # Structure: comfort vs adventure
                        dimension_scores["comfort"] += score
                        dimension_scores["adventure"] += (10 - score)
                        count["comfort"] += 1
                        count["adventure"] += 1
                    elif q_num == 7:  # Social
                        dimension_scores["social"] += score
                        dimension_scores["comfort"] += (10 - score)
                        count["social"] += 1
                        count["comfort"] += 1
                except:
                    pass
        
        # Calculate averages
        for dim in dimension_scores:
            if count[dim] > 0:
                dimension_scores[dim] = dimension_scores[dim] / count[dim]
        
        # Normalize to 0-10 scale
        max_score = max(dimension_scores.values()) or 1
        for dim in dimension_scores:
            dimension_scores[dim] = (dimension_scores[dim] / max_score) * 10
        
        # Find closest personality match
        best_personality = self._find_closest_personality(dimension_scores)
        match_score = self._calculate_match_score(dimension_scores, best_personality)
        
        return {
            "personality_type": best_personality,
            "dimensions": dimension_scores,
            "match_score": round(match_score, 1),
            "details": TRAVEL_PERSONALITIES.get(best_personality, {})
        }
    
    def _find_closest_personality(self, user_dims: Dict[str, float]) -> str:
        """Find closest personality using Euclidean distance"""
        min_dist = float('inf')
        closest = "Adventure Seeker"
        
        for personality, centroid in self.personality_centroids.items():
            dist = 0
            for dim in user_dims:
                if dim in centroid:
                    dist += (user_dims[dim] - centroid[dim]) ** 2
            dist = np.sqrt(dist)
            
            if dist < min_dist:
                min_dist = dist
                closest = personality
        
        return closest
    
    def _calculate_match_score(self, user_dims: Dict[str, float], personality: str) -> float:
        """Calculate match percentage (0-100)"""
        centroid = self.personality_centroids.get(personality, {})
        max_possible = np.sqrt(len(user_dims) * (10 ** 2))
        
        dist = 0
        for dim in user_dims:
            if dim in centroid:
                dist += (user_dims[dim] - centroid[dim]) ** 2
        dist = np.sqrt(dist)
        
        return max(0, 100 - (dist / max_possible) * 100)