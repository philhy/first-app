from rest_framework import serializers
from .models import *

class NFLTeamStatsSerializer(serializers.ModelSerializer):
    class Meta:
        model = NFLTeamStats
        fields = '__all__'