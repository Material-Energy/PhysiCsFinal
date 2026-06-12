Web VPython 3.2

scene = canvas(width=700, height=500, align="left", background = color.gray(0.9), resizable = False)
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


num_loops = 8
num_turns = 50


# vectors
B_vec = vec(1, 0, 0)
lf = vec(0, 0, 0)
rf = vec(0, 0, 0)


# time stuff
dt = 1/60
xmax = 3.0


running = False
init = True

slowmo = False
slowmo_factor = 1
plot_counter = 0

lorentz_visible = True
magnetic_visible = True
polarity_visible = True


# sliders
def update_sliders(evt):
    global I, B, V, R, num_loops, num_turns, load_torque
    global init_slider_text
    
    if evt.id == "I":
        I = round(evt.value)
        slider_text[0].text = init_slider_text[0].format(I)
        I = 10 ** I

    elif evt.id == "B":
        B = round(4*evt.value) / 4
        slider_text[1].text = init_slider_text[1].format(B)
        
        update_B_arrow()
       
    elif evt.id == "V":
        V = round(2*evt.value) / 2
        slider_text[2].text = init_slider_text[2].format(V)
        
    elif evt.id == "R":
        R = round(10*evt.value) / 10
        slider_text[3].text = init_slider_text[3].format(R)
        
    elif evt.id == "L":
        num_loops = round(evt.value)
        slider_text[4].text = init_slider_text[4].format(num_loops)
        delete_moving_objs()
        create_moving_objs()
        
    elif evt.id == "T":
        num_turns = round(evt.value)
        slider_text[5].text = init_slider_text[5].format(num_turns)
        
    elif evt.id == "LT":
        load_torque = round(evt.value)
        if load_torque == -5: 
            load_torque = 0
            slider_text[6].text = "Load Torque: 0 <i>Nm</i>\n\n"
            
        else:
            slider_text[6].text = init_slider_text[6].format(load_torque)
            load_torque = 10 ** load_torque
    
def update_toggles(evt):
    global lorentz_visible, magnetic_visible, polarity_visible
    if evt.id is "lorentz":
        lorentz_visible = evt.checked
    elif evt.id is "magnetic":
        magnetic_visible = evt.checked
        update_B_arrow()
    elif evt.id is "polarity":
        polarity_visible = evt.checked

    

def init_toggles():
    global toggles
    lorentz_toggle = checkbox(bind=update_toggles, id="lorentz", text="Lorentz Force\n", name="i", checked=lorentz_visible)
    B_toggle = checkbox(bind=update_toggles, id="magnetic", text="Magnetic Field\n", name="love", checked=magnetic_visible)
    polarity_toggle = checkbox(bind=update_toggles, id="polarity", text="Magnetic Polarity", name="yuri", checked=polarity_visible)

    toggles = [lorentz_toggle, B_toggle, polarity_toggle]
    

# Run / Pause
def toggle_run(evt):
    global sliders, running
    
    if running:
        run_button.text = "Run"
        run_button.background = color.green
        
    else:
        run_button.text = "Pause"
        run_button.background = color.red
        for s in sliders[:-1]: s.disabled = True

    running = not running
        

run_button = button(bind=toggle_run, text="Run", background=color.green, pos=scene.title_anchor)


# Reset
reset_button = button(bind=reset, text="Reset", background=color.red, pos=scene.title_anchor)

# toggle slowmo

def toggle_slowmo(evt):
    global slowmo
    
    if slowmo:
        slowmo_button.text = "<b>Slowmo</b>"
        slowmo_button.color = color.blue
    else:
        slowmo_button.text = "<b>Normal</b>"
        slowmo_button.color = color.cyan
        
    slowmo = not slowmo
        
slowmo_button = button(bind = toggle_slowmo, color = color.blue, background=color.white, text = "<b>Slowmo</b>", pos=scene.title_anchor)



rotation_axis = vec(0,0,-1).rotate(angle = -3 * pi/4, axis=vec(1, 0, 0))
arrow(axis = rotation_axis)

def make_loop(path, angle):
    tmp = path[:]
    tmp.insert(0, path[0] + rotation_axis)
    
    wire = curve(pos=tmp, radius = 0.1, color=copper if angle != 0 else color.white)
    wire.rotate(axis=rotation_axis, angle = angle)

    return wire

def get_current_loop():
    for i in range(num_loops):
        a1, a2 = commutator_angles[i]
        a3, a4 = commutator_angles[i + num_loops]
