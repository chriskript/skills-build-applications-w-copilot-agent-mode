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

        # Drop existing collections (use singular names to match expected schema)
        db.users.drop()
        db.teams.drop()
        db.activity.drop()
        db.leaderboard.drop()
        db.workouts.drop()

        # Insert users (deepcopy to avoid mutation issues)
        import copy
        users_to_insert = copy.deepcopy(TEST_USERS)
        teams_to_insert = copy.deepcopy(TEST_TEAMS)
        activities_to_insert = copy.deepcopy(TEST_ACTIVITIES)
        leaderboard_to_insert = copy.deepcopy(TEST_LEADERBOARD)
        workouts_to_insert = copy.deepcopy(TEST_WORKOUTS)
        db.users.insert_many(users_to_insert)

        # Assign user ObjectIds to teams, activities, leaderboard
        user_ids = [user['_id'] for user in users_to_insert]
        for team in teams_to_insert:
            team['members'] = user_ids
        db.teams.insert_many(teams_to_insert)

        # Assign users to activities and leaderboard
        for i, activity in enumerate(activities_to_insert):
            activity['user'] = user_ids[i % len(user_ids)]
            if isinstance(activity['duration'], timedelta):
                activity['duration'] = int(activity['duration'].total_seconds())
            activity['activity_id'] = i + 1  # Add unique activity_id for each activity
        db.activity.insert_many(activities_to_insert)

        for i, entry in enumerate(leaderboard_to_insert):
            entry['user'] = user_ids[i % len(user_ids)]
        db.leaderboard.insert_many(leaderboard_to_insert)

        db.workouts.insert_many(workouts_to_insert)
        self.stdout.write(self.style.SUCCESS('Successfully populated octofit_db with test data using PyMongo.'))
