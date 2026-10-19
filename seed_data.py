"""
Seed Data Script — Gym Membership & Workout Tracking System
=============================================================
This script:
1. Drops and recreates the gym_db database
2. Creates collections WITH schema validation rules
3. Inserts sample data (plans, trainers, members, workouts)
4. Creates indexes

Run this ONCE before starting the app:
    python seed_data.py
"""

from pymongo import MongoClient, ASCENDING, DESCENDING, TEXT
from datetime import datetime, timedelta
import random

# ============================================================
# CONNECT TO MONGODB
# ============================================================
import os
from dotenv import load_dotenv

# Automatically load variables from .env if present
load_dotenv()

MONGO_URI = os.getenv('MONGO_URI') or 'mongodb://localhost:27017/'
client = MongoClient(MONGO_URI)

# Drop existing database for a clean start
client.drop_database('gym_db')
db = client['gym_db']

print("🗑️  Dropped existing gym_db (if any)")
print("📦  Creating fresh database...\n")


# ============================================================
# 1. CREATE COLLECTIONS WITH SCHEMA VALIDATION
# ============================================================

# ---- Members Collection with JSON Schema Validation ----
db.create_collection('members', validator={
    '$jsonSchema': {
        'bsonType': 'object',
        'required': ['name', 'email', 'phone', 'age', 'gender', 'membership'],
        'properties': {
            'name': {
                'bsonType': 'string',
                'description': 'Name is required and must be a string'
            },
            'email': {
                'bsonType': 'string',
                'description': 'Email is required and must be a string'
            },
            'phone': {
                'bsonType': 'string',
                'minLength': 10,
                'maxLength': 15,
                'description': 'Phone must be a string of 10-15 characters'
            },
            'age': {
                'bsonType': 'int',
                'minimum': 16,
                'maximum': 80,
                'description': 'Age must be an integer between 16 and 80'
            },
            'gender': {
                'bsonType': 'string',
                'enum': ['Male', 'Female', 'Other'],
                'description': 'Gender must be Male, Female, or Other'
            },
            'membership': {
                'bsonType': 'object',
                'required': ['plan_name', 'status'],
                'properties': {
                    'plan_name': {
                        'bsonType': 'string',
                        'description': 'Plan name is required'
                    },
                    'status': {
                        'bsonType': 'string',
                        'enum': ['active', 'expired', 'cancelled'],
                        'description': 'Status must be active, expired, or cancelled'
                    }
                }
            }
        }
    }
}, validationAction='error')

print("✅  Created 'members' collection with schema validation")

# ---- Workouts Collection with JSON Schema Validation ----
db.create_collection('workouts', validator={
    '$jsonSchema': {
        'bsonType': 'object',
        'required': ['member_email', 'date', 'workout_type', 'duration_minutes', 'calories_burned'],
        'properties': {
            'member_email': {
                'bsonType': 'string',
                'description': 'Member email is required'
            },
            'date': {
                'bsonType': 'date',
                'description': 'Date is required and must be a valid date'
            },
            'workout_type': {
                'bsonType': 'string',
                'enum': ['Strength', 'Cardio', 'Flexibility', 'HIIT', 'Yoga'],
                'description': 'Workout type must be one of: Strength, Cardio, Flexibility, HIIT, Yoga'
            },
            'duration_minutes': {
                'bsonType': 'int',
                'minimum': 10,
                'maximum': 300,
                'description': 'Duration must be between 10 and 300 minutes'
            },
            'calories_burned': {
                'bsonType': 'int',
                'minimum': 0,
                'description': 'Calories burned must be non-negative'
            }
        }
    }
}, validationAction='error')

print("✅  Created 'workouts' collection with schema validation")

# ---- Plans & Trainers (no strict validation needed, but created normally) ----
db.create_collection('plans')
db.create_collection('trainers')

print("✅  Created 'plans' and 'trainers' collections\n")


# ============================================================
# 2. INSERT SAMPLE DATA
# ============================================================

