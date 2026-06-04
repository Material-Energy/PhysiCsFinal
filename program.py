Web VPython 3.2


scene = canvas(width=800, height=600, align="left", background = color.gray(0.9), resizable = False)
scene.forward = vec(0, -1, 1)

init_camera = [
    scene.camera.pos,
    scene.camera.axis,
    scene.forward,
    scene.range
]

    
# constants
L = 0.02 # height of loop (m)
r = 0.025 # radius of loop (m)


num_loops = 4
num_turns = 1
offset = pi / num_loops
angles = [offset * i for i in range(num_loops)] # how much to rotate each loop from first loop
total_segments = 2 * num_loops # total commutator segments

# vectors
B_vec = vec(1, 0, 0)
lf = vec(0, 0, 0)
rf = vec(0, 0, 0)


# time stuff
dt = 1/60
xmax = 3.0


commutator_angles = []

running = False
init = True


# sliders
def update_sliders(evt):
    global I, B, V, R
    
    if evt.id == "I":
        I = round(evt.value)
        slider_text[0].text = f"Rotational Inertia: 10<sup>{I}</sup> <i>kg&middot;m<sup>2</sup></i>\n\n"
        I = 10 ** I

    elif evt.id == "B":
        B = round(evt.value)
        slider_text[1].text = f"Magnetic Field: {B} <i>T</i> \n\n"
       
    elif evt.id == "V":
        V = round(evt.value)
        slider_text[2].text = f"Source Voltage: {V} <i>V</i> \n\n"
        
    elif evt.id == "R":
        R =round(evt.value)
        slider_text[3].text = f"Equivalent Resistance: {R} <i>&Omega;</i> \n\n"
    







# Run / Pause
def toggle_run(evt):
    global sliders, running
    
    if running:
        run_button.text = "Run"
        run_button.background = color.green
        for s in sliders: s.disabled = False
        
    else:
        run_button.text = "Pause"
        run_button.background = color.red
        for s in sliders: s.disabled = True
        

    running = not running
        

run_button = button(bind=toggle_run, text="Run", background=color.green, pos=scene.title_anchor)


# Reset
reset_button = button(bind=reset, text="Reset", background=color.red, pos=scene.title_anchor)

rotation_axis = vec(0,0,-1).rotate(angle = -3 * pi/4, axis=vec(1, 0, 0))
arrow(axis = rotation_axis)

def make_loop(path, angle):
    
    
    wire = curve(pos=path, radius = 0.1, color=copper)
    wire.rotate(axis=rotation_axis, angle = angle)

    return wire

def calc_domega_dt(omega, theta):
    i_dir = 1
    theta %= (2*pi)
#    print(commutator_angles)
    phi = pi/2 - theta
    
    for i in range(num_loops):
        a1, a2 = commutator_angles[i]
        a3, a4 = commutator_angles[i + num_loops]
        
        
        if (min(a1, a2) <= theta <= max(a1, a2)):
            break
        if (min(a3, a4) <= theta <= max(a3, a4)):
            i_dir = -1
            break
        
        if (i == num_loops - 1):
            i_dir = 0
        
    phi += angles[i] # angle betweeen normal and B
    
    
#    print(f"Using loop {i}")
#    print(f"theta: {theta}")
#    print(f"phi: {phi}")
    
    V_back = num_turns * B * A * omega * sin(phi)

    i_loop = (i_dir * V - V_back) / R
        
    F_B = i_loop * B * L * sin(phi) # Lorentz force on EACH turn
    

    torque = num_turns * 2*r*F_B
    
    domega_dt = torque / I
    
    flux = B * A * cos(phi)
    
    return domega_dt, [V_back, i_loop, F_B, flux, torque]
    
    
def update_arrows(path):
    global lf, rf
    
    lf.visible = False
    rf.visible = False
    
    
    L_vec = path[3]-path[2]
    arrow(axis=L_vec)
    arrow(axis=B_vec)
#    arrow(axis = cross(L_vec, B_vec))
    
    
    midpoint = (path[2] + path[3]) / 2
    lf = arrow(pos=midpoint, axis = 2 * norm(cross(L_vec, B_vec)), shaftwidth=0.1)
    
    midpoint = (path[4] + path[5]) / 2
    L_vec = path[5] - path[4]
    rf = arrow(pos=midpoint, axis = 2 * norm(cross(L_vec, B_vec)), shaftwidth=0.1)
    
    lf.visible = True
    rf.visible = True
    
    
