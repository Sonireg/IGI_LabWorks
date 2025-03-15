"""
Task 2: Count odd natural numbers.
Lab: 1
Title: Odd Natural Numbers Counter
Version: 1.0
Developer: Mahiliavets Dzianis
Date: 2025-03-05
"""
from utils import get_valid_input

def count_odd_natural_numbers():
    """Count odd natural numbers entered by the user until 0 is input."""
    count = 0
    while True:
        try:
            num = int(input("Enter an integer (0 to stop): "))
            if num == 0:
                break
            if num > 0 and num % 2 == 1:
                count += 1
        except ValueError:
            print("Invalid input. Please enter an integer.")
    return count

def task2_main():
    """Main function for Task 2: handles input and displays the result."""
    print("Enter integers. 0 to stop.")
    count = count_odd_natural_numbers()
    print(f"Number of odd natural numbers: {count}")