from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Prediction

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        full_name = serializers.CharField()
        fields = ['id', 'username', 'password', 'first_name', 'last_name', 'email']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        print(user)
        return user
    
class PredictionSerializer(serializers.ModelSerializer):
    author_username = serializers.CharField(source="author.username", read_only=True)
    class Meta:
        model = Prediction
        fields = ['id', 'title', 'category', 'content', 'created_at', 'author', 'author_username']
        extra_kwargs = {'author': {'read_only': True}}