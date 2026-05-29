Web VPython 3.2

B = 1.0 # magnitude of mangetic field from external magnets
V = 5.0 # source voltage
R = 10 # resistance of wire

B_vec = vec(1, 0, 0)
lf = vec(0, 0, 0)
rf = vec(0, 0, 0)

i_wire = V / R
L = 3 # height of loop
r = 2.5 # radius of loop
I = 2.0 # moment of inertia of the armature

t = 0
dt = 0.01


rotation_axis = vec(0,0,-1).rotate(angle = -3 * pi/4, axis=vec(1, 0, 0))
#circle = shapes.circle(radius=0.25, np=128)
#line_path = paths.curv
#
#line_path.insert(0, line_path[0] + vec(
#ext = extrusion(shape = circle, path=line_path)
#ext.rotate(axis = vec(1, 0, 0), angle=pi/6)

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
width = 2 * r
height = L
bronze = vec(1,0.7,0.2)

path = paths.rectangle(width=width, height = height)
print(path)
path.insert(0, path[0]+vec(-width/4, 0, 0))
path[-1] = path[-2] + vec(width/4, 0, 0)

path.insert(0, path[0]+vec(0, 0, height/2))
path.append(path[-1]+vec(0, 0, height/2))

for i in range(len(path)):
    path[i] = rotate(path[i], axis=vector(1, 0, 0), angle=-3*pi/4)
    
wire = curve(pos=path, radius = 0.1, color=bronze)

#print(wire.slice(0, wire.npoint)[0])
print(wire.point(0)['pos'])

arc = paths.arc(pos=wire.point(0)['pos'] + vec(-wire.point(0)['pos'].x, 0, 0), radius = width/4 + width / 80, angle1=pi/32 - pi/2, angle2=31*pi/32 - pi/2)
commutator_left = extrusion(shape=shapes.rectangle(width=0.1, height=2), path=arc, color=bronze)
commutator_left.rotate(axis=vector(1, 0, 0), angle=3 * pi/4)

arc = paths.arc(pos=wire.point(wire.npoints - 1)['pos'] + vec(-wire.point(wire.npoints - 1)['pos'].x, 0, 0), radius = width/4+ width / 80, angle1=pi/32 + pi/2, angle2=31*pi/32 + pi/2)
commutator_right = extrusion(shape=shapes.rectangle(width=0.1, height=2), path=arc, color=bronze)
commutator_right.rotate(axis=vector(1, 0, 0), angle=3 * pi/4)

commutators = compound([commutator_left, commutator_right])


# physics stuff
A = width * height
 
theta = 0
omega = 0

RPM_graph = graph(title = "RPM vs time", xtitle = "t", ytitle = "RPM")
gd = gdots()


while t < 10:
    t += dt
    rate (1 / dt)
    
    V_back = B*A*omega*sin(theta)
    
    domega_dt = (r*B*L) / (I*R) * (V - V_back)
    omega += domega_dt * dt
    theta += omega * dt
    
    
    
    i_loop = i_wire - V_back / R
    F_B = i_loop * B * L
    
    update_arrows(path, lf, rf)
    
#    print(f"Omega*dt: {omega*dt}")
#    print(f"RPM: {r*omega}")
    RPM_graph.select()
    gd.plot(t, r*omega)


    arrow(axis = rotation_axis)
    
    

    for i in range(len(path)):
        path[i] = rotate(path[i], axis=rotation_axis, angle=omega*dt)
        
    wire.visible = False
    wire = curve(pos=path, radius = 0.1, color=bronze)
    wire.visible = True
    
    
    update_arrows(path, lf, rf)
    
    commutators.rotate(axis=rotation_axis, angle = omega* dt)
    
