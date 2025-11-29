"""
Service layer for business logic operations
"""
from datetime import datetime, timezone
from .util_layer import get_db_connection, serialize_todos_list
from .model import TodoInput


class TodoService:
    """Service class for managing todo operations"""
    
    def __init__(self):
        self.db = get_db_connection()
    
    def get_all_todos(self):
        """
        Retrieves all todos sorted by creation date (newest first)
        
        Returns:
            list: List of serialized todo dictionaries
            
        Raises:
            Exception: If database query fails
        """
        todos_cursor = self.db.todos.find().sort("created_at", -1)
        return serialize_todos_list(todos_cursor)
    
    def create_todo(self, todo_data):
        """
        Creates a new todo item
        
        Args:
            todo_data (dict): Todo data from request
            
        Returns:
            str: ID of the created todo
            
        Raises:
            ValueError: If todo data is invalid
            Exception: If database insertion fails
        """
        # Validate input
        try:
            todo_input = TodoInput(**todo_data)
        except Exception as e:
            raise ValueError(f"Invalid todo data: {str(e)}")
        
        # Prepare todo document
        todo = todo_input.model_dump()
        todo["created_at"] = datetime.now(timezone.utc)
        
        # Insert into database
        result = self.db.todos.insert_one(todo)
        
        return str(result.inserted_id)
