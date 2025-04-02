"""
Developer: Mahiliavets Dzianis
Lab: 2
Task: 1
Program: Advanced Cos Series Analysis
Version: 2.1
Date: 2025-03-16
"""

import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import math
import matplotlib.pyplot as plt
from utils import timer_decorator
from statistics import mean, median, mode, variance, stdev
from typing import List, Tuple

class CosSeriesAnalyzer:
    """Class for advanced cosine series analysis with statistical and visualization features.
    
    Attributes:
        x (float): Input value in radians.
        eps (float): Precision for series convergence.
        terms (List[float]): List of series terms.
        partial_sums (List[float]): Cumulative sums during calculation.
    """
    
    def __init__(self, x: float, eps: float = 1e-6):
        """
        Initialize analyzer with parameters.
        
        Args:
            x: Input value in radians
            eps: Precision threshold (default: 1e-6)
        """
        self.x = x
        self.eps = eps
        self.terms = []
        self.partial_sums = []  # For graph plotting

    @timer_decorator
    def compute_series(self) -> Tuple[float, int]:
        """Calculate cosine series sum with term storage."""
        sum_total = 1.0
        self.terms = [sum_total]
        self.partial_sums = [sum_total]
        
        for n in range(1, 500):
            term = ((-1) ** n) * (self.x ** (2 * n)) / math.factorial(2 * n)
            if abs(term) < self.eps:
                break
                
            sum_total += term
            self.terms.append(term)
            self.partial_sums.append(sum_total)
            
        return sum_total, len(self.terms)

    @property
    def statistical_metrics(self) -> dict:
        """Calculate statistical parameters of the series terms."""
        if not self.terms:
            raise ValueError("No terms available. Run compute_series() first.")
            
        return {
            'mean': mean(self.terms),
            'median': median(self.terms),
            'mode': mode(self.terms),
            'variance': variance(self.terms),
            'stdev': stdev(self.terms)
        }

    def plot_comparison(self, save_path: str = "") -> None:
        """Generate comparison plot between series and math.cos."""
        if not self.partial_sums:
            raise ValueError("No data available. Run compute_series() first.")

        plt.figure(figsize=(10, 6))
        x_vals = list(range(1, len(self.partial_sums) + 1))
        
        # Series approximation plot
        plt.plot(x_vals, self.partial_sums, 
                'b--', 
                label=f'Series Approximation (n={len(self.terms)})')
        
        # Math.cos reference line
        math_val = math.cos(self.x)
        plt.axhline(y=math_val, color='r', 
                   linestyle='-', 
                   label='math.cos(x)')
        
        plt.xlabel('Number of Terms')
        plt.ylabel('Function Value')
        plt.title(f'Cosine Series Convergence (x={self.x:.2f} rad)')
        plt.legend()
        plt.grid(True)
        
        # Add annotation for final difference
        final_diff = abs(self.partial_sums[-1] - math_val)
        plt.annotate(f'Final difference: {final_diff:.2e}',
                    xy=(0.5, 0.1), 
                    xycoords='axes fraction',
                    ha='center')
        
        if save_path:
            plt.savefig(save_path, dpi=300)
        plt.show()

    def plot_fixed_n_comparison(self, n: int, x_range: Tuple[float, float] = (-2 * math.pi, 2 * math.pi), save_path: str = "") -> None:
        """
        Plot math.cos(x) and series sum for a fixed number of terms (n) over a range of x values.
        
        Args:
            n: Number of terms to use in the series.
            x_range: Tuple (start, end) for x values (default: -2π to 2π).
            save_path: Path to save the plot (optional).
        """
        x_start, x_end = x_range
        x_values = [x_start + i * (x_end - x_start) / 100 for i in range(101)]
        
        # Calculate math.cos values
        math_cos_values = [math.cos(x) for x in x_values]
        
        # Calculate series sum for fixed n
        series_values = []
        for x in x_values:
            sum_total = 1.0  # First term (n=0)
            for k in range(1, n):
                term = ((-1) ** k) * (x ** (2 * k)) / math.factorial(2 * k)
                sum_total += term
            series_values.append(sum_total)
        
        # Plotting
        plt.figure(figsize=(10, 6))
        plt.plot(x_values, math_cos_values, 'r-', label='math.cos(x)')
        plt.plot(x_values, series_values, 'b--', label=f'Series Sum (n={n})')
        
        plt.xlabel('x (radians)')
        plt.ylabel('Function Value')
        plt.title(f'Comparison of math.cos(x) and Series Sum (n={n})')
        plt.legend()
        plt.grid(True)
        
        if save_path:
            plt.savefig(save_path, dpi=300)
        plt.show()

    def __str__(self) -> str:
        """String representation of analyzer state."""
        return f"CosSeriesAnalyzer(x={self.x}, eps={self.eps})"