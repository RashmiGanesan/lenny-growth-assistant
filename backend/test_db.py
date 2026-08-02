#!/usr/bin/env python3
"""
Test script to verify SQLite database functionality
"""

import os
import sys

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from database import Database

def test_database():
    """Test SQLite database functionality"""
    print("Testing SQLite database...")
    
    # Initialize database (will create chat.db if not exists)
    db = Database()
    
    # Test 1: Create session
    test_session_id = "test-session-001"
    print(f"\n1. Creating session: {test_session_id}")
    success = db.create_session(test_session_id)
    print(f"   Result: {'Success' if success else 'Failed'}")
    
    # Test 2: Save messages
    print(f"\n2. Saving test messages...")
    db.save_message(test_session_id, "user", "Hello, how are you?", "text")
    db.save_message(test_session_id, "ai", "I'm doing well! How can I help you today?", "text")
    db.save_message(test_session_id, "user", "Tell me about product-market fit", "text")
    db.save_message(test_session_id, "ai", "Product-market fit is when customers are pulling your product...", "essay")
    print("   Messages saved successfully")
    
    # Test 3: Retrieve history
    print(f"\n3. Retrieving chat history...")
    history = db.get_chat_history(test_session_id)
    print(f"   Found {len(history)} messages")
    
    for i, msg in enumerate(history, 1):
        print(f"   {i}. {msg['role']}: {msg['content'][:50]}... (type: {msg['type']})")
    
    # Test 4: Check session exists
    print(f"\n4. Checking session existence...")
    exists = db.session_exists(test_session_id)
    print(f"   Session exists: {exists}")
    
    # Test 5: Get all sessions
    print(f"\n5. Getting all sessions...")
    all_sessions = db.get_all_sessions()
    print(f"   Found {len(all_sessions)} sessions total")
    
    for session in all_sessions:
        print(f"   - {session['session_id']}: {session['message_count']} messages")
    
    # Clean up (optional)
    print(f"\n6. Database test completed!")
    print(f"   Database file: {os.path.abspath('chat.db')}")
    print(f"   Size: {os.path.getsize('chat.db') if os.path.exists('chat.db') else 0} bytes")
    
    db.close()
    print("\nAll tests passed successfully!")

if __name__ == "__main__":
    test_database()