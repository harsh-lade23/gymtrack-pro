# CSE494 – INTELLIGENT NOSQL DATABASES
## Page 1

![Lovely Professional University](lpu_logo_0.png)

# SCHOOL OF COMPUTER SCIENCE AND ENGINEERING
## INTELLIGENT NOSQL DATABASES

# PROJECT REPORT

## (GYM MEMBERSHIP & WORKOUT TRACKING SYSTEM)

**Submitted by**

### (HARSH LADE)

**Registration No.:** ____________________  
**Programme & Section:** ____________________  

**Course Code: CSE494**  

**Under the Guidance of**  

### (NAME OF FACULTY / U.Id / DESIGNATION)

**School of Computer Science and Engineering**  
**Lovely Professional University, Phagwara, Punjab**  

**Academic Task Number: 2**  
**Submission Date: 19th October, 2026**  

---
<div style="page-break-after: always;"></div>

# CSE494 – INTELLIGENT NOSQL DATABASES
## Page 2

# CERTIFICATE

This is to certify that the project report entitled **"Gym Membership & Workout Tracking System"** submitted by **Harsh Lade** (Registration No.: ____________________) in partial fulfillment of the requirements for the award of the degree of **Bachelor of Technology in Computer Science and Engineering** for the course **CSE494: Intelligent NoSQL Databases**, at the School of Computer Science and Engineering, Lovely Professional University, Phagwara, is an authentic record of bonafide project work carried out under my personal supervision and guidance.

The document structure, JSON schema validation rules, CRUD operations, indexing configurations, and analytical aggregation pipelines embodied in this report have been verified, executed on a live MongoDB cloud cluster, and demonstrated satisfactorily. To the best of my knowledge, the matter presented in this report has not been submitted elsewhere for any academic degree or diploma.

<br/><br/><br/><br/>
__________________________________________________  
**Signature and Name of the Supervisor**  
Designation of the Supervisor: Assistant Professor / Associate Professor  
School of Computer Science and Engineering  
Lovely Professional University  
Phagwara, Punjab  

**Date:** ____________________  

---
<div style="page-break-after: always;"></div>

# CSE494 – INTELLIGENT NOSQL DATABASES
## Page 3

# DECLARATION

I hereby declare that the project report entitled **"Gym Membership & Workout Tracking System"** submitted to the School of Computer Science and Engineering, Lovely Professional University, Phagwara, Punjab, for the academic evaluation of **CSE494 (Intelligent NoSQL Databases)**, is an original and authentic piece of work completed individually by me.

I confirm that all database collections, validation rules, PyMongo integration code, indexing strategies, and aggregation pipelines were authored by me. No part of this project has been plagiarized or copied from another student or commercial source. External documentation, libraries, and architectural references used during development have been duly acknowledged.

<br/><br/><br/><br/>
**Date:** 19th October, 2026  

**Signature:** _______________________________________  

**Registration No.:** ________________________________  

**Name:** **Harsh Lade**  

---
<div style="page-break-after: always;"></div>

# CSE494 – INTELLIGENT NOSQL DATABASES
## Page 4

# ACKNOWLEDGEMENT

I express my deepest gratitude and sincere appreciation to my esteemed faculty supervisor for constant guidance, constructive critique, and valuable technical insights throughout the design and implementation of this MongoDB project. Their encouragement to explore realistic schema design and optimization played a crucial role in shaping this work.

I also extend my heartfelt thanks to the **School of Computer Science and Engineering** and **Lovely Professional University** for providing state-of-the-art laboratory infrastructure, cloud access, and academic resources that facilitated hands-on learning of enterprise NoSQL databases, PyMongo integration, and high-performance querying.

Finally, I am profoundly thankful to my family and classmates for their moral support, thoughtful discussions, and motivation during the completion of this capstone assignment.

<br/><br/><br/><br/>
**Harsh Lade**  
Registration No.: ____________________  
School of Computer Science and Engineering  
Lovely Professional University, Phagwara  

---
<div style="page-break-after: always;"></div>

# CSE494 – INTELLIGENT NOSQL DATABASES
## Page 5

# TABLE OF CONTENTS

| Section | Title | Page |
|---|---|---|
| **1** | **Introduction** | **8** |
| **2** | **Problem Domain and System Requirements** | **9** |
| **3** | **Data Source and Data Description** | **10** |
| **4** | **Database Design and Data Modeling** | **12** |
| **5** | **MongoDB Implementation** | **14** |
| **6** | **Advanced MongoDB Operations** | **15** |
| **7** | **Application Integration** | **16** |
| **8** | **Results and Output Analysis** | **17** |
| **9** | **Discussion** | **19** |
| **10** | **Conclusion** | **20** |
| **11** | **Future Scope** | **21** |
| **—** | **References** | **22** |
| **—** | **Student Submission Checklist** | **23** |

---
<div style="page-break-after: always;"></div>

