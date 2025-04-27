import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
# Script to populate octofit_db with test data for users, teams, activities, leaderboard, and workouts
from pymongo import MongoClient
from bson import ObjectId
from datetime import timedelta
from test_data import test_users, test_teams, test_activities, test_leaderboard, test_workouts

# Connect to MongoDB
client = MongoClient('localhost', 27017)
db = client['octofit_db']

# Drop existing collections
for col in ['users', 'teams', 'activities', 'leaderboard', 'workouts']:
    db[col].drop()

# Insert users
db['users'].insert_many(test_users)

# Assign user ObjectIds to teams, activities, leaderboard
user_ids = [user['_id'] for user in test_users]

# Assign all users to both teams
for team in test_teams:
    team['members'] = user_ids

db['teams'].insert_many(test_teams)

# Assign users to activities and leaderboard
for i, activity in enumerate(test_activities):
    activity['user'] = user_ids[i]
for i, entry in enumerate(test_leaderboard):
    entry['user'] = user_ids[i]

# Convert timedelta to seconds for MongoDB compatibility
for activity in test_activities:
    if isinstance(activity["duration"], timedelta):
        activity["duration"] = int(activity["duration"].total_seconds())

db['activities'].insert_many(test_activities)
db['leaderboard'].insert_many(test_leaderboard)
db['workouts'].insert_many(test_workouts)

print('Successfully populated octofit_db with test data.')
