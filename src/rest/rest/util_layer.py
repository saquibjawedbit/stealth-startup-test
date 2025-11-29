"""
Utility layer for database connections and data transformations
"""
import os
from pymongo import MongoClient


def get_db_connection():
    """
    Establishes and returns a MongoDB database connection
    
    Returns:
        Database: MongoDB database instance
    """
    mongo_uri = 'mongodb://' + os.environ["MONGO_HOST"] + ':' + os.environ["MONGO_PORT"]
    client = MongoClient(mongo_uri)
    return client['test_db']


def serialize_todo(todo):
    """
    Converts a MongoDB todo document to a JSON-serializable format
    
    Args:
        todo (dict): MongoDB document with ObjectId
        
    Returns:
        dict: Serialized todo with string ID
    """
    todo['id'] = str(todo.pop('_id'))
    return todo


def serialize_todos_list(todos_cursor):
    """
    Converts a MongoDB cursor to a list of serialized todos
    
    Args:
        todos_cursor: MongoDB cursor object
        
    Returns:
        list: List of serialized todo dictionaries
    """
    todos_list = []
    for todo in todos_cursor:
        todos_list.append(serialize_todo(todo))
    return todos_list