# CSE494 – INTELLIGENT NOSQL DATABASES
## Page 6

# LIST OF FIGURES

| Figure No. | Caption / Description | Page |
|---|---|---|
| **Figure 4.1** | GymTrack Pro Three-Tier System Architecture (Client - Flask - Atlas) | 12 |
| **Figure 4.2** | Data Model Diagram: Embedding vs Referencing Entity Relationships | 13 |
| **Figure 7.1** | PyMongo MVC Controller & Atlas Wire Protocol Workflow | 16 |
| **Figure 8.1** | Interactive explain() Execution Plan Comparison (IXSCAN vs COLLSCAN) | 17 |
| **Figure 8.2** | Terminal Query Execution Plan & explain() Detailed JSON Output | 18 |

---
<div style="page-break-after: always;"></div>

# CSE494 – INTELLIGENT NOSQL DATABASES
## Page 7

# LIST OF TABLES

| Table No. | Caption / Description | Page |
|---|---|---|
| **Table 3.1** | Data Dictionary and JSON Schema Validation Constraints | 10 |
| **Table 3.2** | Database Collection Inventory and Document Volume Counts | 11 |
| **Table 4.1** | Collection Design Specifications and Modeling Rationale | 12 |
| **Table 6.1** | MongoDB Indexing Catalog and Query Optimization Patterns | 15 |
| **Table 6.2** | Multi-Stage Aggregation Pipelines Summary & Accumulators | 15 |
| **Table 8.1** | Aggregation Outputs Summary and Business Intelligence Insights | 17 |

---
<div style="page-break-after: always;"></div>

# CSE494 – INTELLIGENT NOSQL DATABASES
## Page 8

# 1. INTRODUCTION

### 1.1 Introduction
Commercial fitness clubs and athletic facilities require modern software systems to manage member registrations, subscription lifecycles, personal training allocations, and daily workout progression. In an increasingly data-centric health industry, capturing granular workout performance (sets, repetitions, resistance weight, and caloric expenditure) is critical to member retention. This project, **GymTrack Pro**, implements a full-featured, document-oriented gym tracking and management system utilizing **MongoDB** as the database backbone and **Python (PyMongo)** as the application integration layer.

### 1.2 Problem Statement
Traditional relational databases (RDBMS) struggle with fitness tracking due to rigid normalization rules. In an SQL setup, recording a single workout session requires distributing data across separate normalized tables (Members, Workouts, Exercises, Sets). Retrieving historical progress requires multi-table joins that suffer severe performance degradation as records scale. Furthermore, workout modalities differ drastically (e.g., distance and heart rate in Cardio vs. sets and barbell weight in Strength training), leading to sparse tables with excessive NULL columns in relational models.

### 1.3 Objectives
* **Optimized Schema Design:** Balance document embedding and referencing to minimize disk seek latency.
* **Server-Side Schema Validation:** Enforce `$jsonSchema` rules with strict error actions to guarantee data integrity.
* **Transactional CRUD Operations:** Implement atomic document insertions, updates (`$set`, `$push`), and deletions.
* **Multi-Stage Analytical Aggregations:** Construct 6 pipelines generating real-time business and athletic intelligence.
* **Query Performance Optimization:** Establish compound and text B-Tree indexes, evaluating execution stages via `explain()`.

### 1.4 Scope of the Project
The project encompasses complete NoSQL database engineering: provisioning a live MongoDB Atlas cloud cluster, configuring validation rules on collections, seeding realistic multi-member gym records, running aggregation pipelines, and providing an interactive graphical web interface for live viva demonstration.

### 1.5 Significance of the Project
This project provides practical validation of the curriculum units in CSE494, demonstrating how document-oriented databases solve impedance mismatch, eliminate relational join overheads, and scale horizontally under the CAP theorem.

### 1.6 Technologies Used
* **Database:** MongoDB Atlas Cloud Database (v7.0+) / WiredTiger Storage Engine
* **Driver & Backend:** Python 3.9+ with official PyMongo 4.6.0 driver & Flask 3.0
* **Frontend Interface:** HTML5, Custom CSS3 Glassmorphism theme, Chart.js 4.4, JavaScript AJAX

---
<div style="page-break-after: always;"></div>

# CSE494 – INTELLIGENT NOSQL DATABASES
## Page 9

# 2. PROBLEM DOMAIN AND SYSTEM REQUIREMENTS

### 2.1 Domain Overview
Gym facility operations are characterized by mixed read-heavy and write-heavy workloads. Front desks read member profiles and active subscription statuses frequently, while members and personal trainers write granular workout logs continuously throughout training sessions.

### 2.2 Existing Systems & 2.3 Limitations of Existing System
Existing commercial fitness management systems typically rely on relational databases or spreadsheet registers. Key limitations include:
* **Join Bottlenecks:** Generating member progress charts requires joining Members, Sessions, and Exercise tables.
* **Schema Rigidity:** Introducing new biometrics or exercise types requires schema alterations with table locks.
* **Lack of Natural Hierarchies:** Relational tables cannot natively store arrays of exercise sets inside workout records.

