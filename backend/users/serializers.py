from rest_framework import serializers
from users.models import User
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'username', 'is_staff', 'password']
        extra_kwargs = {
            'password': {'write_only': True}
        }