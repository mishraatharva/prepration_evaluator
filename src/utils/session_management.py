class SessionMemory:
    """
    In-memory session storage.
    In production, use Redis or a database.
    """
    
    def __init__(self, ttl_minutes: int = 30):
        """
        Initialize session memory.
        
        Args:
            ttl_minutes: Session time-to-live in minutes
        """
        self.sessions: Dict[str, Dict] = {}
        self.ttl = timedelta(minutes=ttl_minutes)
    
    def create_session(self, user_id: int) -> str:
        """Create a new session."""
        session_id = str(uuid.uuid4())
        self.sessions[session_id] = {
            "created_at": datetime.now(),
            "last_accessed": datetime.now(),
            "conversation_history": []
        }
        return session_id
    
    def get_session(self, session_id: str) -> Optional[Dict]:
        """Get session data."""
        if session_id not in self.sessions:
            return None
        
        session = self.sessions[session_id]
        
        # Check TTL
        if datetime.now() - session["last_accessed"] > self.ttl:
            del self.sessions[session_id]
            return None
        
        # Update last accessed
        session["last_accessed"] = datetime.now()
        return session
    
    def add_to_history(self, session_id: str, role: str, content: str):
        """Add a message to conversation history."""
        session = self.get_session(session_id)
        if session:
            session["conversation_history"].append({
                "role": role,
                "content": content,
                "timestamp": datetime.now().isoformat()
            })
    
    def get_history(self, session_id: str) -> List[BaseMessage]:
        """Get conversation history as BaseMessage objects."""
        session = self.get_session(session_id)
        if not session:
            return []
        
        messages = []
        for msg in session["conversation_history"]:
            if msg["role"] == "user":
                messages.append(HumanMessage(content=msg["content"]))
            elif msg["role"] == "assistant":
                messages.append(AIMessage(content=msg["content"]))
        
        return messages
    
    def clear_session(self, session_id: str):
        """Clear a session."""
        if session_id in self.sessions:
            del self.sessions[session_id]