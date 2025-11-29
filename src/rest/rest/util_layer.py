"""
Utility layer for database connections and data transformations
"""
import os
from pymongo import MongoClient


# Singleton database connection
_db_instance = None


def get_db_connection():
    """
    Returns a singleton MongoDB database connection
    
    Returns:
        Database: MongoDB database instance
    """
    global _db_instance
    if _db_instance is None:
        mongo_uri = 'mongodb://' + os.environ["MONGO_HOST"] + ':' + os.environ["MONGO_PORT"]
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
