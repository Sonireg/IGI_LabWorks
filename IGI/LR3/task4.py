"""
Task 4: Analyze text.
Lab: 1
Title: Text Analysis
Version: 1.0
Developer: Mahiliavets Dzianis
Date: 2025-03-05
"""

def task4a(sentence: str) -> int:
    """
    Count words starting with a vowel.
    
    Args:
        sentence (str): Input sentence.
    
    Returns:
        int: Number of words starting with a vowel.
    """
    vowels = {'a', 'e', 'i', 'o', 'u'}
    words = sentence.replace(',', ' ').split()
    count = 0
    for word in words:
        if word and word[0].lower() in vowels:
            count += 1
    return count

def task4b(sentence: str) -> list[tuple[str, int]]:
    """
    Find words with consecutive repeated letters and their positions.
    
    Args:
        sentence (str): Input sentence.
    
    Returns:
        list[tuple[str, int]]: List of tuples (word, position).
    """
    words = sentence.replace(',', ' ').split()
    result = []
    for idx, word in enumerate(words, 1):
        for i in range(len(word) - 1):
            if word[i].lower() == word[i + 1].lower():
                result.append((word, idx))
                break
    return result

def task4c(sentence: str) -> list[str]:
    """
    Sort words alphabetically (case-insensitive).
    
    Args:
        sentence (str): Input sentence.
    
    Returns:
        list[str]: Sorted list of words.
    """
    words = sentence.replace(',', ' ').split()
    return sorted(words, key=lambda x: x.lower())

def task4_main():
    """Main function for Task 4: runs analysis on a predefined text."""
    sample_text = "So she was considering in her own mind, as well as she could, for the hot day made her feel very sleepy and stupid, whether the pleasure of making a daisy-chain would be worth the trouble of getting up and picking the daisies, when suddenly a White Rabbit with pink eyes ran close by her."
    
    print("4a: Number of words starting with a vowel:", task4a(sample_text))
    
    print("\n4b: Words with consecutive repeated letters:")
    for word, pos in task4b(sample_text):
        print(f"Word: {word}, Position: {pos}")
    
    print("\n4c: Words in alphabetical order:")
    print(', '.join(task4c(sample_text)))