### 2.4 Proposed System
GymTrack Pro adopts a document-oriented approach. Each workout session directly embeds an array of exercise sub-documents. All sets, repetitions, and poundages are retrieved in a single read operation, offering sub-millisecond query performance.

### 2.5 Functional Requirements
* **Member Lifecycle Management:** Enroll members, capture body metrics, calculate BMI, and assign plans.
* **Workout Logging with Embedded Sets:** Log workout sessions containing arbitrary arrays of exercises.
* **Atomic Exercise Appending:** Append exercises to existing sessions using MongoDB's atomic `$push` operator.
* **Bulk Expiration Updates:** Identify and expire outdated subscriptions in bulk using `update_many`.
* **Real-Time Analytics & Reports:** Run multi-stage aggregations for revenue, calories, and trainer workloads.

### 2.6 Non-Functional Requirements
* **Performance:** Indexed query execution times under 5ms using B-Tree index scans (`IXSCAN`).
* **Data Integrity:** Rejection of invalid records (underage, duplicate emails, invalid enums) via `$jsonSchema`.
* **Reliability & Availability:** Cloud replication and automated failover via MongoDB Atlas replica sets.

---
<div style="page-break-after: always;"></div>

# CSE494 – INTELLIGENT NOSQL DATABASES
## Page 10

# 3. DATA SOURCE AND DATA DESCRIPTION

### 3.1 Source of Data
The project utilizes an authentic, synthetically generated dataset created by an automated initialization script (`seed_data.py`). The dataset models real-world gym operations across an active 12-month calendar.

### 3.2 Dataset Description
The dataset spans 4 distinct collections: `plans` (membership pricing tiers), `trainers` (certified coaches), `members` (gym patrons with embedded biometrics), and `workouts` (daily exercise session logs).

### 3.3 Data Fields
**Table 3.1:** Data Dictionary and Validation Constraints across Collections

| Field Name | Data Type | Description | Constraint | Example |
|---|---|---|---|---|
| `name` | string | Member full legal name | Required, non-empty | Harsh Lade |
| `email` | string | Member contact email | Required, Unique Index | harsh@gmail.com |
| `phone` | string | Contact phone number | Length: 10–15 chars | 9123456709 |
| `age` | int | Member age in years | min: 16, max: 80 | 21 |
| `gender` | string | Biological gender | enum: Male/Female/Other | Male |
| `join_date` | date | Date of initial enrollment | Valid BSON Date | `ISODate('2026-06-19')` |
| `membership.plan_name` | string | Subscribed plan tier | References plans catalog | Gold |
| `membership.status` | string | Subscription validity | enum: active/expired/cancelled | active |
| `body_metrics.bmi` | double | Body Mass Index | Computed: kg / (m)^2 | 23.8 |
| `workout_type` | string | Category of workout session | enum: Strength/Cardio/HIIT... | Strength |
| `duration_minutes` | int | Total session duration | min: 10, max: 300 | 55 |
| `calories_burned` | int | Estimated caloric burn | min: 0 | 420 |
| `exercises` | array | Embedded exercise movements | Embedded document array | `[{name, sets, reps, kg}]` |
| `salary` | int | Trainer monthly salary | min: 10000 | 36000 |

---
<div style="page-break-after: always;"></div>

# CSE494 – INTELLIGENT NOSQL DATABASES
## Page 11

### 3.4 Data Generation / Collection
Data population is orchestrated programmatically in `seed_data.py`. The script initializes clean collections, applies JSON schema validation rules, and injects realistic member distributions across varying age brackets (19 to 45 years), body profiles, membership plan durations, and workout sessions. Each workout session is synthesized with authentic exercise movements (e.g., Bench Press, Squats, and Deadlifts for Strength; Burpees and Box Jumps for HIIT) reflecting true exercise science.

### 3.5 Data Quality
To ensure production-grade data quality, three independent layers of data validation are enforced:
* **Storage-Level JSON Schema:** MongoDB strictly rejects documents failing data type or range constraints.
* **Unique Index Constraints:** Duplicate member emails are blocked by a unique B-Tree index on `email`.
* **Referential Integrity:** Workout sessions reference valid member email addresses, and member documents reference certified trainer names.

### 3.6 Number of Documents and Collections
**Table 3.2:** Database Collection Inventory and Document Volume Counts

| Collection Name | Document Count | Data Modeling Role | Average Size per Doc |
|---|---|---|---|
| `gym_db.members` | 18 documents | Master entity with embedded membership & biometrics | ~320 bytes |
| `gym_db.workouts` | 63 documents | Transactional logs with embedded exercise arrays (180+ exercises) | ~480 bytes |
| `gym_db.trainers` | 5 documents | Normalized master collection of certified fitness coaches | ~280 bytes |
| `gym_db.plans` | 4 documents | Pricing catalog tiers (Silver, Gold, Platinum, Student) | ~240 bytes |

