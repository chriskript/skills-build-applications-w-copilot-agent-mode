# Test data for OctoFit Tracker, adapted from MonaFit Tracker
TEST_USERS = [
    {"username": "alice", "email": "alice@example.com", "password": "alicepass"},
    {"username": "bob", "email": "bob@example.com", "password": "bobpass"},
    {"username": "carol", "email": "carol@example.com", "password": "carolpass"}
]

TEST_TEAMS = [
    {"name": "Team Octopus", "members": ["alice", "bob"]},
    {"name": "Team Kraken", "members": ["carol"]}
]

TEST_ACTIVITIES = [
    {"user": "alice", "activity_type": "Running", "duration": 3600},
    {"user": "bob", "activity_type": "Walking", "duration": 1800},
    {"user": "carol", "activity_type": "Cycling", "duration": 5400}
]

TEST_LEADERBOARD = [
    {"user": "alice", "score": 120},
    {"user": "bob", "score": 80},
    {"user": "carol", "score": 150}
]

TEST_WORKOUTS = [
    {"name": "Morning Cardio", "description": "30 minutes of running and jumping jacks."},
    {"name": "Strength Circuit", "description": "Push-ups, squats, and planks."}
]
