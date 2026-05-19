import numpy as np

def motion_regimen(A, B, a, b, omega):
    """
    Analyzes the motion regimes of a mass on an accelerating vertical/horizontal plane.
    X = Horizontal axis (Prescribed Acc = A * cos(omega * t + a))
    Y = Vertical axis   (Prescribed Acc = B * sin(omega * t + b))
    """
    # Define physical constants inside the function
    g = 9.81     # Acceleration due to gravity (m/s^2)
    mu = 0.3     # Friction coefficient
    
    print("=" * 50)
    print("        PLANE MOTION REGIME ANALYSIS")
    print("=" * 50)
    
    # 1. Check for Fly-Off (Vertical Axis Condition)
    # Fly-off happens if the plane's peak downward acceleration exceeds gravity (B > g)
    if B > g:
        fly_off_possible = True
        min_normal_acc = g - B
        print(f"[!] FLY-OFF WILL OCCUR: Peak vertical acceleration ({B:.2f} m/s²)" 
              f" exceeds gravity ({g} m/s²).")
        print(f"    The normal force will drop to zero when g + B*sin(w*t + b) < 0.")
    else:
        fly_off_possible = False
        min_normal_acc = g - B
        print(f"[*] CONTINUOUS CONTACT: Vertical acceleration ({B:.2f} m/s²)" 
              f" is less than gravity ({g} m/s²).")
        print("    The mass will never leave the surface of the plane.")
        
    print("-" * 50)
    
    # 2. Check for Slip vs. Pure Stick (Horizontal Axis Condition)
    # We evaluate a dense array over one full cycle to find the true peak demand vs capacity
    T = 2 * np.pi / omega
    t = np.linspace(0, T, 2000)
    
    # Instantaneous inertial demand (absolute value of horizontal plane acceleration)
    inertial_demand = np.abs(A * np.cos(omega * t + a))
    
    # Instantaneous maximum static friction capacity (mu * N / m)
    # If fly-off is possible, we clamp the capacity at 0 when the mass loses contact
    normal_profile = g + B * np.sin(omega * t + b)
    friction_capacity = mu * np.maximum(0, normal_profile)
    
    # Determine if demand ever exceeds capacity
    slip_indices = np.where(inertial_demand > friction_capacity)[0]
    
    if len(slip_indices) > 0:
        slips = True
        # Find the first time slip happens in the cycle
        t_slip_start = t[slip_indices[0]]
        print(f"[!] SLIPPING WILL OCCUR: Horizontal inertial demand exceeds friction capacity.")
        if fly_off_possible:
            print("    Mass will experience both slipping and flying phases.")
        else:
            print("    Mass will slide but remain strictly flat on the surface.")
    else:
        slips = False
        print("[*] PURE STICKING: Friction is always strong enough to hold the mass.")
        print("    The mass moves perfectly in sync with the plane horizontally.")

    print("=" * 50)
    
    # Return a dictionary of the boolean states for use in a simulation loop
    return {
        "fly_off_possible": fly_off_possible,
        "slips": slips,
        "min_normal_force_factor": min_normal_acc
    }

#analysis = check_motion_regimes(A=6.0, B=12.0, a=0, b=np.pi/4, omega=5.0)
