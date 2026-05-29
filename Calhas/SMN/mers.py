# =============================================================================
# PROJECT CHRONO - http://projectchrono.org
# Multi-Axis Phase-Shifted Industrial Vibration Sandbox
# =============================================================================

print("Project Chrono Sandbox: Phase-Shifted Multi-Axis Floor Oscillation")

import pychrono as chrono
import pychrono.irrlicht as chirr

# 1. Create a physical system
my_system = chrono.ChSystemNSC()
my_system.SetGravitationalAcceleration(chrono.ChVector3d(0, -9.81, 0))
my_system.SetCollisionSystemType(chrono.ChCollisionSystem.Type_BULLET)

# 2. Create a shared contact material
material = chrono.ChContactMaterialNSC()
material.SetFriction(0.3)
material.SetCompliance(0)

# =============================================================================
# ADD BODY A (The Oscillating Floor Slab)
# =============================================================================
bodyA = chrono.ChBody()
bodyA.SetMass(20)
bodyA.SetName('FloorSlab')
bodyA.SetInertiaXX(chrono.ChVector3d(10, 10, 10))
bodyA.SetPos(chrono.ChVector3d(0, -1, 0))  # Set physical initial coordinate placement

# Physical contact geometry
shapeA = chrono.ChCollisionShapeBox(material, 10, 1, 10)
bodyA.AddCollisionShape(shapeA)

# 3D Window Mesh geometry
visualA = chrono.ChVisualShapeBox(10, 1, 10)
bodyA.AddVisualShape(visualA)

# Unfix the body so the kinematic constraint link can drive it execution paths
bodyA.SetFixed(False)
bodyA.EnableCollision(True)
my_system.Add(bodyA)

# =============================================================================
# KINEMATIC MOTION LINK SETUP (Single Imposed Link)
# =============================================================================
# Absolute static universe anchor
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
motion_spatial.SetFunctionY(pos_profile_y)  # Oscillates smoothly around local relative zero

# --- Z-Axis Position Profile: Explicitly lock displacement tracking to zero ---
motion_spatial.SetFunctionZ(chrono.ChFunctionConst(0.0))

# Attach the coordinate container to the kinematic link
motion_link.SetPositionFunction(motion_spatial)

# INITIALIZATION FIX: Initialize the link frame translation directly at Y = -1.0. 
# This shifts the local "0" references of the sine waves down to the floor's plane.
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
bodyB.SetPos(chrono.ChVector3d(0, 1, 0))  # Spawned high up to drop onto the floor

# Physical contact geometry
shapeB = chrono.ChCollisionShapeBox(material, 1, 1, 1)
bodyB.AddCollisionShape(shapeB)

# 3D Window Mesh geometry
visualB = chrono.ChVisualShapeBox(1, 1, 1)
bodyB.AddVisualShape(visualB)

bodyB.EnableCollision(True)
my_system.Add(bodyB)

# =============================================================================
# INITIALIZE IRR_LICHT 3D VIEWPORT CONTEXT
# =============================================================================
vis = chirr.ChVisualSystemIrrlicht()
vis.AttachSystem(my_system)
vis.SetWindowSize(1024, 768)
vis.SetWindowTitle("Project Chrono - Stable Multi-Axis Vibration")
vis.Initialize()

# Position camera looking downward at the simulation space origin
vis.AddCamera(chrono.ChVector3d(0, 6, -10), chrono.ChVector3d(0, 0, 0))
vis.AddTypicalLights()

# =============================================================================
# SIMULATION RENDERING LOOP
# =============================================================================
# =============================================================================
# OPTIMIZED RENDERING LOOP WITH POSITION LOGGING
# =============================================================================
time_step = 0.001       # Internal physics time step (1ms)
render_step = 0.016     # Visual refresh target (~60 FPS / 16ms)
render_timer = 0.0      # Tracking clock accumulation

# Counter to throttle the terminal prints so they don't lag the simulation
log_step = 0.1          # Log data to terminal every 100ms
log_timer = 0.0

while vis.Run():
    # 1. Visual Render Control (~60 FPS)
    if render_timer >= render_step:
        vis.BeginScene()
        vis.Render()
        vis.EndScene()
        render_timer = 0.0

    # 2. Terminal Logging Control (Every 100ms)
    if log_timer >= log_step:
        current_time = my_system.GetChTime()
        pos = bodyB.GetPos()
        print(f"Time: {current_time:.2f}s | Box B Position -> X: {pos.x:6.3f} | Y: {pos.y:6.3f} | Z: {pos.z:6.3f}")
        log_timer = 0.0

    # 3. Advance Physics System
    my_system.DoStepDynamics(time_step)

    # Accumulate timers
    render_timer += time_step
    log_timer += time_step


# =============================================================================
# HEADLESS SIMULATION ENGINE LOOP (No 3D Rendering)
# =============================================================================
# time_step = 0.001       # Internal physics integration time step (1ms)
# duration = 1000          # Stop the simulation automatically after 5 seconds
# log_step = 0.1          # Print to console every 100ms
# log_timer = 0.0
#
# print("\nStarting simulation in headless data mode...")
# print("Time(s) | Box B Coordinates")
# print("---------------------------------------")
#
# while my_system.GetChTime() < duration:
#     # Check if it's time to log the position metrics
#     if log_timer >= log_step:
#         current_time = my_system.GetChTime()
#         pos = bodyB.GetPos()
#         print(f"{current_time:6.2f}s | X: {pos.x:6.3f} | Y: {pos.y:6.3f} | Z: {pos.z:6.3f}")
#         log_timer = 0.0
#
#     # Advance the physics loop forward at maximum processing speed
#     my_system.DoStepDynamics(time_step)
#
#     # Increment our terminal logging clock
#     log_timer += time_step
#
# print("\nSimulation complete! Data pipeline closed.")
