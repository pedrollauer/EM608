from Pynite import FEModel3D

def build_base_beam():
    """Helper function to build the nodes, supports, and members."""
    model = FEModel3D()
    
    # 1. Define Material: Steel
    # Density (rho=7850) is strictly required for the modal analysis!
    model.add_material('Steel', E=200e9, G=77e9, nu=0.3, rho=7850)

    # 2. Define the Cross-section
    Iy, Iz, J, A = 0.0001, 0.0001, 0.00005, 0.005
    model.add_section('BeamSection', A=A, Iy=Iy, Iz=Iz, J=J)

    # 3. Define Nodes (10m total length, supports at 0, 5, and 10)
    model.add_node('Node1', 0, 0, 0)
    model.add_node('Node2', 5, 0, 0)
    model.add_node('Node3', 10, 0, 0)

    # 4. Define Supports
    # Pinning DZ and RX to prevent matrix instability.
    model.def_support('Node1', support_DX=True, support_DY=True, support_DZ=True, support_RX=True, support_RY=False, support_RZ=False)
    model.def_support('Node2', support_DX=False, support_DY=True, support_DZ=True, support_RX=True, support_RY=False, support_RZ=False)
    model.def_support('Node3', support_DX=False, support_DY=True, support_DZ=True, support_RX=True, support_RY=False, support_RZ=False)

    # 5. Define Members
    model.add_member('Span1', 'Node1', 'Node2', 'Steel', 'BeamSection')
    model.add_member('Span2', 'Node2', 'Node3', 'Steel', 'BeamSection')
    
    return model

def analyze_beam_system():
    # ==========================================
    # STEP 1: Find the Max Deflection Location
    # ==========================================
    model_uniform = build_base_beam()
    
    # Apply uniform downward load (-5000 N/m)
    model_uniform.add_member_dist_load('Span1', 'Fy', -5000, -5000)
    model_uniform.add_member_dist_load('Span2', 'Fy', -5000, -5000)
    
    model_uniform.analyze()
    
    max_defl = 0.0
    target_span = ""
    target_x = 0.0
    
    # Robustly sample the beam to find the max deflection and its 'x' location
    for span_name in ['Span1', 'Span2']:
        member = model_uniform.members[span_name]
        length = member.L() if callable(member.L) else member.L
        
        for i in range(101):
            x = i * length / 100.0
            defl = member.deflection('dy', x)
            if defl < max_defl:
                max_defl = defl
                target_span = span_name
                target_x = x

    # Handle both string names and direct Node objects
    i_node = model_uniform.members[target_span].i_node
    if isinstance(i_node, str):
        start_node_x = model_uniform.nodes[i_node].X
    else:
        start_node_x = i_node.X 

    global_x = start_node_x + target_x

    print("--- 1. UNIFORM LOAD ANALYSIS ---")
    print(f"Largest downward deflection occurs on {target_span}.")
    print(f"Local position: x = {target_x:.3f} m (Global X = {global_x:.3f} m)")
    print(f"Deflection value: {max_defl * 1000:.2f} mm")

    # ==========================================
    # STEP 2: Calculate Local Spring Constant
    # ==========================================
    model_stiffness = build_base_beam()
    
    # Apply a virtual point load (10 kN) exactly at the weakest point
    test_load = -10000 
    model_stiffness.add_member_pt_load(target_span, 'Fy', test_load, target_x)
    
    model_stiffness.analyze()
    
    # Get the resulting deflection at that exact local position
    test_defl = model_stiffness.members[target_span].deflection('dy', target_x)
    spring_constant = abs(test_load / test_defl)
    
    print("\n--- 2. STIFFNESS RESULTS ---")
    print(f"Test Load Applied: {abs(test_load):,.0f} N")
    print(f"Resulting Local Deflection: {test_defl * 1000:.3f} mm")
    print(f"Equivalent Spring Constant (k): {spring_constant:,.2f} N/m")

    # ==========================================
    # STEP 3: Modal Analysis
    # ==========================================
    # A beam with nodes ONLY at the supports has no free Y-direction nodes 
    # to vibrate, making it "massless". We must discretize (mesh) it!
    
    model_modal = FEModel3D()
    model_modal.add_material('Steel', E=200e9, G=77e9, nu=0.3, rho=7850)
    Iy, Iz, J, A = 0.0001, 0.0001, 0.00005, 0.005
    model_modal.add_section('BeamSection', A=A, Iy=Iy, Iz=Iz, J=J)
    
    # Split the 10m beam into 20 elements (0.5m each)
    for i in range(21):
        x = i * 0.5
        node_name = f'N{i}'
        model_modal.add_node(node_name, x, 0, 0)
        
        # Apply supports at exactly 0.0m, 5.0m, and 10.0m
        if x in [0.0, 5.0, 10.0]:
            # Pin Y. Pin X only at the start.
            model_modal.def_support(node_name, support_DX=(x==0.0), support_DY=True, support_DZ=True, support_RX=True, support_RY=False, support_RZ=False)
        else:
            # FREE internal nodes! Just pin Z and twist to keep the vibration 2D
            model_modal.def_support(node_name, support_DX=False, support_DY=False, support_DZ=True, support_RX=True, support_RY=False, support_RZ=False)

    # Create the small members connecting the nodes
    for i in range(20):
        model_modal.add_member(f'Elem{i}', f'N{i}', f'N{i+1}', 'Steel', 'BeamSection')

    # KEY FIX: Tell PyNite to compile the physical members into mathematical elements
    model_modal.analyze()

    # Now the compiled internal nodes have free mass to vibrate!
    frequencies = model_modal.analyze_modal(num_modes=3, mass_direction='Y')
    
    print("\n--- 3. MODAL ANALYSIS ---")
    for i, freq in enumerate(frequencies):
        print(f"Mode {i+1} Natural Frequency: {freq:.2f} Hz")
    
    print("\n--- 3. MODAL ANALYSIS ---")
    for i, freq in enumerate(frequencies):
        print(f"Mode {i+1} Natural Frequency: {freq:.2f} Hz")

if __name__ == "__main__":
    analyze_beam_system()

