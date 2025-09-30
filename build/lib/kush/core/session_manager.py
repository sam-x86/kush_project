# kush-framework/kush/core/session_manager.py
"""
Session manager for agent sessions
"""

import time
from typing import Dict, List
from colorama import Fore, Style

class SessionManager:
    def __init__(self):
        self.sessions: Dict[str, Dict] = {}
    
    def create_session(self, session_data: Dict) -> str:
        """Create a new session"""
        session_id = f"session_{len(self.sessions) + 1}"
        session_data['id'] = session_id
        session_data['created'] = time.time()
        session_data['last_seen'] = time.time()
        session_data['active'] = True
        
        self.sessions[session_id] = session_data
        return session_id
    
    def get_session(self, session_id: str) -> Dict:
        """Get session by ID"""
        return self.sessions.get(session_id, {})
    
    def update_session(self, session_id: str, data: Dict):
        """Update session data"""
        if session_id in self.sessions:
            self.sessions[session_id].update(data)
            self.sessions[session_id]['last_seen'] = time.time()
    
    def list_sessions(self) -> List[Dict]:
        """List all sessions"""
        return list(self.sessions.values())
    
    def cleanup_sessions(self):
        """Clean up inactive sessions"""
        current_time = time.time()
        inactive_sessions = []
        
        for session_id, session in self.sessions.items():
            if current_time - session['last_seen'] > 300:  # 5 minutes
                inactive_sessions.append(session_id)
        
        for session_id in inactive_sessions:
            del self.sessions[session_id]
            print(f"{Fore.YELLOW}[!] Removed inactive session: {session_id}{Style.RESET_ALL}")