# =============================================================================
# PROJECT CHRONO - http://projectchrono.org
# Fully Fixed Multi-Axis Oscillation & 3D Visualizer Script
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
bodyA.SetPos(chrono.ChVector3d(0, -1, 0))

# Physical contact geometry
shapeA = chrono.ChCollisionShapeBox(material, 10, 1, 10)
bodyA.AddCollisionShape(shapeA)

# 3D Window Mesh geometry
visualA = chrono.ChVisualShapeBox(10, 1, 10)
bodyA.AddVisualShape(visualA)

# Unfix the body so the kinematic constraint link can drive it
bodyA.SetFixed(False)
bodyA.EnableCollision(True)
my_system.Add(bodyA)

# =============================================================================
# KINEMATIC MOTION LINK SETUP (Phase-Shifted Acceleration)
# =============================================================================
# =============================================================================
# KINEMATIC MOTION LINK SETUP (Stable Multi-Motor Configuration)
# =============================================================================
# 1. Create an intermediate dummy body to isolate the X and Y translations
# This keeps the two single-axis motors from fighting over the same coordinates.
int_body = chrono.ChBody()
int_body.SetFixed(False)
int_body.SetMass(1)
my_system.Add(int_body)

# 2. Create an absolute stationary anchor ground body
ground = chrono.ChBody()
ground.SetFixed(True)
my_system.Add(ground)

# -----------------------------------------------------------------------------
# MOTOR 1: Drives Horizontal Oscillation (X-Axis) between Ground and Intermediate Body
# -----------------------------------------------------------------------------
motor_x = chrono.ChLinkMotorLinearPosition()
motor_x.Initialize(int_body, ground, chrono.ChFramed(chrono.ChVector3d(0, -1.0, 0), chrono.QuatFromAngleY(chrono.CH_PI_2)))

vx_amplitude = 30 / 377  
speed_profile_x = chrono.ChFunctionSine(377, vx_amplitude)
speed_profile_x.SetPhase(-chrono.CH_PI_2)  
motor_x.SetMotionFunction(speed_profile_x)
my_system.Add(motor_x)

# -----------------------------------------------------------------------------
# MOTOR 2: Drives Vertical Oscillation (Y-Axis) between Intermediate Body and Floor Plate
# -----------------------------------------------------------------------------
motor_y = chrono.ChLinkMotorLinearPosition()
# Note: Pointing the motor frame along the Z-axis vector up ensures it acts vertically (Y-Axis)
motor_y.Initialize(bodyA, int_body, chrono.ChFramed(chrono.ChVector3d(0, -1.0, 0), chrono.QuatFromAngleX(chrono.CH_PI_2)))

vy_amplitude = 20 / 377  
speed_profile_y = chrono.ChFunctionSine(377, vy_amplitude)

target_phase_angle = chrono.CH_PI_4  
speed_profile_y.SetPhase(-chrono.CH_PI_2 + target_phase_angle)
motor_y.SetMotionFunction(speed_profile_y)
my_system.Add(motor_y)

# =============================================================================
# ADD BODY B (The Falling Box)
# =============================================================================
bodyB = chrono.ChBody()
bodyB.SetName('FallingBox')
bodyB.SetPos(chrono.ChVector3d(0, 4, 0))  # Placed high enough to watch the floor cycle

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
vis.SetWindowTitle("Project Chrono - Multi-Axis Acceleration Sandbox")
vis.Initialize()

# Position the visual camera looking down at the moving system
vis.AddCamera(chrono.ChVector3d(0, 6, -10), chrono.ChVector3d(0, 0, 0))
vis.AddTypicalLights()

# =============================================================================
# SIMULATION RENDERING LOOP
# =============================================================================
while vis.Run():
    vis.BeginScene()      # Flush display graphics buffer
    vis.Render()          # Re-rasterize all active ChVisualShapes
    vis.EndScene()        # Swap image processing memory pages
    
    # Run the core solver loop forward at a 10-millisecond step
    my_system.DoStepDynamics(0.001)
