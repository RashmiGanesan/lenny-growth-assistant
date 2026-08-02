import sqlite3
import os
from typing import List, Dict, Any
from datetime import datetime

class Database:
    def __init__(self, db_path: str = "chat.db"):
        """Initialize SQLite database connection"""
        self.db_path = db_path
        self.conn = None
        self.connect()
        self.create_tables_if_not_exists()
    
    def connect(self):
        """Connect to SQLite database"""
        try:
            self.conn = sqlite3.connect(self.db_path, check_same_thread=False)
            self.conn.row_factory = sqlite3.Row
            print(f"Connected to SQLite database: {self.db_path}")
        except sqlite3.Error as e:
            print(f"Error connecting to database: {e}")
            raise
    
    def create_tables_if_not_exists(self):
        """Create necessary tables if they don't exist"""
        try:
            cursor = self.conn.cursor()
            
            # Create chat_sessions table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS chat_sessions (
                    session_id TEXT PRIMARY KEY,
                    created_at TEXT,
                    updated_at TEXT
                )
            ''')
            
            # Create chat_messages table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS chat_messages (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    session_id TEXT NOT NULL,
                    role TEXT NOT NULL,
                    content TEXT NOT NULL,
                    response_type TEXT NOT NULL DEFAULT 'text',
                    created_at TEXT,
                    FOREIGN KEY (session_id) REFERENCES chat_sessions (session_id)
                )
            ''')
            
            # Create indexes for better performance
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_chat_messages_session_id ON chat_messages(session_id)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_chat_messages_created_at ON chat_messages(created_at)')
            
            self.conn.commit()
            print("Database tables created/verified successfully")
            
        except sqlite3.Error as e:
            print(f"Error creating tables: {e}")
            raise
    
    def create_session(self, session_id: str) -> bool:
        """Create a new chat session"""
        try:
            cursor = self.conn.cursor()
            current_time = datetime.now().isoformat()
            
            cursor.execute('''
                INSERT INTO chat_sessions (session_id, created_at, updated_at)
                VALUES (?, ?, ?)
            ''', (session_id, current_time, current_time))
            
            self.conn.commit()
            print(f"Created session: {session_id}")
            return True
            
        except sqlite3.Error as e:
            print(f"Error creating session: {e}")
            return False
    
    def save_message(self, session_id: str, role: str, content: str, response_type: str = "text") -> bool:
        """Save a chat message"""
        try:
            cursor = self.conn.cursor()
            current_time = datetime.now().isoformat()
            
            # First, update the session's updated_at timestamp
            cursor.execute('''
                UPDATE chat_sessions 
                SET updated_at = ? 
                WHERE session_id = ?
            ''', (current_time, session_id))
            
            # Save the message
            cursor.execute('''
                INSERT INTO chat_messages (session_id, role, content, response_type, created_at)
                VALUES (?, ?, ?, ?, ?)
            ''', (session_id, role, content, response_type, current_time))
            
            self.conn.commit()
            print(f"Saved {role} message for session {session_id}")
            return True
            
        except sqlite3.Error as e:
            print(f"Error saving message: {e}")
            return False
    
    def get_chat_history(self, session_id: str) -> List[Dict[str, Any]]:
        """Get chat history for a session"""
        try:
            cursor = self.conn.cursor()
            
            cursor.execute('''
                SELECT role, content, response_type, created_at
                FROM chat_messages
                WHERE session_id = ?
                ORDER BY created_at
            ''', (session_id,))
            
            rows = cursor.fetchall()
            
            messages = []
            for row in rows:
                messages.append({
                    "role": row["role"],
                    "content": row["content"],
                    "type": row["response_type"],
                    "timestamp": row["created_at"]
                })
            
            print(f"Retrieved {len(messages)} messages for session {session_id}")
            return messages
            
        except sqlite3.Error as e:
            print(f"Error getting chat history: {e}")
            return []
    
    def session_exists(self, session_id: str) -> bool:
        """Check if a session exists"""
        try:
            cursor = self.conn.cursor()
            cursor.execute('SELECT 1 FROM chat_sessions WHERE session_id = ?', (session_id,))
            return cursor.fetchone() is not None
        except sqlite3.Error as e:
            print(f"Error checking session existence: {e}")
            return False
    
    def get_all_sessions(self) -> List[Dict[str, Any]]:
        """Get all chat sessions (for future features)"""
        try:
            cursor = self.conn.cursor()
            cursor.execute('''
                SELECT s.session_id, s.created_at, s.updated_at, 
                       COUNT(m.id) as message_count
                FROM chat_sessions s
                LEFT JOIN chat_messages m ON s.session_id = m.session_id
                GROUP BY s.session_id
                ORDER BY s.updated_at DESC
            ''')
            
            rows = cursor.fetchall()
            sessions = []
            for row in rows:
                sessions.append({
                    "session_id": row["session_id"],
                    "created_at": row["created_at"],
                    "updated_at": row["updated_at"],
                    "message_count": row["message_count"]
                })
            
            return sessions
            
        except sqlite3.Error as e:
            print(f"Error getting all sessions: {e}")
            return []
    
    def close(self):
        """Close the database connection"""
        if self.conn:
            self.conn.close()
            print("Database connection closed")
    
    def __del__(self):
        """Destructor to ensure connection is closed"""
        self.close()

# Example usage
if __name__ == "__main__":
    # Test the database
    db = Database()
    
    # Test session creation
    test_session = "test-session-123"
    db.create_session(test_session)
    
    # Test message saving
    db.save_message(test_session, "user", "Hello, world!")
    db.save_message(test_session, "ai", "Hi there! How can I help?", "text")
    
    # Test getting history
    history = db.get_chat_history(test_session)
    print(f"History: {history}")
    
    print("Database test completed successfully")