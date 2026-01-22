from rest_framework import serializers
from .models import User, Team, Activity, Leaderboard, Workout


class UserSerializer(serializers.ModelSerializer):
    id = serializers.SerializerMethodField()
    team_name = serializers.SerializerMethodField()
    team_id = serializers.SerializerMethodField()
    points = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'profile', 'team_name', 'team_id', 'points', 'created_at']
        extra_kwargs = {'password': {'write_only': True}}
    
    def get_id(self, obj):
        return str(obj._id)
    
    def get_team_name(self, obj):
        """Get team name from profile or by team_id field"""
        # First check if team info is in profile as a string
        if obj.profile and 'team' in obj.profile:
            return obj.profile['team']
        
        # Check if team_id is in profile
        if obj.profile and 'team_id' in obj.profile:
            try:
                team = Team.objects.get(_id=obj.profile['team_id'])
                return team.name if team else None
            except Team.DoesNotExist:
                pass
        
        # Otherwise, find the team this user is a member of
        try:
            team = Team.objects.filter(members__contains=str(obj._id)).first()
            return team.name if team else None
        except:
            return None
    
    def get_team_id(self, obj):
        """Get team ID from profile or by looking up team"""
        # Check if team_id is in profile
        if obj.profile and 'team_id' in obj.profile:
            return str(obj.profile['team_id'])
        
        # Otherwise, find the team this user is a member of
        try:
            team = Team.objects.filter(members__contains=str(obj._id)).first()
            return str(team._id) if team else None
        except:
            return None
    
    def get_points(self, obj):
        """Get user points from leaderboard (total calories)"""
        from pymongo import MongoClient
        try:
            # Direct MongoDB query to avoid Django ORM type issues
            client = MongoClient('localhost', 27017)
            db = client['octofit_db']
            leaderboard = db.leaderboard.find_one({'user_id': obj._id})
            client.close()
            
            if leaderboard:
                return leaderboard.get('total_calories', 0)
            return 0
        except Exception as e:
            return 0
    
    def create(self, validated_data):
        user = User(**validated_data)
        user.save()
        return user


class TeamSerializer(serializers.ModelSerializer):
    id = serializers.SerializerMethodField()
    members_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Team
        fields = ['id', 'name', 'description', 'members', 'members_count', 'captain_id', 'created_at']
    
    def get_id(self, obj):
        return str(obj._id)
    
    def get_members_count(self, obj):
        """Get the count of members in the team"""
        return len(obj.members) if obj.members else 0


class ActivitySerializer(serializers.ModelSerializer):
    id = serializers.SerializerMethodField()
    user_name = serializers.SerializerMethodField()
    
    class Meta:
        model = Activity
        fields = ['id', 'user_id', 'user_name', 'activity_type', 'duration', 'distance', 'calories', 'date', 'notes', 'created_at']
    
    def get_id(self, obj):
        return str(obj._id)
    
    def get_user_name(self, obj):
        """Get username for the activity"""
        try:
            user = User.objects.get(_id=obj.user_id)
            return user.username
        except User.DoesNotExist:
            return None


class LeaderboardSerializer(serializers.ModelSerializer):
    id = serializers.SerializerMethodField()
    user_name = serializers.SerializerMethodField()
    team_name = serializers.SerializerMethodField()
    
    class Meta:
        model = Leaderboard
        fields = ['id', 'user_id', 'user_name', 'team_id', 'team_name', 'total_activities', 
                  'total_duration', 'total_distance', 'total_calories', 'rank', 'period', 'updated_at']
    
    def get_id(self, obj):
        return str(obj._id)
    
    def get_user_name(self, obj):
        """Get username for the leaderboard entry"""
        try:
            user = User.objects.get(_id=obj.user_id)
            return user.username
        except User.DoesNotExist:
            return None
    
    def get_team_name(self, obj):
        """Get team name for the leaderboard entry"""
        if obj.team_id:
            try:
                team = Team.objects.get(_id=obj.team_id)
                return team.name
            except Team.DoesNotExist:
                return None
        return None


class WorkoutSerializer(serializers.ModelSerializer):
    id = serializers.SerializerMethodField()
    
    class Meta:
        model = Workout
        fields = ['id', 'user_id', 'name', 'description', 'difficulty_level', 
                  'duration', 'category', 'created_at']
    
    def get_id(self, obj):
        return str(obj._id)
    
    def to_representation(self, instance):
        """Custom representation to map field names"""
        representation = super().to_representation(instance)
        # Map the actual model fields to expected frontend fields
        representation['name'] = instance.title
        representation['difficulty_level'] = instance.difficulty
        representation['category'] = instance.category
        return representation
