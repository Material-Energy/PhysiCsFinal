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

path = paths.rectangle(width=width, height = height)
#print(path)
path.insert(0, path[0]+vec(-width/4, 0, 0))
path[-1] = path[-2] + vec(width/4, 0, 0)

path.insert(0, path[0]+vec(0, 0, height))
path.append(path[-1]+vec(0, 0, height))

wire = curve(pos=path, radius = 0.1, color=vec(1,0.7,0.2))
print(wire.slice(0, wire.npoint)[0])