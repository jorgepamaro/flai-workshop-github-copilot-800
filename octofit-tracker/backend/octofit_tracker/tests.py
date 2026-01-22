from django.test import TestCase
from rest_framework.test import APITestCase
from rest_framework import status
from .models import User, Team, Activity, Leaderboard, Workout
from datetime import datetime


class UserModelTest(TestCase):
    """Test cases for User model"""
    
    def setUp(self):
        self.user = User.objects.create(
            username='testuser',
            email='test@example.com',
            password='testpass123',
            profile={'age': 30, 'gender': 'male'}
        )
    
    def test_user_creation(self):
        """Test that a user can be created"""
        self.assertEqual(self.user.username, 'testuser')
        self.assertEqual(self.user.email, 'test@example.com')
    
    def test_user_str(self):
        """Test user string representation"""
        self.assertEqual(str(self.user), 'testuser')


class TeamModelTest(TestCase):
    """Test cases for Team model"""
    
    def setUp(self):
        self.team = Team.objects.create(
            name='Test Team',
            description='A test team',
            members=['user1', 'user2'],
            captain_id='user1'
        )
    
    def test_team_creation(self):
        """Test that a team can be created"""
        self.assertEqual(self.team.name, 'Test Team')
        self.assertEqual(len(self.team.members), 2)
    
    def test_team_str(self):
        """Test team string representation"""
        self.assertEqual(str(self.team), 'Test Team')


class ActivityModelTest(TestCase):
    """Test cases for Activity model"""
    
    def setUp(self):
        self.activity = Activity.objects.create(
            user_id='user123',
            activity_type='Running',
            duration=30,
            distance=5.0,
            calories=300,
            date=datetime.now(),
            notes='Morning run'
        )
    
    def test_activity_creation(self):
        """Test that an activity can be created"""
        self.assertEqual(self.activity.activity_type, 'Running')
        self.assertEqual(self.activity.duration, 30)
        self.assertEqual(self.activity.distance, 5.0)


class UserAPITest(APITestCase):
    """Test cases for User API endpoints"""
    
    def test_create_user(self):
        """Test creating a user via API"""
        url = '/api/users/'
        data = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password': 'newpass123',
            'profile': {}
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().username, 'newuser')
    
    def test_list_users(self):
        """Test listing users via API"""
        User.objects.create(username='user1', email='user1@example.com', password='pass1')
        User.objects.create(username='user2', email='user2@example.com', password='pass2')
        
        url = '/api/users/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)


class ActivityAPITest(APITestCase):
    """Test cases for Activity API endpoints"""
    
    def test_create_activity(self):
        """Test creating an activity via API"""
        url = '/api/activities/'
        data = {
            'user_id': 'user123',
            'activity_type': 'Running',
            'duration': 45,
            'distance': 7.5,
            'calories': 450,
            'date': datetime.now().isoformat(),
            'notes': 'Evening run'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Activity.objects.count(), 1)


class WorkoutAPITest(APITestCase):
    """Test cases for Workout API endpoints"""
    
    def setUp(self):
        self.workout = Workout.objects.create(
            user_id='user123',
            title='Morning Workout',
            description='A great morning workout',
            exercises=[{'name': 'Push-ups', 'reps': 20}],
            difficulty='intermediate',
            duration=30,
            category='Strength',
            is_recommended=True
        )
    
    def test_get_recommended_workouts(self):
        """Test getting recommended workouts"""
        url = '/api/workouts/recommended/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertTrue(response.data[0]['is_recommended'])