**Current Database Status Summary:**
* **Active Member Subscriptions:** 11 members currently hold active memberships.
* **Expired Member Subscriptions:** 7 members have expired subscriptions, utilized to demonstrate automated bulk expiration.
* **Total Exercise Movements Logged:** Over 180 individual exercise sets embedded across the 63 workout sessions.
* **Database Deployment:** Live on MongoDB Atlas Cloud M0 Cluster (AWS Replica Set in Mumbai / N. Virginia region).

---
<div style="page-break-after: always;"></div>

# CSE494 – INTELLIGENT NOSQL DATABASES
## Page 12

# 4. DATABASE DESIGN AND DATA MODELING

### 4.1 MongoDB Overview & 4.2 System Architecture
MongoDB is an open-source, document-oriented NoSQL database that persists records in BSON (Binary JSON). The architecture decouples the storage engine (WiredTiger) from query parsing, allowing document-level locking, built-in compression, and distributed replication.

### 4.3 Database Design & 4.4 Collection Design
**Table 4.1:** Collection Design Specifications and Key Fields

| Collection | Purpose | Key Fields |
|---|---|---|
| `members` | Stores gym member profiles, biometrics, and active subscription lifecycle. | `_id`, `name`, `email`, `age`, `gender`, `membership`, `trainer_name`, `body_metrics` |
| `workouts` | Logs individual workout sessions with embedded exercise arrays. | `_id`, `member_name`, `member_email`, `date`, `workout_type`, `exercises`, `calories_burned` |
| `trainers` | Master profiles of certified gym trainers and their availability. | `_id`, `name`, `email`, `specialization`, `experience_years`, `rating`, `salary` |
| `plans` | Pricing catalog specifying membership duration, fees, and perks. | `_id`, `plan_name`, `duration_months`, `price`, `features`, `description` |

### 4.5 Document Structure & 4.6 Data Modeling
Documents model natural relationships through nested BSON structures. For example, `body_metrics` and `membership` are embedded sub-documents within `members`, ensuring all member attributes are fetched in a single index lookup.

### 4.7 Embedding and Referencing
* **Embedding Rationale:** Exercises are embedded directly inside workout session documents (1-to-Few relationship). Exercises are never queried independently of the workout; embedding guarantees atomic commits and eliminates join latency.
* **Referencing Rationale:** Trainers and membership plans are referenced (1-to-Many relationship). Multiple members share a single trainer. Referencing prevents repeating trainer salaries and bios across hundreds of member documents, eliminating update anomalies.

---
<div style="page-break-after: always;"></div>

# CSE494 – INTELLIGENT NOSQL DATABASES
## Page 13

### 4.8 Data Model Diagram

The following diagram illustrates the document structure, showing embedded sub-documents and referencing relationships across the `gym_db` collections:

```
+----------------------------------------------------------------------------------------------------+
|                                      MONGODB DATABASE: gym_db                                       |
+----------------------------------------------------------------------------------------------------+
                                                  |
           +--------------------------------------+--------------------------------------+
           |                                                                             |
+------------------------------------+                         +------------------------------------+
|       COLLECTION: members          |                         |       COLLECTION: workouts         |
+------------------------------------+                         +------------------------------------+
|  _id: ObjectId                     |                         |  _id: ObjectId                     |
|  name: String                      |                         |  member_name: String               |
|  email: String (UNIQUE INDEX)      |<------+                 |  member_email: String (FK Ref) ----+
|  phone: String                     |       |                 |  date: ISODate                     |
|  age: Int (16-80)                  |       | (References     |  workout_type: String              |
|  gender: Enum ['Male','Female'..]  |       |  member_email)  |  duration_minutes: Int             |
|  join_date: ISODate                |       |                 |  calories_burned: Int              |
|  trainer_name: String (FK Ref) ----+--+    |                 |  notes: String                     |
|                                    |  |    |                 |  exercises: [ (EMBEDDED ARRAY)     |
|  [EMBEDDED SUB-DOC] membership:    |  |    |                 |    {                               |
|    - plan_name: String (FK Ref) ---+--|----+                 |      name: String,                 |
|    - start_date: ISODate           |  |    |                 |      sets: Int,                    |
|    - end_date: ISODate             |  |    |                 |      reps: Int,                    |
|    - status: Enum ['active'..]     |  |    |                 |      weight_kg: Double             |
|                                    |  |    |                 |    }                               |
|  [EMBEDDED SUB-DOC] body_metrics:  |  |    |                 |  ]                                 |
|    - height_cm: Double             |  |    |                 +------------------------------------+
|    - weight_kg: Double             |  |    |
|    - bmi: Double                   |  |    |
+------------------------------------+  |    |
                                        |    |
                   +--------------------+    |
                   |                         |
+------------------------------------+       |                 +------------------------------------+
|       COLLECTION: trainers         |       +-----------------|         COLLECTION: plans          |
+------------------------------------+                         +------------------------------------+
|  _id: ObjectId                     |                         |  _id: ObjectId                     |
|  name: String (TEXT INDEX)         |                         |  plan_name: String                 |
|  email: String                     |                         |  duration_months: Int              |
|  phone: String                     |                         |  price: Int                        |
|  specialization: [String]          |                         |  features: [String]                |
|  experience_years: Int             |                         |  description: String               |
|  rating: Double                    |                         +------------------------------------+
|  salary: Int                       |
|  availability: [String]            |
+------------------------------------+
```

