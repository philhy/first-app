from django.contrib import admin
from .models import *

@admin.action(description="Delete all team stats")
def delete_all_team_stats(modeladmin, request, queryset):
    NFLTeamStats.objects.all().delete()

class NFLTeamStatsAdmin(admin.ModelAdmin):
    actions = [delete_all_team_stats]

admin.site.register(NFLTeamStats, NFLTeamStatsAdmin)