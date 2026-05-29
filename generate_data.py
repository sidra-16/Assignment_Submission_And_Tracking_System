import json
import random

# ------------------ DEPARTMENTS ------------------
departments = []
for i in range(10):
    departments.append({
        "_id": i,
        "department_name": f"Department_{i}"
    })

with open("departments.json", "w") as f:
    json.dump(departments, f, indent=4)


# ------------------ INSTRUCTORS ------------------
instructors = []
for i in range(50):
    instructors.append({
        "_id": i,
        "name": f"Instructor_{i}",
        "email": f"instructor{i}@uni.edu",
        "department_id": random.randint(0,9)
    })

with open("instructors.json", "w") as f:
    json.dump(instructors, f, indent=4)


# ------------------ COURSES ------------------
courses = []
for i in range(100):
    courses.append({
        "_id": i,
        "course_name": f"Course_{i}",
        "instructor_id": random.randint(0,49)
    })

with open("courses.json", "w") as f:
    json.dump(courses, f, indent=4)


# ------------------ STUDENTS ------------------
students = []
for i in range(1000):
    students.append({
        "_id": i,
        "name": f"Student_{i}",
        "email": f"student{i}@gmail.com",
        "department_id": random.randint(0,9),
        "semester_id": random.randint(1,8),
        "courses": [random.randint(0,99), random.randint(0,99)]
    })

with open("students.json", "w") as f:
    json.dump(students, f, indent=4)


# ------------------ ASSIGNMENTS ------------------
assignments = []
for i in range(400):
    assignments.append({
        "_id": i,
        "title": f"Assignment_{i}",
        "course_id": random.randint(0,99),
        "deadline": f"2026-04-{random.randint(1,28)}"
    })

with open("assignments.json", "w") as f:
    json.dump(assignments, f, indent=4)


# ------------------ SUBMISSIONS ------------------
submissions = []
for i in range(2000):
    submissions.append({
        "_id": i,
        "student_id": random.randint(0,999),
        "assignment_id": random.randint(0,399),
        "submission_date": f"2026-04-{random.randint(1,28)}",
        "file": {
            "file_name": f"file_{i}.pdf",
            "file_path": f"/uploads/file_{i}.pdf"
        },
        "grade": {
            "marks": random.randint(40,100)
        },
        "feedback": {
            "comments": random.choice(["Good", "Average", "Excellent", "Needs Improvement"])
        }
    })

with open("submissions.json", "w") as f:
    json.dump(submissions, f, indent=4)


# ------------------ NOTIFICATIONS ------------------
notifications = []
for i in range(300):
    notifications.append({
        "_id": i,
        "message": random.choice([
            "Assignment deadline approaching",
            "New assignment uploaded",
            "Grades released"
        ]),
        "date": f"2026-04-{random.randint(1,28)}",
        "student_id": random.randint(0,999)
    })

with open("notifications.json", "w") as f:
    json.dump(notifications, f, indent=4)


print("All JSON files generated successfully!")