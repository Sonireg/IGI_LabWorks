import csv
import pickle
from typing import List
from student import Student

class SchoolClass:
    """
    Represents a school class containing multiple students.
    """
    def __init__(self):
        self.students: List[Student] = []
    
    def add_student(self, student: Student):
        self.students.append(student)
    
    def save_to_csv(self, filename: str):
        """ Saves students data to a CSV file. """
        try:
            with open(filename, mode='w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow(["Full Name", "Day", "Month", "Year"])
                for student in self.students:
                    writer.writerow([student.full_name, student.birth_day, student.birth_month, student.birth_year])
        except Exception as e:
            print(f"Error saving CSV file: {e}")
    
    def load_from_csv(self, filename: str):
        """ Loads students data from a CSV file. """
        try:
            with open(filename, mode='r', newline='', encoding='utf-8') as file:
                reader = csv.reader(file)
                next(reader)  # Skip header row
                self.students = [Student(row[0], int(row[1]), int(row[2]), int(row[3])) for row in reader]
        except Exception as e:
            print(f"Error loading CSV file: {e}")
    
    def save_to_pickle(self, filename: str):
        """ Saves students data to a binary pickle file. """
        try:
            with open(filename, 'wb') as file:
                pickle.dump(self.students, file)
        except Exception as e:
            print(f"Error saving pickle file: {e}")
    
    def load_from_pickle(self, filename: str):
        """ Loads students data from a binary pickle file. """
        try:
            with open(filename, 'rb') as file:
                self.students = pickle.load(file)
        except Exception as e:
            print(f"Error loading pickle file: {e}")
    
    def find_students_by_month(self, month: int) -> List[Student]:
        """ Returns a list of students born in the specified month. """
        return [student for student in self.students if student.birth_month == month]
