import numpy as np

def solve_cubic_numpy(a, b, c, d):
    """
    Solves ax^3 + bx^2 + cx + d = 0 using NumPy.
    Returns an array of all three roots (real and/or complex).
    """
    # Define the coefficients in descending order of power
    coefficients = [a, b, c, d]
    
    # Calculate roots
    roots = np.roots(coefficients)
    
    return roots

# Example usage: x^3 - 6x^2 + 11x - 6 = 0 (Roots are 1, 2, 3)
if __name__ == "__main__":
    a, b, c, d = 274910.8, 824.7324, 0.618549,-0.001329361
    roots = solve_cubic_numpy(a, b, c, d)
    
    print("NumPy Roots:")
    for i, root in enumerate(roots):
        # Format to 4 decimal places for clean output
        print(f"  Root {i+1}: {root:.4f}")
