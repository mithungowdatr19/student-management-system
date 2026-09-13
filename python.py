
import json
import pandas as pd


class Students:

    def __init__(self, iid, name, age, marks, fee, course):

        self.iid = iid
        self.name = name
        self.age = age
        self.marks = marks
        self.fee = fee
        self.course = course


    def show_details(self):

        return {
            "USN": self.iid,
            "Name": self.name,
            "Age": self.age,
            "Marks": self.marks,
            "Fees": self.fee,
            "Course": self.course
        }



def load_json(filename):
    try:
        with open(filename, "r") as file:
            data = json.load(file)
        return data
    except FileNotFoundError:
        return []
    except json.JSONDecodeError:
        print("JSON file is corrupted!")
        return []


def save_json(filename, data):
    with open(filename, "w") as file:
        json.dump(data,file,indent=4)
    print("Data saved successfully!")


def add_student(filename, student_list):
    print("\n========================================")
    print("             ADD STUDENT")
    print("========================================")
    try:
        iid = int(input("Enter Student ID / USN :- "))

        existing_data = load_json(filename)
        for student in existing_data:
            if student["USN"] == iid:
                print(f"USN {iid} already exists!")
                print(f"Student Name: {student['Name']}")

                return

        for student in student_list:
            if student["USN"] == iid:
                print(f"USN {iid} already exists!")
                return

        name = input("Enter Student Name :- ")
        age = int(input("Enter Student Age :- "))
        marks = float(input("Enter Student Marks :- "))
        fee = float(input("Enter Student Fees :- ") )
        course = input("Enter Student Course :- ")


        student = Students(iid,name,age,marks,fee,course)
        student_list.append(student.show_details())

        print("\nStudent added successfully!")
    except ValueError:
        print("Please enter valid numeric values!")



def save_students(filename, student_list):
    if len(student_list) == 0:
        print("No new student data to save!")
        return

    old_data = load_json(filename)
    old_data.extend(student_list)
    save_json(filename,old_data)
    # Clear temporary list
    student_list.clear()


def display_students(filename):
    data = load_json(filename)
    if len(data) == 0:
        print("No student data available!")
        return
    df = pd.DataFrame(data)
    # Sort by USN
    df = df.sort_values(by="USN")

    print("\n========================================")
    print("           ALL STUDENTS")
    print("========================================")

    print(df.to_string(index=False))
    print("========================================")


def delete_student(filename):
    data = load_json(filename)
    if len(data) == 0:
        print("No student data available!")
        return
    try:
        iid = int(input("Enter Student ID / USN to Delete :- "))
    except ValueError:
        print("Please enter a valid USN!")
        return
    
    new_data = []
    found = False

    for student in data:
        if student["USN"] == iid:
            found = True
        else:
            new_data.append(student)

    if found:
        save_json(filename,new_data)
        print("Student deleted successfully!")
    else:
        print("Student not found!")


def search_student(filename):
    data = load_json(filename)
    if len(data) == 0:
        print("No student data available!")
        return
    try:
        iid = int(input("Enter Student ID / USN to Search :- "))
    except ValueError:
        print("Please enter a valid USN!")
        return
    
    for student in data:
        if student["USN"] == iid:
            print("\n========================================")
            print("           STUDENT FOUND")
            print("========================================")

            print("USN    :", student["USN"])
            print("Name   :", student["Name"])
            print("Age    :", student["Age"])
            print("Marks  :", student["Marks"])
            print("Fees   :", student["Fees"])
            print("Course :", student["Course"])

            print("========================================")
            return
        
    print("Student not found!")

def main():
    filename = "data.json"
    student_list = []

    while True:

        print("\n========================================")
        print("       STUDENT MANAGEMENT SYSTEM")
        print("========================================")

        print("1. Add Student")
        print("2. Save Student to JSON")
        print("3. Display Students")
        print("4. Delete Student")
        print("5. Search Student")
        print("6. Exit")

        print("========================================")

        try:
            choice = int(input("Enter Your Choice :- "))
        except ValueError:
            print("Please enter a valid choice!")
            continue

        if choice == 1:
            add_student(filename, student_list)

        elif choice == 2:
            save_students(filename,student_list)

        elif choice == 3:
            display_students(filename)

        elif choice == 4:
            delete_student(filename)

        elif choice == 5:
            search_student(filename)

        elif choice == 6:
            # Automatically save unsaved students
            if len(student_list) > 0:
                print("\nYou have unsaved student data.")
                save_students(filename,student_list)
            print("\nStudent Management System Ended!")
            break
        
        else:
            print("Invalid Choice!")


if __name__ == "__main__":
    main()