import numpy as np

def calculate_plate_deflection(a, b, h, E, nu, q0, m_max=10, n_max=10):
    """
    a, b: dimensions of the plate (m)
    h: thickness (m)
    E: Young's Modulus (Pa)
    nu: Poisson's ratio
    q0: Uniform load (N/m^2)
    """
    # Flexural Rigidity (D) for Kirchhoff-Love Plate
    D = (E * h**3) / (12 * (1 - nu**2))
    
    # Grid for calculation (Center of the plate)
    x, y = a / 2, b / 2
    w_center = 0
    
    # Navier Series Summation
    for m in range(1, m_max + 1, 2): # Only odd terms for uniform load
        for n in range(1, n_max + 1, 2):
            term_denom = ((m/a)**2 + (n/b)**2)**2
            term_num = np.sin(m * np.pi * x / a) * np.sin(n * np.pi * y / b)
            
            # The Fourier coefficient for uniform load is 16*q0 / (pi^6 * m * n)
            w_center += (16 * q0) / (np.pi**6 * D * m * n * term_denom)
            
    return w_center

# Example: Aluminum plate for a book press
# 200mm x 200mm, 5mm thick, 10kN/m^2 load
defl = calculate_plate_deflection(a=0.2, b=0.2, h=0.005, E=70e9, nu=0.33, q0=10000)

print(f"Max Deflection at Center: {defl*1000:.4f} mm")
