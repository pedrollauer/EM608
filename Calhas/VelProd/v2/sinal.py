import numpy as np
from scipy.fft import fft, fftfreq
import v2 as vp
import cond as cd
import math as m

from scipy.integrate import solve_ivp

def slipping(A, B, a, b, omega):
    """
    Checks parameters, then numerically solves for the ABSOLUTE horizontal
    and vertical acceleration, velocity, and displacement profiles of the mass.
    """
    g = 9.81     # Gravity (m/s^2)
    mu = 0.3     # Friction coefficient
    
    # 1. Precondition Check
    if B > g:
        print(f"[-] Fly-off detected (B = {B:.2f} > g = {g}). Quitting.")
        return None
        
    T = 2 * np.pi / omega
    t_span = (0, T)
    t_eval = np.linspace(0, T, 1000)
    
    # Check if slipping actually occurs
    t_check = np.linspace(0, T, 500)
    demand = np.abs(A * np.cos(omega * t_check + a))
    capacity = mu * (g + B * np.sin(omega * t_check + b))
    if np.all(demand <= capacity):
        print("[-] Slipping condition NOT met. Mass sticks perfectly. Quitting.")
        return None

    print("[+] Solving for ABSOLUTE motion profiles...")
    print("=" * 60)

    # 2. State Space Equations [Absolute Displacement, Absolute Velocity] -> [X_m, V_xm]
    def absolute_dynamics(t, state):
        X_m = state[0]
        V_xm = state[1]
        
        # Calculate the plane's analytical horizontal velocity at time t
        V_xp = (A / omega) * np.sin(omega * t + a) - (A / omega) * np.sin(a)
        
        # Relative velocity determines friction direction
        x_dot = V_xm - V_xp
        
        if np.abs(x_dot) < 1e-6:
            friction_sign = 0.0
        else:
            friction_sign = np.sign(x_dot)
            
        # Absolute horizontal acceleration is governed completely by friction
        X_m_ddot = -mu * (g + B * np.sin(omega * t + b)) * friction_sign
        
        return [V_xm, X_m_ddot]

    # Initial absolute conditions [X_m(0) = 0, V_xm(0) = 0]
    initial_conditions = [0.0, 0.0]
    
    sol = solve_ivp(absolute_dynamics, t_span, initial_conditions, t_eval=t_eval, 
                     method='RK45', rtol=1e-6, atol=1e-8)

    # 3. Extract Horizontal Data
    X_disp_abs = sol.y[0]
    V_tx_abs = sol.y[1]
    
    X_acc_abs = np.zeros_like(sol.t)
    for i, t_val in enumerate(sol.t):
        _, x_m_ddot = absolute_dynamics(t_val, [X_disp_abs[i], V_tx_abs[i]])
        X_acc_abs[i] = x_m_ddot

    # 4. Compute Analytical Vertical Absolute Motion (Since locked to plane)
    Y_acc_abs = B * np.sin(omega * sol.t + b)
    Y_vel_abs = (-B / omega) * np.cos(omega * sol.t + b) + (B / omega) * np.cos(b)
    Y_disp_abs = (-B / omega**2) * np.sin(omega * sol.t + b) + (B / omega) * np.cos(b) * sol.t + (B / omega**2) * np.sin(b)

    # 5. Compute Metrics over One Cycle
    avg_vel_x_abs = np.trapz(V_tx_abs, sol.t) / T
    avg_vel_y_abs = np.trapz(Y_vel_abs, sol.t) / T
    
    net_disp_x_abs = X_disp_abs[-1] - X_disp_abs[0]
    net_disp_y_abs = Y_disp_abs[-1] - Y_disp_abs[0]

    # 6. Output Summary Data
    print(f"Cycle Period (T):          {T:.4f} seconds")
    print(f"Net Absolute X Disp:       {net_disp_x_abs:.6f} meters")
    print(f"Net Absolute Y Disp:       {net_disp_y_abs:.6f} meters")
    print(f"Avg Absolute X Velocity:   {avg_vel_x_abs:.6f} m/s")
    print(f"Avg Absolute Y Velocity:   {avg_vel_y_abs:.6f} m/s")
    print("=" * 60)

    return {
        "time": sol.t,
        "abs_x_acc": X_acc_abs,
        "abs_x_vel": V_tx_abs,
        "abs_x_disp": X_disp_abs,
        "abs_y_disp": Y_disp_abs
    }

