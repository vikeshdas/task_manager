
"""
This module provides endpoints for task management including:
- Task creation with user assignments
- Task assignment to users
- Retrieving tasks assigned to specific user
"""

import json
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from task_manager.models import Task, User
from task_manager.permissions import IsAdminUser

@method_decorator(csrf_exempt, name='dispatch')
class TaskView(APIView):
    """
    This class Provides functionality for creating new tasks and assigning users to task
    
    Permissions:
        - Requires authentication
        - Only admin users can create tasks
    """
    permission_classes = [IsAuthenticated,IsAdminUser]

    def put(self, request):
        """
        This method creates a new task with optional user assignments

        Args:
            request: HTTP request containing:
                - name (str): Task name (required)
                - description (str): Task description (required)
                - task_type (str): Task type (required)
                - status (str): Task status (optional, default='Pending')
                - user_id (int/list): Single user ID or list of IDs (optional)
        
        Returns:
            JsonResponse: 
                Success (201): Returns created task data with assigned users
                Error (400/500): Error message with details
        
        """
        try:
            data = json.loads(request.body)

            task = Task.objects.create(
                name=data['name'],
                description=data['description'],
                task_type=data['task_type'],
                status=data.get('status', 'Pending')
            )

            if 'user_id' in data:

                user_ids = [data['user_id']] if isinstance(data['user_id'], (int, str)) else data['user_id']
                

                user_ids = [int(user_id) if isinstance(user_id, str) else user_id for user_id in user_ids]
                
                users = User.objects.filter(id__in=user_ids)
                
                if len(users) != len(user_ids):
                    existing_ids = set(users.values_list('id', flat=True))
                    missing_ids = [uid for uid in user_ids if uid not in existing_ids]
                    return JsonResponse(
                        {"error": f"Users not found with IDs: {missing_ids}"},
                        status=400
                    )
                
                task.assigned_users.add(*users)

            return JsonResponse(
                {
                    "message": "Task created successfully", 
                    "data": {
                        **task.task_serializer(),
                        "assigned_user_ids": list(task.assigned_users.values_list('id', flat=True))
                    }
                },
                status=201
            )
            
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    
    def post(self, request, task_id):
        """
        This method assign a task to multiple users.
        
        Args:
            request: HTTP request containing:
                - user_ids (list): List of user IDs to assign
                -task_id (int): ID of the task to assign users to
        
        Returns:
            JsonResponse:
                Success (200): Confirmation with assigned user IDs
                Error (400/404/500): Error message with details
        """
        try:

            task = get_object_or_404(Task, id=task_id)
            
            user_ids = request.data.get('user_ids', [])
            if not isinstance(user_ids, list):
                return JsonResponse({"error": "user_ids must be a list of user IDs"}, status=status.HTTP_400_BAD_REQUEST)

            users = User.objects.filter(id__in=user_ids)
            found_ids = set(users.values_list('id', flat=True))
            missing_ids = set(user_ids) - found_ids

            if missing_ids:
                return JsonResponse({"error": f"Users not found with IDs: {sorted(missing_ids)}"},
                    status=status.HTTP_404_NOT_FOUND)

            task.assigned_users.add(*users)
            
            return JsonResponse({
                "message": f"Task {task_id} assigned to {len(users)} users",
                "assigned_users": list(found_ids)
            }, status=status.HTTP_200_OK)

        except Exception as e:
            return JsonResponse(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        
class CustomPagination(PageNumberPagination):
    """
    Custom pagination configuration
    
    Attributes:
        page_size (int): Default number of items per page
        page_size_query_param (str): Query parameter for page size
        max_page_size (int): Maximum allowed page size
    """
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

class UserTasksView(APIView):
    """
    This API endpoint  retrieves tasks assigned to a specific user
    
    Provides paginated list of tasks assigned to a user along with user information
    """
    permission_classes = [IsAuthenticated]
    
    def get(self, request, user_id):
        """
        Get paginated tasks assigned to a user
        
        Args:
            request: HTTP request
            user_id (int): ID of the user whose tasks to retrieve
        
        Returns:
            JsonResponse:
                Success (200): Paginated response with user info and tasks
                Error (404/500): Error message with details
        """
        try:
            try:
                user = User.objects.get(id=user_id)
            except User.DoesNotExist:
                return JsonResponse({"error": "User not found"},status=status.HTTP_404_NOT_FOUND)

            tasks = Task.objects.filter(assigned_users=user_id).order_by('-created_at')

            paginator = CustomPagination()
            paginated_tasks = paginator.paginate_queryset(tasks, request)
            
            response_data = {
                "user": {
                    "id": user.id,
                    "name": user.name,
                    "email": user.email,
                    "is_admin": user.is_admin
                },
                "tasks": [task.task_serializer() for task in paginated_tasks]
            }

            return paginator.get_paginated_response(response_data)

        except Exception as e:
            return JsonResponse(
                {"error": f"Server error: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )