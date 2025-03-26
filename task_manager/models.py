"""
Custom User and Task Models Module.This module defines the core database models for the task management system:

- Custom User model extending AbstractBaseUser
- Task model with assignment capabilities
- Custom UserManager for user creation
"""

from django.contrib.auth.models import AbstractBaseUser
from django.db import models
from django.utils.translation import gettext_lazy as _


from django.contrib.auth.models import BaseUserManager

class UserManager(BaseUserManager):
    """
    Custom user model manager extending BaseUserManager.
    Provides methods for creating regular users and superusers.
    """
    def create_user(self, name, email, phone, password):
        """
        Creates and saves a regular User with the given details.
        
        Args:
            name (str): User's full name
            email (str): User's email address (must be unique)
            phone (str): User's phone number (optional)
            password (str): User's password (optional)
            
        Returns:
            User: The newly created user instance
            
        Raises:
            ValueError: If email is not provided
        """
        if not email:
            raise ValueError("Email field cannot be empty")

        email = self.normalize_email(email)
        user = self.model(
            name=name,
            email=email,
            phone=phone,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser( self, name, email, phone, password):
        """
        Creates and saves a superuser with admin privileges.
        
        Args:
            name (str): Admin's full name
            email (str): Admin's email address
            phone (str): Admin's phone number
            password (str): Admin's password
            
        Returns:
            User: The newly created superuser instance
        """
        user = self.create_user(name=name,email=email,phone=phone,password=password)
        user.is_admin = True
        user.is_staff = True
        user.is_superadmin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    """
    Custom User model implementing a fully featured User model with:
    - Email as username field
    - Admin/compliance flags
    - Timestamps for creation/modification
    
    Extends:
        AbstractBaseUser: Core authentication functionality
    """
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100, unique=True)
    phone = models.CharField(max_length=20, blank=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_superadmin = models.BooleanField(default=False)

    USERNAME_FIELD = "email"

    objects = UserManager()

    def user_serializer(self):
        """
            Serializes the user object into a dictionary format.
            Returns:
                dict: A dictionary containing user details
        """
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "phone": self.phone,
            "date_joined": self.date_joined,
            "updated_date": self.updated_date,
            "is_admin": self.is_admin,
            "is_staff": self.is_staff,
            "is_active": self.is_active,
            "is_superadmin": self.is_superadmin,
        }


class Task(models.Model):
    """
    Task model representing work items in the system.
    Supports status tracking, type categorization, and user assignments.
    """
        
    TASK_STATUS = [
        ('Pending', 'Pending'),
        ('In Progress', 'In Progress'),
        ('Completed', 'Completed'),
    ]
    
    TASK_TYPES = [
        ('Bug', 'Bug'),
        ('Feature', 'Feature'),
        ('Improvement', 'Improvement'),
    ]
    
    name = models.CharField(max_length=255)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    task_type = models.CharField(max_length=20, choices=TASK_TYPES)
    completed_at = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=TASK_STATUS, default='Pending')
    assigned_users = models.ManyToManyField(User, related_name='tasks')

    def task_serializer(self):

        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "created_at": self.created_at,
            "completed_at": self.completed_at,
            "status": self.status,
        }