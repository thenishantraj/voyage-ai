"""Destination Data Store"""

from typing import List, Dict, Any

# Destination Categories
DESTINATION_CATEGORIES = [
    "Adventure", "Cultural", "Luxury", "Nature", 
    "Urban", "Beach", "Wellness"
]

class DestinationData:
    """Store and manage destination data"""
    
    def __init__(self):
        self.destinations = self._initialize_destinations()
    
    def _initialize_destinations(self) -> List[Dict[str, Any]]:
        """Initialize sample destinations"""
        return [
            {
                "id": 1,
                "name": "Swiss Alps",
                "country": "Switzerland",
                "category": "Adventure",
                "description": "Experience breathtaking mountain views, world-class hiking trails, and charming alpine villages. Perfect for outdoor enthusiasts and nature lovers.",
                "highlights": ["Matterhorn", "Jungfrau Region", "Lake Geneva", "Zermatt", "Interlaken"],
                "average_cost": 3500,
                "best_season": "June-September",
                "weather_score": 8.5,
                "crowd_score": 7.0,
                "dna_affinity": {
                    "adventure": 9.5, "comfort": 7.0, "culture": 6.0,
                    "luxury": 7.5, "nature": 9.0, "urban": 4.0, "social": 6.5
                }
            },
            {
                "id": 2,
                "name": "Kyoto",
                "country": "Japan",
                "category": "Cultural",
                "description": "Ancient temples, traditional tea houses, and stunning gardens. Immerse yourself in Japanese culture and history.",
                "highlights": ["Fushimi Inari Shrine", "Kinkaku-ji", "Arashiyama Bamboo Grove", "Gion District"],
                "average_cost": 2800,
                "best_season": "March-May, October-November",
                "weather_score": 8.0,
                "crowd_score": 8.5,
                "dna_affinity": {
                    "adventure": 4.0, "comfort": 7.5, "culture": 9.5,
                    "luxury": 6.5, "nature": 7.0, "urban": 7.5, "social": 7.0
                }
            },
            {
                "id": 3,
                "name": "Maldives",
                "country": "Maldives",
                "category": "Luxury",
                "description": "Overwater bungalows, crystal-clear waters, and ultimate relaxation. The epitome of luxury tropical paradise.",
                "highlights": ["Overwater Villas", "House Reef", "Male Atoll", "Biosphere Reserves"],
                "average_cost": 5000,
                "best_season": "November-April",
                "weather_score": 9.0,
                "crowd_score": 6.0,
                "dna_affinity": {
                    "adventure": 3.0, "comfort": 9.5, "culture": 3.0,
                    "luxury": 9.5, "nature": 8.5, "urban": 2.0, "social": 5.0
                }
            },
            {
                "id": 4,
                "name": "Costa Rica",
                "country": "Costa Rica",
                "category": "Nature",
                "description": "Rainforests, wildlife, and eco-adventures. A paradise for nature lovers and sustainable travelers.",
                "highlights": ["Monteverde Cloud Forest", "Arenal Volcano", "Manuel Antonio", "Tortuguero"],
                "average_cost": 2200,
                "best_season": "December-April",
                "weather_score": 8.5,
                "crowd_score": 6.5,
                "dna_affinity": {
                    "adventure": 8.0, "comfort": 5.5, "culture": 5.0,
                    "luxury": 4.0, "nature": 9.5, "urban": 3.0, "social": 7.0
                }
            },
            {
                "id": 5,
                "name": "New York City",
                "country": "USA",
                "category": "Urban",
                "description": "The city that never sleeps. World-class dining, Broadway shows, iconic landmarks, and endless energy.",
                "highlights": ["Times Square", "Central Park", "Empire State Building", "Statue of Liberty"],
                "average_cost": 3200,
                "best_season": "April-June, September-November",
                "weather_score": 7.5,
                "crowd_score": 9.0,
                "dna_affinity": {
                    "adventure": 6.0, "comfort": 7.0, "culture": 8.5,
                    "luxury": 8.0, "nature": 4.0, "urban": 9.5, "social": 8.5
                }
            },
            {
                "id": 6,
                "name": "Phuket",
                "country": "Thailand",
                "category": "Beach",
                "description": "Stunning beaches, vibrant nightlife, and Thai hospitality. Perfect for beach lovers and party seekers.",
                "highlights": ["Patong Beach", "Phi Phi Islands", "Big Buddha", "Old Phuket Town"],
                "average_cost": 1800,
                "best_season": "November-February",
                "weather_score": 8.5,
                "crowd_score": 8.0,
                "dna_affinity": {
                    "adventure": 7.0, "comfort": 7.5, "culture": 6.5,
                    "luxury": 6.0, "nature": 7.5, "urban": 6.0, "social": 8.0
                }
            },
            {
                "id": 7,
                "name": "Bali",
                "country": "Indonesia",
                "category": "Wellness",
                "description": "Spiritual retreats, yoga, and natural beauty. Find your inner peace in this tropical paradise.",
                "highlights": ["Ubud", "Tanah Lot Temple", "Rice Terraces", "Seminyak"],
                "average_cost": 2000,
                "best_season": "April-October",
                "weather_score": 8.0,
                "crowd_score": 7.5,
                "dna_affinity": {
                    "adventure": 6.5, "comfort": 8.0, "culture": 8.0,
                    "luxury": 7.0, "nature": 8.5, "urban": 5.0, "social": 7.5
                }
            },
            {
                "id": 8,
                "name": "Rome",
                "country": "Italy",
                "category": "Cultural",
                "description": "Ancient history, incredible food, and romantic atmosphere. Walk through thousands of years of history.",
                "highlights": ["Colosseum", "Vatican City", "Trevi Fountain", "Roman Forum"],
                "average_cost": 2600,
                "best_season": "April-June, September-October",
                "weather_score": 8.0,
                "crowd_score": 8.5,
                "dna_affinity": {
                    "adventure": 4.5, "comfort": 7.5, "culture": 9.5,
                    "luxury": 7.0, "nature": 5.0, "urban": 8.5, "social": 7.5
                }
            },
            {
                "id": 9,
                "name": "Queenstown",
                "country": "New Zealand",
                "category": "Adventure",
                "description": "The adventure capital of the world. Bungee jumping, skydiving, and stunning landscapes.",
                "highlights": ["Bungee Jumping", "Milford Sound", "Skiing", "Lake Wakatipu"],
                "average_cost": 3000,
                "best_season": "December-February",
                "weather_score": 7.5,
                "crowd_score": 6.5,
                "dna_affinity": {
                    "adventure": 9.5, "comfort": 6.0, "culture": 4.0,
                    "luxury": 5.5, "nature": 8.5, "urban": 4.0, "social": 7.0
                }
            },
            {
                "id": 10,
                "name": "Dubai",
                "country": "UAE",
                "category": "Luxury",
                "description": "Ultra-modern architecture, luxury shopping, and desert adventures. Experience the future of travel.",
                "highlights": ["Burj Khalifa", "Palm Jumeirah", "Desert Safari", "Dubai Mall"],
                "average_cost": 4000,
                "best_season": "November-March",
                "weather_score": 9.0,
                "crowd_score": 8.0,
                "dna_affinity": {
                    "adventure": 6.0, "comfort": 9.0, "culture": 5.0,
                    "luxury": 9.5, "nature": 3.0, "urban": 9.0, "social": 7.5
                }
            }
        ]
    
    def get_all_destinations(self) -> List[Dict[str, Any]]:
        """Return all destinations"""
        return self.destinations
    
    def get_destination_by_id(self, dest_id: int) -> Dict[str, Any]:
        """Get destination by ID"""
        for dest in self.destinations:
            if dest["id"] == dest_id:
                return dest
        return None
    
    def get_destinations_by_category(self, category: str) -> List[Dict[str, Any]]:
        """Filter destinations by category"""
        return [d for d in self.destinations if d["category"] == category]
