"""
Developer: Mahiliavets Dzianis
Lab: 2
Task: Geometric Shapes
Version: 1.0
Date: 2025-03-16

Module containing geometric shape classes with inheritance, polymorphism, and abstraction.
"""

from abc import ABC, abstractmethod
import math
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle as MplRectangle, Circle, Polygon

class Color:
    """Represents a color with validation."""
    
    def __init__(self, color: str):
        self._color = color.lower()
    
    @property
    def color(self) -> str:
        """Get the color name."""
        return self._color
    
    @color.setter
    def color(self, value: str):
        """Set the color name with basic validation."""
        if not isinstance(value, str) or len(value) < 3:
            raise ValueError("Invalid color format")
        self._color = value.lower()

class GeometricShape(ABC):
    """Abstract base class for geometric shapes."""
    
    @abstractmethod
    def area(self) -> float:
        """Calculate the area of the shape."""
        pass
    
    @classmethod
    def shape_name(cls) -> str:
        """Get the shape's display name."""
        return cls.__name__

class Rectangle(GeometricShape):
    """Rectangle shape with width, height, and color."""
    
    SHAPE_NAME = "Rectangle"  # Static attribute
    
    def __init__(self, width: float, height: float, color: str):
        self._width = width
        self._height = height
        self.color = Color(color)  # Composition
        
    @property
    def width(self) -> float:
        return self._width
    
    @width.setter
    def width(self, value: float):
        if value <= 0:
            raise ValueError("Width must be positive")
        self._width = value
        
    @property
    def height(self) -> float:
        return self._height
    
    @height.setter
    def height(self, value: float):
        if value <= 0:
            raise ValueError("Height must be positive")
        self._height = value
    
    def area(self) -> float:
        return self._width * self._height
    
    def get_info(self) -> str:
        """Return formatted shape information."""
        return "Shape: {name}\nColor: {color}\nArea: {area:.2f}".format(
            name=self.SHAPE_NAME,
            color=self.color.color,
            area=self.area()
        )
    
    def draw(self, label: str = "", filename: str = ""):
        """Draw the shape using matplotlib."""
        fig, ax = plt.subplots()
        rect = MplRectangle((0.1, 0.1), self.width, self.height, 
                          facecolor=self.color.color, edgecolor='black')
        ax.add_patch(rect)
        plt.text(0.5 * self.width, 0.5 * self.height, label, 
                ha='center', va='center')
        ax.set_xlim(0, self.width * 1.2)
        ax.set_ylim(0, self.height * 1.2)
        plt.title(self.SHAPE_NAME)
        
        if filename:
            plt.savefig(filename)
        plt.show()

class CircleShape(GeometricShape):
    """Circle shape with radius and color."""
    
    SHAPE_NAME = "Circle"
    
    def __init__(self, radius: float, color: str):
        self._radius = radius
        self.color = Color(color)
    
    @property
    def radius(self) -> float:
        return self._radius
    
    @radius.setter
    def radius(self, value: float):
        if value <= 0:
            raise ValueError("Radius must be positive")
        self._radius = value
    
    def area(self) -> float:
        return math.pi * self._radius ** 2
    
    def get_info(self) -> str:
        return "Shape: {name}\nColor: {color}\nArea: {area:.2f}".format(
            name=self.SHAPE_NAME,
            color=self.color.color,
            area=self.area()
        )
    
    def draw(self, label: str = "", filename: str = ""):
        fig, ax = plt.subplots()
        circle = Circle((0.5, 0.5), self.radius, 
                       facecolor=self.color.color, edgecolor='black')
        ax.add_patch(circle)
        plt.text(0.5, 0.5, label, ha='center', va='center')
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        plt.title(self.SHAPE_NAME)
        
        if filename:
            plt.savefig(filename)
        plt.show()

class InscribedTriangle(GeometricShape):
    """Equilateral triangle inscribed in a circle."""
    
    SHAPE_NAME = "Inscribed Triangle"
    
    def __init__(self, radius: float, color: str):
        self._radius = radius
        self.color = Color(color)
    
    @property
    def radius(self) -> float:
        return self._radius
    
    @radius.setter
    def radius(self, value: float):
        if value <= 0:
            raise ValueError("Radius must be positive")
        self._radius = value
    
    def area(self) -> float:
        side = self._radius * math.sqrt(3)
        return (math.sqrt(3)/4) * side ** 2
    
    def get_info(self) -> str:
        return "Shape: {name}\nColor: {color}\nArea: {area:.2f}".format(
            name=self.SHAPE_NAME,
            color=self.color.color,
            area=self.area()
        )
    
    def draw(self, label: str = "", filename: str = ""):
        # Calculate triangle coordinates
        angles = [0, 120, 240]
        points = [
            (self._radius * math.cos(math.radians(ang)),
             self._radius * math.sin(math.radians(ang))) 
             for ang in angles
        ]
        
        fig, ax = plt.subplots()
        
        # Draw the circumscribed circle
        circle = Circle((0, 0), self._radius, 
                           fill=False, edgecolor='blue', linestyle='--')
        ax.add_patch(circle)
        
        # Draw the triangle
        triangle = Polygon(points, closed=True, 
                             facecolor=self.color.color, 
                             edgecolor='black')
        ax.add_patch(triangle)
        
        # Add label and title
        plt.text(0, 0, label, ha='center', va='center')
        ax.set_xlim(-self._radius*1.5, self._radius*1.5)
        ax.set_ylim(-self._radius*1.5, self._radius*1.5)
        plt.title(self.SHAPE_NAME)
        plt.gca().set_aspect('equal', adjustable='box')
        
        if filename:
            plt.savefig(filename, dpi=300, bbox_inches='tight')
        plt.show()