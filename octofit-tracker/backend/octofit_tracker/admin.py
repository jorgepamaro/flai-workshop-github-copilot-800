from django.contrib import admin
from .models import User, Team, Activity, Leaderboard, Workout


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'email', 'created_at']
    search_fields = ['username', 'email']
    readonly_fields = ['created_at']
    list_filter = ['created_at']


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ['name', 'captain_id', 'created_at']
    search_fields = ['name']
    readonly_fields = ['created_at']
    list_filter = ['created_at']


@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
    list_display = ['activity_type', 'user_id', 'duration', 'distance', 'calories', 'date']
    search_fields = ['activity_type', 'user_id']
    readonly_fields = ['created_at']
    list_filter = ['activity_type', 'date', 'created_at']
    ordering = ['-date']


@admin.register(Leaderboard)
class LeaderboardAdmin(admin.ModelAdmin):
    list_display = ['rank', 'user_id', 'team_id', 'total_activities', 'total_duration', 
                    'total_distance', 'total_calories', 'period']
    search_fields = ['user_id', 'team_id']
    readonly_fields = ['updated_at']
    list_filter = ['period', 'updated_at']
    ordering = ['rank']


@admin.register(Workout)
class WorkoutAdmin(admin.ModelAdmin):
    list_display = ['title', 'user_id', 'difficulty', 'duration', 'category', 'is_recommended', 'created_at']
    search_fields = ['title', 'user_id', 'category']
    readonly_fields = ['created_at']
    list_filter = ['difficulty', 'category', 'is_recommended', 'created_at']
    ordering = ['-created_at']
