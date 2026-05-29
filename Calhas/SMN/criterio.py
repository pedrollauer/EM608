import sympy as sp
from sympy.physics.continuum_mechanics.beam import Beam
from scipy.optimize import minimize_scalar
import warnings

# Suppress scipy optimization warnings for cleaner output
warnings.filterwarnings('ignore')

def calculate_beam_stiffness(L, E, I, supports, uniform_load):
    """
    Calculates the point of maximum deflection and its equivalent spring constant.
    
    Parameters:
    L (float): Length of the beam (m)
    E (float): Young's Modulus (Pa)
    I (float): Area Moment of Inertia (m^4)
    supports (list of floats): Positions of the supports (m) - up to 3 supports
    uniform_load (float): Downward distributed load to find max deflection point (N/m)
    """
    if len(supports) > 3:
        raise ValueError("This program supports a maximum of 3 supports.")

    print(f"--- BEAM ANALYSIS ---")
    print(f"Length: {L} m | Supports: {supports} m")
    
    # ==========================================
    # STEP 1: Find the point of max deflection
    # ==========================================
    # Initialize the beam
    b = Beam(L, E, I)

    # Apply supports (unknown reaction forces)
    reactions = []
    for i, loc in enumerate(supports):
        R = sp.Symbol(f'R_{i}')
        reactions.append(R)
        # Apply the reaction as a point load (order -1)
        b.apply_load(R, loc, -1)
        # Boundary condition: Deflection at the support is 0
        b.bc_deflection.append((loc, 0))

    # Apply the primary continuous load (order 0) downward
    b.apply_load(-abs(uniform_load), 0, 0, L)

    # Solve for the unknown reaction forces
    b.solve_for_reaction_loads(*reactions)

    # Get the deflection equation and convert to Piecewise for numerical evaluation
    deflection_eq = b.deflection().rewrite(sp.Piecewise)
    
    # Create a numerical function to find the minimum (largest downward deflection)
    defl_func = sp.lambdify(b.variable, deflection_eq, 'numpy')
    
    # Find the x position that minimizes the deflection function (largest negative value)
    res = minimize_scalar(lambda x: float(defl_func(x)), bounds=(0, L), method='bounded')
    x_max_defl = res.x
    max_defl = res.fun
    
    print(f"\nUnder a uniform load of {uniform_load} N/m:")
    print(f"Largest deflection occurs at x = {x_max_defl:.3f} m")
    print(f"Maximum deflection value = {max_defl:.6e} m")

    # ==========================================
    # STEP 2: Calculate Spring Constant (Stiffness) at x_max_defl
    # ==========================================
    # To find stiffness, we apply a virtual point load P at the location of max deflection
    # and calculate k = P / delta_P
    
    b_stiff = Beam(L, E, I)
    
    reactions_stiff = []
    for i, loc in enumerate(supports):
        R = sp.Symbol(f'R_stiff_{i}')
        reactions_stiff.append(R)
        b_stiff.apply_load(R, loc, -1)
        b_stiff.bc_deflection.append((loc, 0))

    # Apply a virtual downward test load of 10,000 N (10 kN) at the target point
    test_load = -10000 
    b_stiff.apply_load(test_load, x_max_defl, -1)

    # Solve the new beam system
    b_stiff.solve_for_reaction_loads(*reactions_stiff)
    
    # Calculate deflection at exactly x_max_defl
    stiff_deflection_eq = b_stiff.deflection().rewrite(sp.Piecewise)
    delta_at_test = float(stiff_deflection_eq.subs(b_stiff.variable, x_max_defl))
    
    # Spring constant k = Force / Deflection
    spring_constant = abs(test_load / delta_at_test)
    
    print(f"\n--- STIFFNESS RESULTS ---")
    print(f"Equivalent Spring Constant (k) at x = {x_max_defl:.3f} m:")
    print(f"k = {spring_constant:,.2f} N/m")

    return x_max_defl, spring_constant

if __name__ == "__main__":
    # --- EXAMPLE USAGE ---
    
    # Material: Steel (Young's Modulus E = 200 GPa)
    E_steel = 200e9 
    
    # Cross-section: Let's assume an I-beam with I = 0.0001 m^4
    I_beam = 0.0001 
    
    # Beam length: 10 meters
    Length = 10.0 
    
    # Supports at start, middle, and end (Statically indeterminate)
    # Try changing this to [0, 10] for a simply supported beam!
    support_locations = [0.0, 5.0, 10.0,] 
    
    # Uniform load of 5,000 N/m applied to find the weakest point
    load = 5000.0 

    # Run the analysis
    calculate_beam_stiffness(Length, E_steel, I_beam, support_locations, load)
