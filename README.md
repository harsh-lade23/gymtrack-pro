# 🏋️ GymTrack Pro — Gym Membership & Workout Tracking System
> **Course:** CSE494 – Intelligent NoSQL Databases  
> **Tech Stack:** Python 3, Flask, PyMongo, MongoDB Community / Atlas, Vanilla HTML5/CSS3, Chart.js  

---

## 📌 1. Project Overview & Real-World Relevance

**GymTrack Pro** is a modern, responsive web application and NoSQL database system designed for fitness clubs and gym management. In a real-world fitness facility, gym owners and trainers need to:
1. **Manage Diverse Member Profiles:** Track membership tiers, contact details, payment statuses, and physical body metrics (BMI, height, weight).
2. **Log Granular Workout Sessions:** Record workout types (Strength, Cardio, HIIT, Yoga) along with sets, reps, and weights for each exercise.
3. **Analyze Business & Health Metrics:** Run multi-stage aggregation queries to compute total revenue, popular training regimes, most active members, trainer workloads, and monthly signups.
4. **Enforce Business Constraints:** Ensure age validity (16–80), valid email formats, and strict membership status enums using MongoDB JSON Schema Validation.
5. **Optimize Query Performance:** Use Single-field, Compound, Unique, and Text indexes to achieve sub-millisecond query execution (`IXSCAN`) instead of slow full collection scans (`COLLSCAN`).

---

## 🎯 2. Syllabus Alignment (Unit I – Unit IV)

| Unit | Syllabus Topics Covered | Implementation in GymTrack Pro |
|---|---|---|
| **Unit I** | NoSQL Intro, SQL vs NoSQL, Document Model, CAP Theorem, MongoDB Architecture | Document-oriented data modeling in MongoDB, high availability & horizontal scalability discussion, BSON documents. |
| **Unit II** | MongoDB CRUD Operations, BSON Data Types, Query Optimization | `insert_one`, `insert_many`, `find()`, `find_one()`, `update_one` (`$set`, `$push`), `update_many`, `delete_one`, `delete_many`. |
| **Unit III** | Schema Design, Embedding vs Referencing, Relationships (1:1, 1:N, N:M), Validation Rules | • **Embedded:** `exercises` array inside `workouts`; `body_metrics` and `membership` inside `members`.<br>• **Referenced:** `trainer_name` and `plan_name`.<br>• **Validation:** `$jsonSchema` rules with `validationAction: "error"`. |
| **Unit IV** | Indexing (Single, Compound, Text, Unique) & Aggregation Framework | • **Indexes:** Unique on `email`, single on `status`, compound on `(member_email, date)`, text on `name`.<br>• **Aggregations:** 6 multi-stage pipelines using `$match`, `$project`, `$group`, `$sort`, `$limit`, and `$avg/$sum/$min/$max`. |

---

## 🗄️ 3. Database & Document Schema Design

The application uses the `gym_db` database containing 4 collections:

```
gym_db
├── members      (Embeds membership subdoc & body_metrics subdoc; references trainer_name)
├── workouts     (Embeds exercises array; references member_email)
├── trainers     (Referenced master collection with text index)
└── plans        (Referenced catalog collection of pricing tiers)
```

### Why Embedding vs. Referencing was Chosen:
1. **Embedded Exercises in Workouts (1-to-Few):** An individual workout session contains 3–8 exercises. These are always retrieved, viewed, and logged together. Embedding eliminates expensive joins (`$lookup`) and ensures atomic writes.
2. **Embedded Membership in Members (1-to-1):** A member's active plan, start date, and status are core attributes retrieved on every profile lookup.
3. **Referenced Trainers (1-to-Many):** Trainers have separate salaries, certifications, and availability. Referencing `trainer_name` prevents repeating trainer details across hundreds of member documents.

---

## ⚡ 4. MongoDB Operations & Query Reference

### A. CRUD Operations
- **Create:** 
  - `members_col.insert_one(member_doc)`
  - `workouts_col.insert_one(workout_doc)`
  - `db.plans.insert_many(plans_data)`
- **Read:**
  - `members_col.find().sort('name', ASCENDING)`
  - `workouts_col.find().sort('date', DESCENDING)`
- **Update:**
  - `$set` operator: `members_col.update_one({'_id': ObjectId(id)}, {'$set': update_data})`
  - `$push` operator: `workouts_col.update_one({'_id': ObjectId(id)}, {'$push': {'exercises': exercise}})`
  - Bulk update: `members_col.update_many({'membership.end_date': {'$lt': now}, 'membership.status': 'active'}, {'$set': {'membership.status': 'expired'}})`
- **Delete:**
  - `members_col.delete_one({'_id': ObjectId(id)})`
  - Bulk delete: `workouts_col.delete_many({'date': {'$lt': one_year_ago}})`

