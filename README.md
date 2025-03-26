
# Overview
This is a robust Task Management System built with Django REST Framework that provides secure API endpoints for user and task management. The system features:
```
Used JWT Authentication for secure API access

Implimented Role-based access control (Admin vs Regular users)

Task assignment functionality

MySQL database backend

Django ORM for database operations
```

## Key Features
```
Single endpoint for creating both regular users and admin users

Admin users are created with is_admin=true flag

JWT token-based authentication
```

## Task Management:
```
Only admin users can create tasks

Tasks can be assigned to one or multiple users

Task status tracking (Pending/In Progress/Completed)
```

### Access Control:
```
Admin privileges required for task creation

All authenticated users can view their assigned tasks
```

## API Documentation

### Authentication
```
Endpoint: POST /api/token/

Request:
{
  "email": "user@example.com",
  "password": "yourpassword"
}

{
  "refresh": "xxxxx.yyyyy.zzzzz",
  "access": "aaaaa.bbbbb.ccccc"
}
```

Refresh Token
```
POST /api/token/refresh/

Request:
    {
    "refresh": "your-refresh-token"
    }

Response
{
  "access": "new-access-token"
}

```

#### User Endpoints
```
Create User (Regular or Admin)

Endpoint: PUT /user/

Request:{
  "name": "Vikesh Das",
  "email": "vikesh@gamil.com",
  "phone": "1234567890",
  "password": "securepassword123",
}

Response:
{
  "message": "User created successfully",
  "data": {
    "id": 1,
    "name": "Vikesh Das",
    "email": "vikesh@gmail.com",
    "phone": "1234567890",
  }
}
```

### Task Endpoints

```
Create Task (Admin Only)

Endpoint: POST /task/

Authentication: Bearer token (admin required)

Request:
{
  "name": "Fix login page",
  "description": "Fix authentication issues",
  "task_type": "Bug",
  "status": "Pending",
  "user_id": [1, 2]
}

Response:
{
  "message": "Task created successfully",
  "data": {
    "id": 1,
    "name": "Fix login page",
    "description": "Fix authentication issues",
    "status": "Pending",
    "assigned_user_ids": [1, 2]
  }
}
```

### Assign task to users
```
Endpoint: POST /tasks/<task_id>/assign/

Authentication: Bearer token (admin required)

Request:
{
  "user_ids": [3, 4]
}

Response:
{
  "message": "Task 1 assigned to 2 users",
  "assigned_users": [3, 4]
}
```

#### Get User's Tasks
```
Endpoint: GET /users/<user_id>/tasks/

Authentication: Bearer token (any authenticated user)

Response (Success - 200 OK):
{
  "count": 2,
  "next": null,
  "previous": null,
  "results": {
    "user": {
      "id": 1,
      "name": "Vikesh das",
      "email": "vikesh@gmail.com",
      "is_admin": false
    },
    "tasks": [
      {
        "id": 1,
        "name": "Fix login",
        "status": "Pending"
      }
    ]
  }
}
```