import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from utils import get_valid_input
from school import SchoolClass
from student import Student


def main():
    school_class = SchoolClass()
    school_class.add_student(Student("Alice Smith", 10, 3, 2005))
    school_class.add_student(Student("Bob Johnson", 22, 7, 2004))
    school_class.add_student(Student("Charlie Brown", 5, 3, 2006))
    
    # Save and load CSV
    school_class.save_to_csv("students.csv")
    school_class.load_from_csv("students.csv")
    
    # Save and load pickle
    school_class.save_to_pickle("students.pkl")
    school_class.load_from_pickle("students.pkl")
    
    # Search students by birth month
    month = get_valid_input("Enter birth month to search: ", int, lambda x: 1 <= x <= 12, "Please enter a valid month (1-12).")
    found_students = school_class.find_students_by_month(month)
    if found_students:
        print("Students born in this month:")
        for student in found_students:
            print(student)
    else:
        print("No students found for this month.")

if __name__ == "__main__":
    main()
