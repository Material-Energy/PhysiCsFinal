Web VPython 3.2

scene = canvas(width=800, height=600, align="left", background = color.gray(0.9))

# constants
B = 0.0 # magnitude of mangetic field from external magnets
V = 1.0 # source voltage
R = 1 # resistance of wire

L = 0.02 # height of loop (m)
r = 0.025 # radius of loop (m)

I = 1e-4 # moment of inertia of the armature

num_loops = 3
num_turns = 5
offset = pi / num_loops
angles = [offset * i for i in range(num_loops)] # how much to rotate each loop from first loop
total_segments = 2 * num_loops # total commutator segments

# vectors
B_vec = vec(1, 0, 0)
lf = vec(0, 0, 0)
rf = vec(0, 0, 0)
#
# time stuff
t = 0
dt = 0.01
xmax = 3.0

commutator_angles = []


# sliders 

def handle_sliders(evt):
    global I, B, V, R
    
    if evt.id == "I":
        I = 10 ** evt.value
        I_text.text = f"Rotational Inertia: \\(10^{{{evt.value}}} \\: kg \\cdot m^2\\) \n\n"
        MathJax.Hub.Queue(["Typeset",MathJax.Hub, I_text.text])
    elif evt.id == "B":
        B = evt.value
        B_text.text = f"Magnetic Field: \\({{{evt.value}}} \\: T\\) \n\n"
        MathJax.Hub.Queue(["Typeset",MathJax.Hub, B_text.text])
    elif evt.id == "V":
        V = evt.value
        V_text.text = f"Source Voltage: \\({{{evt.value}}} \\: V\\) \n\n"
        MathJax.Hub.Queue(["Typeset",MathJax.Hub, V_text.text])
    elif evt.id == "R":
        R = evt.value
        R_text.text = f"Equivalent Resistance: \\({{{evt.value}}} \\: \\Omega\\) \n\n"
        MathJax.Hub.Queue(["Typeset",MathJax.Hub, R_text.text])

scene.select()

I_slider = slider(bind=handle_sliders, min=-7, max=0, step=1, value=-5, id = "I", align="left")
I_text = wtext(text = "Rotational Inertia: \\(10^{-5} \\: kg \\cdot m^2\\) \n\n")
MathJax.Hub.Queue(["Typeset",MathJax.Hub, I_text.text])

B_slider = slider(bind=handle_sliders, min=0, max=10, step=1, value=1, id = "B", align="left")
B_text = wtext(text = "Magnetic Field: \\(1 \\: T\\) \n\n")
MathJax.Hub.Queue(["Typeset",MathJax.Hub, B_text.text])

V_slider = slider(bind=handle_sliders, min=0, max=10, step=1, value=5, id = "V", align="left")
V_text = wtext(text = "Source Voltage: \\(5 \\: V\\) \n\n")
MathJax.Hub.Queue(["Typeset",MathJax.Hub, V_text.text])

R_slider = slider(bind=handle_sliders, min=1, max=1000, step=1, value=1, id = "R", align="left")
R_text = wtext(text = "Equivalent Resistance: \\(1 \\: \\Omega\\) \n\n")
MathJax.Hub.Queue(["Typeset",MathJax.Hub, R_text.text])


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
    
    return domega_dt, V_back, i_loop, F_B, flux, torque
    
    
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
    
    
scene.forward = vec(0, -1, 1)
width = 2 * 100*r
height = 100*L
copper = vec(0.961, 0.686, 0.373)

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



# physics stuff
A = 2 * r * L
 
theta = 0
omega = 0

scene.append_to_caption("\n" * 30)
RPM_graph = graph(title = "RPM vs time", xtitle = "t", ytitle = "RPM", scroll=True, xmin = 0, xmax = xmax, width=480, height=360, align="left")
gc1 = gcurve()

flux_graph = graph(title = "Flux vs time", xtitle = "t", ytitle = "Flux", scroll=True, xmin = 0, xmax = xmax, width=480, height=360)
gc2 = gcurve()

back_emf_graph = graph(title = "Back-Emf vs time", xtitle = "t", ytitle = "Back-EMF", scroll=True, xmin = 0, xmax = xmax, width=480, height=360)
gc3 = gcurve()

torque_graph = graph(title = "Torque vs time", xtitle = "t", ytitle = "Torque", scroll=True, xmin = 0, xmax = xmax, width=480, height=360)
gc4 = gcurve()


while t < 1000:

    rate (1/dt)
    

    domega_dt_i, _ = calc_domega_dt(omega, theta)
    
    theta_mid = theta + omega * (dt / 2)
    omega_mid = omega + domega_dt_i * (dt / 2)
    
    domega_dt_mid, _ = calc_domega_dt(omega_mid, theta_mid)
    
    
    theta += omega_mid * dt
    omega += domega_dt_mid * dt
    
    t += dt
    
    # update graphed values
    _, V_back, i_loop, F_b, flux, torque = calc_domega_dt(omega, theta)
#    print(f"theta: {theta}")
    
    
#    update_arrows(path, lf, rf)
    
#    print(f"Omega*dt: {omega_mid*dt}")

#    print(f"V_back: {V_back:.4f}")
#    print(f"omega: {omega:.4f}")
#    print(f"B: {B:.4f}")
#    print(f"A: {A:.4f}")
#    print(f"sin(theta): {sin(theta):.4f}")
#    print(f"i loop: {i_loop:.4f}")



    RPM_graph.select()
    gc1.plot(t, omega * 60 / (2*pi))
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
    
    
    
