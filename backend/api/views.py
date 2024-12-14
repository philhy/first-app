from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import *
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import *

@api_view(['GET'])
def user_info(request):
    user = request.user
    if user.is_authenticated:
        return Response({
            "username": user.username,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "email": user.email,
        })
    else:
        return Response({
            "detail":
            "Authentication credentials were not provided."
        }, status=401)
    
# Create your views here.
class CreateUserView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

class AllPredictionListCreate(generics.ListCreateAPIView):
    serializer_class = PredictionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Prediction.objects.all()
    
    def perform_create(self, serializer):
        if serializer.is_valid():
            serializer.save(author=self.request.user)
        else:
            print(serializer.errors)

class PredictionListCreate(generics.ListCreateAPIView):
    serializer_class = PredictionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Prediction.objects.filter(author=user)
    
    def perform_create(self, serializer):
        if serializer.is_valid():
            serializer.save(author=self.request.user)
        else:
            print(serializer.errors)

class PredictionDelete(generics.DestroyAPIView):
    serializer_class = PredictionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Prediction.objects.filter(author=user)
    
class NFLTeamStatsListView(generics.ListAPIView):
    queryset = NFLTeamStats.objects.all()
    serializer_class = NFLTeamStatsSerializer