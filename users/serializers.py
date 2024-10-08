from rest_framework import serializers
from .models import ApplicationProfile
from django.contrib.auth import get_user_model

class UserSerializer(serializers.ModelSerializer):
    '''serializer for the user object'''
    class Meta:
        model = get_user_model()
        fields = ('email', 'username', 'password', 'id')
        extra_kwargs = {'password': {'write_only': True, 'min_length': 5}}
    
    def create(self, validated_data):
        return get_user_model().objects.create_user(**validated_data)
    
class ApplicationProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = ApplicationProfile
        fields = '__all__'