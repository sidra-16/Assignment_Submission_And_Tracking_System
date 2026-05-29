# 🎓 SASTS Project — Complete Explanation

> **SASTS** = **S**tudent **A**ssignment **S**ubmission & **T**racking **S**ystem

This is a **web app** that lets you manage students, courses, assignments, and submissions — all stored in a **MongoDB** database. It demonstrates key concepts from your Advanced Database course.

---

## 📁 Project Files — What Does Each File Do?

| File | Purpose |
|---|---|
| **`app.py`** | The main application — contains all the pages, UI, and logic |
| **`db.py`** | Connects to MongoDB (just 14 lines!) |
| **`styles.py`** | CSS styling that makes the app look nice |
| **`generate_data.py`** | One-time script that creates fake/sample data as JSON files |
| **`requirements.txt`** | Lists the 3 Python libraries needed: `streamlit`, `pymongo`, `pandas` |
| **`*.json` files** | Sample data files (students, courses, etc.) imported into MongoDB |

---

## 🔌 How Does It Connect to MongoDB?

This is handled by **`db.py`** — the simplest but most important file:

```python
from pymongo import MongoClient

MONGO_URI = "mongodb://localhost:27017"   # Where MongoDB is running
DB_NAME = "assignment_db"                  # Our database name

def get_db():
    client = MongoClient(MONGO_URI)        # Open connection
    return client[DB_NAME]                 # Return the database

def get_collection(name):
    return get_db()[name]                  # Return a specific collection
```

**In simple words:**
1. `MongoClient("mongodb://localhost:27017")` — Opens a connection to MongoDB running on your computer at port 27017
2. `client["assignment_db"]` — Selects the database called `assignment_db`
3. `get_collection("students")` — Gives you access to the `students` collection (like a table in SQL)

**The `@st.cache_resource` decorator** means the connection is created **once** and reused — it doesn't reconnect every time you click something.

---

## 📦 The Data Model — 7 Collections

Think of **collections** like tables in SQL, and **documents** like rows. Here are all 7:

### 1. 👨‍🎓 Students (1000 documents)
```json
{
    "_id": 0,
    "name": "Student_0",
    "email": "student0@gmail.com",
    "department_id": 3,        ← references departments collection
    "semester_id": 5,
    "courses": [12, 45]        ← array of course IDs (EMBEDDED data)
}
```
> **Note:** `courses` is an **embedded array** — instead of a separate "enrollment" table, the course IDs are stored directly inside the student document. This is a MongoDB design pattern called **embedding**.

### 2. 👨‍🏫 Instructors (50 documents)
```json
{
    "_id": 0,
    "name": "Instructor_0",
    "email": "instructor0@uni.edu",
    "department_id": 7          ← references departments collection
}
```

### 3. 📚 Courses (100 documents)
```json
{
    "_id": 0,
    "course_name": "Course_0",
    "instructor_id": 23         ← references instructors collection
}
```

### 4. 📝 Assignments (400 documents)
```json
{
    "_id": 0,
    "title": "Assignment_0",
    "course_id": 55,            ← references courses collection
    "deadline": "2026-04-15"
}
```

### 5. 📤 Submissions (2000 documents)
```json
{
    "_id": 0,
    "student_id": 42,           ← references students (REFERENCING)
    "assignment_id": 100,       ← references assignments (REFERENCING)
    "submission_date": "2026-04-10",
    "file": {                   ← EMBEDDED document
        "file_name": "file_0.pdf",
        "file_path": "/uploads/file_0.pdf"
    },
    "grade": {                  ← EMBEDDED document
        "marks": 85
    },
    "feedback": {               ← EMBEDDED document
        "comments": "Good"
    }
}
```
> This collection shows **hybrid modeling**: `student_id` and `assignment_id` use **referencing** (like foreign keys), while `file`, `grade`, and `feedback` use **embedding** (nested objects stored directly).

### 6. 🏢 Departments (10 documents)
```json
{
    "_id": 0,
    "department_name": "Department_0"
}
```

### 7. 🔔 Notifications (300 documents)
```json
{
    "_id": 0,
    "message": "Assignment deadline approaching",
    "date": "2026-04-12",
    "student_id": 456
}
```

---

## 🔄 CRUD Operations — How Create/Read/Update/Delete Works

Every collection page has 3 tabs:

### 📋 Tab 1: Browse & Delete (READ + DELETE)
```python
docs = list(col.find())              # READ all documents from MongoDB
col.delete_one({"_id": del_id})      # DELETE one document by its _id
```
- `col.find()` → Gets ALL documents from the collection (like `SELECT * FROM table`)
- `col.delete_one({"_id": 5})` → Deletes the document where `_id` equals 5

