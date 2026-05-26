Web VPython 3.2


#circle = shapes.circle(radius=0.25, np=128)
#line_path = paths.curv
#
#line_path.insert(0, line_path[0] + vec(
#ext = extrusion(shape = circle, path=line_path)
#ext.rotate(axis = vec(1, 0, 0), angle=pi/6)

scene.forward = vec(0, -1, 0)
width = 5
height = 3
bronze = vec(1,0.7,0.2)

path = paths.rectangle(width=width, height = height)
#print(path)
path.insert(0, path[0]+vec(-width/4, 0, 0))
path[-1] = path[-2] + vec(width/4, 0, 0)

path.insert(0, path[0]+vec(0, 0, height))
path.append(path[-1]+vec(0, 0, height))

for i in range(len(path)):
    path[i] = rotate(path[i], axis=vector(1, 0, 0), angle=-3*pi/4)
    
wire = curve(pos=path, radius = 0.1, color=bronze)

#print(wire.slice(0, wire.npoint)[0])
print(wire.point(0)['pos'])

arc = paths.arc(pos=wire.point(0)['pos'] + vec(-wire.point(0)['pos'].x + width/40, 0, 1), radius = width/4, angle1=pi/24 - pi/2, angle2=23*pi/24 - pi/2)
commutatorL = extrusion(shape=shapes.rectangle(width=0.1, height=2), path=arc, color=bronze)
commutatorL.rotate(axis=vector(1, 0, 0), angle=-pi/6)

arc = paths.arc(pos=wire.point(wire.npoints - 1)['pos'] + vec(-wire.point(wire.npoints - 1)['pos'].x - width/40, 0, 1), radius = width/4, angle1=pi/24 + pi/2, angle2=23*pi/24 + pi/2)
commutatorR = extrusion(shape=shapes.rectangle(width=0.1, height=2), path=arc, color=bronze)
commutatorR.rotate(axis=vector(1, 0, 0), angle=-pi/6)
#commutator.rotate(axis=wire.point(wire.npoints - 1)['pos'], angle=pi/2)