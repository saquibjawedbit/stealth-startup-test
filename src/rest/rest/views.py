from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import logging
from .service_layer import TodoService

logger = logging.getLogger(__name__)


class TodoListView(APIView):
    """
    API View for managing todo items
    """
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.todo_service = TodoService()

    def get(self, request):
        """
        Retrieve all todos
        """
        try:
            todos_list = self.todo_service.get_all_todos()
            return Response({"todos": todos_list}, status=status.HTTP_200_OK)
        except Exception as e:
            logger.exception("GET /todos failed")
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    def post(self, request):
        """
        Create a new todo
        """
        try:
            todo_id = self.todo_service.create_todo(request.data)
            return Response({"id": todo_id}, status=status.HTTP_201_CREATED)
        except ValueError as e:
            # Validation error
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.exception("POST /todos failed")
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