# print("Second tutorial: create and populate a physical system with 3D Viewer")
#
# import pychrono as chrono
# import pychrono.irrlicht as chirr  # <-- IMPORT THE VISUALIZER LAYER
#
# # 1. Create a physical system
# my_system = chrono.ChSystemNSC()
# my_system.SetGravitationalAcceleration(chrono.ChVector3d(0, -9.81, 0))
# my_system.SetCollisionSystemType(chrono.ChCollisionSystem.Type_BULLET)
#
# # 2. Create a contact material
# material = chrono.ChContactMaterialNSC()
# material.SetFriction(0.3)
# material.SetCompliance(0)
#
# # =============================================================================
# # ADD BODY A (The Fixed Floor)
# # =============================================================================
# bodyA = chrono.ChBody()
# bodyA.SetMass(20)
# bodyA.SetName('BodyA')
# bodyA.SetInertiaXX(chrono.ChVector3d(10, 10, 10))
# bodyA.SetPos(chrono.ChVector3d(0, -1, 0))
#
# shapeA = chrono.ChCollisionShapeBox(material, 10, 1, 10)
# bodyA.AddCollisionShape(shapeA)
#
# # ADD VISUAL SHAPE FOR EYE CANDY: Without this, the body is a physical ghost in the 3D window!
# visualA = chrono.ChVisualShapeBox(10, 1, 10)
# bodyA.AddVisualShape(visualA)
#
# bodyA.SetFixed(False)
# bodyA.EnableCollision(True)
# my_system.Add(bodyA)
#
# # 1. Create a completely stationary anchor body for the system
# # 1. Create a completely stationary anchor body for the system
# # 1. Create a stationary ground anchor body
# ground = chrono.ChBody()
# ground.SetFixed(True)
# my_system.Add(ground)
#
# # 2. Use a Speed Motor instead of Imposed Motion
# motion_link = chrono.ChLinkMotorLinearSpeed()
#
# # 3. Define parameters matching your target acceleration
# # Let's say target max acceleration A = 2.0 m/s^2 at frequency w = 5.0 rad/s
# amplitude_acc = 40
# frequency = 376
#
# # Calculate the matching velocity amplitude: A / w (2.0 / 5.0 = 0.4 m/s)
# amplitude_vel = amplitude_acc / frequency
#
# # 4. Create the integrated velocity profile: v(t) = -0.4 * cos(5*t)
# # Note: ChFunctionSine with a phase shift of -PI/2 is mathematically a negative cosine!
# speed_profile = chrono.ChFunctionSine(frequency, amplitude_vel)
# speed_profile.SetPhase(-chrono.CH_PI_2)
#
# # 5. Assign the function to guide the motor speed channel
# motion_link.SetSpeedFunction(speed_profile)
#
# # 6. Initialize the linear motor acting along the X-axis direction
# motion_link.Initialize(
#     bodyA, 
#     ground, 
#     chrono.ChFramed(chrono.ChVector3d(0, -1, 0), chrono.QuatFromAngleY(chrono.CH_PI_2))
# )
# my_system.Add(motion_link)
# # ground = chrono.ChBody()
# # ground.SetFixed(True)
# # my_system.Add(ground)
# #
# # # 2. Create the moving link
# # motion_link = chrono.ChLinkMotionImposed()
# #
# # # 3. Create a multi-dimensional function split across X, Y, and Z axes
# # motion_spatial = chrono.ChFunctionPositionXYZFunctions()
# #
# # # 4. Define your sine wave math (Frequency = 5.0 rad/s, Amplitude = 2.0 meters)
# # sine_wave_x = chrono.ChFunctionSine(5.0, 2.0)
# # sine_wave_y = chrono.ChFunctionSine(5.0, 2.0)
# #
# # # 5. Route the sine wave directly into the X-axis tracking slot
# # motion_spatial.SetFunctionX(sine_wave_x)
# # motion_spatial.SetFunctionY(sine_wave_y)
# #
# # # 6. Set the position track function target reference
# # motion_link.SetPositionFunction(motion_spatial)
# #
# # # 7. Lock the link at the floor's initial coordinate center
# # motion_link.Initialize(ground, bodyA, chrono.ChFramed(chrono.ChVector3d(0, -1, 0)))
# # my_system.Add(motion_link)
# # 1. Create a completely stationary anchor body for the system
# # =============================================================================
# # ADD BODY B (The Falling Box)
# # =============================================================================
# bodyB = chrono.ChBody()
# bodyB.SetName('BodyB')
# bodyB.SetPos(chrono.ChVector3d(0, 3, 0)) # Spawned a bit higher for better viewing
#
# shapeB = chrono.ChCollisionShapeBox(material, 1, 1, 1)
# bodyB.AddCollisionShape(shapeB)
#
# # ADD VISUAL SHAPE FOR EYE CANDY
# visualB = chrono.ChVisualShapeBox(1, 1, 1)
# bodyB.AddVisualShape(visualB)
#
# bodyB.EnableCollision(True)
# my_system.Add(bodyB)
#
#
# # =============================================================================
# # INITIALIZE THE 3D WINDOW CONTEXT
# # =============================================================================
# # Create the window manager object linked to our core physical system
# vis = chirr.ChVisualSystemIrrlicht()
# vis.AttachSystem(my_system)
# vis.SetWindowSize(1024, 768)
# vis.SetWindowTitle("Project Chrono 3D Physics Sandbox")
# vis.Initialize()
#
# # Set up the camera position and target direction
# vis.AddCamera(chrono.ChVector3d(0, 5, -8), chrono.ChVector3d(0, 0, 0))
# vis.AddTypicalLights()
#
# # =============================================================================
# # SIMULATION RENDERING LOOP
# # =============================================================================
# # The loop runs dynamically as long as you keep the 3D GUI window open
# while vis.Run():
#     vis.BeginScene()      # Clear the screen buffers
#     vis.Render()          # Automatically draws all ChVisualShapes (Floor & Box)
#     vis.EndScene()        # Swap frames to push output to your display monitor
#
#     # Advance the engine clock by 10 milliseconds
#     my_system.DoStepDynamics(0.01)