# ---- Plans (insert_many) ----
plans_data = [
    {
        'plan_name': 'Silver',
        'duration_months': 1,
        'price': 1500,
        'features': ['Gym Access', 'Locker Room'],
        'description': 'Basic 1-month plan for beginners'
    },
    {
        'plan_name': 'Gold',
        'duration_months': 6,
        'price': 5000,
        'features': ['Gym Access', 'Personal Trainer', 'Diet Plan', 'Locker Room'],
        'description': 'Premium 6-month plan with trainer'
    },
    {
        'plan_name': 'Platinum',
        'duration_months': 12,
        'price': 8500,
        'features': ['Gym Access', 'Personal Trainer', 'Diet Plan', 'Locker Room', 'Supplements', 'Spa Access'],
        'description': 'Ultimate annual plan with all benefits'
    },
    {
        'plan_name': 'Student',
        'duration_months': 3,
        'price': 2500,
        'features': ['Gym Access', 'Group Training', 'Locker Room'],
        'description': 'Special 3-month plan for students'
    }
]

db.plans.insert_many(plans_data)
print(f"📋  Inserted {len(plans_data)} plans")

# ---- Trainers (insert_many) ----
trainers_data = [
    {
        'name': 'Rahul Sharma',
        'email': 'rahul@gymtrackpro.com',
        'phone': '9876543210',
        'specialization': ['Strength Training', 'HIIT'],
        'experience_years': 5,
        'rating': 4.8,
        'salary': 35000,
        'availability': ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
    },
    {
        'name': 'Priya Singh',
        'email': 'priya@gymtrackpro.com',
        'phone': '9876543211',
        'specialization': ['Yoga', 'Flexibility'],
        'experience_years': 7,
        'rating': 4.9,
        'salary': 38000,
        'availability': ['Monday', 'Wednesday', 'Friday', 'Saturday']
    },
    {
        'name': 'Arjun Patel',
        'email': 'arjun@gymtrackpro.com',
        'phone': '9876543212',
        'specialization': ['Cardio', 'Weight Loss'],
        'experience_years': 3,
        'rating': 4.5,
        'salary': 28000,
        'availability': ['Tuesday', 'Thursday', 'Saturday', 'Sunday']
    },
    {
        'name': 'Neha Gupta',
        'email': 'neha@gymtrackpro.com',
        'phone': '9876543213',
        'specialization': ['Strength Training', 'CrossFit'],
        'experience_years': 4,
        'rating': 4.6,
        'salary': 32000,
        'availability': ['Monday', 'Tuesday', 'Thursday', 'Friday']
    },
    {
        'name': 'Vikram Reddy',
        'email': 'vikram@gymtrackpro.com',
        'phone': '9876543214',
        'specialization': ['HIIT', 'Cardio', 'Functional Training'],
        'experience_years': 6,
        'rating': 4.7,
        'salary': 36000,
        'availability': ['Monday', 'Wednesday', 'Friday', 'Sunday']
    }
]

db.trainers.insert_many(trainers_data)
print(f"🏋️  Inserted {len(trainers_data)} trainers")

# ---- Members (insert_many) ----
trainer_names = [t['name'] for t in trainers_data]
plan_names = ['Silver', 'Gold', 'Platinum', 'Student']
plan_durations = {'Silver': 30, 'Gold': 180, 'Platinum': 365, 'Student': 90}