width = 2 * 100*r
height = 100*L
copper = vec(0.961, 0.686, 0.373)


def reset(evt):
    global sliders, slider_text
    global I, B, V, R
    global t, theta, omega
    
    global loops, commutator_segments, stator_parts
    global commutator, stator
    
    global graphs, gcs
    
    global init
    global running
    
    
    
    init_slider_text = [
        "Rotational Inertia: 10<sup>-5</sup> <i>kg&middot;m<sup>2</sup></i>\n\n",
        "Magnetic Field: 1.0 <i>T</i> \n\n",
        "Source Voltage: 5 <i>V</i> \n\n",
        "Equivalent Resistance: 1 <i>&Omega;</i> \n\n"
    ]
    
    init_constants = [
        -5.0, # 10 raised to this number is the moment of inertia of each loop
        1.0, # magnitude of mangetic field from external magnets
        5.0, # source voltage
        1.0 # resistance of wire
    ]
    
    
    if init:
        init = False
        
        
        I_slider = slider(bind=update_sliders, min=-7, max=0, value=init_constants[0], id = "I", align="left")
        I_text = wtext(text = init_slider_text[0])
    
            
        B_slider = slider(bind=update_sliders, min=0, max=10, value=init_constants[1], id = "B", align="left")
        B_text = wtext(text = init_slider_text[1])
  
        
        V_slider = slider(bind=update_sliders, min=0, max=10, value=init_constants[2], id = "V", align="left")
        V_text = wtext(text = init_slider_text[2])
    
         
        R_slider = slider(bind=update_sliders, min=1, max=100, value=init_constants[3], id = "R", align="left")
        R_text = wtext(text = init_slider_text[3])
   
   
        sliders = [I_slider, B_slider, V_slider, R_slider]
        slider_text = [I_text, B_text, V_text, R_text]
        
        
        scene.append_to_caption("\n" * 30)
        
        stator_parts = []
        colors = [color.blue, color.red]
        
        for i in range(2):
            start = i * pi
            
            arc = paths.arc(pos=center, radius = width/2 + width/8, angle1=start-pi/3, angle2=start+pi/3)
            magnet = extrusion(shape=shapes.rectangle(width=0.2, height=3), path=arc, color=colors[i])
            
            arc = paths.arc(pos=center, radius = width/2 + width/8 + 0.2, angle1=start-pi/3, angle2=start+pi/3)
            out = extrusion(shape=shapes.rectangle(width=0.2, height=3), path=arc, color=color.gray(0.7))
            
            stator_parts += [magnet, out]
        
        
        stator = compound(stator_parts)
        stator.rotate(axis=vector(1, 0, 0), angle = 3*pi/4)
        
    
    else:
        scene.camera.pos = init_camera[0]
        scene.camera.axis = init_camera[1]
        scene.forward = init_camera[2]
        scene.range = init_camera[3]
        
        running = True
        toggle_run(evt)
    
        for i in range(len(sliders)):
            sliders[i].value = init_constants[i]
            slider_text[i].text = init_slider_text[i]
#            
        for obj in loops:
            obj.visible = False
            del obj
        
