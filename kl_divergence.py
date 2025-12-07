import pandas as pd
import numpy as np
#from scipy.spatial.distance import entropy
from scipy.stats import entropy as scipy_entropy
import sys


def normalize_distribution(values, bins=10):
    """Convert values to a normalized probability distribution."""
    counts, _ = np.histogram(values, bins=bins)
    # Add small epsilon to avoid log(0)
    counts = counts + 1e-10
    return counts / np.sum(counts)


def calculate_kl_divergence(file1, file2, column=None, bins=10):
    """
    Calculate Kullback-Leibler divergence between two CSV files.
    
    Parameters:
    -----------
    file1 : str
        Path to first CSV file
    file2 : str
        Path to second CSV file
    column : str, optional
        Column name to compare. If None, compares all numeric columns
    bins : int, default=10
        Number of bins for histogram discretization
    """
    # Load CSV files
    df1 = pd.read_csv(file1)
    df2 = pd.read_csv(file2)
    
    print(f"Loaded {file1}: {df1.shape[0]} rows, {df1.shape[1]} columns")
    print(f"Loaded {file2}: {df2.shape[0]} rows, {df2.shape[1]} columns")
    print()
    
    # Get numeric columns
    numeric_cols1 = df1.select_dtypes(include=[np.number]).columns.tolist()
    numeric_cols2 = df2.select_dtypes(include=[np.number]).columns.tolist()
    
    if column:
        # Compare specific column
        if column not in numeric_cols1 or column not in numeric_cols2:
            print(f"Error: Column '{column}' not found in both files or not numeric")
            return
        
        columns_to_compare = [column]
    else:
        # Find common numeric columns
        columns_to_compare = list(set(numeric_cols1) & set(numeric_cols2))
        if not columns_to_compare:
            print("No common numeric columns found between the two files")
            return
    
    print(f"Comparing {len(columns_to_compare)} column(s):")
    print()
    
    # Calculate KL divergence for each column
    total_kl = 0
    for col in columns_to_compare:
        values1 = df1[col].dropna().values
        values2 = df2[col].dropna().values
        
        # Normalize to distributions
        p = normalize_distribution(values1, bins=bins)
        q = normalize_distribution(values2, bins=bins)
        
        # Calculate KL divergence: D_KL(P || Q)
        kl_div = scipy_entropy(p, q)
        total_kl += kl_div
        
        print(f"Column: {col}")
        print(f"  File 1 - min: {values1.min():.4f}, max: {values1.max():.4f}, mean: {values1.mean():.4f}")
        print(f"  File 2 - min: {values2.min():.4f}, max: {values2.max():.4f}, mean: {values2.mean():.4f}")
        print(f"  KL Divergence (File1 || File2): {kl_div:.6f}")
        print()
    
    # Print summary
    print(f"Average KL Divergence across {len(columns_to_compare)} column(s): {total_kl / len(columns_to_compare):.6f}")
    print(f"Total KL Divergence: {total_kl:.6f}")


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python kl_divergence.py <file1.csv> <file2.csv> [column_name] [bins]")
        print("\nExample:")
        print("  python kl_divergence.py data1.csv data2.csv")
        print("  python kl_divergence.py data1.csv data2.csv age 20")
        sys.exit(1)
    
    file1 = sys.argv[1]
    file2 = sys.argv[2]
    column = sys.argv[3] if len(sys.argv) > 3 else None
    bins = int(sys.argv[4]) if len(sys.argv) > 4 else 10
    
    calculate_kl_divergence(file1, file2, column=column, bins=bins)