### ➕ Tab 2: Insert New (CREATE)
```python
max_doc = col.find_one(sort=[("_id", -1)])    # Find the highest _id
vals["_id"] = max_doc["_id"] + 1               # New _id = highest + 1
col.insert_one(vals)                           # INSERT the new document
```
- First, it finds the highest existing `_id` to auto-generate the next one
- Then `col.insert_one(vals)` inserts your new document (like `INSERT INTO table`)

### ✏️ Tab 3: Update
```python
col.find_one({"_id": edit_id})                         # Load the document
col.update_one({"_id": eid}, {"$set": updates})        # Update specific fields
```
- `find_one` loads the document so you can see its current values
- `update_one` with `$set` updates only the fields you changed (not the whole document)

---

## 📊 Dashboard — How the Charts Work

The dashboard shows:

**1. Stat Cards** — One for each collection showing total document count:
```python
cnt = get_collection("students").count_documents({})   # Count all students
# {} means "no filter" = count everything
```

**2. Feedback Distribution Chart:**
```python
subs = get_collection("submissions").find({}, {"feedback.comments": 1, "_id": 0})
# {} = no filter (get all)
# {"feedback.comments": 1, "_id": 0} = PROJECTION: only return the feedback.comments field
```
This is **projection** — instead of fetching entire documents, we only fetch the `feedback.comments` field. It's faster and uses less memory.

**3. Students per Department Chart:**
```python
studs = get_collection("students").find({}, {"department_id": 1, "_id": 0})
```
Groups students by their `department_id` and counts how many are in each.

---

## 📈 Aggregation Pipelines — The Most Advanced MongoDB Feature

Aggregation is MongoDB's way of doing complex data analysis — like `GROUP BY`, `JOIN`, `AVG`, `SUM` in SQL but done through a **pipeline** (a series of stages).

### Pipeline 1: Average Marks per Assignment
```javascript
// MongoDB Shell syntax (displayed in the app):
db.submissions.aggregate([
    {$group: {_id: "$assignment_id", avg: {$avg: "$grade.marks"}}}
])
```
```python
# What actually runs (PyMongo):
col.aggregate([
    {"$group": {"_id": "$assignment_id", "avg": {"$avg": "$grade.marks"}}}
])
```
**What it does:** Groups all submissions by `assignment_id`, then calculates the average marks for each assignment.

### Pipeline 2: Top 5 Students
```python
col.aggregate([
    {"$group": {"_id": "$student_id", "total": {"$sum": "$grade.marks"}}},
    {"$sort": {"total": -1}},    # Sort by total marks, highest first
    {"$limit": 5}                 # Only return top 5
])
```
**What it does:** Sums up all marks per student → sorts descending → picks the top 5.

### Pipeline 3: Late Submissions (uses $lookup = JOIN)
```python
col.aggregate([
    {"$lookup": {                           # JOIN with assignments collection
        "from": "assignments",
        "localField": "assignment_id",
        "foreignField": "_id",
        "as": "a"
    }},
    {"$unwind": "$a"},                      # Flatten the joined array
    {"$match": {                            # Filter: submission_date > deadline
        "$expr": {"$gt": ["$submission_date", "$a.deadline"]}
    }}
])
```
**What it does:**
1. `$lookup` = JOINs submissions with assignments (like SQL JOIN)
2. `$unwind` = Converts the joined array into individual documents
3. `$match` = Filters only those where submission date is AFTER the deadline

---

## 🔄 ACID Transactions — What's Happening?

ACID stands for:
- **A**tomicity — All steps succeed, or none do (all-or-nothing)
- **C**onsistency — Database stays in a valid state
- **I**solation — Concurrent operations don't interfere
- **D**urability — Once committed, data survives crashes

### The Transaction Demo:
When you click "Execute Transaction", it does this:

```
Step 1: Check if Student ID exists in the students collection
Step 2: Check if Assignment ID exists in the assignments collection
Step 3: Insert a new submission document
Step 4: COMMIT ✅
```

