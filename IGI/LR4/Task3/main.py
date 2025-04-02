"""
Developer: Mahiliavets Dzianis
Lab: 2
Task: 1
Program: Advanced Cos Analysis CLI
Version: 2.1
Date: 2025-03-16
"""

from cos_analyzer import CosSeriesAnalyzer
from utils import get_valid_input
import math

def main():
    """Main workflow with user interaction."""
    print("Cosine Series Analysis Program")
    
    while True:
        x = get_valid_input("Enter x in radians: ", float)
        eps = get_valid_input("Enter precision (epsilon): ", 
                             float, 
                             lambda x: x > 0, 
                             "Epsilon must be positive")
        
        analyzer = CosSeriesAnalyzer(x, eps)
        sum_series, n_terms = analyzer.compute_series()
        stats = analyzer.statistical_metrics
        
        # Display results
        print("\nCalculation Results:")
        print(f"{'Series sum':<20}: {sum_series:.6f}")
        print(f"{'math.cos(x)':<20}: {math.cos(x):.6f}")
        print(f"{'Terms used':<20}: {n_terms}")
        
        print("\nStatistical Analysis:")
        for metric, value in stats.items():
            print(f"{metric.capitalize():<20}: {value:.4f}")
        
        # Generate and save plot
        save_file = input("\nEnter filename to save plot (empty to skip): ").strip()
        if save_file:
            analyzer.plot_comparison(save_file)
            print(f"Plot saved to {save_file}")
        
        # Plot fixed n comparison
        if input("\nPlot fixed n comparison? (y/n): ").lower() == 'y':
            n = get_valid_input("Enter number of terms (n): ", int, lambda x: x > 0, "n must be positive")
            save_fixed_n = input("Enter filename to save fixed n plot (empty to skip): ").strip()
            analyzer.plot_fixed_n_comparison(n, save_path=save_fixed_n)
            if save_fixed_n:
                print(f"Fixed n plot saved to {save_fixed_n}")
        
        if input("\nRepeat analysis? (y/n): ").lower() != 'y':
            break

if __name__ == "__main__":
    main()