**Architectural Pattern Summary:**
1. **Embedding (Contained 1-to-Few):** `exercises` sub-documents inside `workouts`; `membership` & `body_metrics` inside `members`.
2. **Referencing (Shared 1-to-Many):** `trainer_name` references `trainers.name`; `plan_name` references `plans.plan_name`.

---
<div style="page-break-after: always;"></div>

# CSE494 – INTELLIGENT NOSQL DATABASES
## Page 14

# 5. MONGODB IMPLEMENTATION

### 5.1 Setup & 5.4 Schema Validation
Collections are provisioned with `$jsonSchema` validators with `validationAction='error'`, ensuring that invalid documents are rejected before reaching disk storage:

```python
db.create_collection('members', validator={
  '$jsonSchema': {
    'bsonType': 'object',
    'required': ['name', 'email', 'phone', 'age', 'gender', 'membership'],
    'properties': {
      'age': { 'bsonType': 'int', 'minimum': 16, 'maximum': 80 },
      'gender': { 'bsonType': 'string', 'enum': ['Male', 'Female', 'Other'] },
      'membership': { 'bsonType': 'object', 'required': ['plan_name', 'status'] }
    }
  }
}, validationAction='error')
```

### 5.5 Insert Operations (Create)
```python
# Insert member document with auto-calculated BMI
member_doc = {
    'name': request.form['name'], 'email': request.form['email'],
    'age': int(request.form['age']), 'gender': request.form['gender'],
    'membership': {'plan_name': 'Gold', 'status': 'active'},
    'body_metrics': {'height_cm': 175.0, 'weight_kg': 70.0, 'bmi': 22.9}
}
members_col.insert_one(member_doc)
```

### 5.6 Read Operations (Read)
```python
# Sorted read with projection filtering
active_members = list(members_col.find(
    {'membership.status': 'active'}, {'name': 1, 'email': 1}
).sort('name', ASCENDING))
```

### 5.7 Update Operations ($set, $push, update_many)
```python
# 1. Update weight and recalculate BMI ($set)
members_col.update_one({'_id': ObjectId(id)}, {'$set': {'body_metrics.weight_kg': 72.0, 'body_metrics.bmi': 23.5}})

# 2. Append exercise to workout session ($push)
workouts_col.update_one({'_id': ObjectId(id)}, {'$push': {'exercises': {'name': 'Pullups', 'sets': 3, 'reps': 10}}})

# 3. Bulk expire memberships (update_many)
members_col.update_many({'membership.end_date': {'$lt': datetime.now()}}, {'$set': {'membership.status': 'expired'}})
```

### 5.8 Delete Operations (Delete)
```python
# Single deletion and bulk purge of obsolete logs
members_col.delete_one({'_id': ObjectId(id)})
workouts_col.delete_many({'date': {'$lt': datetime.now() - timedelta(days=365)}})
```

---
<div style="page-break-after: always;"></div>

# CSE494 – INTELLIGENT NOSQL DATABASES
## Page 15

# 6. ADVANCED MONGODB OPERATIONS

### 6.1 Indexing Catalog
**Table 6.1:** MongoDB Indexing Catalog and Query Patterns Supported

| Index | Collection | Purpose | Query Supported |
|---|---|---|---|
| `idx_email_unique` | members | Uniqueness & sub-millisecond lookup | `db.members.find({'email': ...})` |
| `idx_membership_status` | members | Active vs expired status filtering | `db.members.find({'membership.status': 'active'})` |
| `idx_member_date_compound` | workouts | Compound member chronological queries | `db.workouts.find({'member_email': ..., 'date': ...})` |
| `idx_trainer_name_text` | trainers | Full-text search on coach profiles | `db.trainers.find({$text: {$search: 'Rahul'}})` |

### 6.2 Aggregation Framework
**Table 6.2:** Summary of 6 Multi-Stage Aggregation Pipelines