#        print(str(a1) + " <= " + theta + " <= " + str(a2))
#        print(str(a3) + " <= " + theta + " <= " + str(a4))
        
        if (min(a1, a2) <= theta <= max(a1, a2) or min(a3, a4) <= theta <= max(a3, a4) or min(a1, a2) <= theta - 2 * pi <= max(a1, a2)):
            return i
        
        if (i == num_loops - 1):
            return -1

def calc_domega_dt(omega, theta):
    i_dir = 1
    theta %= (2*pi)
#    print(commutator_angles)
    phi = pi/2 - theta
    
    
    loop_index = get_current_loop()    
        
    phi += angles[loop_index] if not loop_index == -1 else 0 # angle betweeen normal and B 
    
    if sin(phi) > 0:
        i_dir = 1
    elif sin(phi) < 0:
        i_dir = -1
    
#    print(f"Using loop {i}")
#    print(f"theta: {theta}")
#    print(f"phi: {phi}")
    
    V_back = num_turns * B * A * omega * sin(phi)

    i_loop = (i_dir * V - V_back) / (num_turns * R)
    if loop_index == -1: i_loop = 0
        
    F_B = i_loop * B * L * sin(phi) # Lorentz force on EACH turn        
    

    torque = num_turns * 2*r*F_B
    
    sign_torque = 1 if torque >= 0 else -1
    
    if omega == 0:
        if (abs(torque) >= load_torque):
            torque -= load_torque * sign_torque
        else:
            torque = 0
    else:
        torque -= load_torque * sign_torque
        
    
    domega_dt = torque / I
    
    flux = B * A * cos(phi)
    
    return domega_dt, V_back, i_loop, F_B, flux, torque



def update_arrows(path, theta):
    global lf, rf
    path = path[1:]
    
    lf.visible = False
    rf.visible = False
    
    
    L_vec = path[3]-path[2]
#    print(L_vec)
#    print(vec(B_vec))
#    arrow(axis = cross(L_vec, B_vec))
    magnitude = abs(B * i_loop * 2)
    if magnitude < 0.0125: magnitude = 0
    magnitude = min(sqrt(magnitude), 4)
    
    
    midpoint = (path[2] + path[3]) / 2
    lf = arrow(pos=midpoint.rotate(axis = rotation_axis, angle = theta), axis = magnitude * norm(cross(L_vec, B_vec)), shaftwidth=0.1, color=color.black)
    
    midpoint = (path[4] + path[5]) / 2
    L_vec = path[5] - path[4]
    rf = arrow(pos=midpoint.rotate(axis = rotation_axis, angle = theta), axis = magnitude * norm(cross(L_vec, B_vec)), shaftwidth=0.1, color=color.black)
    
    lf.visible = True
    rf.visible = True
    
    
width = 2 * 100*r
height = 100*L
copper = vec(0.961, 0.686, 0.373)

def create_moving_objs():
    global path, loops, commutator, commutator_segments
    global commutator_angles, angles
    
    
    offset = pi / num_loops
    total_segments = 2 * num_loops # total commutator segments

    commutator_angles = []
    angles = [offset * i for i in range(num_loops)] # how much to rotate each loop from first loop
    
    
    loops = []
    
    for i in range(num_loops):
        loops.append(make_loop(path, angles[i]))
        

    #print(wire.slice(0, wire.npoint)[0])
    #print(wire.point(0)['pos'])
    
    # commutators
    wire = loops[0] # make sure first loop always has angle = 0 in make_loop
    center = wire.point(1)['pos'] - vec(wire.point(1)['pos'].x, 0, 0)
    
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

def update_B_arrow():
    global B_vec, B_arrow1, B_arrow2

    B_length = 3 * B
    B_vec = vec(B, 0, 0)
    if B_arrow1: B_arrow1.visible = False
    if magnetic_visible: B_arrow1 = arrow(pos = vec(-1.5 * B, width / 3, width / 3), axis = B_length * vec(1, 0, 0), color = color.purple)
    if B_arrow2: B_arrow2.visible = False
    if magnetic_visible: B_arrow2 = arrow(pos = vec(-1.5 * B, -width / 3, -width / 3), axis = B_length * vec(1, 0, 0), color = color.purple)

