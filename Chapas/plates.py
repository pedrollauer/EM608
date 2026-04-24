def analyze_plate_load(length, width, thickness, yield_strength_mpa, applied_load_n):
    """
    Calculates max allowable load and Factor of Safety (FoS).
    Units: mm for dimensions, MPa for stress, N for force.
    """
    # Using the simplified engineering formula: F_max = (sigma_y * b * h^2) / L
    # This is slightly conservative compared to the theoretical 1.5 coefficient.
    max_load = (yield_strength_mpa * width * (thickness**2)) / length
    
    fos = max_load / applied_load_n
    
    return max_load, fos

# --- Input your design parameters here ---
L = 150       # Span distance (mm)
B = 50        # Width of the plate (mm)
H = 2.0       # Thickness (mm)
SIGMA_Y = 250 # Yield strength (MPa) - e.g., Mild Steel
LOAD = 500    # The actual load you plan to apply (N)

max_f, safety_factor = analyze_plate_load(L, B, H, SIGMA_Y, LOAD)

print(f"--- Sheet Metal Analysis ---")
print(f"Max Allowable Load: {max_f:.2f} N")
print(f"Applied Load:      {LOAD:.2f} N")
print(f"Factor of Safety:  {safety_factor:.2f}")

if safety_factor < 1.0:
    print("WARNING: Part will likely yield (permanently deform)!")
elif safety_factor < 2.0:
    print("CAUTION: Low safety margin for mechanical parts.")
else:
    print("Design appears structurally sound for static loading.")
