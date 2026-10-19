"""
Gym Membership & Workout Tracking System
=========================================
Flask + PyMongo Web Application
Course: CSE494 – Intelligent NoSQL Databases

This file contains all routes, CRUD operations, aggregation pipelines,
indexing demos, and schema validation logic.
"""

from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from pymongo import MongoClient, ASCENDING, DESCENDING, TEXT
from pymongo.errors import WriteError, OperationFailure, DuplicateKeyError
from bson import ObjectId
from datetime import datetime, timedelta
import json

# ============================================================
# APP CONFIGURATION
# ============================================================
app = Flask(__name__)
app.secret_key = 'gym_tracking_cse494_2026'

# ============================================================
# MONGODB CONNECTION (PyMongo)
# ============================================================
import os
from dotenv import load_dotenv

# Automatically load variables from .env if present
load_dotenv()

MONGO_URI = os.getenv('MONGO_URI') or 'mongodb://localhost:27017/'
client = MongoClient(MONGO_URI)
db = client['gym_db']

# Collection references
plans_col = db['plans']
trainers_col = db['trainers']
members_col = db['members']
workouts_col = db['workouts']

# ============================================================
# HELPER FUNCTIONS
# ============================================================

# Rotating avatar colors for the UI
AVATAR_COLORS = ['violet', 'cyan', 'green', 'amber', 'rose']

def get_avatar_color(name):
    """Assign a consistent avatar color based on the name."""
    return AVATAR_COLORS[sum(ord(c) for c in name) % len(AVATAR_COLORS)]

def get_initials(name):
    """Get initials from a full name."""
    parts = name.strip().split()
    if len(parts) >= 2:
        return (parts[0][0] + parts[1][0]).upper()
    return name[0:2].upper()


# ============================================================
# PAGE ROUTES
# ============================================================