def create_static_objs():
    global stator_parts, stator, center
    global path
    stator_parts = []
    colors = [color.blue, color.red]
    
    for i in range(2):
        start = i * pi
        
        arc = paths.arc(pos=center, radius = width/2 + width/8, angle1=start-pi/3, angle2=start+pi/3)
        magnet = extrusion(shape=shapes.rectangle(width=0.2, height=3), path=arc, color=colors[i])
        
        arc = paths.arc(pos=center, radius = width/2 + width/8 + 0.2, angle1=start-pi/3, angle2=start+pi/3)
        out = extrusion(shape=shapes.rectangle(width=0.2, height=3), path=arc, color=color.gray(0.7))
        
        stator_parts += [magnet, out]
    
    update_B_arrow()
    
    
    stator = compound(stator_parts)
    stator.rotate(axis=vector(1, 0, 0), angle = 3*pi/4)
    
    sqrt_2 = sqrt(2)
    # brushes
    brushes = []
    s = 0.4
    delta = s/2 + 0.1
    brush = box(pos = path[0] + vec(delta, 0, 0) + vec(0, height / 10, -height / 10), length = s, height = s, width = s)
    brush.rotate(axis=vector(1, 0, 0), angle=-3*pi/4)
    connector = box(pos = path[0] + vec(delta + 3 * s / 2, 0, 0) + vec(0, height / 10, -height / 10), length = 2 * s, height = s * 1.5, width = s * 1.5, color = copper)
    connector.rotate(axis=vector(1, 0, 0), angle=-3*pi/4)
    brushes.append(brush)
    brushes.append(connector)
    brush = box(pos = path[-1] - vec(delta, 0, 0) + vec(0, height / 10, -height / 10), length = s, height = s, width = s)
    brush.rotate(axis=vector(1, 0, 0), angle=-3*pi/4)
    connector = box(pos = path[-1] - vec(delta + 3 * s / 2, 0, 0) + vec(0, height / 10, -height / 10), length = 2 * s, height = s * 1.5, width = s * 1.5, color = copper)
    connector.rotate(axis=vector(1, 0, 0), angle=-3*pi/4)
    brushes.append(brush)
    brushes.append(connector)
    
    
    circuit = [vec(width / 2 * 0.87, height * 1.15 / sqrt_2, -height * 1.15 / sqrt_2), vec(-width / 2 * 0.87, height * 1.15 / sqrt_2, -height * 1.15 / sqrt_2)]
    circuit.insert(1, circuit[0] + vec(width / 2, 0, 0))
    circuit.insert(2, circuit[1] + vec(0, 4 / sqrt_2, -4 / sqrt_2))
    circuit.insert(3, circuit[-1] + vec(-width / 2, 4 / sqrt_2, -4 / sqrt_2))
    circuit.insert(4, circuit[-1] + vec(-width / 2, 0, 0))
    
    curve(pos=circuit, radius = 0.1, color=copper)
#    .rotate(axis=rotation_axis, angle = 3*pi/4)
    # wire
    
    pos_term = box(pos=(circuit[2] + circuit[3]) / 2 + vec(-1, 0, 0), length = 2, width = 1, height= 1, color = color.blue).rotate(axis=vector(1, 0, 0), angle=-3*pi/4)
    neg_term = box(pos=(circuit[2] + circuit[3]) / 2 - vec(-1, 0, 0), length = 2, width = 1, height= 1, color = color.red).rotate(axis=vector(1, 0, 0), angle=-3*pi/4)
    battery = [pos_term, neg_term]

def delete_moving_objs():
    global loops, commutator, polarity_dia
    
    for obj in loops:
        obj.visible = False
        del obj
    
    commutator.visible = False
    del commutator
    
    if polarity_dia:
        polarity_dia.visible = False
        del polarity_dia


