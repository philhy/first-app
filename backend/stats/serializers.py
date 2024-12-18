from rest_framework import serializers
from .models import *

class NFLTeamStatsSerializer(serializers.ModelSerializer):
    class Meta:
        model = NFLTeamStats
        fields = '__all__'

class NFLPlayerStatsSerializer(serializers.ModelSerializer):
    class Meta:
        model = NFLPlayerStats
        fields = '__all__'