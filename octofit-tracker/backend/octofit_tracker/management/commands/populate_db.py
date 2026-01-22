from django.core.management.base import BaseCommand
from pymongo import MongoClient
from datetime import datetime, timedelta
import random


class Command(BaseCommand):
    help = 'Populate the octofit_db database with test data'

    def handle(self, *args, **kwargs):
        # Connect to MongoDB
        client = MongoClient('localhost', 27017)
        db = client['octofit_db']

        self.stdout.write(self.style.SUCCESS('Connected to octofit_db database'))

        # Clear existing data
        self.stdout.write('Clearing existing data...')
        db.users.delete_many({})
        db.teams.delete_many({})
        db.activities.delete_many({})
        db.leaderboard.delete_many({})
        db.workouts.delete_many({})

        # Create unique index on email field
        db.users.create_index('email', unique=True)
        self.stdout.write(self.style.SUCCESS('Created unique index on email field'))

        # Define teams
        teams_data = [
            {
                '_id': 1,
                'name': 'Team Marvel',
                'description': 'Earth\'s Mightiest Heroes',
                'created_at': datetime.now()
            },
            {
                '_id': 2,
                'name': 'Team DC',
                'description': 'Justice for All',
                'created_at': datetime.now()
            }
        ]

        # Insert teams
        db.teams.insert_many(teams_data)
        self.stdout.write(self.style.SUCCESS(f'Created {len(teams_data)} teams'))

        # Define users (superheroes)
        users_data = [
            # Team Marvel
            {
                '_id': 1,
                'username': 'ironman',
                'email': 'tony.stark@marvel.com',
                'password': 'marvel123',
                'profile': {
                    'first_name': 'Tony',
                    'last_name': 'Stark',
                    'team_id': 1
                },
                'created_at': datetime.now()
            },
            {
                '_id': 2,
                'username': 'captainamerica',
                'email': 'steve.rogers@marvel.com',
                'password': 'marvel123',
                'profile': {
                    'first_name': 'Steve',
                    'last_name': 'Rogers',
                    'team_id': 1
                },
                'created_at': datetime.now()
            },
            {
                '_id': 3,
                'username': 'blackwidow',
                'email': 'natasha.romanoff@marvel.com',
                'password': 'marvel123',
                'profile': {
                    'first_name': 'Natasha',
                    'last_name': 'Romanoff',
                    'team_id': 1
                },
                'created_at': datetime.now()
            },
            {
                '_id': 4,
                'username': 'thor',
                'email': 'thor.odinson@marvel.com',
                'password': 'marvel123',
                'profile': {
                    'first_name': 'Thor',
                    'last_name': 'Odinson',
                    'team_id': 1
                },
                'created_at': datetime.now()
            },
            {
                '_id': 5,
                'username': 'hulk',
                'email': 'bruce.banner@marvel.com',
                'password': 'marvel123',
                'profile': {
                    'first_name': 'Bruce',
                    'last_name': 'Banner',
                    'team_id': 1
                },
                'created_at': datetime.now()
            },
            # Team DC
            {
                '_id': 6,
                'username': 'batman',
                'email': 'bruce.wayne@dc.com',
                'password': 'dc123',
                'profile': {
                    'first_name': 'Bruce',
                    'last_name': 'Wayne',
                    'team_id': 2
                },
                'created_at': datetime.now()
            },
            {
                '_id': 7,
                'username': 'superman',
                'email': 'clark.kent@dc.com',
                'password': 'dc123',
                'profile': {
                    'first_name': 'Clark',
                    'last_name': 'Kent',
                    'team_id': 2
                },
                'created_at': datetime.now()
            },
            {
                '_id': 8,
                'username': 'wonderwoman',
                'email': 'diana.prince@dc.com',
                'password': 'dc123',
                'profile': {
                    'first_name': 'Diana',
                    'last_name': 'Prince',
                    'team_id': 2
                },
                'created_at': datetime.now()
            },
            {
                '_id': 9,
                'username': 'flash',
                'email': 'barry.allen@dc.com',
                'password': 'dc123',
                'profile': {
                    'first_name': 'Barry',
                    'last_name': 'Allen',
                    'team_id': 2
                },
                'created_at': datetime.now()
            },
            {
                '_id': 10,
                'username': 'aquaman',
                'email': 'arthur.curry@dc.com',
                'password': 'dc123',
                'profile': {
                    'first_name': 'Arthur',
                    'last_name': 'Curry',
                    'team_id': 2
                },
                'created_at': datetime.now()
            }
        ]

        # Insert users
        db.users.insert_many(users_data)
        self.stdout.write(self.style.SUCCESS(f'Created {len(users_data)} users'))

        # Define workout types
        workout_types = [
            'Running', 'Swimming', 'Cycling', 'Weight Training', 
            'Yoga', 'Boxing', 'CrossFit', 'HIIT'
        ]

        # Define activities
        activities_data = []
        activity_id = 1

        for user in users_data:
            # Generate 5-10 activities per user
            num_activities = random.randint(5, 10)
            for i in range(num_activities):
                days_ago = random.randint(0, 30)
                activity_date = datetime.now() - timedelta(days=days_ago)
                
                activities_data.append({
                    '_id': activity_id,
                    'user_id': user['_id'],
                    'type': random.choice(workout_types),
                    'duration_minutes': random.randint(15, 120),
                    'distance_km': round(random.uniform(1, 20), 2) if random.choice([True, False]) else None,
                    'calories_burned': random.randint(100, 800),
                    'notes': f'Great workout session by {user["username"]}!',
                    'created_at': activity_date
                })
                activity_id += 1

        # Insert activities
        db.activities.insert_many(activities_data)
        self.stdout.write(self.style.SUCCESS(f'Created {len(activities_data)} activities'))

        # Calculate leaderboard data
        leaderboard_data = []
        
        for user in users_data:
            user_activities = [a for a in activities_data if a['user_id'] == user['_id']]
            total_duration = sum(a['duration_minutes'] for a in user_activities)
            total_calories = sum(a['calories_burned'] for a in user_activities)
            total_distance = sum(a['distance_km'] for a in user_activities if a['distance_km'])
            
            leaderboard_data.append({
                '_id': user['_id'],
                'user_id': user['_id'],
                'username': user['username'],
                'team_id': user['profile']['team_id'],
                'total_workouts': len(user_activities),
                'total_duration_minutes': total_duration,
                'total_calories': total_calories,
                'total_distance_km': round(total_distance, 2),
                'rank': 0,  # Will be calculated after sorting
                'updated_at': datetime.now()
            })

        # Sort by total_calories and assign ranks
        leaderboard_data.sort(key=lambda x: x['total_calories'], reverse=True)
        for idx, entry in enumerate(leaderboard_data, start=1):
            entry['rank'] = idx

        # Insert leaderboard
        db.leaderboard.insert_many(leaderboard_data)
        self.stdout.write(self.style.SUCCESS(f'Created {len(leaderboard_data)} leaderboard entries'))

        # Define workout suggestions
        workouts_data = [
            {
                '_id': 1,
                'name': 'Super Soldier Training',
                'description': 'High-intensity interval training inspired by Captain America',
                'type': 'HIIT',
                'difficulty': 'Advanced',
                'duration_minutes': 45,
                'calories_estimate': 600,
                'exercises': [
                    {'name': 'Shield Throws', 'sets': 3, 'reps': 15},
                    {'name': 'Star Jumps', 'sets': 4, 'reps': 20},
                    {'name': 'Combat Push-ups', 'sets': 3, 'reps': 25}
                ],
                'created_at': datetime.now()
            },
            {
                '_id': 2,
                'name': 'Asgardian Strength Training',
                'description': 'Build godly strength with Thor\'s favorite exercises',
                'type': 'Weight Training',
                'difficulty': 'Advanced',
                'duration_minutes': 60,
                'calories_estimate': 500,
                'exercises': [
                    {'name': 'Hammer Curls', 'sets': 4, 'reps': 12},
                    {'name': 'Thunder Squats', 'sets': 5, 'reps': 10},
                    {'name': 'Lightning Deadlifts', 'sets': 4, 'reps': 8}
                ],
                'created_at': datetime.now()
            },
            {
                '_id': 3,
                'name': 'Speed Force Cardio',
                'description': 'Lightning-fast cardio workout inspired by The Flash',
                'type': 'Running',
                'difficulty': 'Intermediate',
                'duration_minutes': 30,
                'calories_estimate': 400,
                'exercises': [
                    {'name': 'Sprint Intervals', 'duration': '10 minutes'},
                    {'name': 'High Knees', 'sets': 3, 'duration': '1 minute'},
                    {'name': 'Cool Down Jog', 'duration': '5 minutes'}
                ],
                'created_at': datetime.now()
            },
            {
                '_id': 4,
                'name': 'Amazonian Warrior Workout',
                'description': 'Build strength and grace like Wonder Woman',
                'type': 'CrossFit',
                'difficulty': 'Intermediate',
                'duration_minutes': 45,
                'calories_estimate': 550,
                'exercises': [
                    {'name': 'Lasso Rope Climbs', 'sets': 3, 'reps': 5},
                    {'name': 'Shield Wall Sits', 'sets': 4, 'duration': '1 minute'},
                    {'name': 'Warrior Burpees', 'sets': 3, 'reps': 15}
                ],
                'created_at': datetime.now()
            },
            {
                '_id': 5,
                'name': 'Dark Knight Combat Training',
                'description': 'Martial arts and agility training from the Batcave',
                'type': 'Boxing',
                'difficulty': 'Advanced',
                'duration_minutes': 50,
                'calories_estimate': 650,
                'exercises': [
                    {'name': 'Shadow Boxing', 'duration': '10 minutes'},
                    {'name': 'Grappling Hook Pull-ups', 'sets': 4, 'reps': 12},
                    {'name': 'Bat Agility Drills', 'sets': 3, 'duration': '5 minutes'}
                ],
                'created_at': datetime.now()
            },
            {
                '_id': 6,
                'name': 'Atlantean Swimming Circuit',
                'description': 'Master the water like Aquaman',
                'type': 'Swimming',
                'difficulty': 'Intermediate',
                'duration_minutes': 40,
                'calories_estimate': 450,
                'exercises': [
                    {'name': 'Freestyle Laps', 'sets': 10, 'distance': '100m'},
                    {'name': 'Underwater Holds', 'sets': 5, 'duration': '30 seconds'},
                    {'name': 'Trident Kicks', 'sets': 8, 'reps': 20}
                ],
                'created_at': datetime.now()
            },
            {
                '_id': 7,
                'name': 'Zen Warrior Yoga',
                'description': 'Find inner peace and flexibility',
                'type': 'Yoga',
                'difficulty': 'Beginner',
                'duration_minutes': 30,
                'calories_estimate': 200,
                'exercises': [
                    {'name': 'Sun Salutations', 'sets': 5},
                    {'name': 'Warrior Poses', 'duration': '10 minutes'},
                    {'name': 'Meditation', 'duration': '5 minutes'}
                ],
                'created_at': datetime.now()
            },
            {
                '_id': 8,
                'name': 'Arc Reactor Cycling',
                'description': 'High-tech cycling workout designed by Tony Stark',
                'type': 'Cycling',
                'difficulty': 'Intermediate',
                'duration_minutes': 45,
                'calories_estimate': 500,
                'exercises': [
                    {'name': 'Steady State Ride', 'duration': '20 minutes'},
                    {'name': 'Hill Climbs', 'sets': 5, 'duration': '3 minutes'},
                    {'name': 'Sprint Intervals', 'sets': 4, 'duration': '1 minute'}
                ],
                'created_at': datetime.now()
            }
        ]

        # Insert workouts
        db.workouts.insert_many(workouts_data)
        self.stdout.write(self.style.SUCCESS(f'Created {len(workouts_data)} workout suggestions'))

        # Summary
        self.stdout.write(self.style.SUCCESS('\n=== Database Population Complete ==='))
        self.stdout.write(self.style.SUCCESS(f'Teams: {len(teams_data)}'))
        self.stdout.write(self.style.SUCCESS(f'Users: {len(users_data)}'))
        self.stdout.write(self.style.SUCCESS(f'Activities: {len(activities_data)}'))
        self.stdout.write(self.style.SUCCESS(f'Leaderboard Entries: {len(leaderboard_data)}'))
        self.stdout.write(self.style.SUCCESS(f'Workout Suggestions: {len(workouts_data)}'))
        
        client.close()
