"""
Task 3: Count Latin letters and digits.
Lab: 1
Title: String Analyzer
Version: 1.0
Developer: Mahiliavets Dzianis
Date: 2025-03-05
"""

def count_latin_letters_digits(s: str) -> tuple[int, int]:
    """
    Count the number of Latin letters and digits in a string.
    
    Args:
        s (str): Input string.
    
    Returns:
        tuple[int, int]: Number of Latin letters and digits.
    """
    letters = 0
    digits = 0
    for c in s:
        if c.isalpha() and 'a' <= c.lower() <= 'z':
            letters += 1
        elif c.isdigit():
            digits += 1
    return letters, digits

def task3_main():
    """Main function for Task 3: handles input and displays results."""
    s = input("Enter a string: ")
    letters, digits = count_latin_letters_digits(s)
    print(f"Latin letters: {letters}, Digits: {digits}")