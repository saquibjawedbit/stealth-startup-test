"""
Utility layer for database connections and data transformations
"""
import os
import threading
from pymongo import MongoClient


# Singleton database connection with thread safety
_db_instance = None
_db_lock = threading.Lock()


def get_db_connection():
    """
    Returns a singleton MongoDB database connection (thread-safe)
    
    Uses double-check locking pattern to ensure thread safety while
    minimizing lock contention.
    
    Returns:
        Database: MongoDB database instance
    """
    global _db_instance
    
    # First check (without lock for performance)
    if _db_instance is None:
        # Acquire lock for thread-safe initialization
        with _db_lock:
            # Double-check inside lock (another thread might have initialized it)
            if _db_instance is None:
                mongo_host = os.environ.get("MONGO_HOST")
                mongo_port = os.environ.get("MONGO_PORT")
                
                if not mongo_host or not mongo_port:
                    raise ValueError(
                        "Missing required environment variables: MONGO_HOST and MONGO_PORT must be set"
                    )
                
                mongo_uri = f'mongodb://{mongo_host}:{mongo_port}'
                client = MongoClient(mongo_uri)
                _db_instance = client['test_db']
    
    return _db_instance


def serialize_todo(todo):
    """
    Converts a MongoDB todo document to a JSON-serializable format
    
    Args:
        todo (dict): MongoDB document with ObjectId
        
    Returns:
        dict: Serialized todo with string ID (new dict, doesn't mutate original)
    """
    # Create a copy to avoid mutating the original document
    serialized = {k: v for k, v in todo.items() if k != '_id'}
    serialized['id'] = str(todo['_id'])
    return serialized


def serialize_todos_list(todos_cursor):
    """
    Converts a MongoDB cursor to a list of serialized todos
    
    Args:
        todos_cursor: MongoDB cursor object
        
    Returns:
        list: List of serialized todo dictionaries
    """
    return [serialize_todo(todo) for todo in todos_cursor]
