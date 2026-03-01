"""
Gemini AI Client for Trip Explanations
Optional feature - falls back to mock explanations if API key not available
"""

import streamlit as st
from typing import Dict, Any, Optional

class GeminiExplainer:
    """AI-powered trip explanation generator"""
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or st.secrets.get("GEMINI_API_KEY", "")
        
        if not self.api_key:
            self.mock_mode = True
        else:
            try:
                import google.generativeai as genai
                genai.configure(api_key=self.api_key)
                self.model = genai.GenerativeModel('gemini-pro')
                self.mock_mode = False
            except:
                self.mock_mode = True
    
    def generate_trip_explanation(self, destination: Dict, 
                                 user_profile: Dict, 
                                 preferences: Dict) -> Dict[str, str]:
        """Generate AI-powered trip justification and regret preview"""
        
        if self.mock_mode:
            return self._mock_explanation(destination, user_profile)
        
        try:
            prompt = self._build_prompt(destination, user_profile, preferences)
            response = self.model.generate_content(prompt)
            
            if response.text:
                return self._parse_response(response.text)
            else:
                return self._mock_explanation(destination, user_profile)
        except:
            return self._mock_explanation(destination, user_profile)
    
    def generate_trip_comparison(self, dest_a: Dict, dest_b: Dict, 
                               user_profile: Dict) -> str:
        """Generate comparison between two destinations"""
        
        if self.mock_mode:
            return self._mock_comparison(dest_a, dest_b, user_profile)
        
        try:
            personality = user_profile.get("personality_type", "Traveler") if user_profile else "Traveler"
            
            prompt = f"""
            Compare these two destinations for a traveler with {personality} personality:
            
            Destination A: {dest_a['name']}, {dest_a['country']}
            Category: {dest_a['category']}
            Highlights: {', '.join(dest_a['highlights'][:3])}
            
            Destination B: {dest_b['name']}, {dest_b['country']}
            Category: {dest_b['category']}
            Highlights: {', '.join(dest_b['highlights'][:3])}
            
            Provide a concise comparison (150-200 words) focusing on:
            1. Which better aligns with their personality
            2. Key experiential differences
            3. Trade-offs for each option
            """
            
            response = self.model.generate_content(prompt)
            return response.text if response.text else self._mock_comparison(dest_a, dest_b, user_profile)
        except:
            return self._mock_comparison(dest_a, dest_b, user_profile)
    
    def _build_prompt(self, dest: Dict, profile: Dict, prefs: Dict) -> str:
        """Build prompt for Gemini"""
        personality = profile.get("personality_type", "Traveler") if profile else "Traveler"
        dimensions = profile.get("dimensions", {}) if profile else {}
        
        return f"""
        You are a travel psychologist for VoyageAI.
        
        Traveler Personality: {personality}
        Traveler Dimensions: {dimensions}
        
        Destination: {dest['name']}, {dest['country']}
        Category: {dest['category']}
        Description: {dest['description']}
        Highlights: {', '.join(dest['highlights'][:3])}
        
        Generate TWO sections:
        
        JUSTIFICATION: Why this destination is a perfect psychological fit (100-150 words)
        
        REGRET_PREVIEW: Honest trade-offs they might experience (50-75 words)
        
        Format:
        JUSTIFICATION: [text]
        REGRET_PREVIEW: [text]
        """
    
    def _parse_response(self, text: str) -> Dict[str, str]:
        """Parse Gemini response"""
        lines = text.strip().split('\n')
        justification = ""
        regret = ""
        current = None
        
        for line in lines:
            if line.startswith("JUSTIFICATION:"):
                current = "just"
                justification = line.replace("JUSTIFICATION:", "").strip()
            elif line.startswith("REGRET_PREVIEW:"):
                current = "regret"
                regret = line.replace("REGRET_PREVIEW:", "").strip()
            elif current == "just":
                justification += " " + line.strip()
            elif current == "regret":
                regret += " " + line.strip()
        
        return {
            "justification": justification or "This destination aligns with your travel personality.",
            "regret_preview": regret or "Consider timing and your personal preferences."
        }
    
    def _mock_explanation(self, dest: Dict, profile: Dict) -> Dict[str, str]:
        """Mock explanation when API unavailable"""
        category = dest.get("category", "").lower()
        
        justifications = {
            "adventure": "Your adventurous spirit will thrive here. The activities and landscapes are designed for those seeking thrill and authentic experiences.",
            "cultural": "This destination satisfies your curiosity for history and culture. You'll find deep meaning in its traditions and stories.",
            "luxury": "Every detail has been crafted for your comfort and enjoyment. You'll appreciate the premium experiences and exceptional service.",
            "nature": "You'll feel rejuvenated by the natural beauty and peaceful environments. This place speaks to your connection with the earth.",
            "urban": "The energy and diversity of this city match your dynamic personality. You'll discover endless opportunities for exploration.",
            "beach": "Your desire for relaxation and beauty is perfectly met here. The serene environment allows for true rejuvenation.",
            "wellness": "This destination aligns with your need for balance and self-care. You'll find the peace and restoration you seek."
        }
        
        regrets = {
            "adventure": "If you prefer predictable plans and luxury, the physical demands and rustic conditions might challenge you.",
            "cultural": "If you primarily seek relaxation or nightlife, the focus on structured cultural activities might feel overwhelming.",
            "luxury": "Those seeking authentic, rugged experiences might find the premium environment less appealing.",
            "nature": "If you crave urban excitement and constant connectivity, the remote location might feel isolating.",
            "urban": "If you need solitude and quiet, the city's constant energy and crowds could be overwhelming.",
            "beach": "Adventure-seekers or culture enthusiasts might find extended beach time less stimulating.",
            "wellness": "Travelers seeking high-energy activities might find the peaceful pace too gentle."
        }
        
        cat_key = category if category in justifications else "adventure"
        
        return {
            "justification": justifications.get(cat_key, justifications["adventure"]),
            "regret_preview": regrets.get(cat_key, regrets["adventure"])
        }
    
    def _mock_comparison(self, dest_a: Dict, dest_b: Dict, profile: Dict) -> str:
        """Mock comparison when API unavailable"""
        personality = profile.get("personality_type", "Traveler") if profile else "Traveler"
        
        return f"""
        For a {personality} traveler, these destinations offer distinct experiences:
        
        {dest_a['name']} focuses on {dest_a['category'].lower()} experiences with highlights including {dest_a['highlights'][0].lower()}. This destination provides structured opportunities that align well with travelers seeking {dest_a['category'].lower()} immersion.
        
        {dest_b['name']} emphasizes {dest_b['category'].lower()} with highlights such as {dest_b['highlights'][0].lower()}. This option might better suit those valuing {dest_b['category'].lower()} aspects of travel.
        
        Choose {dest_a['name']} if you prioritize structured discovery and {dest_a['category'].lower()} experiences. Opt for {dest_b['name']} if you prefer {dest_b['category'].lower()} and flexible exploration. Your {personality} personality could find fulfillment in either, depending on your current travel goals.
        """