members_data = [
    {'name': 'Amit Kumar', 'email': 'amit@gmail.com', 'phone': '9123456701', 'age': 25, 'gender': 'Male',
     'plan': 'Gold', 'trainer': 'Rahul Sharma', 'height': 175, 'weight': 78, 'months_ago': 8},
    {'name': 'Sneha Verma', 'email': 'sneha@gmail.com', 'phone': '9123456702', 'age': 28, 'gender': 'Female',
     'plan': 'Platinum', 'trainer': 'Priya Singh', 'height': 162, 'weight': 58, 'months_ago': 10},
    {'name': 'Rohan Joshi', 'email': 'rohan@gmail.com', 'phone': '9123456703', 'age': 22, 'gender': 'Male',
     'plan': 'Student', 'trainer': 'Arjun Patel', 'height': 180, 'weight': 85, 'months_ago': 2},
    {'name': 'Kavya Nair', 'email': 'kavya@gmail.com', 'phone': '9123456704', 'age': 30, 'gender': 'Female',
     'plan': 'Gold', 'trainer': 'Neha Gupta', 'height': 158, 'weight': 55, 'months_ago': 5},
    {'name': 'Aryan Mehta', 'email': 'aryan@gmail.com', 'phone': '9123456705', 'age': 35, 'gender': 'Male',
     'plan': 'Platinum', 'trainer': 'Vikram Reddy', 'height': 172, 'weight': 90, 'months_ago': 11},
    {'name': 'Pooja Desai', 'email': 'pooja@gmail.com', 'phone': '9123456706', 'age': 26, 'gender': 'Female',
     'plan': 'Silver', 'trainer': 'Priya Singh', 'height': 165, 'weight': 62, 'months_ago': 1},
    {'name': 'Kunal Chopra', 'email': 'kunal@gmail.com', 'phone': '9123456707', 'age': 29, 'gender': 'Male',
     'plan': 'Gold', 'trainer': 'Rahul Sharma', 'height': 178, 'weight': 82, 'months_ago': 7},
    {'name': 'Divya Rao', 'email': 'divya@gmail.com', 'phone': '9123456708', 'age': 24, 'gender': 'Female',
     'plan': 'Student', 'trainer': '', 'height': 160, 'weight': 52, 'months_ago': 3},
    {'name': 'Harsh Lade', 'email': 'harsh@gmail.com', 'phone': '9123456709', 'age': 21, 'gender': 'Male',
     'plan': 'Gold', 'trainer': 'Vikram Reddy', 'height': 174, 'weight': 72, 'months_ago': 4},
    {'name': 'Meera Iyer', 'email': 'meera@gmail.com', 'phone': '9123456710', 'age': 33, 'gender': 'Female',
     'plan': 'Platinum', 'trainer': 'Neha Gupta', 'height': 168, 'weight': 65, 'months_ago': 9},
    {'name': 'Siddharth Malhotra', 'email': 'sid@gmail.com', 'phone': '9123456711', 'age': 27, 'gender': 'Male',
     'plan': 'Silver', 'trainer': 'Arjun Patel', 'height': 182, 'weight': 88, 'months_ago': 2},
    {'name': 'Ananya Bhatt', 'email': 'ananya@gmail.com', 'phone': '9123456712', 'age': 23, 'gender': 'Female',
     'plan': 'Student', 'trainer': 'Priya Singh', 'height': 155, 'weight': 50, 'months_ago': 1},
    {'name': 'Rajesh Khanna', 'email': 'rajesh@gmail.com', 'phone': '9123456713', 'age': 45, 'gender': 'Male',
     'plan': 'Gold', 'trainer': 'Rahul Sharma', 'height': 170, 'weight': 95, 'months_ago': 6},
    {'name': 'Tanvi Agarwal', 'email': 'tanvi@gmail.com', 'phone': '9123456714', 'age': 31, 'gender': 'Female',
     'plan': 'Platinum', 'trainer': 'Vikram Reddy', 'height': 163, 'weight': 57, 'months_ago': 12},
    {'name': 'Nikhil Saxena', 'email': 'nikhil@gmail.com', 'phone': '9123456715', 'age': 20, 'gender': 'Male',
     'plan': 'Student', 'trainer': '', 'height': 176, 'weight': 68, 'months_ago': 1},
    {'name': 'Riya Kapoor', 'email': 'riya@gmail.com', 'phone': '9123456716', 'age': 19, 'gender': 'Female',
     'plan': 'Silver', 'trainer': 'Neha Gupta', 'height': 159, 'weight': 54, 'months_ago': 0},
    {'name': 'Aditya Thakur', 'email': 'aditya@gmail.com', 'phone': '9123456717', 'age': 38, 'gender': 'Male',
     'plan': 'Platinum', 'trainer': 'Rahul Sharma', 'height': 185, 'weight': 92, 'months_ago': 14},
    {'name': 'Sanya Mirza', 'email': 'sanya@gmail.com', 'phone': '9123456718', 'age': 26, 'gender': 'Female',
     'plan': 'Gold', 'trainer': 'Arjun Patel', 'height': 167, 'weight': 60, 'months_ago': 3},
]