# ---- DASHBOARD ----
@app.route('/')
def dashboard():
    """Dashboard page with stats, charts, and recent activity."""
    # Basic counts
    stats = {
        'total_members': members_col.count_documents({}),
        'active_members': members_col.count_documents({'membership.status': 'active'}),
        'total_workouts': workouts_col.count_documents({}),
        'total_trainers': trainers_col.count_documents({}),
        'total_plans': plans_col.count_documents({})
    }

    # --- Aggregation: Total Revenue ---
    revenue_pipeline = [
        {'$match': {'membership.status': {'$in': ['active', 'expired']}}},
        {'$group': {
            '_id': '$membership.plan_name',
            'count': {'$sum': 1}
        }}
    ]
    plan_counts = {r['_id']: r['count'] for r in members_col.aggregate(revenue_pipeline)}
    total_revenue = 0
    for plan in plans_col.find():
        count = plan_counts.get(plan['plan_name'], 0)
        total_revenue += plan.get('price', 0) * count
    stats['total_revenue'] = total_revenue

    # --- Aggregation: Workout Type Distribution ---
    workout_dist = list(workouts_col.aggregate([
        {'$group': {'_id': '$workout_type', 'count': {'$sum': 1}}},
        {'$sort': {'count': DESCENDING}}
    ]))

    # --- Aggregation: Monthly Signups ---
    monthly_signups = list(members_col.aggregate([
        {'$project': {
            'month': {'$month': '$join_date'},
            'monthName': {
                '$arrayElemAt': [
                    ['', 'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
                     'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
                    {'$month': '$join_date'}
                ]
            }
        }},
        {'$group': {'_id': '$month', 'label': {'$first': '$monthName'}, 'count': {'$sum': 1}}},
        {'$sort': {'_id': ASCENDING}}
    ]))

    # Recent members (sorted by join_date descending, limit 5)
    recent_members = list(members_col.find().sort('join_date', DESCENDING).limit(5))

    return render_template('dashboard.html',
                           active_page='dashboard',
                           stats=stats,
                           workout_dist=workout_dist,
                           monthly_signups=monthly_signups,
                           recent_members=recent_members,
                           get_avatar_color=get_avatar_color,
                           get_initials=get_initials)


# ---- MEMBERS PAGE ----
@app.route('/members')
def members_page():
    """Members listing page with CRUD forms."""
    all_members = list(members_col.find().sort('name', ASCENDING))
    all_plans = list(plans_col.find())
    all_trainers = list(trainers_col.find())
    return render_template('members.html',
                           active_page='members',
                           members=all_members,
                           plans=all_plans,
                           trainers=all_trainers,
                           get_avatar_color=get_avatar_color,
                           get_initials=get_initials)


# ---- MEMBERS: CREATE (insert_one) ----
@app.route('/members/add', methods=['POST'])
def add_member():
    """Insert a new member document into the members collection."""
    try:
        height_cm = float(request.form.get('height_cm', 170))
        weight_kg = float(request.form.get('weight_kg', 70))
        bmi = round(weight_kg / ((height_cm / 100) ** 2), 1) if height_cm > 0 else 0

        # Get plan duration for calculating end_date
        plan_name = request.form['plan_name']
        plan = plans_col.find_one({'plan_name': plan_name})
        duration_months = plan['duration_months'] if plan else 1
        start_date = datetime.now()
        end_date = start_date + timedelta(days=duration_months * 30)

        member = {
            'name': request.form['name'],
            'email': request.form['email'],
            'phone': request.form['phone'],
            'age': int(request.form['age']),
            'gender': request.form['gender'],
            'join_date': start_date,
            'membership': {
                'plan_name': plan_name,
                'start_date': start_date,
                'end_date': end_date,
                'status': 'active'
            },
            'trainer_name': request.form.get('trainer_name', ''),
            'body_metrics': {
                'height_cm': height_cm,
                'weight_kg': weight_kg,
                'bmi': bmi
            }
        }
        members_col.insert_one(member)
        flash('Member added successfully!', 'success')
    except DuplicateKeyError:
        flash('A member with this email already exists!', 'error')
    except WriteError as e:
        flash(f'Validation Error: {str(e)}', 'error')
    except Exception as e:
        flash(f'Error: {str(e)}', 'error')
    return redirect(url_for('members_page'))


# ---- MEMBERS: UPDATE (update_one with $set) ----
@app.route('/members/update/<id>', methods=['POST'])
def update_member(id):
    """Update member details using $set operator."""
    try:
        update_data = {}
        if request.form.get('name'):
            update_data['name'] = request.form['name']
        if request.form.get('phone'):
            update_data['phone'] = request.form['phone']
        if request.form.get('age'):
            update_data['age'] = int(request.form['age'])
        if request.form.get('weight_kg'):
            weight = float(request.form['weight_kg'])
            # Fetch current height to recalculate BMI
            member = members_col.find_one({'_id': ObjectId(id)})
            height = member.get('body_metrics', {}).get('height_cm', 170) if member else 170
            update_data['body_metrics.weight_kg'] = weight
            update_data['body_metrics.bmi'] = round(weight / ((height / 100) ** 2), 1)
        if request.form.get('status'):
            update_data['membership.status'] = request.form['status']
        if request.form.get('trainer_name'):
            update_data['trainer_name'] = request.form['trainer_name']

        if update_data:
            result = members_col.update_one({'_id': ObjectId(id)}, {'$set': update_data})
            if result.modified_count > 0:
                flash('Member updated successfully!', 'success')
            else:
                flash('No changes were made.', 'info')
    except WriteError as e:
        flash(f'Validation Error: {str(e)}', 'error')
    except Exception as e:
        flash(f'Error: {str(e)}', 'error')
    return redirect(url_for('members_page'))


# ---- MEMBERS: DELETE (delete_one) ----
@app.route('/members/delete/<id>')
def delete_member(id):
    """Delete a member document."""
    try:
        result = members_col.delete_one({'_id': ObjectId(id)})
        if result.deleted_count > 0:
            # Also delete their workouts
            workouts_col.delete_many({'member_email': members_col.find_one({'_id': ObjectId(id)})})
            flash('Member deleted successfully!', 'success')
        else:
            flash('Member not found.', 'error')
    except Exception as e:
        flash(f'Error: {str(e)}', 'error')
    return redirect(url_for('members_page'))


# ---- MEMBERS: BULK UPDATE (update_many) ----
@app.route('/members/expire-old')
def expire_old_memberships():
    """Mark all memberships with end_date in the past as expired using update_many."""
    try:
        result = members_col.update_many(
            {
                'membership.end_date': {'$lt': datetime.now()},
                'membership.status': 'active'
            },
            {'$set': {'membership.status': 'expired'}}
        )
        flash(f'{result.modified_count} expired memberships updated!', 'success')
    except Exception as e:
        flash(f'Error: {str(e)}', 'error')
    return redirect(url_for('members_page'))


# ---- WORKOUTS PAGE ----
@app.route('/workouts')
def workouts_page():
    """Workouts listing page."""
    all_workouts = list(workouts_col.find().sort('date', DESCENDING))
    all_members = list(members_col.find({}, {'name': 1, 'email': 1}).sort('name', ASCENDING))
    return render_template('workouts.html',
                           active_page='workouts',
                           workouts=all_workouts,
                           members=all_members)


# ---- WORKOUTS: CREATE (insert_one) ----
@app.route('/workouts/add', methods=['POST'])
def add_workout():
    """Log a new workout session."""
    try:
        # Build exercises list from form
        exercises = []
        ex_names = request.form.getlist('ex_name[]')
        ex_sets = request.form.getlist('ex_sets[]')
        ex_reps = request.form.getlist('ex_reps[]')
        ex_weights = request.form.getlist('ex_weight[]')

        for i in range(len(ex_names)):
            if ex_names[i].strip():
                exercises.append({
                    'name': ex_names[i],
                    'sets': int(ex_sets[i]) if ex_sets[i] else 0,
                    'reps': int(ex_reps[i]) if ex_reps[i] else 0,
                    'weight_kg': float(ex_weights[i]) if ex_weights[i] else 0
                })

        # Get member info
        member_email = request.form['member_email']
        member = members_col.find_one({'email': member_email})
        member_name = member['name'] if member else 'Unknown'

        workout = {
            'member_name': member_name,
            'member_email': member_email,
            'date': datetime.strptime(request.form['date'], '%Y-%m-%d') if request.form.get('date') else datetime.now(),
            'workout_type': request.form['workout_type'],
            'duration_minutes': int(request.form['duration_minutes']),
            'calories_burned': int(request.form['calories_burned']),
            'exercises': exercises,
            'notes': request.form.get('notes', '')
        }
        workouts_col.insert_one(workout)
        flash('Workout logged successfully!', 'success')
    except WriteError as e:
        flash(f'Validation Error: {str(e)}', 'error')
    except Exception as e:
        flash(f'Error: {str(e)}', 'error')
    return redirect(url_for('workouts_page'))


# ---- WORKOUTS: UPDATE (update_one with $push) ----
@app.route('/workouts/add-exercise/<id>', methods=['POST'])
def add_exercise_to_workout(id):
    """Add an exercise to an existing workout using $push operator."""
    try:
        exercise = {
            'name': request.form['ex_name'],
            'sets': int(request.form['ex_sets']),
            'reps': int(request.form['ex_reps']),
            'weight_kg': float(request.form.get('ex_weight', 0))
        }
        workouts_col.update_one(
            {'_id': ObjectId(id)},
            {'$push': {'exercises': exercise}}
        )
        flash('Exercise added to workout!', 'success')
    except Exception as e:
        flash(f'Error: {str(e)}', 'error')
    return redirect(url_for('workouts_page'))


# ---- WORKOUTS: DELETE ----
@app.route('/workouts/delete/<id>')
def delete_workout(id):
    """Delete a workout log."""
    try:
        workouts_col.delete_one({'_id': ObjectId(id)})
        flash('Workout deleted successfully!', 'success')
    except Exception as e:
        flash(f'Error: {str(e)}', 'error')
    return redirect(url_for('workouts_page'))


# ---- WORKOUTS: DELETE MANY (delete old workouts) ----
@app.route('/workouts/delete-old')
def delete_old_workouts():
    """Delete all workouts older than 1 year using delete_many."""
    try:
        one_year_ago = datetime.now() - timedelta(days=365)
        result = workouts_col.delete_many({'date': {'$lt': one_year_ago}})
        flash(f'{result.deleted_count} old workouts removed!', 'success')
    except Exception as e:
        flash(f'Error: {str(e)}', 'error')
    return redirect(url_for('workouts_page'))


# ---- TRAINERS PAGE ----
@app.route('/trainers')
def trainers_page():
    """Trainers listing page."""
    all_trainers = list(trainers_col.find().sort('name', ASCENDING))
    return render_template('trainers.html',
                           active_page='trainers',
                           trainers=all_trainers,
                           get_avatar_color=get_avatar_color,
                           get_initials=get_initials)


# ---- TRAINERS: CREATE ----
@app.route('/trainers/add', methods=['POST'])
def add_trainer():
    """Add a new trainer."""
    try:
        specializations = [s.strip() for s in request.form['specialization'].split(',') if s.strip()]
        availability = request.form.getlist('availability')

        trainer = {
            'name': request.form['name'],
            'email': request.form['email'],
            'phone': request.form['phone'],
            'specialization': specializations,
            'experience_years': int(request.form['experience_years']),
            'rating': float(request.form.get('rating', 4.0)),
            'salary': int(request.form['salary']),
            'availability': availability
        }
        trainers_col.insert_one(trainer)
        flash('Trainer added successfully!', 'success')
    except Exception as e:
        flash(f'Error: {str(e)}', 'error')
    return redirect(url_for('trainers_page'))


# ---- TRAINERS: UPDATE ----
@app.route('/trainers/update/<id>', methods=['POST'])
def update_trainer(id):
    """Update trainer details."""
    try:
        update_data = {}
        if request.form.get('phone'):
            update_data['phone'] = request.form['phone']
        if request.form.get('experience_years'):
            update_data['experience_years'] = int(request.form['experience_years'])
        if request.form.get('rating'):
            update_data['rating'] = float(request.form['rating'])
        if request.form.get('salary'):
            update_data['salary'] = int(request.form['salary'])

        if update_data:
            trainers_col.update_one({'_id': ObjectId(id)}, {'$set': update_data})
            flash('Trainer updated successfully!', 'success')
    except Exception as e:
        flash(f'Error: {str(e)}', 'error')
    return redirect(url_for('trainers_page'))


# ---- TRAINERS: DELETE ----
@app.route('/trainers/delete/<id>')
def delete_trainer(id):
    """Delete a trainer."""
    try:
        trainers_col.delete_one({'_id': ObjectId(id)})
        flash('Trainer deleted successfully!', 'success')
    except Exception as e:
        flash(f'Error: {str(e)}', 'error')
    return redirect(url_for('trainers_page'))


# ---- PLANS PAGE ----
@app.route('/plans')
def plans_page():
    """Plans listing page."""
    all_plans = list(plans_col.find().sort('price', ASCENDING))
    return render_template('plans.html',
                           active_page='plans',
                           plans=all_plans)


# ---- PLANS: CREATE ----
@app.route('/plans/add', methods=['POST'])
def add_plan():
    """Add a new membership plan."""
    try:
        features = [f.strip() for f in request.form['features'].split(',') if f.strip()]
        plan = {
            'plan_name': request.form['plan_name'],
            'duration_months': int(request.form['duration_months']),
            'price': int(request.form['price']),
            'features': features,
            'description': request.form.get('description', '')
        }
        plans_col.insert_one(plan)
        flash('Plan added successfully!', 'success')
    except Exception as e:
        flash(f'Error: {str(e)}', 'error')
    return redirect(url_for('plans_page'))


# ---- PLANS: DELETE ----
@app.route('/plans/delete/<id>')
def delete_plan(id):
    """Delete a membership plan."""
    try:
        plans_col.delete_one({'_id': ObjectId(id)})
        flash('Plan deleted successfully!', 'success')
    except Exception as e:
        flash(f'Error: {str(e)}', 'error')
    return redirect(url_for('plans_page'))


# ============================================================
# AGGREGATION REPORTS PAGE
# ============================================================
@app.route('/reports')
def reports_page():
    """Page showing all 6 aggregation pipelines and their results."""
    reports = []

    # --- Pipeline 1: Revenue by Plan ---
    pipeline1 = [
        {'$group': {
            '_id': '$membership.plan_name',
            'member_count': {'$sum': 1}
        }},
        {'$sort': {'member_count': -1}}
    ]
    result1 = list(members_col.aggregate(pipeline1))
    # Enrich with price
    for r in result1:
        plan = plans_col.find_one({'plan_name': r['_id']})
        r['price'] = plan['price'] if plan else 0
        r['revenue'] = r['price'] * r['member_count']
    reports.append({
        'title': 'Revenue by Membership Plan',
        'description': 'Shows how much revenue each plan generates based on member count × price.',
        'stages': '$group → $sort',
        'pipeline_code': "db.members.aggregate([\n  { $group: { _id: '$membership.plan_name',\n             member_count: { $sum: 1 } } },\n  { $sort: { member_count: -1 } }\n])",
        'result': result1,
        'type': 'revenue'
    })

    # --- Pipeline 2: Average Calories by Workout Type ---
    pipeline2 = [
        {'$group': {
            '_id': '$workout_type',
            'avg_calories': {'$avg': '$calories_burned'},
            'total_sessions': {'$sum': 1}
        }},
        {'$sort': {'avg_calories': -1}}
    ]
    result2 = list(workouts_col.aggregate(pipeline2))
    reports.append({
        'title': 'Average Calories Burned by Workout Type',
        'description': 'Which workout type burns the most calories on average?',
        'stages': '$group ($avg) → $sort',
        'pipeline_code': "db.workouts.aggregate([\n  { $group: { _id: '$workout_type',\n             avg_calories: { $avg: '$calories_burned' },\n             total_sessions: { $sum: 1 } } },\n  { $sort: { avg_calories: -1 } }\n])",
        'result': result2,
        'type': 'calories'
    })

    # --- Pipeline 3: Top 5 Most Active Members ---
    pipeline3 = [
        {'$group': {
            '_id': '$member_name',
            'workout_count': {'$sum': 1},
            'total_calories': {'$sum': '$calories_burned'},
            'total_minutes': {'$sum': '$duration_minutes'}
        }},
        {'$sort': {'workout_count': -1}},
        {'$limit': 5}
    ]
    result3 = list(workouts_col.aggregate(pipeline3))
    reports.append({
        'title': 'Top 5 Most Active Members',
        'description': 'Members ranked by total number of workout sessions logged.',
        'stages': '$group → $sort → $limit',
        'pipeline_code': "db.workouts.aggregate([\n  { $group: { _id: '$member_name',\n             workout_count: { $sum: 1 },\n             total_calories: { $sum: '$calories_burned' },\n             total_minutes: { $sum: '$duration_minutes' } } },\n  { $sort: { workout_count: -1 } },\n  { $limit: 5 }\n])",
        'result': result3,
        'type': 'active'
    })

    # --- Pipeline 4: Monthly Signup Trend ---
    pipeline4 = [
        {'$project': {
            'month': {'$month': '$join_date'},
            'monthName': {
                '$arrayElemAt': [
                    ['', 'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
                     'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
                    {'$month': '$join_date'}
                ]
            }
        }},
        {'$group': {
            '_id': '$month',
            'month_name': {'$first': '$monthName'},
            'signups': {'$sum': 1}
        }},
        {'$sort': {'_id': 1}}
    ]
    result4 = list(members_col.aggregate(pipeline4))
    reports.append({
        'title': 'Monthly Member Signup Trend',
        'description': 'Track how many new members join each month.',
        'stages': '$project → $group → $sort',
        'pipeline_code': "db.members.aggregate([\n  { $project: { month: { $month: '$join_date' },\n               monthName: { $arrayElemAt: [...months, { $month: '$join_date' }] } } },\n  { $group: { _id: '$month', month_name: { $first: '$monthName' },\n             signups: { $sum: 1 } } },\n  { $sort: { _id: 1 } }\n])",
        'result': result4,
        'type': 'signups'
    })

    # --- Pipeline 5: Trainer Workload ---
    pipeline5 = [
        {'$match': {'trainer_name': {'$ne': ''}}},
        {'$group': {
            '_id': '$trainer_name',
            'member_count': {'$sum': 1}
        }},
        {'$sort': {'member_count': -1}}
    ]
    result5 = list(members_col.aggregate(pipeline5))
    reports.append({
        'title': 'Trainer Workload Analysis',
        'description': 'How many members is each trainer currently handling?',
        'stages': '$match → $group → $sort',
        'pipeline_code': "db.members.aggregate([\n  { $match: { trainer_name: { $ne: '' } } },\n  { $group: { _id: '$trainer_name',\n             member_count: { $sum: 1 } } },\n  { $sort: { member_count: -1 } }\n])",
        'result': result5,
        'type': 'workload'
    })

    # --- Pipeline 6: Workout Duration Statistics ---
    pipeline6 = [
        {'$group': {
            '_id': '$workout_type',
            'avg_duration': {'$avg': '$duration_minutes'},
            'min_duration': {'$min': '$duration_minutes'},
            'max_duration': {'$max': '$duration_minutes'},
            'total_sessions': {'$sum': 1}
        }},
        {'$sort': {'avg_duration': -1}}
    ]
    result6 = list(workouts_col.aggregate(pipeline6))
    reports.append({
        'title': 'Workout Duration Statistics',
        'description': 'Average, minimum, and maximum duration for each workout type.',
        'stages': '$group ($avg, $min, $max) → $sort',
        'pipeline_code': "db.workouts.aggregate([\n  { $group: { _id: '$workout_type',\n             avg_duration: { $avg: '$duration_minutes' },\n             min_duration: { $min: '$duration_minutes' },\n             max_duration: { $max: '$duration_minutes' },\n             total_sessions: { $sum: 1 } } },\n  { $sort: { avg_duration: -1 } }\n])",
        'result': result6,
        'type': 'duration'
    })

    return render_template('reports.html',
                           active_page='reports',
                           reports=reports)


# ============================================================
# INDEXING DEMO PAGE
# ============================================================
@app.route('/indexes')
def indexes_page():
    """Page demonstrating indexing and explain()."""
    # Get current indexes
    member_indexes = list(members_col.list_indexes())
    workout_indexes = list(workouts_col.list_indexes())
    trainer_indexes = list(trainers_col.list_indexes())

    return render_template('indexes.html',
                           active_page='indexes',
                           member_indexes=member_indexes,
                           workout_indexes=workout_indexes,
                           trainer_indexes=trainer_indexes)


@app.route('/indexes/create', methods=['POST'])
def create_indexes():
    """Create all project indexes."""
    try:
        results = []

        # 1. Unique index on members.email
        try:
            members_col.create_index('email', unique=True, name='idx_email_unique')
            results.append('✓ Unique index on members.email')
        except OperationFailure:
            results.append('⚡ Index on members.email already exists')

        # 2. Single field index on members.membership.status
        try:
            members_col.create_index('membership.status', name='idx_membership_status')
            results.append('✓ Single field index on members.membership.status')
        except OperationFailure:
            results.append('⚡ Index on membership.status already exists')

        # 3. Compound index on workouts (member_email + date)
        try:
            workouts_col.create_index(
                [('member_email', ASCENDING), ('date', DESCENDING)],
                name='idx_member_date_compound'
            )
            results.append('✓ Compound index on workouts (member_email + date)')
        except OperationFailure:
            results.append('⚡ Compound index on workouts already exists')

        # 4. Single field index on workouts.workout_type
        try:
            workouts_col.create_index('workout_type', name='idx_workout_type')
            results.append('✓ Single field index on workouts.workout_type')
        except OperationFailure:
            results.append('⚡ Index on workout_type already exists')

        # 5. Text index on trainers.name
        try:
            trainers_col.create_index([('name', TEXT)], name='idx_trainer_name_text')
            results.append('✓ Text index on trainers.name')
        except OperationFailure:
            results.append('⚡ Text index on trainers already exists')

        flash(' | '.join(results), 'success')
    except Exception as e:
        flash(f'Error creating indexes: {str(e)}', 'error')
    return redirect(url_for('indexes_page'))


@app.route('/indexes/explain')
def explain_query():
    """Run explain() on a query to show index usage."""
    try:
        query_type = request.args.get('type', 'status')

        if query_type == 'status':
            explain_result = members_col.find(
                {'membership.status': 'active'}
            ).explain()
        elif query_type == 'compound':
            explain_result = workouts_col.find(
                {'member_email': 'amit@gmail.com', 'date': {'$gte': datetime(2026, 1, 1)}}
            ).explain()
        elif query_type == 'text':
            explain_result = trainers_col.find(
                {'$text': {'$search': 'Rahul'}}
            ).explain()
        else:
            explain_result = members_col.find(
                {'email': 'amit@gmail.com'}
            ).explain()

        # Extract key info from explain output
        query_planner = explain_result.get('queryPlanner', {})
        winning_plan = query_planner.get('winningPlan', {})
        exec_stats = explain_result.get('executionStats', {})

        explain_info = {
            'query_type': query_type,
            'winning_plan': json.dumps(winning_plan, indent=2, default=str),
            'stage': winning_plan.get('stage', 'N/A'),
            'docs_examined': exec_stats.get('totalDocsExamined', 'N/A'),
            'docs_returned': exec_stats.get('nReturned', 'N/A'),
            'execution_time': exec_stats.get('executionTimeMillis', 'N/A'),
            'index_used': winning_plan.get('inputStage', {}).get('indexName', 'None (COLLSCAN)')
        }

        return jsonify({'success': True, 'explain': explain_info})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})


