from django.urls import path
from . import views

urlpatterns = [
    path('nfl/team/', views.get_nfl_team_stats, name='nfl-team-stats'),
    path('nfl/player/', views.get_nfl_player_stats, name='nfl-player-stats'),
]