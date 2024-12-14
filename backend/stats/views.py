from django.shortcuts import render
from django.http import JsonResponse
from .models import *

def get_nfl_team_stats(request):
    stats = NFLTeamStats.objects.all().values()
    return JsonResponse(list(stats), safe=False)