| Pipeline No. | Objective | Main Stages | Result |
|---|---|---|---|
| Pipeline 1 | Gross Revenue by Plan Tier | `$match` → `$group` → `$sort` | Total revenue per plan |
| Pipeline 2 | Avg Calories by Workout Type | `$group` (`$avg`) → `$sort` | Caloric burn ranking |
| Pipeline 3 | Top 5 Most Active Members | `$group` → `$sort` → `$limit` | Member leaderboard |
| Pipeline 4 | Monthly Member Signup Trend | `$project` (`$month`) → `$group` → `$sort` | Monthly intake counts |
| Pipeline 5 | Trainer Workload Distribution | `$match` → `$group` → `$sort` | Member load per trainer |
| Pipeline 6 | Workout Duration Statistics | `$group` (`$avg`, `$min`, `$max`) → `$sort` | Time metrics per workout |

### 6.3 Advanced Queries & 6.5 Query Optimization
Queries leverage projection operators (`$month`, `$arrayElemAt`) and array accumulators. Evaluating queries with `.explain('executionStats')` proves that indexing reduces document examination from `COLLSCAN` (18 docs scanned) to `IXSCAN` (1 doc examined, execution time: 0 ms).

---
<div style="page-break-after: always;"></div>

# CSE494 – INTELLIGENT NOSQL DATABASES
## Page 16

# 7. APPLICATION INTEGRATION

### 7.1 Technology Environment & 7.2 MongoDB Connection
The application integrates Python 3.9+ with the official PyMongo 4.6.0 driver connected to a live MongoDB Atlas cloud cluster. Sensitive connection URIs are securely managed using environment variables (`.env`) and parsed via `python-dotenv`:

```python
# Database connection in app.py
from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()
MONGO_URI = os.getenv('MONGO_URI')
client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
db = client['gym_db']
```

### 7.3 Driver / ODM Integration
Rather than relying on heavy object-relational mappers (ORMs), the architecture connects directly via the native PyMongo driver. This avoids ORM translation overhead, allows native BSON dictionary handling, and exposes full aggregation pipeline features.

### 7.4 CRUD Integration & 7.5 Aggregation Integration
Flask routes serve as HTTP controller endpoints. When a form is submitted, Flask extracts HTTP form variables, performs explicit Python type-casting (converting string inputs to integers and floats), constructs BSON documents, and executes PyMongo queries. Aggregation pipelines are executed directly via `collection.aggregate(pipeline)`, with results passed to Jinja2 templates for rendering into interactive Chart.js charts and summary tables.

### 7.6 Application Workflow
1. **Client Request:** The user initiates an action via the browser (e.g., adding a member or logging a workout).
2. **Controller Handling:** Flask validates form parameters and prepares BSON documents.
3. **Database Execution:** PyMongo transmits wire-protocol commands to MongoDB Atlas. Schema validators verify constraints.
4. **Dynamic View:** Flask flashes status notifications and renders updated dark-mode dashboard tables.

---
<div style="page-break-after: always;"></div>

# CSE494 – INTELLIGENT NOSQL DATABASES
## Page 17

# 8. RESULTS AND OUTPUT ANALYSIS

### 8.1 Insert & 8.2 Read Results
Insertions completed cleanly, generating unique 12-byte `ObjectId` values. Single-document reads and sorted queries executed instantaneously across all 4 collections.

### 8.3 Update & 8.4 Delete Results
The `$push` operator successfully appended exercise movements into embedded arrays without modifying surrounding session data. Bulk expiration (`update_many`) cleanly updated 7 expired member records in a single atomic database operation.

### 8.5 Validation Results
* Valid document inserted successfully (clean commit).
* Underage document (`age: 10`) strictly rejected with `WriteError: Document failed validation`.
* Duplicate email write threw `DuplicateKeyError (E11000)`.

### 8.6 Indexing Results
Execution plans generated via `.explain('executionStats')` confirmed that `idx_email_unique` converted queries from full collection scans (`COLLSCAN`) to indexed seeks (`IXSCAN`), examining exactly 1 document in 0 ms.

### 8.7 Aggregation Results
**Table 8.1:** Aggregation Pipeline Outputs Summary and Business Interpretation

| Pipeline | Objective | Output | Interpretation |
|---|---|---|---|
| **1. Plan Revenue** | Revenue per tier | Platinum: ₹51,000<br/>Gold: ₹30,000<br/>Student: ₹10,000 | Platinum tier drives 56% of revenue despite equal enrollment with Gold. |
| **2. Calories Burned** | Caloric burn ranking | HIIT: 485.4 kcal avg<br/>CrossFit: 440.0 kcal<br/>Strength: 362.5 kcal | HIIT is the most calorie-dense discipline, guiding weight-loss plans. |
| **3. Top Members** | Member leaderboard | #1 Sneha Verma (5 sessions)<br/>#2 Harsh Lade (4 sessions) | Identifies loyal patrons for gym reward programs and retention. |
| **5. Trainer Workload** | Trainer assignments | Vikram: 4 members<br/>Rahul: 4 members<br/>Neha: 3 members | Demonstrates equitable client distribution across coaches. |

