from rest_framework import serializers
from task_manager.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'first_name', 'phone']
        extra_kwargs = {'password': {'write_only': True}}