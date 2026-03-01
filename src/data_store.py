"""
Synthetic Destination Dataset
20+ global destinations with comprehensive attributes
"""

from typing import List, Dict

DESTINATION_CATEGORIES = [
    "Adventure", "Cultural", "Luxury", "Nature", 
    "Urban", "Beach", "Wellness"
]

class DestinationData:
    """Synthetic destination dataset"""
    
    def __init__(self):
        self.destinations = self._generate_destinations()
    
    def _generate_destinations(self) -> List[Dict]:
        """Generate synthetic destinations"""
        return [
            # Adventure (4)
            {
                "id": "queenstown",
                "name": "Queenstown",
                "country": "New Zealand",
                "category": "Adventure",
                "description": "World's adventure capital with bungee jumping, skiing, and stunning Southern Alps scenery.",
                "average_cost": 3500,
                "best_season": "Spring, Summer, Fall",
                "travel_time": 18,
                "highlights": ["Bungee Jumping", "Milford Sound", "Ski Resorts"],
                "weather_score": 7.5,
                "crowd_score": 6.8,
                "dna_affinity": {"adventure": 9.2, "nature": 8.5, "comfort": 6.0}
            },
            {
                "id": "interlaken",
                "name": "Interlaken",
                "country": "Switzerland",
                "category": "Adventure",
                "description": "Alpine paradise offering paragliding, skiing, and mountain expeditions.",
                "average_cost": 4200,
                "best_season": "Summer, Winter",
                "travel_time": 12,
                "highlights": ["Jungfrau Region", "Paragliding", "Winter Sports"],
                "weather_score": 7.0,
                "crowd_score": 7.2,
                "dna_affinity": {"adventure": 8.8, "nature": 9.0, "comfort": 7.5}
            },
            {
                "id": "cape_town",
                "name": "Cape Town",
                "country": "South Africa",
                "category": "Adventure",
                "description": "Coastal city with Table Mountain, wildlife safaris, and world-class vineyards.",
                "average_cost": 3200,
                "best_season": "Spring, Fall",
                "travel_time": 16,
                "highlights": ["Table Mountain", "Safari Tours", "Penguin Colony"],
                "weather_score": 8.5,
                "crowd_score": 6.5,
                "dna_affinity": {"adventure": 8.0, "nature": 8.5, "culture": 7.0}
            },
            {
                "id": "iceland",
                "name": "Iceland",
                "country": "Iceland",
                "category": "Adventure",
                "description": "Land of fire and ice with glaciers, volcanoes, waterfalls, and Northern Lights.",
                "average_cost": 3800,
                "best_season": "Summer, Winter",
                "travel_time": 7,
                "highlights": ["Northern Lights", "Blue Lagoon", "Glacier Hiking"],
                "weather_score": 6.5,
                "crowd_score": 5.5,
                "dna_affinity": {"adventure": 8.5, "nature": 9.8, "comfort": 5.0}
            },
            
            # Cultural (3)
            {
                "id": "kyoto",
                "name": "Kyoto",
                "country": "Japan",
                "category": "Cultural",
                "description": "Ancient capital with 2000+ temples, traditional tea ceremonies, and seasonal beauty.",
                "average_cost": 3200,
                "best_season": "Spring, Fall",
                "travel_time": 14,
                "highlights": ["Golden Pavilion", "Geisha District", "Cherry Blossoms"],
                "weather_score": 8.0,
                "crowd_score": 8.5,
                "dna_affinity": {"culture": 9.5, "comfort": 8.0, "nature": 7.5}
            },
            {
                "id": "rome",
                "name": "Rome",
                "country": "Italy",
                "category": "Cultural",
                "description": "Eternal city blending ancient history with vibrant modern life and culinary excellence.",
                "average_cost": 2800,
                "best_season": "Spring, Fall",
                "travel_time": 10,
                "highlights": ["Colosseum", "Vatican City", "Italian Cuisine"],
                "weather_score": 8.5,
                "crowd_score": 9.0,
                "dna_affinity": {"culture": 9.2, "urban": 8.0, "comfort": 7.0}
            },
            {
                "id": "istanbul",
                "name": "Istanbul",
                "country": "Turkey",
                "category": "Cultural",
                "description": "City straddling two continents with Byzantine and Ottoman heritage, bustling bazaars.",
                "average_cost": 1800,
                "best_season": "Spring, Fall",
                "travel_time": 12,
                "highlights": ["Hagia Sophia", "Grand Bazaar", "Turkish Baths"],
                "weather_score": 7.5,
                "crowd_score": 7.8,
                "dna_affinity": {"culture": 9.2, "urban": 8.0, "comfort": 6.5}
            },
            
            # Luxury (3)
            {
                "id": "maldives",
                "name": "Maldives",
                "country": "Maldives",
                "category": "Luxury",
                "description": "Tropical paradise with overwater villas, crystal-clear lagoons, and exclusive resorts.",
                "average_cost": 8500,
                "best_season": "Winter, Spring",
                "travel_time": 20,
                "highlights": ["Overwater Bungalows", "Snorkeling", "Private Islands"],
                "weather_score": 9.0,
                "crowd_score": 4.0,
                "dna_affinity": {"luxury": 9.8, "comfort": 9.5, "nature": 8.0}
            },
            {
                "id": "santorini",
                "name": "Santorini",
                "country": "Greece",
                "category": "Luxury",
                "description": "Stunning volcanic island with white-washed buildings, sunset views, and premium amenities.",
                "average_cost": 4500,
                "best_season": "Spring, Summer, Fall",
                "travel_time": 15,
                "highlights": ["Caldera Views", "Wine Tasting", "Luxury Hotels"],
                "weather_score": 9.2,
                "crowd_score": 8.5,
                "dna_affinity": {"luxury": 9.0, "comfort": 8.8, "culture": 7.5}
            },
            {
                "id": "dubai",
                "name": "Dubai",
                "country": "UAE",
                "category": "Luxury",
                "description": "Ultra-modern city with luxury shopping, futuristic architecture, and desert adventures.",
                "average_cost": 5000,
                "best_season": "Winter, Spring",
                "travel_time": 14,
                "highlights": ["Burj Khalifa", "Luxury Malls", "Desert Safaris"],
                "weather_score": 8.0,
                "crowd_score": 7.0,
                "dna_affinity": {"luxury": 9.5, "urban": 8.5, "comfort": 8.0}
            },
            
            # Nature (3)
            {
                "id": "banff",
                "name": "Banff",
                "country": "Canada",
                "category": "Nature",
                "description": "Mountain wilderness in Canadian Rockies with turquoise lakes, glaciers, and wildlife.",
                "average_cost": 3000,
                "best_season": "Summer, Fall",
                "travel_time": 8,
                "highlights": ["Lake Louise", "Wildlife Viewing", "Hiking Trails"],
                "weather_score": 7.8,
                "crowd_score": 7.0,
                "dna_affinity": {"nature": 9.5, "adventure": 8.5, "comfort": 6.5}
            },
            {
                "id": "costa_rica",
                "name": "Costa Rica",
                "country": "Costa Rica",
                "category": "Nature",
                "description": "Biodiversity hotspot with rainforests, volcanoes, beaches, and eco-friendly tourism.",
                "average_cost": 2800,
                "best_season": "Winter, Spring",
                "travel_time": 6,
                "highlights": ["Arenal Volcano", "Cloud Forest", "Wildlife Sanctuaries"],
                "weather_score": 8.5,
                "crowd_score": 6.5,
                "dna_affinity": {"nature": 9.3, "adventure": 8.0, "comfort": 7.0}
            },
            {
                "id": "patagonia",
                "name": "Patagonia",
                "country": "Chile/Argentina",
                "category": "Nature",
                "description": "Remote wilderness with dramatic mountains, glaciers, and pristine lakes.",
                "average_cost": 4000,
                "best_season": "Summer",
                "travel_time": 16,
                "highlights": ["Torres del Paine", "Perito Moreno Glacier", "Trekking"],
                "weather_score": 7.0,
                "crowd_score": 4.5,
                "dna_affinity": {"nature": 9.7, "adventure": 8.0, "comfort": 3.5}
            },
            
            # Urban (3)
            {
                "id": "tokyo",
                "name": "Tokyo",
                "country": "Japan",
                "category": "Urban",
                "description": "Ultra-modern metropolis blending cutting-edge technology with traditional culture.",
                "average_cost": 3800,
                "best_season": "Spring, Fall",
                "travel_time": 14,
                "highlights": ["Shibuya Crossing", "Tsukiji Market", "Traditional Temples"],
                "weather_score": 7.5,
                "crowd_score": 9.5,
                "dna_affinity": {"urban": 9.8, "culture": 8.5, "comfort": 8.0}
            },
            {
                "id": "new_york",
                "name": "New York City",
                "country": "USA",
                "category": "Urban",
                "description": "The city that never sleeps, with world-class museums, Broadway, and diverse neighborhoods.",
                "average_cost": 4200,
                "best_season": "Spring, Fall",
                "travel_time": 8,
                "highlights": ["Broadway", "Central Park", "Metropolitan Museum"],
                "weather_score": 7.0,
                "crowd_score": 9.8,
                "dna_affinity": {"urban": 9.5, "culture": 9.0, "luxury": 8.0}
            },
            {
                "id": "london",
                "name": "London",
                "country": "UK",
                "category": "Urban",
                "description": "Historic global capital with royal heritage, world-class museums, and diverse culture.",
                "average_cost": 3500,
                "best_season": "Spring, Summer, Fall",
                "travel_time": 8,
                "highlights": ["British Museum", "West End", "Historical Sites"],
                "weather_score": 6.5,
                "crowd_score": 8.5,
                "dna_affinity": {"urban": 9.0, "culture": 9.2, "comfort": 7.5}
            },
            
            # Beach (3)
            {
                "id": "bali",
                "name": "Bali",
                "country": "Indonesia",
                "category": "Beach",
                "description": "Island of gods with beautiful beaches, spiritual culture, and luxurious resorts.",
                "average_cost": 2500,
                "best_season": "Summer, Fall",
                "travel_time": 20,
                "highlights": ["Ubud", "Beach Clubs", "Water Temples"],
                "weather_score": 8.8,
                "crowd_score": 7.5,
                "dna_affinity": {"comfort": 8.5, "nature": 8.0, "culture": 7.5}
            },
            {
                "id": "tulum",
                "name": "Tulum",
                "country": "Mexico",
                "category": "Beach",
                "description": "Bohemian beach town with Mayan ruins, cenotes, and eco-chic accommodations.",
                "average_cost": 2200,
                "best_season": "Winter, Spring",
                "travel_time": 5,
                "highlights": ["Mayan Ruins", "Cenotes", "Beach Clubs"],
                "weather_score": 9.0,
                "crowd_score": 7.0,
                "dna_affinity": {"comfort": 8.0, "nature": 8.5, "culture": 7.0}
            },
            {
                "id": "phuket",
                "name": "Phuket",
                "country": "Thailand",
                "category": "Beach",
                "description": "Thailand's largest island with stunning beaches, vibrant nightlife, and island hopping.",
                "average_cost": 2000,
                "best_season": "Winter, Spring",
                "travel_time": 18,
                "highlights": ["Phi Phi Islands", "Beach Resorts", "Night Markets"],
                "weather_score": 8.5,
                "crowd_score": 8.0,
                "dna_affinity": {"comfort": 8.0, "nature": 7.5, "adventure": 6.5}
            },
            
            # Wellness (3)
            {
                "id": "ubud",
                "name": "Ubud",
                "country": "Indonesia",
                "category": "Wellness",
                "description": "Spiritual and wellness center in Bali with yoga retreats, healing centers, and organic cuisine.",
                "average_cost": 2000,
                "best_season": "Year-round",
                "travel_time": 20,
                "highlights": ["Yoga Retreats", "Healing Centers", "Monkey Forest"],
                "weather_score": 8.5,
                "crowd_score": 6.0,
                "dna_affinity": {"comfort": 9.0, "nature": 8.5, "culture": 7.0}
            },
            {
                "id": "sedona",
                "name": "Sedona",
                "country": "USA",
                "category": "Wellness",
                "description": "Desert town famous for red rock formations, spiritual energy vortices, and wellness retreats.",
                "average_cost": 1800,
                "best_season": "Spring, Fall",
                "travel_time": 4,
                "highlights": ["Vortex Sites", "Spa Retreats", "Hiking Trails"],
                "weather_score": 8.0,
                "crowd_score": 5.5,
                "dna_affinity": {"comfort": 8.8, "nature": 8.5, "adventure": 7.0}
            },
            {
                "id": "rishikesh",
                "name": "Rishikesh",
                "country": "India",
                "category": "Wellness",
                "description": "Yoga capital of the world on the Ganges River, with ashrams, meditation centers, and spiritual experiences.",
                "average_cost": 1200,
                "best_season": "Winter, Spring",
                "travel_time": 16,
                "highlights": ["Yoga Ashrams", "Ganga Aarti", "River Rafting"],
                "weather_score": 8.0,
                "crowd_score": 6.5,
                "dna_affinity": {"comfort": 8.0, "nature": 7.5, "culture": 8.0}
            }
        ]
    
    def get_all_destinations(self) -> List[Dict]:
        """Return all destinations"""
        return self.destinations
    
    def get_by_category(self, category: str) -> List[Dict]:
        """Filter destinations by category"""
        return [d for d in self.destinations if d["category"] == category]
    
    def get_by_id(self, dest_id: str) -> Dict:
        """Get destination by ID"""
        for dest in self.destinations:
            if dest["id"] == dest_id:
                return dest
        return None