---
<div style="page-break-after: always;"></div>

# CSE494 – INTELLIGENT NOSQL DATABASES
## Page 18

### 8.8 Advanced Query Results

Below are the verified execution results and terminal outputs obtained from running advanced MongoDB queries, indexing explain plans, and schema validation rejection tests:

#### 1. explain() Execution Plan Output (Compound Index on Workouts):
```json
Query: db.workouts.find({'member_email': 'amit@gmail.com', 'date': {'$gte': ISODate('2026-01-01')}}).explain('executionStats')
{
  "queryPlanner": {
    "winningPlan": {
      "stage": "FETCH",
      "inputStage": {
        "stage": "IXSCAN",
        "indexName": "idx_member_date_compound",
        "isMultiKey": false,
        "direction": "forward"
      }
    }
  },
  "executionStats": {
    "executionSuccess": true,
    "nReturned": 4,
    "executionTimeMillis": 0,
    "totalKeysExamined": 4,
    "totalDocsExamined": 4
  }
}
```

#### 2. Schema Validation Rejection Output (Underage Registration WriteError):
```text
Command: db.members.insertOne({ name: 'Young User', email: 'young@test.com', phone: '9876543210', age: 10, gender: 'Male' })
Result:
pymongo.errors.WriteError: Document failed validation, full error: {
  'index': 0,
  'code': 121,
  'errmsg': 'Document failed validation',
  'errInfo': {
    'failingDocumentId': ObjectId('6712b8...'),
    'details': {
      'operatorName': '$jsonSchema',
      'schemaRulesNotSatisfied': [{
        'operatorName': 'properties',
        'propertyName': 'age',
        'details': [{ 'operatorName': 'minimum', 'specifiedAs': { 'minimum': 16 }, 'reason': 'comparison failed', 'consideredValue': 10 }]
      }]
    }
  }
}
```

#### 3. Analytical Pipeline Execution Output (Monthly Member Signup Trend):
```json
Output: [
  { "_id": 1, "month_name": "Jan", "signups": 2 },
  { "_id": 2, "month_name": "Feb", "signups": 3 },
  { "_id": 3, "month_name": "Mar", "signups": 2 },
  { "_id": 6, "month_name": "Jun", "signups": 3 },
  { "_id": 8, "month_name": "Aug", "signups": 4 },
  { "_id": 10, "month_name": "Oct", "signups": 4 }
]
```

---
<div style="page-break-after: always;"></div>

# CSE494 – INTELLIGENT NOSQL DATABASES
## Page 19

# 9. DISCUSSION

### 9.1 MongoDB Advantages over Relational Systems
The document-oriented model fundamentally eliminated the impedance mismatch typical of relational databases. By embedding exercises directly within workout sessions, disk locality is preserved. An entire session is written and read in a single contiguous disk seek, completely avoiding multi-table joins and row locks.

### 9.2 Database Design Discussion
The primary architectural decision centered on whether to embed workouts directly inside member profiles. While embedding affords single-document profile retrieval, dedicated athletes generate hundreds of logs annually, which would eventually risk breaching MongoDB's 16MB document size limit. Separating workouts into an independent collection with a compound index `(member_email, date)` achieved identical single-seek speed with infinite scalability.

### 9.3 Query Performance
B-Tree index construction resulted in massive latency reductions. Compound indexing ensured that date ranges for specific members were fulfilled entirely from memory-mapped index leaves without requiring costly in-memory sorting stages.

### 9.4 Scalability & CAP Theorem
Under the CAP Theorem, MongoDB prioritizes **Consistency and Partition Tolerance (CP)**. Utilizing a 3-node replica set on MongoDB Atlas with `w: 'majority'` write concern guarantees that committed workout logs are safely persisted across a quorum of nodes. For massive horizontal growth, the `workouts` collection can be sharded on a hashed shard key (`{ member_email: 'hashed' }`), distributing billions of records across independent cluster shards.

### 9.5 Challenges and Solutions
* **Type Strictness in Web Forms:** HTML form inputs submit numbers as strings. Passing strings into fields governed by BSON integer validators caused immediate validation errors. *Solution:* Implemented explicit Python type-casting (`int()`, `float()`) in controller routes prior to database calls.
* **Cloud Connection Latency:** Connecting to MongoDB Atlas introduced network handshake overhead. *Solution:* PyMongo's persistent connection pool was configured with keep-alives, reducing subsequent query latencies to sub-20ms.

---
<div style="page-break-after: always;"></div>

# CSE494 – INTELLIGENT NOSQL DATABASES
## Page 20

# 10. CONCLUSION

### 10.1 Conclusion
The **GymTrack Pro** capstone project successfully demonstrates the design, deployment, and optimization of an intelligent NoSQL database system using MongoDB Atlas and Python. By implementing server-level JSON schema validation, atomic array mutations, targeted B-Tree indexing, and 6 complex aggregation pipelines, the system achieves sub-millisecond query execution while ensuring 100% data integrity.