# ============================================================
# SCHEMA VALIDATION DEMO PAGE
# ============================================================
@app.route('/validation')
def validation_page():
    """Page demonstrating schema validation."""
    # Get current validation rules
    member_validation = {}
    workout_validation = {}

    try:
        coll_info = db.command('listCollections', filter={'name': 'members'})
        for coll in coll_info.get('cursor', {}).get('firstBatch', []):
            member_validation = coll.get('options', {}).get('validator', {})
    except Exception:
        pass

    try:
        coll_info = db.command('listCollections', filter={'name': 'workouts'})
        for coll in coll_info.get('cursor', {}).get('firstBatch', []):
            workout_validation = coll.get('options', {}).get('validator', {})
    except Exception:
        pass

    return render_template('validation.html',
                           active_page='validation',
                           member_validation=json.dumps(member_validation, indent=2, default=str),
                           workout_validation=json.dumps(workout_validation, indent=2, default=str))


@app.route('/validation/test', methods=['POST'])
def test_validation():
    """Test schema validation by attempting to insert a document."""
    try:
        test_type = request.form.get('test_type', 'valid')

        if test_type == 'valid':
            # Valid document that should pass validation
            test_doc = {
                'name': 'Test User',
                'email': f'test_{datetime.now().timestamp()}@gym.com',
                'phone': '9876543210',
                'age': 25,
                'gender': 'Male',
                'join_date': datetime.now(),
                'membership': {
                    'plan_name': 'Gold',
                    'start_date': datetime.now(),
                    'end_date': datetime.now() + timedelta(days=180),
                    'status': 'active'
                },
                'trainer_name': 'Test Trainer',
                'body_metrics': {
                    'height_cm': 175.0,
                    'weight_kg': 70.0,
                    'bmi': 22.9
                }
            }
            result = members_col.insert_one(test_doc)
            # Clean up
            members_col.delete_one({'_id': result.inserted_id})
            return jsonify({
                'success': True,
                'message': '✅ Document passed validation and was inserted successfully!\n\nInserted ID: ' + str(result.inserted_id) + '\n(Document was cleaned up after test)'
            })

        elif test_type == 'invalid_age':
            # Invalid: age below minimum (16)
            test_doc = {
                'name': 'Young User',
                'email': f'young_{datetime.now().timestamp()}@gym.com',
                'phone': '9876543210',
                'age': 10,  # Invalid! Must be >= 16
                'gender': 'Male',
                'join_date': datetime.now(),
                'membership': {
                    'plan_name': 'Silver',
                    'start_date': datetime.now(),
                    'end_date': datetime.now() + timedelta(days=30),
                    'status': 'active'
                },
                'trainer_name': '',
                'body_metrics': {'height_cm': 150.0, 'weight_kg': 45.0, 'bmi': 20.0}
            }
            members_col.insert_one(test_doc)
            return jsonify({
                'success': True,
                'message': '⚠️ Document was inserted (validation may not be set up yet). Run seed_data.py first.'
            })

        elif test_type == 'invalid_gender':
            # Invalid: gender not in enum
            test_doc = {
                'name': 'Alien User',
                'email': f'alien_{datetime.now().timestamp()}@gym.com',
                'phone': '9876543210',
                'age': 25,
                'gender': 'Alien',  # Invalid! Must be Male/Female/Other
                'join_date': datetime.now(),
                'membership': {
                    'plan_name': 'Gold',
                    'start_date': datetime.now(),
                    'end_date': datetime.now() + timedelta(days=180),
                    'status': 'active'
                },
                'trainer_name': '',
                'body_metrics': {'height_cm': 170.0, 'weight_kg': 65.0, 'bmi': 22.5}
            }
            members_col.insert_one(test_doc)
            return jsonify({
                'success': True,
                'message': '⚠️ Document was inserted (validation may not be set up yet). Run seed_data.py first.'
            })

        elif test_type == 'invalid_status':
            # Invalid: membership status not in enum
            test_doc = {
                'name': 'Status User',
                'email': f'status_{datetime.now().timestamp()}@gym.com',
                'phone': '9876543210',
                'age': 30,
                'gender': 'Female',
                'join_date': datetime.now(),
                'membership': {
                    'plan_name': 'Platinum',
                    'start_date': datetime.now(),
                    'end_date': datetime.now() + timedelta(days=365),
                    'status': 'paused'  # Invalid! Must be active/expired/cancelled
                },
                'trainer_name': '',
                'body_metrics': {'height_cm': 165.0, 'weight_kg': 55.0, 'bmi': 20.2}
            }
            members_col.insert_one(test_doc)
            return jsonify({
                'success': True,
                'message': '⚠️ Document was inserted (validation may not be set up yet). Run seed_data.py first.'
            })

    except WriteError as e:
        return jsonify({
            'success': False,
            'message': f'❌ Validation REJECTED the document!\n\nError: {str(e)}'
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error: {str(e)}'
        })


# ============================================================
# SEED DATABASE ROUTE
# ============================================================
@app.route('/seed')
def seed_database():
    """Redirect to run seeding."""
    flash('Please run "python seed_data.py" from the terminal to seed the database.', 'info')
    return redirect(url_for('dashboard'))


# ============================================================
# RUN THE APP
# ============================================================
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    debug_mode = os.environ.get('FLASK_DEBUG', 'False').lower() in ('true', '1')
    print("\n" + "="*55)
    print("  🏋️  GymTrack Pro — Membership & Workout Tracker")
    print("  📦  MongoDB + PyMongo | CSE494 Project")
    print(f"  🌐  Listening on http://0.0.0.0:{port}")
    print("="*55 + "\n")
    app.run(host='0.0.0.0', port=port, debug=debug_mode)