def reset(evt):
    global sliders, slider_text, toggles
    global I, B, V, R, load_torque
    global num_loops, num_turns
    global t, theta, omega
    
    global loops, commutator_segments, stator_parts
    global commutator, stator
    
    global graphs, gcs
    
    global init
    global running, slowmo
    
    global init_slider_text
    global path
    
    theta = 0
    omega = 0
    t = 0
    
    
    init_constants = [
        -4.0, # 10 raised to this number is the moment of inertia of each loop
        0.25, # magnitude of magnetic field from external magnets
        5.0, # source voltage
        0.1, # resistance of wire
        8, # number of loops
        50, # number of turns
        0, # load torque
    ]
    
    I = 10 ** init_constants[0]
    B = init_constants[1]
    V = init_constants[2]
    R = init_constants[3]
    num_loops = init_constants[4]
    num_turns = init_constants[5]
    load_torque = init_constants[6]
    
    
    init_slider_text = [
        "Rotational Inertia: 10<sup>{}</sup> <i>kg&middot;m<sup>2</sup></i>\n\n",
        "Magnetic Field: {} <i>T</i> \n\n",
        "Source Voltage: {} <i>V</i> \n\n",
        "Resistance per Turn: {} <i>&Omega;</i> \n\n",
        "Number of Loops: {}\n\n",
        "Number of Turns: {}\n\n",
        "Load Torque: 10<sup>{}</sup> <i>Nm</i>\n\n"
    ]
    
    
    # armature
    path = paths.rectangle(width=width, height = height)
    #print(path)
    path.insert(0, path[0]+vec(-width/4, 0, 0))
    path[-1] = path[-2] + vec(width/4, 0, 0)
    
    path.insert(0, path[0]+vec(0, 0, height/2))
    path.append(path[-1]+vec(0, 0, height/2))
    
    for i in range(len(path)):
        path[i] = rotate(path[i], axis=vector(1, 0, 0), angle=-3*pi/4)
    
    
    if init:
        init = False
        
        
        I_slider = slider(bind=update_sliders, min=-5, max=0, value=init_constants[0], id = "I", align="left", length = 350)
        I_text = wtext(text = init_slider_text[0].format(init_constants[0]))
    
            
        B_slider = slider(bind=update_sliders, min=0, max=1, value=init_constants[1], id = "B", align="left", length = 350)
        B_text = wtext(text = init_slider_text[1].format(init_constants[1]))

        
        V_slider = slider(bind=update_sliders, min=0, max=10, value=init_constants[2], id = "V", align="left", length = 350)
        V_text = wtext(text = init_slider_text[2].format(init_constants[2]))
    
         
        R_slider = slider(bind=update_sliders, min=0.1, max=3, value=init_constants[3], id = "R", align="left", length = 350)
        R_text = wtext(text = init_slider_text[3].format(init_constants[3]))
        
        loops_slider = slider(bind=update_sliders, min=1, max=10, value=init_constants[4], id = "L", align="left", length = 350)
        loops_text = wtext(text = init_slider_text[4].format(init_constants[4]))
        
        turns_slider = slider(bind=update_sliders, min=1, max=100, value=init_constants[5], id = "T", align="left", length = 350)
        turns_text = wtext(text = init_slider_text[5].format(init_constants[5]))
        
        load_torque_slider = slider(bind=update_sliders, min=-5, max=-1, value=-5, id = "LT", align="left", length = 350)
        load_torque_text = wtext(text = "Load Torque: 0 <i>Nm</i>\n\n")
        
        
        init_toggles()
   
   
        sliders = [I_slider, B_slider, V_slider, R_slider, loops_slider, turns_slider, load_torque_slider]
        slider_text = [I_text, B_text, V_text, R_text, loops_text, turns_text, load_torque_text]
        
        
        scene.append_to_caption("\n" * 20)
        create_static_objs()
        
    else:
        scene.camera.pos = init_camera[0]
        scene.camera.axis = init_camera[1]
        scene.forward = init_camera[2]
        scene.range = init_camera[3]
        
        running = True
        toggle_run(evt)
        slowmo = True
        toggle_slowmo(evt)
        
        for s in sliders: s.disabled = False
    
        for i in range(len(sliders)):
            
            if i == len(sliders) - 1: 
                sliders[i].value = -5
                slider_text[i].text = "Load Torque: 0 <i>Nm</i>\n\n"
            else: 
                sliders[i].value = init_constants[i]
                slider_text[i].text = init_slider_text[i].format(init_constants[i])
            
        
        for tog in toggles: tog.checked = True

        update_B_arrow()
        delete_moving_objs()
 
        for g in graphs: g.delete()
        for c in gcs: c.delete()
        
        lf.visible = False
        rf.visible = False
    
    
    create_moving_objs()
    
    RPM_graph = graph(title = "RPM vs time", xtitle = "t", ytitle = "RPM", scroll=True, xmin = 0, xmax = xmax, width=480, height=360, align="left")
    gc1 = gcurve()

    
    current_graph = graph(title = "Current in Loop vs time", xtitle = "t", ytitle = "Current", scroll=True, xmin = 0, xmax = xmax, width=480, height=360, align="left")
    gc2 = gcurve()
    
    
    back_emf_graph = graph(title = "Back-Emf vs time", xtitle = "t", ytitle = "Back-EMF", scroll=True, xmin = 0, xmax = xmax, width=480, height=360, align="left")
    gc3 = gcurve()
    
    torque_graph = graph(title = "Net Torque vs time", xtitle = "t", ytitle = "Torque", scroll=True, xmin = 0, xmax = xmax, width=480, height=360, align="left")
    gc4 = gcurve()
    
    graphs = [RPM_graph, current_graph, back_emf_graph, torque_graph]
    gcs = [gc1, gc2, gc3, gc4]
    