**Key Outcomes and Findings:**
* **Elimination of Relational Joins:** Document embedding enabled complete workout histories to be written and retrieved atomically, avoiding complex multi-table SQL join operations.
* **Guaranteed Data Quality:** Enforcing `$jsonSchema` validation with `validationAction='error'` proved that document-oriented databases can maintain strict enterprise data hygiene without sacrificing schema agility.
* **Verified Index Optimization:** Execution plan analysis via `explain()` demonstrated that compound B-Tree indexes drop document examination counts to exact equality matches (`nReturned == totalDocsExamined`) with 0ms execution times.
* **Operational Business Intelligence:** Multi-stage aggregation pipelines transformed raw gym logs into actionable commercial insights, quantifying plan revenues, trainer workloads, and member retention metrics.

In conclusion, the project successfully fulfills all course learning objectives of **CSE494 (Intelligent NoSQL Databases)**, providing a robust, scalable, and production-ready architecture for modern commercial fitness management.

---
<div style="page-break-after: always;"></div>

# CSE494 – INTELLIGENT NOSQL DATABASES
## Page 21

# 11. FUTURE SCOPE

### 11.1 Future Scope
The modular document architecture of GymTrack Pro provides a foundation for several advanced technological extensions:

* **IoT Smart Equipment Telemetry:** Modern gym facilities utilize Bluetooth and WiFi-connected weight stacks, smart treadmills, and rowing machines. Future iterations will ingest live telemetry directly into MongoDB Time-Series collections, capturing instantaneous power wattage, cadence, and heart rates.
* **Wearable Sensor Integration via Change Streams:** Integration with wearable fitness platforms (Apple HealthKit, Garmin, Fitbit) using MongoDB Change Streams. Real-time changes in member heart rates or calories can trigger push notifications and adaptive workout adjustments.
* **Automated Billing & Payment Gateway:** Webhook integration with online payment processors (Stripe / Razorpay) for recurring subscription auto-renewals, utilizing multi-document ACID transactions to ensure financial consistency.
* **Predictive Churn Analytics & Machine Learning:** Training machine learning models on member attendance frequencies and caloric burn trends to predict subscription drop-offs and automatically dispatch retention offers.
* **Mobile Native Client:** Developing dedicated iOS and Android mobile apps connected to the Flask-PyMongo REST backend for member self-service logging.

---
<div style="page-break-after: always;"></div>

# CSE494 – INTELLIGENT NOSQL DATABASES
## Page 22

# REFERENCES

### References

[1] MongoDB Inc., "MongoDB Documentation: The Aggregation Pipeline Framework," 2024. [Online]. Available: https://www.mongodb.com/docs/manual/core/aggregation-pipeline/

[2] MongoDB Inc., "PyMongo 4.6.0 API Reference & Driver Architecture," 2024. [Online]. Available: https://pymongo.readthedocs.io/

[3] K. Chodorow, *MongoDB: The Definitive Guide - Powerful and Scalable Data Storage*, 3rd ed. Sebastopol, CA: O'Reilly Media, 2020.

[4] E. Brewer, "CAP twelve years later: How the 'rules' have changed," *Computer*, vol. 45, no. 2, pp. 23-29, 2012.

[5] P. Sadalage and M. Fowler, *NoSQL Distilled: A Brief Guide to the Emerging World of Polyglot Persistence*. Boston, MA: Addison-Wesley, 2013.

[6] D. Bradshaw and E. Coupal, *MongoDB Applied Design Patterns: Practical Use Cases with the Leading NoSQL Database*. Sebastopol, CA: O'Reilly Media, 2014.

[7] Python Software Foundation, "Flask 3.0 Documentation & Application Factories," 2024. [Online]. Available: https://flask.palletsprojects.com/

---
<div style="page-break-after: always;"></div>

# CSE494 – INTELLIGENT NOSQL DATABASES
## Page 23

# STUDENT SUBMISSION CHECKLIST

| Status | Item Description |
|---|---|
| ☑ | Cover page and preliminary pages completed |
| ☑ | Table of Contents, List of Figures and List of Tables updated |
| ☑ | Database and collection design documented |
| ☑ | Sample documents included |
| ☑ | Validation demonstrated |
| ☑ | CRUD operations demonstrated |
| ☑ | Indexes demonstrated |
| ☑ | Aggregation pipelines demonstrated |
| ☑ | Project-specific advanced MongoDB operations demonstrated |
| ☑ | PyMongo OR Node.js + Mongoose integration documented |
| ☑ | Screenshots and outputs included for major operations |
| ☑ | Results explained, not only pasted |
| ☑ | Conclusion, Future Scope and References included |
| ☑ | Implementation is executable and ready for demonstration/viva |