members_insert = []
for m in members_data:
    join_date = datetime.now() - timedelta(days=m['months_ago'] * 30)
    plan_dur = plan_durations[m['plan']]
    end_date = join_date + timedelta(days=plan_dur)
    status = 'active' if end_date > datetime.now() else 'expired'

    bmi = round(m['weight'] / ((m['height'] / 100) ** 2), 1)

    members_insert.append({
        'name': m['name'],
        'email': m['email'],
        'phone': m['phone'],
        'age': m['age'],
        'gender': m['gender'],
        'join_date': join_date,
        'membership': {
            'plan_name': m['plan'],
            'start_date': join_date,
            'end_date': end_date,
            'status': status
        },
        'trainer_name': m['trainer'],
        'body_metrics': {
            'height_cm': float(m['height']),
            'weight_kg': float(m['weight']),
            'bmi': bmi
        }
    })

db.members.insert_many(members_insert)
print(f"👥  Inserted {len(members_insert)} members")

# ---- Workouts (insert_many) ----
workout_types = ['Strength', 'Cardio', 'Flexibility', 'HIIT', 'Yoga']

exercise_library = {
    'Strength': [
        {'name': 'Bench Press', 'sets': 4, 'reps': 10, 'weight_kg': 60},
        {'name': 'Squats', 'sets': 4, 'reps': 12, 'weight_kg': 80},
        {'name': 'Deadlift', 'sets': 3, 'reps': 8, 'weight_kg': 100},
        {'name': 'Overhead Press', 'sets': 3, 'reps': 10, 'weight_kg': 40},
        {'name': 'Barbell Rows', 'sets': 4, 'reps': 10, 'weight_kg': 50},
        {'name': 'Bicep Curls', 'sets': 3, 'reps': 12, 'weight_kg': 15},
        {'name': 'Tricep Dips', 'sets': 3, 'reps': 15, 'weight_kg': 0},
        {'name': 'Lat Pulldown', 'sets': 3, 'reps': 12, 'weight_kg': 45},
    ],
    'Cardio': [
        {'name': 'Treadmill Running', 'sets': 1, 'reps': 1, 'weight_kg': 0},
        {'name': 'Cycling', 'sets': 1, 'reps': 1, 'weight_kg': 0},
        {'name': 'Rowing Machine', 'sets': 1, 'reps': 1, 'weight_kg': 0},
        {'name': 'Jump Rope', 'sets': 3, 'reps': 100, 'weight_kg': 0},
        {'name': 'Elliptical', 'sets': 1, 'reps': 1, 'weight_kg': 0},
    ],
    'HIIT': [
        {'name': 'Burpees', 'sets': 4, 'reps': 15, 'weight_kg': 0},
        {'name': 'Box Jumps', 'sets': 4, 'reps': 12, 'weight_kg': 0},
        {'name': 'Mountain Climbers', 'sets': 3, 'reps': 30, 'weight_kg': 0},
        {'name': 'Battle Ropes', 'sets': 4, 'reps': 20, 'weight_kg': 0},
        {'name': 'Kettlebell Swings', 'sets': 4, 'reps': 15, 'weight_kg': 16},
    ],
    'Yoga': [
        {'name': 'Sun Salutation', 'sets': 5, 'reps': 1, 'weight_kg': 0},
        {'name': 'Warrior Pose', 'sets': 3, 'reps': 1, 'weight_kg': 0},
        {'name': 'Tree Pose', 'sets': 3, 'reps': 1, 'weight_kg': 0},
        {'name': 'Downward Dog', 'sets': 3, 'reps': 1, 'weight_kg': 0},
    ],
    'Flexibility': [
        {'name': 'Hamstring Stretch', 'sets': 3, 'reps': 1, 'weight_kg': 0},
        {'name': 'Quad Stretch', 'sets': 3, 'reps': 1, 'weight_kg': 0},
        {'name': 'Hip Flexor Stretch', 'sets': 3, 'reps': 1, 'weight_kg': 0},
        {'name': 'Shoulder Stretch', 'sets': 3, 'reps': 1, 'weight_kg': 0},
        {'name': 'Foam Rolling', 'sets': 1, 'reps': 1, 'weight_kg': 0},
    ]
}