If any step fails (e.g., student doesn't exist), it shows **ROLLBACK** and nothing is saved. If you check "Force failure", it intentionally fails at Step 3 to demonstrate how a rollback works.

---

## 🔒 Concurrency Control — Locking Demo

This demonstrates what happens when **multiple users** try to edit the same data at the same time.

### Optimistic Locking
**Concept:** "I'll assume nobody else is editing. If they did, I'll detect it."

```python
# Each document has a "version" field
doc = col.find_one({"_id": sub_id})
ver = doc["version"]  # e.g., version = 3

# Try to update ONLY IF version hasn't changed
result = col.update_one(
    {"_id": sub_id, "version": ver},          # Match both _id AND version
    {"$set": {"grade.marks": 95, "version": ver + 1}}  # Bump version
)

if result.matched_count == 1:
    # SUCCESS — nobody else modified it
else:
    # CONFLICT — someone else changed the version before us!
```

**When you check "Simulate conflict":** It bumps the version before your update runs, so your update finds version 4 instead of 3 and fails.

### Pessimistic Locking
**Concept:** "I'll LOCK the resource first. Nobody else can touch it until I'm done."

```python
# Acquire lock — insert a lock document
locks_col.insert_one({
    "resource_id": 0,
    "locked_by": "Admin_1",
    "expires_at": "2026-05-10T21:30:00"    # Auto-expires after 30 seconds
})

# Release lock — delete the lock document
locks_col.delete_one({"resource_id": 0, "locked_by": "Admin_1"})
```

If someone else tries to acquire a lock on the same resource, it checks if an active (non-expired) lock exists and **denies** the request.

---

## 👁 MongoDB Views — Virtual Collections

A **View** is like a saved query. It doesn't store data — it runs an aggregation pipeline every time you query it.

### Active Students View
Shows students who have at least 1 submission:
```javascript
db.createView("active_students_view", "students", [
    {$lookup: {from: "submissions", localField: "_id", foreignField: "student_id", as: "subs"}},
    {$match: {"subs.0": {$exists: true}}},     // Has at least 1 submission
    {$project: {name: 1, email: 1, totalSubs: {$size: "$subs"}}}
])
```

### Submission Summary View
Shows average marks and count per assignment:
```javascript
db.createView("submission_summary", "submissions", [
    {$group: {_id: "$assignment_id", avgMarks: {$avg: "$grade.marks"}, count: {$sum: 1}}},
    {$sort: {avgMarks: -1}}
])
```

---

## ⚡ Indexing — Making Queries Faster

Without indexes, MongoDB scans **every document** to find matches (called a **Collection Scan** — slow!). Indexes create a shortcut.

### Indexes Created:
```javascript
db.assignments.createIndex({course_id: 1, deadline: -1})   // Compound index
db.submissions.createIndex({student_id: 1})                  // Single field
db.submissions.createIndex({assignment_id: 1})               // Single field
```

### explain() Demo:
```javascript
db.submissions.find({student_id: 10}).explain("executionStats")
```
This shows HOW MongoDB executed the query — whether it used an index or did a full collection scan, how many documents it examined, etc.

### Optimization Techniques Shown:
| Technique | What it does |
|---|---|
| **Projection** | `find({}, {name:1, email:1})` — Only return fields you need, not entire documents |
| **Pagination** | `find().skip(10).limit(5)` — Load data in small pages instead of everything |
| **Hybrid Modeling** | Embed frequently-accessed data (grade, feedback), reference shared data (student_id, course_id) |

---

## 🧩 How Everything Connects — The Big Picture

```
┌─────────────────────────────────────────────────┐
│                   STREAMLIT (app.py)             │
│  ┌─────────┐  ┌──────────┐  ┌──────────────┐   │
│  │Dashboard │  │CRUD Pages│  │Advanced Demos│   │
│  │(charts)  │  │(7 colls) │  │(agg, txn,   │   │
│  │          │  │          │  │ lock, views) │   │
│  └────┬─────┘  └────┬─────┘  └──────┬───────┘   │
│       │              │               │           │
│       └──────────────┼───────────────┘           │
│                      │                           │
│              ┌───────▼───────┐                   │
│              │   db.py       │                   │
│              │ PyMongo Client│                   │
│              └───────┬───────┘                   │
└──────────────────────┼───────────────────────────┘
                       │
                       ▼
              ┌────────────────┐
              │   MongoDB      │
              │ localhost:27017│
              │                │
              │ assignment_db  │
              │ ├─ students    │
              │ ├─ instructors │
              │ ├─ courses     │
              │ ├─ assignments │
              │ ├─ submissions │
              │ ├─ departments │
              │ ├─ notifications│
              │ └─ locks       │
              └────────────────┘
```

**In simple words:** The user interacts with Streamlit (the web interface) → Streamlit calls `db.py` → `db.py` talks to MongoDB → MongoDB returns the data → Streamlit displays it.
