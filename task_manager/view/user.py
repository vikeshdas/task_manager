"""
This module provides views for creating and managing user accounts through RESTful API endpoints.It handles both regular user and admin user creation with proper validation and error handling.
"""

import json
from django.contrib.auth import get_user_model
from django.db import IntegrityError
from django.http import HttpRequest, JsonResponse
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.authentication import BasicAuthentication
from task_manager.models import User


User = get_user_model()

class UserView(APIView):
    """
        Provides functionality for creating new user accounts (both regular and admin users).Uses Django's authentication system and custom user model.
        Permissions:
            - Only othorize user can create a user
            - Only admin is allow to create a user 
    """
    permission_classes = [AllowAny]
    authentication_classes = [] 
    def put(self, request: HttpRequest) -> JsonResponse:
        """
        This method handling user creation bothe regular user and admin user.handling validation.
        Args:
            request: HTTP request object containing user data in JSON format
            Expected JSON fields:
                - name (str): User's full name
                - email (str): User's email address (must be unique)
                - phone (str): User's phone number (optional)
                - password (str): Account password
                - is_admin (bool, optional): Flag to create admin user

        Returns:
            JsonResponse: Contains either:
                - Success: User data with 201 status
                - Error: Appropriate error message with status code
        """
        data = json.loads(request.body)
        try:
            if(data.get("is_admin")):
                user = User.objects.create_superuser(name=data.get("name"),email=data.get("email"),phone=data.get("phone"),password=data.get("password"),)
            else:
                user = User.objects.create_user(name=data.get("name"),email=data.get("email"),phone=data.get("phone"),password=data.get("password"),)


            serialized_data = user.user_serializer()
            return JsonResponse(
                {"message": "User created successfully", "data": serialized_data},
                status=201,
                safe=False,
            )

        except IntegrityError as e:
            if "Duplicate entry" in str(e):
                return JsonResponse({"error": "User already exists"}, status=409)
            else:
                return JsonResponse({"error": str(e)}, status=500)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
