"""
VoyageAI - Main Application
A confidence-first travel discovery platform with neon-dark theme
"""

import streamlit as st
import sys
import os
from pathlib import Path
import hashlib
from datetime import datetime, timedelta
import plotly.graph_objects as go
import pandas as pd

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

# Page configuration - MUST BE FIRST STREAMLIT COMMAND
st.set_page_config(
    page_title="VoyageAI | Discover with Confidence",
    page_icon="✈️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Import local modules
from src.auth import hash_password, verify_password, register_user, logout
from src.dna_engine import TravelDNAProfiler, TRAVEL_PERSONALITIES
from src.recommender import ConfidenceEngine
from src.data_store import DestinationData, DESTINATION_CATEGORIES

# Try to import Gemini client (optional)
try:
    from src.gemini_client import GeminiExplainer
    GEMINI_AVAILABLE = True
except:
    GEMINI_AVAILABLE = False

# ========== LOAD CUSTOM CSS ==========
def load_css():
    """Load custom CSS with error handling"""
    css_path = Path(__file__).parent / "assets" / "styles.css"
    try:
        if css_path.exists():
            with open(css_path, 'r', encoding='utf-8') as f:
                css_content = f.read()
                st.markdown(f"<style>{css_content}</style>", unsafe_allow_html=True)
        else:
            # Fallback message
            st.warning("CSS file not found. Using default styling.")
    except Exception as e:
        st.error(f"CSS loading error: {e}")

# ========== INITIALIZE SESSION STATE ==========
def init_session_state():
    """Initialize all session state variables"""
    defaults = {
        'logged_in': False,
        'username': '',
        'user_email': '',
        'current_step': 0,
        'quiz_responses': {},
        'user_profile': None,
        'recommendations': None,
        'show_comparison': False,
        'compare_destinations': [],
        'auth_mode': 'login',
        'active_tab': 0,
        'emotion': None,
        'users_db': {
            'demo': {
                'password': hashlib.sha256('demo123'.encode()).hexdigest(),
                'email': 'demo@example.com',
                'created_at': datetime.now().isoformat()
            }
        }
    }
    
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

# Initialize
load_css()
init_session_state()

# ========== INITIALIZE APP COMPONENTS ==========
dna_profiler = TravelDNAProfiler()
confidence_engine = ConfidenceEngine()
data_store = DestinationData()
gemini = GeminiExplainer() if GEMINI_AVAILABLE else None

# ========== AUTHENTICATION UI ==========
def render_auth():
    """Render login/signup interface with neon-dark theme"""
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("""
        <div style="text-align: center; margin-bottom: 40px;">
            <h1>✈️ VoyageAI</h1>
            <p style="color: #00d4ff; font-size: 1.2rem;">Discover with Confidence</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Tab buttons
        col_a, col_b = st.columns(2)
        with col_a:
            if st.button("LOGIN", use_container_width=True, 
                        type="primary" if st.session_state.auth_mode == 'login' else "secondary"):
                st.session_state.auth_mode = 'login'
                st.rerun()
        with col_b:
            if st.button("SIGN UP", use_container_width=True,
                        type="primary" if st.session_state.auth_mode == 'signup' else "secondary"):
                st.session_state.auth_mode = 'signup'
                st.rerun()
        
        st.markdown("<hr style='margin: 20px 0; border: 1px solid #00d4ff;'>", unsafe_allow_html=True)
        
        # Login Form
        if st.session_state.auth_mode == 'login':
            st.markdown("<h3 style='text-align: center; color: #00d4ff; margin-bottom: 30px;'>Welcome Back</h3>", unsafe_allow_html=True)
            
            with st.form("login_form"):
                username = st.text_input("Username", placeholder="Enter your username", key="login_user")
                password = st.text_input("Password", type="password", placeholder="Enter your password", key="login_pass")
                
                col1, col2, col3 = st.columns([1, 2, 1])
                with col2:
                    submitted = st.form_submit_button("Login", use_container_width=True)
                
                if submitted:
                    if username and password:
                        if verify_password(username, password, st.session_state.users_db):
                            st.session_state.logged_in = True
                            st.session_state.username = username
                            st.session_state.user_email = st.session_state.users_db[username]['email']
                            st.success("Login successful!")
                            st.rerun()
                        else:
                            st.error("Invalid username or password")
                    else:
                        st.error("Please fill in all fields")
        
        # Signup Form
        else:
            st.markdown("<h3 style='text-align: center; color: #00d4ff; margin-bottom: 30px;'>Create Your Account</h3>", unsafe_allow_html=True)
            
            with st.form("signup_form"):
                new_username = st.text_input("Username", placeholder="Choose a username", key="signup_user")
                new_email = st.text_input("Email", placeholder="Enter your email", key="signup_email")
                new_password = st.text_input("Password", type="password", placeholder="Choose a password (min. 6 chars)", key="signup_pass")
                confirm_password = st.text_input("Confirm Password", type="password", placeholder="Confirm your password", key="signup_confirm")
                
                col1, col2, col3 = st.columns([1, 2, 1])
                with col2:
                    submitted = st.form_submit_button("Create Account", use_container_width=True)
                
                if submitted:
                    if not all([new_username, new_email, new_password, confirm_password]):
                        st.error("Please fill in all fields")
                    elif new_password != confirm_password:
                        st.error("Passwords do not match")
                    elif len(new_password) < 6:
                        st.error("Password must be at least 6 characters")
                    else:
                        success, message = register_user(new_username, new_email, new_password, st.session_state.users_db)
                        if success:
                            st.success(message)
                            st.session_state.auth_mode = 'login'
                            st.rerun()
                        else:
                            st.error(message)
        
        # Demo credentials
        st.markdown("""
        <div style="
            margin-top: 30px;
            padding: 15px;
            background: rgba(255, 255, 255, 0.05);
            border: 1px solid #00d4ff;
            border-radius: 10px;
            text-align: center;
        ">
            <p style="color: #ffffff; margin-bottom: 5px;"><strong>Demo Credentials:</strong></p>
            <p style="color: #00d4ff;">Username: demo | Password: demo123</p>
        </div>
        """, unsafe_allow_html=True)

# ========== SIDEBAR ==========
def render_sidebar():
    """Render sidebar with user info and navigation"""
    with st.sidebar:
        st.markdown(f"""
        <div style="
            background: linear-gradient(135deg, #00d4ff20, #1a1a2e);
            border: 2px solid #00d4ff;
            padding: 20px;
            border-radius: 15px;
            margin-bottom: 20px;
            text-align: center;
        ">
            <h3 style="color: #00d4ff; margin-bottom: 5px;">Welcome, {st.session_state.username}!</h3>
            <p style="color: #cccccc; font-size: 0.9rem;">{st.session_state.user_email}</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Navigation
        if st.button("🏠 Home", use_container_width=True):
            st.session_state.active_tab = 0
            st.rerun()
        
        if st.button("🧬 Retake DNA Quiz", use_container_width=True):
            st.session_state.current_step = 0
            st.session_state.quiz_responses = {}
            st.session_state.user_profile = None
            st.session_state.recommendations = None
            st.session_state.active_tab = 0
            st.rerun()
        
        if st.button("🗺️ All Destinations", use_container_width=True):
            st.session_state.active_tab = 3
            st.rerun()
        
        st.markdown("---")
        
        # User stats
        if st.session_state.user_profile:
            personality = st.session_state.user_profile['personality_type']
            details = TRAVEL_PERSONALITIES.get(personality, {})
            
            st.markdown(f"""
            <div style="
                background: rgba(255, 255, 255, 0.05);
                border: 1px solid #00d4ff;
                padding: 15px;
                border-radius: 15px;
                margin-bottom: 20px;
            ">
                <p style="color: #00d4ff; margin-bottom: 5px;"><strong>Your DNA:</strong></p>
                <p style="color: #ffffff; font-weight: 600;">{personality} {details.get('emoji', '')}</p>
                <p style="color: #00d4ff; margin-top: 10px;"><strong>Match Score:</strong></p>
                <p style="color: #00ff00; font-size: 1.5rem; font-weight: 700;">{st.session_state.user_profile['match_score']}%</p>
            </div>
            """, unsafe_allow_html=True)
        
        if st.button("🚪 Logout", use_container_width=True):
            logout()

# ========== MAIN CONTENT ==========
def render_hero():
    """Render hero section"""
    st.markdown("""
    <div style="
        background: linear-gradient(135deg, rgba(0, 212, 255, 0.1) 0%, rgba(26, 26, 46, 0.9) 100%);
        border: 2px solid #00d4ff;
        border-radius: 20px;
        padding: 60px 40px;
        margin: 20px 0;
        text-align: center;
        box-shadow: 0 20px 40px rgba(0, 212, 255, 0.2);
    ">
        <h1 style="font-size: 3.5rem; margin-bottom: 20px;">Discover Your Next Journey with <span style="color: #00d4ff;">Confidence</span></h1>
        <p style="color: #ffffff; font-size: 1.2rem; max-width: 800px; margin: 0 auto;">VoyageAI uses psychological profiling to eliminate decision anxiety and match you with destinations that truly resonate with your personality</p>
    </div>
    """, unsafe_allow_html=True)

def render_dna_quiz():
    """Render DNA quiz"""
    st.markdown("<h2>🧬 Your Travel DNA</h2>", unsafe_allow_html=True)
    
    questions = dna_profiler.get_quiz_questions()
    
    if st.session_state.current_step < len(questions):
        q = questions[st.session_state.current_step]
        
        st.markdown(f"""
        <div style="
            background: rgba(255, 255, 255, 0.05);
            border: 2px solid #00d4ff;
            border-radius: 20px;
            padding: 30px;
            margin-bottom: 20px;
        ">
            <h3 style="color: #ffffff; margin-bottom: 20px;">{q['question']}</h3>
        """, unsafe_allow_html=True)
        
        if q["type"] == "multiple_choice":
            default_index = 0
            if q['id'] in st.session_state.quiz_responses:
                try:
                    default_index = q["options"].index(st.session_state.quiz_responses[q['id']])
                except:
                    pass
            
            response = st.radio(
                "Select your answer:",
                options=q["options"],
                key=f"q_{q['id']}",
                index=default_index,
                label_visibility="collapsed"
            )
            st.session_state.quiz_responses[q['id']] = response
        
        elif q["type"] == "slider":
            min_val, max_val = q.get("range", [1, 10])
            labels = q.get("labels", ["Low", "High"])
            
            col1, col2 = st.columns([1, 5])
            with col1:
                st.markdown(f"<p style='color: #cccccc;'>{labels[0]}</p>", unsafe_allow_html=True)
            with col2:
                response = st.slider(
                    "",
                    min_value=min_val,
                    max_value=max_val,
                    value=st.session_state.quiz_responses.get(q['id'], 5),
                    key=f"slider_{q['id']}",
                    label_visibility="collapsed"
                )
            with col1:
                st.markdown(f"<p style='color: #cccccc;'>{labels[1]}</p>", unsafe_allow_html=True)
            
            st.session_state.quiz_responses[q['id']] = response
        
        st.markdown("</div>", unsafe_allow_html=True)
        
        # Navigation
        col1, col2, col3 = st.columns([1, 1, 1])
        with col1:
            if st.session_state.current_step > 0:
                if st.button("← Previous", use_container_width=True):
                    st.session_state.current_step -= 1
                    st.rerun()
        
        with col3:
            if st.session_state.current_step < len(questions) - 1:
                if st.button("Next →", use_container_width=True):
                    st.session_state.current_step += 1
                    st.rerun()
            else:
                if st.button("✨ See My DNA", type="primary", use_container_width=True):
                    profile = dna_profiler.analyze_responses(st.session_state.quiz_responses)
                    st.session_state.user_profile = profile
                    st.rerun()
        
        # Progress
        progress = ((st.session_state.current_step + 1) / len(questions)) * 100
        st.markdown(f"""
        <div style="
            background: rgba(255, 255, 255, 0.05);
            border: 1px solid #00d4ff;
            padding: 20px;
            border-radius: 15px;
            margin-top: 20px;
        ">
            <div style="display: flex; justify-content: space-between; margin-bottom: 10px;">
                <span style="color: #cccccc;">Question {st.session_state.current_step + 1}/{len(questions)}</span>
                <span style="color: #00d4ff;">{progress:.0f}% Complete</span>
            </div>
            <div style="
                height: 8px;
                background: rgba(255, 255, 255, 0.1);
                border-radius: 4px;
                overflow: hidden;
            ">
                <div style="
                    height: 100%;
                    width: {progress}%;
                    background: linear-gradient(90deg, #00d4ff, #1a1a2e);
                    border-radius: 4px;
                "></div>
            </div>
        </div>
        """, unsafe_allow_html=True)

def render_dna_results():
    """Render DNA results"""
    if not st.session_state.user_profile:
        return
    
    profile = st.session_state.user_profile
    personality = profile['personality_type']
    details = profile.get('details', {})
    
    st.markdown("<h2>✨ Your Travel DNA Results</h2>", unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown(f"""
        <div style="
            background: rgba(255, 255, 255, 0.05);
            border: 2px solid #00d4ff;
            border-radius: 20px;
            padding: 30px;
            height: 100%;
        ">
            <h3 style="color: #00d4ff; margin-bottom: 15px;">{personality} {details.get('emoji', '')}</h3>
            <p style="color: #ffffff; margin-bottom: 10px;"><strong style="color: #00d4ff;">Traits:</strong> {details.get('traits', '')}</p>
            <p style="color: #ffffff; margin-bottom: 10px;"><strong style="color: #00d4ff;">Style:</strong> {details.get('style', '')}</p>
            <p style="color: #ffffff; margin-bottom: 20px;"><strong style="color: #00d4ff;">Perfect For:</strong> {details.get('perfect_for', '')}</p>
            <div style="
                background: rgba(0, 212, 255, 0.1);
                border: 1px solid #00d4ff;
                padding: 20px;
                border-radius: 15px;
                text-align: center;
            ">
                <span style="color: #cccccc; font-size: 1.1rem;">Match Score:</span>
                <span style="color: #00ff00; font-size: 2.5rem; font-weight: 700; display: block;">{profile['match_score']}%</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        # Radar chart
        dimensions = profile['dimensions']
        
        fig = go.Figure(data=go.Scatterpolar(
            r=[dimensions.get('adventure', 5), dimensions.get('comfort', 5), 
               dimensions.get('culture', 5), dimensions.get('luxury', 5), 
               dimensions.get('nature', 5), dimensions.get('urban', 5),
               dimensions.get('social', 5)],
            theta=['Adventure', 'Comfort', 'Culture', 'Luxury', 'Nature', 'Urban', 'Social'],
            fill='toself',
            line_color='#00d4ff',
            fillcolor='rgba(0, 212, 255, 0.2)'
        ))
        
        fig.update_layout(
            polar=dict(
                radialaxis=dict(visible=True, range=[0, 10], color='#cccccc'),
                bgcolor='rgba(255, 255, 255, 0.05)'
            ),
            showlegend=False,
            height=400,
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#ffffff')
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("Continue to Trip Planner →", type="primary", use_container_width=True):
            st.session_state.active_tab = 1
            st.rerun()

def render_trip_planner():
    """Render trip planner - FIXED VERSION"""
    st.markdown("<h2>🧭 Plan Your Trip</h2>", unsafe_allow_html=True)
    
    with st.form("planner_form"):
        st.markdown("""
        <div style="
            background: rgba(255, 255, 255, 0.05);
            border: 2px solid #00d4ff;
            border-radius: 20px;
            padding: 30px;
        ">
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            travel_style = st.selectbox(
                "Travel Style",
                ["Solo", "Couple", "Family", "Friends", "Business"]
            )
            
            budget_min = st.number_input("Minimum Budget ($)", min_value=500, max_value=10000, value=1500, step=500)
            budget_max = st.number_input("Maximum Budget ($)", min_value=500, max_value=10000, value=4000, step=500)
            
            start_date = st.date_input("Start Date", datetime.now())
            end_date = st.date_input("End Date", datetime.now() + timedelta(days=7))
        
        with col2:
            interests = st.multiselect(
                "Interests",
                ["Adventure", "Culture", "Luxury", "Nature", "Urban", "Beach", "Wellness", "Food"],
                default=["Adventure", "Culture"]
            )
            
            weather_priority = st.slider("Weather Importance", 1, 10, 7)
            crowd_tolerance = st.slider("Crowd Tolerance", 1, 10, 5)
            
            st.markdown("<br>", unsafe_allow_html=True)
            submitted = st.form_submit_button("🎯 Find Confident Matches", type="primary", use_container_width=True)
        
        st.markdown("</div>", unsafe_allow_html=True)
        
        if submitted:
            with st.spinner("Analyzing destinations..."):
                # FIXED: Make sure travel_dna is passed correctly
                user_profile = st.session_state.user_profile if st.session_state.user_profile else {}
                
                prefs = {
                    "travel_style": travel_style,
                    "budget_min": budget_min,
                    "budget_max": budget_max,
                    "travel_dates": (start_date.isoformat(), end_date.isoformat()),
                    "interests": interests,
                    "weather_priority": weather_priority,
                    "crowd_tolerance": crowd_tolerance,
                    "travel_dna": user_profile  # Pass the full profile
                }
                
                destinations = data_store.get_all_destinations()
                recs = confidence_engine.calculate_recommendations(destinations, prefs)
                
                # FIXED: Add debug info
                if recs and len(recs) > 0:
                    st.session_state.recommendations = recs
                    st.session_state.active_tab = 2
                    st.success(f"Found {len(recs)} matching destinations!")
                    st.rerun()
                else:
                    st.error("No destinations match your criteria. Try adjusting your filters.")

def render_recommendations():
    """Render recommendations - FIXED VERSION"""
    if not st.session_state.recommendations:
        st.info("👆 Go to Trip Planner to get your personalized recommendations")
        return
    
    st.markdown("<h2>🎯 Your Confidence-Backed Matches</h2>", unsafe_allow_html=True)
    
    recs = st.session_state.recommendations
    
    for i, rec in enumerate(recs[:6]):
        conf = rec['confidence_score']
        
        # Determine color based on confidence
        if conf >= 85:
            color = "#00ff00"
            badge = "Excellent Match"
        elif conf >= 70:
            color = "#00d4ff"
            badge = "Great Match"
        else:
            color = "#ffaa00"
            badge = "Good Match"
        
        # FIXED: Use st.markdown with proper formatting, not just HTML
        st.markdown(f"""
        <div class="trip-card">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 15px; flex-wrap: wrap; gap: 15px;">
                <h3 style="margin: 0;">{rec['name']}, {rec['country']}</h3>
                <div style="text-align: center;">
                    <div class="confidence-score" style="color: {color};">{conf:.0f}%</div>
                    <span style="color: #cccccc; font-size: 0.8rem;">{badge}</span>
                </div>
            </div>
            
            <div style="display: flex; gap: 20px; margin-bottom: 15px; color: #cccccc; flex-wrap: wrap;">
                <span>📍 {rec['category']}</span>
                <span>📅 7 Days</span>
                <span>💰 ${rec['average_cost']:,}</span>
                <span>⭐ Best: {rec['best_season']}</span>
            </div>
            
            <p style="color: #ffffff; margin-bottom: 20px;">{rec['description']}</p>
        </div>
        """, unsafe_allow_html=True)
        
        # FIXED: Use st.columns for metrics instead of HTML
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Budget Fit", f"{rec.get('budget_score', 0):.1f}/10")
        with col2:
            st.metric("DNA Match", f"{rec.get('dna_match', 0):.1f}/10")
        with col3:
            st.metric("Weather", f"{rec.get('weather_score', 0):.1f}/10")
        with col4:
            st.metric("Crowds", f"{rec.get('crowd_score', 0):.1f}/10")
        
        col_a, col_b, col_c = st.columns([1, 1, 1])
        
        with col_a:
            with st.expander("🔍 Why this trip?"):
                # FIXED: Use plain text, not HTML
                if 'why' in rec:
                    st.write(rec['why'])
                else:
                    category = rec.get('category', '').lower()
                    why_texts = {
                        "adventure": "Perfect for thrill-seekers with exciting activities and breathtaking landscapes.",
                        "cultural": "Rich in history and culture with authentic local experiences.",
                        "luxury": "Premium accommodations and exclusive experiences await you.",
                        "nature": "Connect with nature in this stunning natural paradise.",
                        "urban": "Experience the vibrant city life and modern attractions.",
                        "beach": "Relax on beautiful beaches and enjoy the coastal lifestyle.",
                        "wellness": "Rejuvenate your mind and body in this peaceful setting."
                    }
                    st.write(why_texts.get(category, "This destination aligns perfectly with your preferences."))
        
        with col_b:
            with st.expander("⚖️ Regret Preview"):
                # FIXED: Use plain text, not HTML
                category = rec.get('category', '').lower()
                regret_texts = {
                    "adventure": "Physical demands and rustic conditions may challenge you if you prefer luxury.",
                    "cultural": "Structured activities might feel overwhelming if you seek pure relaxation.",
                    "luxury": "May feel less authentic if you prefer rugged, budget-friendly experiences.",
                    "nature": "Remote location might feel isolating if you need constant connectivity.",
                    "urban": "Constant energy and crowds could be overwhelming if you need peace.",
                    "beach": "Extended beach time might feel less stimulating for adventure seekers.",
                    "wellness": "Peaceful pace might be too gentle if you're looking for high-energy activities."
                }
                st.write(f"⚠️ {regret_texts.get(category, 'Consider timing and your personal preferences.')}")
        
        with col_c:
            if st.button(f"✅ Book with Confidence", key=f"book_{i}", use_container_width=True):
                st.balloons()
                st.success(f"✨ Booking initiated for {rec['name']}! Check your email for details.")
        
        st.markdown("---")

def render_destination_explorer():
    """Render destination explorer"""
    st.markdown("<h2>🌍 Explore All Destinations</h2>", unsafe_allow_html=True)
    
    # Filters
    with st.container():
        st.markdown("""
        <div style="
            background: rgba(255, 255, 255, 0.05);
            border: 1px solid #00d4ff;
            padding: 20px;
            border-radius: 15px;
            margin-bottom: 20px;
        ">
        """, unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns(3)
        with col1:
            category_filter = st.multiselect("Categories", DESTINATION_CATEGORIES, default=[])
        with col2:
            max_budget = st.slider("Max Budget ($)", 500, 10000, 5000, step=500)
        with col3:
            search = st.text_input("Search", placeholder="Destination name...")
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    # Filter destinations
    all_dests = data_store.get_all_destinations()
    filtered = []
    
    for dest in all_dests:
        if category_filter and dest['category'] not in category_filter:
            continue
        if dest['average_cost'] > max_budget:
            continue
        if search and search.lower() not in dest['name'].lower() and search.lower() not in dest['country'].lower():
            continue
        filtered.append(dest)
    
    # Display in grid
    if filtered:
        rows = [filtered[i:i+3] for i in range(0, len(filtered), 3)]
        
        for row in rows:
            cols = st.columns(3)
            for idx, dest in enumerate(row):
                with cols[idx]:
                    st.markdown(f"""
                    <div style="
                        background: rgba(255, 255, 255, 0.05);
                        border: 1px solid #00d4ff;
                        border-radius: 15px;
                        padding: 20px;
                        height: 280px;
                        margin-bottom: 20px;
                        transition: all 0.3s ease;
                    ">
                        <h4 style="color: #00d4ff; margin-bottom: 5px;">{dest['name']}</h4>
                        <p style="color: #cccccc; font-size: 0.9rem; margin-bottom: 10px;">{dest['country']}</p>
                        <p style="color: #00d4ff; font-size: 0.9rem; margin-bottom: 10px;">{dest['category']} • ${dest['average_cost']}</p>
                        <p style="color: #ffffff; font-size: 0.9rem; margin-bottom: 10px;">Best: {dest['best_season']}</p>
                        <p style="color: #cccccc; font-size: 0.85rem;">{dest['description'][:100]}...</p>
                    </div>
                    """, unsafe_allow_html=True)
    else:
        st.info("No destinations match your filters")

# ========== MAIN APP ==========
def main():
    """Main application entry point"""
    
    if not st.session_state.logged_in:
        render_auth()
        return
    
    render_sidebar()
    render_hero()
    
    tab_names = ["🧬 DNA Quiz", "🧭 Trip Planner", "🎯 Recommendations", "🌍 Explorer"]
    
    if st.session_state.user_profile:
        default_tab = st.session_state.active_tab
    else:
        default_tab = 0
    
    tabs = st.tabs(tab_names)
    
    with tabs[0]:
        if st.session_state.user_profile:
            render_dna_results()
        else:
            render_dna_quiz()
    
    with tabs[1]:
        render_trip_planner()
    
    with tabs[2]:
        render_recommendations()
    
    with tabs[3]:
        render_destination_explorer()
    
    # Footer
    st.markdown("""
    <div class="footer">
        <p>Made with ❤️ by <a href="#">VoyageAI</a></p>
        <p style="color: #888; font-size: 0.8rem;">Confidence-first travel discovery platform</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
