from flask import (
    Flask,
    request,
    jsonify,
    send_file
)

import json

from insights import (
    get_student_insights,
    get_course_students
)


# ==========================================
# FLASK APP
# ==========================================

app = Flask(__name__)


# ==========================================
# FILE
# ==========================================

FILE = "data.json"


# ==========================================
# LOAD DATA
# ==========================================

def load_data():

    try:

        with open(FILE, "r") as file:

            return json.load(file)

    except FileNotFoundError:

        return []

    except json.JSONDecodeError:

        return []


# ==========================================
# SAVE DATA
# ==========================================

def save_data(data):

    with open(FILE, "w") as file:

        json.dump(
            data,
            file,
            indent=4
        )


# ==========================================
# HOME PAGE
# ==========================================

@app.route("/")
def home():

    return send_file("index.html")


# ==========================================
# GET ALL STUDENTS
# ==========================================

@app.route("/api/students")
def students():

    data = load_data()

    data.sort(
        key=lambda x: x["USN"]
    )

    return jsonify(data)


# ==========================================
# ADD STUDENT
# ==========================================

@app.route(
    "/api/add",
    methods=["POST"]
)
def add_student():

    student = request.get_json()


    required_fields = [

        "USN",
        "Name",
        "Age",
        "Marks",
        "Fees",
        "Course"

    ]


    # --------------------------------------
    # Check fields
    # --------------------------------------

    for field in required_fields:

        if field not in student:

            return jsonify({

                "success": False,

                "message":
                    f"Missing field: {field}"

            })


    data = load_data()


    # --------------------------------------
    # Check duplicate USN
    # --------------------------------------

    for existing in data:

        if existing["USN"] == student["USN"]:

            return jsonify({

                "success": False,

                "message":
                    f"USN {student['USN']} already exists!"

            })


    # --------------------------------------
    # Add
    # --------------------------------------

    data.append(student)

    save_data(data)


    return jsonify({

        "success": True,

        "message":
            "Student added successfully!"

    })


# ==========================================
# SEARCH STUDENT
# ==========================================

@app.route(
    "/api/search/<int:usn>"
)
def search_student(usn):

    data = load_data()


    for student in data:

        if student["USN"] == usn:

            return jsonify({

                "success": True,

                "student": student

            })


    return jsonify({

        "success": False,

        "message":
            "Student not found!"

    })


# ==========================================
# DELETE STUDENT
# ==========================================

@app.route(
    "/api/delete/<int:usn>",
    methods=["DELETE"]
)
def delete_student(usn):

    data = load_data()


    new_data = []

    found = False


    for student in data:

        if student["USN"] == usn:

            found = True

        else:

            new_data.append(student)


    if not found:

        return jsonify({

            "success": False,

            "message":
                "Student not found!"

        })


    save_data(new_data)


    return jsonify({

        "success": True,

        "message":
            "Student deleted successfully!"

    })


# ==========================================
# STUDENT INSIGHTS
# ==========================================

@app.route(
    "/api/insights/<int:usn>"
)
def student_insights(usn):

    data = load_data()


    # --------------------------------------
    # Find student
    # --------------------------------------

    student = None


    for s in data:

        if s["USN"] == usn:

            student = s

            break


    if student is None:

        return jsonify({

            "success": False,

            "message":
                "Student not found!"

        })


    # --------------------------------------
    # Get insights from insights.py
    # --------------------------------------

    insights = get_student_insights(
        data,
        student
    )


    # --------------------------------------
    # Course students
    # --------------------------------------

    course_students = get_course_students(
        data,
        student
    )


    insights["course_students"] = (
        course_students
    )


    return jsonify({

        "success": True,

        "insights": insights

    })


# ==========================================
# RUN SERVER
# ==========================================

if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )