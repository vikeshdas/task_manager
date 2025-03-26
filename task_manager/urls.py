from django.urls import path
from django.contrib import admin
from task_manager.view import user
from task_manager.view import task
from django.urls import path
from rest_framework_simplejwt.views import (TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('user/', user.UserView.as_view()),
    path('task/', task.TaskView.as_view(), name='task-list'),
    path('tasks/<int:task_id>/assign/', task.TaskView.as_view(), name='task-assign'),
    path('users/<int:user_id>/tasks/', task.UserTasksView.as_view(), name='user-tasks'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]