import numpy as np
from scipy.integrate import solve_ivp


# ==========================================
# 2. PLANE KINEMATICS FUNCTIONS
# ==========================================

# ==========================================
# 3. SYSTEM DYNAMICS (ODEs)
# ==========================================

def vel_prod(A,B,w, a, b):
# ==========================================
# 1. PARAMETERS & INITIAL CONDITIONS
# ==========================================
# Plane parameters
    omega = w

# Friction and Gravity
    mu = 0.3     # Friction coefficient (assumed mu_s = mu_k for simplicity)
    g = 9.81     # Gravity (m/s^2)

# Time definitions (Exactly 1 cycle)
    T = 2 * np.pi / omega
    t_span = (0, T)
    t_eval = np.linspace(0, T, 1000)

# Initial conditions of the mass (Absolute coordinates)
# [X_m, Y_m, V_xm, V_ym]
    initial_state = [0.0, 0.0, 0.0, 0.0]

    print("ADOOOORNO")
    def dynamics(t, state):
        X_m, Y_m, V_xm, V_ym = state
        
        # Get current plane kinematics
        a_p = plane_acc(t)
        v_p = plane_vel(t)
        
        # Calculate relative velocity
        v_rel = np.array([V_xm - v_p[0], V_ym - v_p[1]])
        v_rel_norm = np.linalg.norm(v_rel)
        
        # Required acceleration to stick perfectly to the plane
        a_req = a_p
        a_req_norm = np.linalg.norm(a_req)
        
        # Threshold for slip condition
        max_friction_acc = mu * g
        
        # Tolerance for determining if relative velocity is practically zero
        tol = 1e-5
        
        if v_rel_norm < tol and a_req_norm <= max_friction_acc:
            # --- STICKING STATE ---
            # The mass moves perfectly with the plane
            ax_m = a_p[0]
            ay_m = a_p[1]
        else:
            # --- SLIPPING STATE ---
            # Friction opposes the direction of relative velocity
            if v_rel_norm < tol:
                # If transitioning from stick to slip, use the direction of required force
                direction = a_req / a_req_norm
            else:
                direction = v_rel / v_rel_norm
                
            ax_m = - max_friction_acc * direction[0]
            ay_m = - max_friction_acc * direction[1]
            
        return [V_xm, V_ym, ax_m, ay_m]


    def plane_acc(t):
        ax_p = A * np.sin(omega * t + a)
        ay_p = B * np.sin(omega * t + b)
        return np.array([ax_p, ay_p])

    def plane_vel(t):
        # Analytical integrals of plane acceleration (assuming C=0 for steady state)
        vx_p = - (A / omega) * np.cos(omega * t + a)
        vy_p = - (B / omega) * np.cos(omega * t + b)
        return np.array([vx_p, vy_p])
# ==========================================
# 4. RUN SIMULATION & COMPUTE AVERAGES
# ==========================================
    sol = solve_ivp(dynamics, t_span, initial_state, t_eval=t_eval, method='RK45', rtol=1e-6)
# Extract results
    X_m_hist = sol.y[0]
    Y_m_hist = sol.y[1]
    V_xm_hist = sol.y[2]
    V_ym_hist = sol.y[3]

# Calculate Net Displacement over 1 cycle
    disp_x = X_m_hist[-1] - X_m_hist[0]
    disp_y = Y_m_hist[-1] - Y_m_hist[0]

# Calculate Average Velocity vector over 1 cycle (Using numerical integration)
    avg_vx = np.trapz(V_xm_hist, sol.t) / T
    avg_vy = np.trapz(V_ym_hist, sol.t) / T

# Check if slip ever occurred
    plane_acc_vals = np.array([plane_acc(t) for t in sol.t])
    plane_acc_norms = np.linalg.norm(plane_acc_vals, axis=1)
    slip_occurred = np.any(plane_acc_norms > (mu * g))

# ==========================================
# 5. DISPLAY RESULTS
# ==========================================
    print(f"--- Simulation Results over One Cycle (T = {T:.4f} s) ---")
    print(f"Slip condition met during cycle?: {slip_occurred}")
    print(f"Net Displacement X: {disp_x:.6f} m")
    print(f"Net Displacement Y: {disp_y:.6f} m")
    print(f"Average Velocity X: {avg_vx:.6f} m/s")
    print(f"Average Velocity Y: {avg_vy:.6f} m/s")
