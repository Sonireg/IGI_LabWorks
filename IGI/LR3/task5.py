"""
Task 5: Process list of integers.
Lab: 1
Title: List Processor
Version: 1.0
Developer: Mahiliavets Dzianis
Date: 2025-03-05
"""
from initialization import input_list_user, generate_list_random
from utils import get_valid_input

def display_list(lst: list):
    """Display the list elements."""
    print("List elements:", lst)

def compute_products_and_sum(lst: list) -> tuple[int, int]:
    """
    Compute product of even elements at even indices and sum between first and last non-zero elements.
    
    Args:
        lst (list): List of integers.
    
    Returns:
        tuple[int, int]: Product and sum.
    """
    product = 1
    for i in range(len(lst)):
        if (i + 1) % 2 == 0 and lst[i] % 2 == 0:
            product *= abs(lst[i])
    
    first = next((i for i, x in enumerate(lst) if x != 0), None)
    last = next((i for i in reversed(range(len(lst))) if lst[i] != 0), None)
    
    sum_between = 0
    if first is not None and last is not None and first < last:
        sum_between = sum(lst[first + 1 : last])
    return product, sum_between

def task5_main():
    """Main function for Task 5: handles list initialization and processing."""
    print("Initialize list:")
    print("1. User input")
    print("2. Random generator")
    choice = get_valid_input("Select method (1/2): ", int, lambda x: x in (1, 2))
    lst = input_list_user() if choice == 1 else generate_list_random()
    display_list(lst)
    product, sum_between = compute_products_and_sum(lst)
    print(f"Product of even elements at even positions: {product}")
    print(f"Sum between first and last non-zero elements: {sum_between}")