def solve_fly_off_motion(A, B, a, b, omega):
    """
    Checks for the fly-off condition of a mass on a vibrating plane.
    If met, analytically solves the acceleration, velocity, and displacement 
    profiles for exactly one full cycle.
    
    Plane Profiles:
      X_acc = A * cos(omega * t + a)
      Y_acc = B * sin(omega * t + b)
    """
    # 1. Define physical constants inside the function
    g = 9.81     # Gravity (m/s^2)
    
    # 2. Check the Fly-Off Condition
    if B <= g:
        print(f"[-] Fly-off condition NOT met (B = {B:.2f} m/s² <= g = {g} m/s²).")
        print("    The plane does not drop fast enough. Quitting function.")
        return None

    print(f"[+] Fly-off condition MET (B = {B:.2f} m/s² > g = {g} m/s²).")
    print("    Analyzing pure ballistic flight trajectories over 1 cycle...")
    print("=" * 60)
    
    # 3. Setup time grid for one full cycle
    T = 2 * np.pi / omega
    t = np.linspace(0, T, 1000)
    
    # 4. Set baseline initial conditions at t = 0 (Launch phase context)
    # For a clean cycle visualization, we assume ground zero starting points:
    Xm0, Vxm0 = 0.0, 0.0
    Ym0, Vym0 = 0.0, 0.0
    
    # 5. Calculate Absolute Motion of the Mass (Free Fall / Projectile Dynamics)
    # Absolute Accelerations
    X_acc_abs = np.zeros_like(t)       # No horizontal forces during flight
    Y_acc_abs = np.full_like(t, -g)    # Pure gravity
    
    # Absolute Velocities (Analytical integration from t=0)
    X_vel_abs = np.full_like(t, Vxm0)
    Y_vel_abs = Vym0 - g * t
    
    # Absolute Displacements (Analytical integration from t=0)
    X_disp_abs = Xm0 + Vxm0 * t
    Y_disp_abs = Ym0 + Vym0 * t - 0.5 * g * t**2
    
    # 6. Calculate Plane Kinematics for Reference (Analytical Integrals)
    # X Plane Kinematics
    X_acc_p = A * np.cos(omega * t + a)
    X_vel_p = (A / omega) * np.sin(omega * t + a) - (A / omega) * np.sin(a)
    X_disp_p = (-A / omega**2) * np.cos(omega * t + a) - (A / omega) * np.sin(a) * t + (A / omega**2) * np.cos(a)
    
    # Y Plane Kinematics
    Y_acc_p = B * np.sin(omega * t + b)
    Y_vel_p = (-B / omega) * np.cos(omega * t + b) + (B / omega) * np.cos(b)
    Y_disp_p = (-B / omega**2) * np.sin(omega * t + b) + (B / omega) * np.cos(b) * t + (B / omega**2) * np.sin(b)
    
    # 7. Calculate Relative Motion Profiles (Mass relative to Plane)
    # x = X_m - X_p
    x_acc_rel = X_acc_abs - X_acc_p
    x_vel_rel = X_vel_abs - X_vel_p
    x_disp_rel = X_disp_abs - X_disp_p
    
    # y = Y_m - Y_p
    y_acc_rel = Y_acc_abs - Y_acc_p
    y_vel_rel = Y_vel_abs - Y_vel_p
    y_disp_rel = Y_disp_abs - Y_disp_p
    
    # 8. Compute Cycle Statistics
    avg_vel_x_rel = np.trapz(x_vel_rel, t) / T
    avg_vel_y_rel = np.trapz(y_vel_rel, t) / T
    net_disp_x_rel = x_disp_rel[-1] - x_disp_rel[0]
    
    # 9. Output Summary Data
    print(f"Cycle Period (T):          {T:.4f} seconds")
    print(f"Net Relative X Disp:       {net_disp_x_rel:.6f} meters")
    print(f"Avg Relative X Velocity:   {avg_vel_x_rel:.6f} m/s")
    print(f"Avg Relative Y Velocity:   {avg_vel_y_rel:.6f} m/s")
    print("=" * 60)
    
    # Return structured simulation profiles for tracking or checking
    return {
        "time": t,
        "rel_x_acc": x_acc_rel,
        "rel_x_vel": x_vel_rel,
        "rel_x_disp": x_disp_rel,
        "rel_y_disp": y_disp_rel
    }


