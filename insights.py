import json
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


def load_data(filename):
    try:
        with open(filename, "r") as file:
            data = json.load(file)
        return data
    except FileNotFoundError:
        print("data.json file not found!")
        return []
    except json.JSONDecodeError:
        print("JSON file is corrupted!")
        return []



def find_student(data, iid):
    for student in data:
        if student["USN"] == iid:
            return student
    return None


def student_details(student):

    print("\n========================================")
    print("          STUDENT DETAILS")
    print("========================================")

    print("USN    :", student["USN"])
    print("Name   :", student["Name"])
    print("Age    :", student["Age"])
    print("Marks  :", student["Marks"])
    print("Fees   :", student["Fees"])
    print("Course :", student["Course"])

    print("========================================")


def marks_graph(student):
    name = student["Name"]
    marks = student["Marks"]
    plt.figure(figsize=(7, 5))
    ax = sns.barplot(x=[name],y=[marks])
    plt.title(f"Marks of {name} (USN: {student['USN']})")
    plt.xlabel("Student Name")
    plt.ylabel("Marks")
    plt.ylim(0, 100)
    # Show value above bar
    ax.bar_label(ax.containers[0],fmt="%.1f")
    plt.tight_layout()
    plt.show()


def fees_graph(student):
    name = student["Name"]
    fees = student["Fees"]
    plt.figure(figsize=(7, 5))
    ax = sns.barplot(x=[name],y=[fees])

    plt.title(f"Fees of {name} (USN: {student['USN']})")
    plt.xlabel("Student Name")
    plt.ylabel("Fees")
    # Show value above bar
    ax.bar_label(ax.containers[0],fmt="%.0f")
    plt.tight_layout()
    plt.show()



def age_graph(student):
    name = student["Name"]
    age = student["Age"]
    plt.figure(figsize=(7, 5))
    ax = sns.barplot(x=[name],y=[age])

    plt.title(f"Age of {name} (USN: {student['USN']})")
    plt.xlabel("Student Name")
    plt.ylabel("Age")
    # Show value above bar
    ax.bar_label(ax.containers[0],fmt="%.0f")
    plt.tight_layout()
    plt.show()


def course_comparison(data, student):
    course = student["Course"]
    course_students = []
    for s in data:
        if s["Course"] == course:
            course_students.append(s)

    if len(course_students) == 0:
        print("No students found in this course!")
        return

    df = pd.DataFrame(course_students)
    plt.figure(figsize=(10, 6))
    ax = sns.barplot(data=df,x="Name",y="Marks")
    plt.title(f"Marks Comparison - {course}")
    plt.xlabel("Student Name")
    plt.ylabel("Marks")
    plt.xticks(rotation=45)
    # Show marks above bars
    ax.bar_label(ax.containers[0],fmt="%.1f")
    plt.tight_layout()
    plt.show()


def course_average(data, student):
    course = student["Course"]
    course_students = []
    for s in data:
        if s["Course"] == course:
            course_students.append(s)
    if len(course_students) == 0:
        return
    marks = []
    for s in course_students:
        marks.append(s["Marks"])
        
    average = sum(marks) / len(marks)

    print(f"\nAverage Marks of {course}: "f"{average:.2f}")
    print(f"{student['Name']}'s Marks: "f"{student['Marks']}")


    if student["Marks"] > average:
        print("Result: Above Course Average")

    elif student["Marks"] < average:
        print("Result: Below Course Average")
    else:
        print("Result: Equal to Course Average")



def student_rank(data, student):
    course = student["Course"]
    course_students = []
    for s in data:
        if s["Course"] == course:
            course_students.append(s)
    # Sort highest marks first
    course_students.sort(key=lambda x: x["Marks"],reverse=True)

    rank = 0
    for i, s in enumerate(course_students):
        if s["USN"] == student["USN"]:
            rank = i + 1
            break

    print(f"\n{student['Name']}'s Rank "f"in {course}: {rank}")
    print(f"Total Students in {course}: "f"{len(course_students)}")



