from django.core.management.base import BaseCommand
from django.conf import settings
from octofit_tracker.test_data import TEST_USERS, TEST_TEAMS, TEST_ACTIVITIES, TEST_LEADERBOARD, TEST_WORKOUTS
from pymongo import MongoClient
from datetime import timedelta

class Command(BaseCommand):
    help = 'Populate the octofit_db database with test data using PyMongo.'

    def handle(self, *args, **kwargs):
        # Connect to MongoDB
        client = MongoClient(settings.DATABASES['default']['HOST'], settings.DATABASES['default']['PORT'])
        db = client[settings.DATABASES['default']['NAME']]

        # Drop existing collections
        db.users.drop()
        db.teams.drop()
        db.activities.drop()
        db.leaderboard.drop()
        db.workouts.drop()

        # Insert users
        db.users.insert_many(TEST_USERS)

        # Assign user ObjectIds to teams, activities, leaderboard
        user_ids = [user['_id'] for user in TEST_USERS]
        for team in TEST_TEAMS:
            team['members'] = user_ids
        db.teams.insert_many(TEST_TEAMS)

        # Assign users to activities and leaderboard
        for i, activity in enumerate(TEST_ACTIVITIES):
            activity['user'] = user_ids[i]
            if isinstance(activity['duration'], timedelta):
                activity['duration'] = int(activity['duration'].total_seconds())
        db.activities.insert_many(TEST_ACTIVITIES)

        for i, entry in enumerate(TEST_LEADERBOARD):
            entry['user'] = user_ids[i]
        db.leaderboard.insert_many(TEST_LEADERBOARD)

        db.workouts.insert_many(TEST_WORKOUTS)
        self.stdout.write(self.style.SUCCESS('Successfully populated octofit_db with test data using PyMongo.'))
