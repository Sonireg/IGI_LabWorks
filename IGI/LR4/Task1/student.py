class Student:
    """
    Represents a student with full name and birth date.
    """
    def __init__(self, full_name: str, birth_day: int, birth_month: int, birth_year: int):
        self.full_name = full_name
        self.birth_day = birth_day
        self.birth_month = birth_month
        self.birth_year = birth_year
    
    def __str__(self):
        return f"{self.full_name} ({self.birth_day:02d}.{self.birth_month:02d}.{self.birth_year})"