init = True
reset(None)
init = False

# physics stuff
A = 2 * r * L

while True:
#    print(t, omega, theta)
    rate(1/dt)
    
    if (running):
        if (slowmo): 
            slowmo_factor = max(omega / (2*pi), 1) # RPM / 60
            dt_eff = dt / slowmo_factor
        else: dt_eff = dt
        
        omega_old = omega
        domega_dt_i, _ = calc_domega_dt(omega, theta)
        
        theta_mid = theta + omega * (dt_eff / 2)
        omega_mid = omega + domega_dt_i * (dt_eff / 2)
        
        domega_dt_mid, _ = calc_domega_dt(omega_mid, theta_mid)
        
        
        theta += omega_mid * dt_eff
        omega += domega_dt_mid * dt_eff
        
        t += dt_eff
        
        if (omega_old * omega < 0): omega = 0 # detect sign flip, prevent overshoot
        
#        
        
        
        # update graphed values
        _, V_back, i_loop, F_B, flux, torque = calc_domega_dt(omega, theta)
        theta %= (2*pi)
    #    print(f"theta: {theta}")
        
        
    #    update_arrows(path, lf, rf)
        
    #    print(f"Omega*dt: {omega_mid*dt}")
    
    #    print(f"V_back: {V_back:.4f}")
    #    print(f"omega: {omega:.4f}")
    #    print(f"B: {B:.4f}")
    #    print(f"A: {A:.4f}")
    #    print(f"sin(theta): {sin(theta):.4f}")
    #    print(f"i loop: {i_loop:.4f}")
    
        if slowmo:
            plot_counter += 1
        else:
            plot_counter = 0
      
        if plot_counter % int(slowmo_factor) == 0:
             
            graphs[0].select()
            gcs[0].plot(t, omega * 60 / (2*pi))
            
            graphs[1].select()
            gcs[1].plot(t, i_loop)
            
            graphs[2].select()
            gcs[2].plot(t, V_back)
            
            graphs[3].select()
            gcs[3].plot(t, torque)
        
        
        
    
    
        
        
        
        for wire in loops:
            wire.rotate(axis=rotation_axis, angle=omega_mid*dt_eff)
    #        
    #    wire.visible = False
    #    wire = curve(pos=path, radius = 0.1, color=bronze)
    #    wire.visible = True
        
        cur_path = get_current_loop()
        if cur_path != -1:
            delta = (theta + commutator_angles[0][1]) % pi - angles[cur_path] - commutator_angles[0][1]
            if lorentz_visible:
                loop_arrow = [loops[cur_path].point(x)['pos'] for x in range(loops[cur_path].npoints)]
                update_arrows(loop_arrow, delta)
            else:
                if lf:
                    lf.visible = False
                if rf:
                    rf.visible = False
            
            
            if polarity_visible:            
                if polarity_dia:
                    polarity_dia.visible = False
                    del polarity_dia
                polarity_objs = []
                north = box(pos=vec(0, 0.15, 0) ,length=width-0.4, width=height-0.4, height=0.3, color=color.red)
                south = box(pos=vec(0, -0.15, 0) ,length=width-0.4, width=height-0.4, height=0.3, color=color.blue)
                polarity_objs.append(north)
                polarity_objs.append(south)
                
                polarity_dia = compound(polarity_objs)
                polarity_dia.rotate(axis=vector(1, 0, 0), angle = -3*pi/4)
                polarity_dia.rotate(axis=rotation_axis, angle=delta)
            else:
                if polarity_dia:
                    polarity_dia.visible = False
                    del polarity_dia
        else:
            if lf:
                lf.visible = False
            if rf:
                rf.visible = False
            if polarity_dia:
                polarity_dia.visible = False
        
        commutator.rotate(axis=rotation_axis, angle = omega_mid*dt_eff)

        
    
    
    