### B. Aggregation Pipelines (6 Built-in Reports)
1. **Revenue by Plan:** `$group` by `$membership.plan_name` with `$sum: 1` → `$sort`.
2. **Average Calories by Workout:** `$group` by `$workout_type` with `$avg: '$calories_burned'` → `$sort`.
3. **Top 5 Active Members:** `$group` by `$member_name` with `$sum: 1` → `$sort: -1` → `$limit: 5`.
4. **Monthly Signups:** `$project` (`$month: '$join_date'`) → `$group` by month with `$sum: 1` → `$sort`.
5. **Trainer Workload:** `$match` (`trainer_name != ''`) → `$group` by `$trainer_name` → `$sort`.
6. **Workout Duration Stats:** `$group` with `$avg`, `$min`, `$max` duration → `$sort`.

### C. Indexes & explain()
1. `members.create_index('email', unique=True, name='idx_email_unique')`
2. `members.create_index('membership.status', name='idx_membership_status')`
3. `workouts.create_index([('member_email', 1), ('date', -1)], name='idx_member_date_compound')`
4. `workouts.create_index('workout_type', name='idx_workout_type')`
5. `trainers.create_index([('name', 'text')], name='idx_trainer_name_text')`

---

## 🚀 5. How to Run the Project (Step-by-Step)

### Prerequisites (Install when ready):
1. **Python 3.9+** ([python.org](https://www.python.org/downloads/))
2. **MongoDB Community Edition** ([mongodb.com/try/download/community](https://www.mongodb.com/try/download/community)) OR **MongoDB Atlas** free cloud cluster

### Step 1: Open Terminal in the Project Folder
```bash
cd "/Users/harsh.lade/Desktop/xyz/coll project"
```

### Step 2: Create and Activate a Virtual Environment
**On macOS / Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```
**On Windows:**
```cmd
python -m venv venv
venv\Scripts\activate
```

### Step 3: Install Required Packages
```bash
pip install -r requirements.txt
```

### Step 4: Start MongoDB
- If running locally:
  ```bash
  # macOS (Homebrew):
  brew services start mongodb-community
  
  # Or run mongod directly:
  mongod --dbpath ~/data/db
  ```
- If using MongoDB Atlas: Update line 27 in `app.py` and line 21 in `seed_data.py` with your Atlas connection string:
  ```python
  client = MongoClient('mongodb+srv://<username>:<password>@cluster0.mongodb.net/?retryWrites=true&w=majority')
  ```

### Step 5: Seed the Database with Demo Data
```bash
python seed_data.py
```
*This drops any existing database, applies `$jsonSchema` validators, creates 5 plans, 5 trainers, 18 members, 60+ workouts, and builds all 5 indexes.*

### Step 6: Start the Web Application
```bash
python app.py
```
Open your browser and navigate to: **`http://127.0.0.1:5000`**

---

## 🎤 6. Viva & Presentation Guide (Expected Q&A)

### Q1: Why did you choose MongoDB instead of a relational database like MySQL?
> **Answer:** Fitness tracker data is hierarchical and polymorphic. Workouts have variable sets of exercises with varying weights and reps. In SQL, this requires 4-5 normalized tables with foreign keys and multi-table joins. In MongoDB, document embedding provides natural, nested representation, single-read retrieval speed, and effortless horizontal scaling.

### Q2: How does MongoDB ensure data integrity if it is "schema-less"?
> **Answer:** MongoDB is schema-flexible by default, but provides `$jsonSchema` collection validators. In our project, `members` and `workouts` collections enforce required fields, data types (`bsonType`), numerical ranges (e.g. `age: {minimum: 16, maximum: 80}`), and string enums with `validationAction: "error"` so invalid writes are rejected.

### Q3: What is the difference between COLLSCAN and IXSCAN?
> **Answer:** `COLLSCAN` (Collection Scan) reads every document from disk sequentially in $O(N)$ time. `IXSCAN` (Index Scan) traverses a B-Tree index structure in $O(\log N)$ time, loading only matching index pointers. In our application's `explain()` demo, queries on email or status show execution times drop to near 0ms.

### Q4: Explain the CAP theorem in the context of MongoDB.
> **Answer:** MongoDB is fundamentally a **CP (Consistency & Partition Tolerance)** system. In a replica set, write concerns (`w: "majority"`) ensure strong consistency. If network partitions occur, the majority partition elects a primary while the minority rejects writes until reconnected, prioritizing consistency over 100% availability.

### Q5: What is the difference between $set and $push?
> **Answer:** `$set` modifies or replaces specific field values in a document without touching untouched fields. `$push` is an array update operator that appends a new element to an embedded array (used in our project to add new exercises to an existing workout session).
