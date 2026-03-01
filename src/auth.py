"""
Authentication Module
Handles user login, signup, and session management
"""

import streamlit as st
import hashlib
from datetime import datetime
from typing import Tuple

def hash_password(password: str) -> str:
    """Hash password using SHA-256"""
    return hashlib.sha256(password.encode()).hexdigest()

def verify_password(username: str, password: str, users_db: dict) -> bool:
    """Verify username and password"""
    if username in users_db:
        stored_hash = users_db[username]['password']
        return stored_hash == hash_password(password)
    return False

def register_user(username: str, email: str, password: str, users_db: dict) -> Tuple[bool, str]:
    """Register a new user"""
    if not username or not email or not password:
        return False, "All fields are required"
    
    if username in users_db:
        return False, "Username already exists"
    
    if len(password) < 6:
        return False, "Password must be at least 6 characters"
    
    if '@' not in email or '.' not in email:
        return False, "Please enter a valid email"
    
    users_db[username] = {
        'password': hash_password(password),
        'email': email,
        'created_at': datetime.now().isoformat()
    }
    return True, "Registration successful!"

def logout():
    """Logout user and clear session"""
    for key in ['logged_in', 'username', 'user_email', 'current_step', 
                'quiz_responses', 'user_profile', 'recommendations']:
        if key in st.session_state:
            if key == 'logged_in':
                st.session_state[key] = False
            else:
                st.session_state[key] = None if key != 'current_step' else 0
    st.rerun()