def overall_insights(data, student):

    print("\n========================================")
    print("           OVERALL INSIGHTS")
    print("========================================")

    marks = student["Marks"]
    age = student["Age"]
    fees = student["Fees"]

    print(f"Student Name : {student['Name']}")
    print(f"Marks        : {marks}")
    print(f"Age          : {age}")
    print(f"Fees         : {fees}")
    print(f"Course       : {student['Course']}")

    # Grade
    if marks >= 90:
        grade = "A+"
    elif marks >= 80:
        grade = "A"
    elif marks >= 70:
        grade = "B"
    elif marks >= 60:
        grade = "C"
    elif marks >= 50:
        grade = "D"
    else:
        grade = "F"


    print(f"Grade        : {grade}")
    percentage = marks
    print(f"Percentage   : {percentage:.2f}%")
    print("========================================")


def get_student_insights(data, student):
    marks = student["Marks"]

    if marks >= 90:
        grade = "A+"
    elif marks >= 80:
        grade = "A"
    elif marks >= 70:
        grade = "B"
    elif marks >= 60:
        grade = "C"
    elif marks >= 50:
        grade = "D"
    else:
        grade = "F"

    course_students = []
    for s in data:
        if s["Course"] == student["Course"]:
            course_students.append(s)


    if len(course_students) > 0:
        total_marks = 0
        for s in course_students:
            total_marks += s["Marks"]
        average = total_marks / len(course_students)
    else:
        average = 0

    course_students.sort(key=lambda x: x["Marks"],reverse=True)


    rank = 0
    for i, s in enumerate(course_students):
        if s["USN"] == student["USN"]:
            rank = i + 1
            break

    if marks > average:
        average_result = "Above Course Average"
    elif marks < average:
        average_result = "Below Course Average"
    else:
        average_result = "Equal to Course Average"

    return {

        "student": {

            "USN": student["USN"],
            "Name": student["Name"],
            "Age": student["Age"],
            "Marks": student["Marks"],
            "Fees": student["Fees"],
            "Course": student["Course"]

        },

        "grade": grade,

        "percentage": marks,

        "course_average": round(
            average,
            2
        ),

        "average_result": average_result,

        "rank": rank,

        "total_students": len(
            course_students
        )

    }

def get_course_students(data, student):

    course = student["Course"]

    course_students = []

    for s in data:

        if s["Course"] == course:

            course_students.append({

                "Name": s["Name"],
                "USN": s["USN"],
                "Marks": s["Marks"]

            })


    course_students.sort(
        key=lambda x: x["Marks"],
        reverse=True
    )


    return course_students


def main():
    filename = "data.json"
    data = load_data(filename)
    if len(data) == 0:
        print("No student data available!")
        return


    while True:

        print("\n========================================")
        print("          STUDENT INSIGHTS")
        print("========================================")
        print("1. Student Details")
        print("2. Marks Graph")
        print("3. Fees Graph")
        print("4. Age Graph")
        print("5. Course Marks Comparison")
        print("6. Course Average")
        print("7. Student Rank")
        print("8. Overall Insights")
        print("9. Exit")
        print("========================================")

        choice = int(
            input("Enter Your Choice :- ")
        )

        if choice in range(1, 9):
            iid = int(input("Enter Student ID / USN :- "))
            student = find_student(data,iid)
            if student is None:
                print("Student not found!")
                continue

        if choice == 1:
            student_details(student)

        elif choice == 2:
            marks_graph(student)

        elif choice == 3:
            fees_graph(student)

        elif choice == 4:
            age_graph(student)

        elif choice == 5:
            course_comparison(data,student)

        elif choice == 6:
            course_average(data,student)

        elif choice == 7:
            student_rank(data,student)

        elif choice == 8:
            overall_insights(data,student)

        elif choice == 9:
            print("Insights Program Ended!" )
            break
        else:
            print("Invalid Choice!")



if __name__ == "__main__":
    main()