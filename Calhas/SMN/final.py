# =============================================================================
# PROJECT CHRONO - http://projectchrono.org
# Headless High-Frequency Multi-Axis Vibration Sandbox
# =============================================================================

print("Project Chrono Sandbox: Phase-Shifted Multi-Axis Floor Oscillation")

import pychrono as chrono

# 1. Create a physical system
my_system = chrono.ChSystemNSC()
my_system.SetGravitationalAcceleration(chrono.ChVector3d(0, -9.81, 0))
my_system.SetCollisionSystemType(chrono.ChCollisionSystem.Type_BULLET)

# 2. Create a shared contact material
material = chrono.ChContactMaterialNSC()
material.SetFriction(0.4)
material.SetCompliance(0)

# =============================================================================
# ADD BODY A (The Oscillating Floor Slab)
# =============================================================================
bodyA = chrono.ChBody()
bodyA.SetMass(20.0)
bodyA.SetName('FloorSlab')
bodyA.SetInertiaXX(chrono.ChVector3d(10, 10, 10))
bodyA.SetPos(chrono.ChVector3d(0, -1.0, 0))  # Physical coordinate center

# Physical contact geometry
shapeA = chrono.ChCollisionShapeBox(material, 10.0, 1.0, 10.0)
bodyA.AddCollisionShape(shapeA)

# Unfix the body so the kinematic constraint link can drive it execution paths
bodyA.SetFixed(False)
bodyA.EnableCollision(True)
my_system.Add(bodyA)

# =============================================================================
# KINEMATIC MOTION LINK SETUP (Single Imposed Link)
# =============================================================================
# FIX: Absolute static universe anchor must be explicitly added to the system container!
ground = chrono.ChBody()
ground.SetFixed(True)
my_system.Add(ground) 

motion_link = chrono.ChLinkMotionImposed()

# Using the multidimensional position container space mapping
motion_spatial = chrono.ChFunctionPositionXYZFunctions()

# Frequency and denominator calculation (w^2)
w = 377.0
denom = w * w  # 142129.0

# --- X-Axis Position Profile: x(t) = - (30 / 377^2) * sin(377 * t) ---
amp_x = -30.0 / denom
pos_profile_x = chrono.ChFunctionSine(w, amp_x)
motion_spatial.SetFunctionX(pos_profile_x)

# --- Y-Axis Position Profile: y(t) = - (20 / 377^2) * sin(377 * t + phase) ---
amp_y = -20.0 / denom
pos_profile_y = chrono.ChFunctionSine(w, amp_y)
target_phase_angle = chrono.CH_PI_4  
pos_profile_y.SetPhase(target_phase_angle)
motion_spatial.SetFunctionY(pos_profile_y)  # Oscillates around local frame center

# --- Z-Axis Position Profile ---
motion_spatial.SetFunctionZ(chrono.ChFunctionConst(0.0))

# Attach the coordinate container to the kinematic link
motion_link.SetPositionFunction(motion_spatial)

# Initialize the link frame translation directly at Y = -1.0 relative to ground
motion_link.Initialize(
    ground, 
    bodyA, 
    chrono.ChFramed(chrono.ChVector3d(0, -1.0, 0), chrono.ChQuaterniond(1, 0, 0, 0))
)
my_system.Add(motion_link)

# =============================================================================
# ADD BODY B (The Falling Box)
# =============================================================================
bodyB = chrono.ChBody()
bodyB.SetName('FallingBox')
bodyB.SetPos(chrono.ChVector3d(0, 4.0, 0))  # Placed high up to track drop velocity

# Physical contact geometry
shapeB = chrono.ChCollisionShapeBox(material, 1.0, 1.0, 1.0)
bodyB.AddCollisionShape(shapeB)

bodyB.SetFixed(False)
bodyB.EnableCollision(True)
my_system.Add(bodyB)

# =============================================================================
# HEADLESS SIMULATION ENGINE LOOP
# =============================================================================
time_step = 0.001       # Internal integration step size (1ms)
duration = 2000.0          # Cap data generation window at 2 seconds
log_step = 0.05         # Output to terminal window every 50ms for fine parsing
log_timer = 0.0

print("\nStarting execution loop...")
print("Time(s) | Box B Coordinates")
print("---------------------------------------")

while my_system.GetChTime() < duration:
    if log_timer >= log_step:
        current_time = my_system.GetChTime()
        pos = bodyB.GetPos()
        print(f"{current_time:6.2f}s | X: {pos.x:6.3f} | Y: {pos.y:6.3f} | Z: {pos.z:6.3f}")
        log_timer = 0.0

    my_system.DoStepDynamics(time_step)
    log_timer += time_step

print("\nSimulation completed successfully.")