def analisar_acelerometro(arquivo):
    data = np.loadtxt(arquivo, skiprows=1)
    
    t = data[:, 0]
    ax = data[:, 1]
    ay = data[:, 2]
    az = data[:, 3]
    
    #O sinal está tratado?
    media = np.mean(ay)
    tratado = "Sinal tratado."
    if(media > 1):
        tratado = "Sinal não tratado."
        ax = ax - np.mean(ax)
        ay = ay - np.mean(ay)
        az = az - np.mean(ay)

    print(f"Dado tratado: {media}")
    n = len(t)
    dt = t[1] - t[0]  
    
    def obter_dominante(sinal):
        yf = fft(sinal)
        xf = fftfreq(n, dt)
        
        pos_mask = xf > 0
        xf_pos = xf[pos_mask]
        yf_pos = np.abs(yf[pos_mask])
        
        idx_max = np.argmax(yf_pos)
        f_Hz = xf_pos[idx_max]
        
        amplitude = 2.0 * np.abs(yf[pos_mask][idx_max]) / n
        fase = np.angle(yf[pos_mask][idx_max])
        
        return f_Hz, amplitude, fase

    f_maior, A, fase_x = obter_dominante(ax)
    _, B, fase_y = obter_dominante(ay)
    _, C, fase_z = obter_dominante(az)
    
    w = 2 * np.pi * f_maior
    
    angulo = m.degrees(m.atan2(A, B))
    
    print("============== VEL Prod =========================")
    print("Vel Prod 1.0")

    print(f"--- Funções do Acelerômetro (Frequência: {f_maior:.2f} Hz) ---")
    print(f"w = {w:.4f} rad/s")
    print(f"ax = {A:.4f} * cos({w:.4f}t + {fase_x:.4f})")
    print(f"ay = {B:.4f} * cos({w:.4f}t + {fase_y:.4f})")
    print(f"az = {C:.4f} * cos({w:.4f}t + {fase_z:.4f})")
    print(f"Ângulo de aplicação de força: {angulo: 2f}")
    print(f"Condicionamento do sinal: {tratado}")

    print("")
    #vp.vel_prod(A,B,f_maior,fase_x, fase_y)
    #cd.motion_regimen()
    cd.motion_regimen(A, B, fase_x, fase_y, w)
    print("====FLYOFF====")
    solve_fly_off_motion(A, B, fase_x, fase_y, w)
    slipping(A, B, fase_x, fase_y, w)

if __name__ == "__main__":
    print("==================== Calha Boa 1=========================")
    analisar_acelerometro('b_1.txt')
    print("\n\n")
    print("==================== Calha Boa 2=========================")
    analisar_acelerometro('b_2.txt')
    print("\n\n")
    print("==================== Calha Boa 3=========================")
    analisar_acelerometro('b_3.txt')
    print("\n\n")

    print("==================== Calha Ruim =========================")
    analisar_acelerometro('r_1.txt')

    print("==================== Calha Ruim =========================")
    analisar_acelerometro('r_2.txt')

    print("==================== Calha Ruim =========================")
    analisar_acelerometro('r_3.txt')