#        print(commutator_segments)
        
        for obj in commutator_segments:
            obj.visible = False
            del obj
            
        commutator.visible = False
        del commutator
 
        for g in graphs: g.delete()
        for c in gcs: c.delete()
        
            
    theta = 0
    omega = 0
    t = 0
    
    I = 10 ** init_constants[0]
    B = init_constants[1]
    V = init_constants[2]
    R = init_constants[3]
    

    # armature
    path = paths.rectangle(width=width, height = height)
    #print(path)
    path.insert(0, path[0]+vec(-width/4, 0, 0))
    path[-1] = path[-2] + vec(width/4, 0, 0)
    
    path.insert(0, path[0]+vec(0, 0, height/2))
    path.append(path[-1]+vec(0, 0, height/2))
    
    for i in range(len(path)):
        path[i] = rotate(path[i], axis=vector(1, 0, 0), angle=-3*pi/4)
    
    loops = []
    
    for i in range(num_loops):
        loops.append(make_loop(path, angles[i]))
        

    #print(wire.slice(0, wire.npoint)[0])
    #print(wire.point(0)['pos'])
    
    # commutators
    wire = loops[0] # make sure first loop always has angle = 0 in make_loop
    center = wire.point(0)['pos'] - vec(wire.point(0)['pos'].x, 0, 0)
    
    commutator_segments = []
    dtheta = 2 * pi / total_segments
    gap = pi/4 / total_segments
    
    for i in range(total_segments):
        start = i * dtheta
        
        angle1 = start - (dtheta-gap) / 2
        angle2 = start + (dtheta-gap) / 2
        
        arc = paths.arc(pos=center, radius = width/4 + 0.1, angle1=angle1+pi, angle2=angle2+pi)
        segment = extrusion(shape=shapes.rectangle(width=0.1, height=2), path=arc, color=copper)
        
        commutator_segments.append(segment)
        
    #    angle1 += 2*pi; angle1 %= (2*pi)
    #    angle2 += 2*pi; angle2 %= (2*pi)
        
        commutator_angles.append((angle1, angle2))
    
    delta = height / sqrt(2)
    center += vec(0, -delta, delta)
    sphere(pos=center, radius=0.1)
    commutator = compound(commutator_segments)
    commutator.rotate(axis=vector(1, 0, 0), angle = 3*pi/4)
    
    
    
    RPM_graph = graph(title = "RPM vs time", xtitle = "t", ytitle = "RPM", scroll=True, xmin = 0, xmax = xmax, width=480, height=360, align="left")
    gc1 = gcurve()
    
    flux_graph = graph(title = "Flux vs time", xtitle = "t", ytitle = "Flux", scroll=True, xmin = 0, xmax = xmax, width=480, height=360)
    gc2 = gcurve()
    
    back_emf_graph = graph(title = "Back-Emf vs time", xtitle = "t", ytitle = "Back-EMF", scroll=True, xmin = 0, xmax = xmax, width=480, height=360)
    gc3 = gcurve()
    
    torque_graph = graph(title = "Torque vs time", xtitle = "t", ytitle = "Torque", scroll=True, xmin = 0, xmax = xmax, width=480, height=360)
    gc4 = gcurve()
    
    graphs = [RPM_graph, flux_graph, back_emf_graph, torque_graph]
    gcs = [gc1, gc2, gc3, gc4]
    

    





reset(None)

# physics stuff
A = 2 * r * L


while True:
#    print(t, omega, theta)
    rate (1/dt)
    
    if (running):
          
        domega_dt_i, _ = calc_domega_dt(omega, theta)
        
        theta_mid = theta + omega * (dt / 2)
        omega_mid = omega + domega_dt_i * (dt / 2)
        
        domega_dt_mid, _ = calc_domega_dt(omega_mid, theta_mid)
        
        
        theta += omega_mid * dt
        omega += domega_dt_mid * dt
        
        t += dt
        
        # update graphed values
        _, graphed_values = calc_domega_dt(omega, theta)
    #    print(f"theta: {theta}")
        
        
    #    update_arrows(path, lf, rf)
        
    #    print(f"Omega*dt: {omega_mid*dt}")
    
    #    print(f"V_back: {V_back:.4f}")
    #    print(f"omega: {omega:.4f}")
    #    print(f"B: {B:.4f}")
    #    print(f"A: {A:.4f}")
    #    print(f"sin(theta): {sin(theta):.4f}")
    #    print(f"i loop: {i_loop:.4f}")
    
    
    
        graphs[0].select()
        gcs[0].plot(t, omega * 60 / (2*pi))
    #    
    #    flux_graph.select()
    #    gc2.plot(t, flux)
    ##    
    #    back_emf_graph.select()
    #    gc3.plot(t, V_back)
    #    
    #    torque_graph.select()
    #    gc4.plot(t, torque)
    
    
        
        
        
        for wire in loops:
            wire.rotate(axis=rotation_axis, angle=omega_mid*dt)
    #    for i in range(len(path)):
    #        path[i] = rotate(path[i], axis=rotation_axis, angle=omega*dt)
    #        
    #    wire.visible = False
    #    wire = curve(pos=path, radius = 0.1, color=bronze)
    #    wire.visible = True
        
        
    #    update_arrows(path, lf, rf)
        
        commutator.rotate(axis=rotation_axis, angle = omega_mid*dt)
        
    
    
    
