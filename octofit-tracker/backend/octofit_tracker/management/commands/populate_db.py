from django.core.management.base import BaseCommand
from octofit_tracker.test_data import TEST_USERS, TEST_TEAMS, TEST_ACTIVITIES, TEST_LEADERBOARD, TEST_WORKOUTS
from octofit_tracker.models import User, Team, Activity, Leaderboard, Workout
from bson import ObjectId
from datetime import timedelta

class Command(BaseCommand):
    help = 'Populate the octofit_db database with test data.'

    def handle(self, *args, **kwargs):
        # Clear existing data
        User.objects.all().delete()
        Team.objects.all().delete()
        Activity.objects.all().delete()
        Leaderboard.objects.all().delete()
        Workout.objects.all().delete()

        # Create users
        user_objs = {}
        for user in TEST_USERS:
            obj = User.objects.create(_id=ObjectId(), username=user['username'], email=user['email'], password=user['password'])
            user_objs[user['username']] = obj
        self.stdout.write(self.style.SUCCESS('Users created.'))

        # Create teams
        for team in TEST_TEAMS:
            team_obj = Team.objects.create(_id=ObjectId(), name=team['name'])
            for member in team['members']:
                team_obj.members.add(user_objs[member])
        self.stdout.write(self.style.SUCCESS('Teams created.'))

        # Create activities
        for activity in TEST_ACTIVITIES:
            Activity.objects.create(_id=ObjectId(), user=user_objs[activity['user']], activity_type=activity['activity_type'], duration=timedelta(seconds=activity['duration']))
        self.stdout.write(self.style.SUCCESS('Activities created.'))

        # Create leaderboard
        for entry in TEST_LEADERBOARD:
            Leaderboard.objects.create(_id=ObjectId(), user=user_objs[entry['user']], score=entry['score'])
        self.stdout.write(self.style.SUCCESS('Leaderboard created.'))

        # Create workouts
        for workout in TEST_WORKOUTS:
            Workout.objects.create(_id=ObjectId(), name=workout['name'], description=workout['description'])
        self.stdout.write(self.style.SUCCESS('Workouts created.'))
