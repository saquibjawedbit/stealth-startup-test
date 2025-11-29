from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import json, logging, os
from datetime import datetime
from pymongo import MongoClient
from pydantic import BaseModel, Field

logger = logging.getLogger(__name__)

mongo_uri = 'mongodb://' + os.environ["MONGO_HOST"] + ':' + os.environ["MONGO_PORT"]
db = MongoClient(mongo_uri)['test_db']

class TodoListView(APIView):

    def get(self, request):
        try:
            # Query all todos and sort by created_at descending
            todos_cursor = db.todos.find().sort("created_at", -1)
            
            # Convert cursor to list and ObjectId to string for JSON serialization
            todos_list = []
            for todo in todos_cursor:
                todo['id'] = str(todo['_id'])  # Convert ObjectId to string
                todos_list.append(todo)
            
            return Response({"todos": todos_list}, status=status.HTTP_200_OK)
        except Exception as e:
            logger.exception("GET /todos failed", e)    
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    def post(self, request):
        try:
            todo = request.data

            try:
                todo_input = TodoInput(**todo)
            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

            todo = todo_input.dict()
            todo["created_at"] = datetime.utcnow().replace(tzinfo=timezone.utc)
            result = db.todos.insert_one(todo)
            
            # Return the created todo with its ID
            todo['id'] = str(result.inserted_id)
            return Response({"todo": todo}, status=status.HTTP_201_CREATED)
        except Exception as e:
            logger.exception("POST /todos failed", e)
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