notes_options = [
    'Great session!', 'Felt strong today', 'Need to increase weight next time',
    'Good progress', 'Focused on form', 'Pushed hard today',
    'Recovery day, took it easy', 'New personal best!', 'Felt tired but finished strong',
    ''
]

workouts_insert = []
for m in members_data:
    # Each member gets 2-5 random workouts
    num_workouts = random.randint(2, 5)
    for _ in range(num_workouts):
        wtype = random.choice(workout_types)
        exercises = random.sample(exercise_library[wtype], min(random.randint(2, 4), len(exercise_library[wtype])))

        # Randomize the exercise weights/reps slightly
        modified_exercises = []
        for ex in exercises:
            modified_exercises.append({
                'name': ex['name'],
                'sets': ex['sets'] + random.randint(-1, 1),
                'reps': max(1, ex['reps'] + random.randint(-3, 3)),
                'weight_kg': max(0, ex['weight_kg'] + random.randint(-10, 10))
            })

        duration = random.randint(30, 90)
        calories = random.randint(150, 600)
        days_ago = random.randint(0, 180)

        workouts_insert.append({
            'member_name': m['name'],
            'member_email': m['email'],
            'date': datetime.now() - timedelta(days=days_ago),
            'workout_type': wtype,
            'duration_minutes': duration,
            'calories_burned': calories,
            'exercises': modified_exercises,
            'notes': random.choice(notes_options)
        })

db.workouts.insert_many(workouts_insert)
print(f"💪  Inserted {len(workouts_insert)} workouts\n")


# ============================================================
# 3. CREATE INDEXES
# ============================================================
print("📇  Creating indexes...")

# Unique index on members.email
db.members.create_index('email', unique=True, name='idx_email_unique')
print("   ✓ Unique index: members.email")

# Single field index on membership status
db.members.create_index('membership.status', name='idx_membership_status')
print("   ✓ Single field index: members.membership.status")

# Compound index on workouts
db.workouts.create_index(
    [('member_email', ASCENDING), ('date', DESCENDING)],
    name='idx_member_date_compound'
)
print("   ✓ Compound index: workouts (member_email + date)")

# Single field index on workout type
db.workouts.create_index('workout_type', name='idx_workout_type')
print("   ✓ Single field index: workouts.workout_type")

# Text index on trainer name
db.trainers.create_index([('name', TEXT)], name='idx_trainer_name_text')
print("   ✓ Text index: trainers.name")


# ============================================================
# 4. VERIFY
# ============================================================
print("\n" + "="*50)
print("  ✅  DATABASE SEEDED SUCCESSFULLY!")
print("="*50)
print(f"\n  Database: gym_db")
print(f"  Plans:    {db.plans.count_documents({})} documents")
print(f"  Trainers: {db.trainers.count_documents({})} documents")
print(f"  Members:  {db.members.count_documents({})} documents")
print(f"  Workouts: {db.workouts.count_documents({})} documents")
print(f"\n  Active Members:  {db.members.count_documents({'membership.status': 'active'})}")
print(f"  Expired Members: {db.members.count_documents({'membership.status': 'expired'})}")
print(f"\n  Now run: python app.py")
print("="*50 + "\n")
