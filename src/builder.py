import numpy as np
from stl import mesh


def get_logo(height):
    # load logo mesh from file
    logo = mesh.Mesh.from_file('resources/logo.stl')
    
    # scale logo to correct height
    logo.z *= height

    return logo

def get_logo_old(height):
    num_sides = 40
    radius = 30
    coords_bottom = []
    for i in range(num_sides):
        deg = i * 360/num_sides
        x = int(radius * np.sin(deg * np.pi/180))
        y = int(radius * np.cos(deg * np.pi/180))
        coords_bottom.append((x,y,0))
    coords_bottom.append((0,0,0)) # center point
    coords_bottom = np.asarray(coords_bottom)
    coords_up = np.copy(coords_bottom)
    coords_up[:,2] = coords_up[:,2] + height

    vertices = np.concatenate((coords_bottom, coords_up))
    
    faces = []
    for i in range(num_sides):
        # walls
        faces.append((
            i,  
            i+1+num_sides,
            (i+1) % num_sides))
        faces.append((
            (i+1) % num_sides,
            i+1+num_sides, 
            (i+1) % num_sides + 1 + num_sides))
        # top
        faces.append((
            i+1+num_sides,
            2*num_sides + 1, 
            (i+1) % num_sides + 1 + num_sides
        ))
        # bottom 
        faces.append((
            i, 
            (i+1) % num_sides,
            num_sides
        ))
    faces = np.asarray(faces)

    return _build_mesh(vertices, faces)

def get_bar(size, height):
    
    coords_bottom = np.asarray([
        # upper rounding
        (-3.36, -3.20 + size/2, 0), 
        (-2.72, -1.22 + size/2, 0),
        (-1.04,  0.00 + size/2, 0),
        (+1.04,  0.00 + size/2, 0),
        (+2.72, -1.22 + size/2, 0),
        (+3.36, -3.20 + size/2, 0),
        # lower rounding
        (+3.36, +3.20 - size/2, 0), 
        (+2.72, +1.22 - size/2, 0),
        (+1.04,  0.00 - size/2, 0),
        (-1.04,  0.00 - size/2, 0),
        (-2.72, +1.22 - size/2, 0),
        (-3.36, +3.20 - size/2, 0)])
    coords_up = np.copy(coords_bottom)
    coords_up[:,2] = coords_up[:,2] + height

    vertices = np.concatenate((coords_bottom, coords_up))

    faces = np.array([
        # walls
        (0, 12, 1), (1, 12, 13),
        (1, 13, 2), (2, 13, 14),
        (2, 14, 3), (3, 14, 15),
        (3, 15, 4), (4, 15, 16),
        (4, 16, 5), (5, 16, 17),
        (5, 17, 6), (6, 17, 18),
        (6, 18, 7), (7, 18, 19),
        (7, 19, 8), (8, 19, 20),
        (8, 20, 9), (9, 20, 21),
        (9, 21, 10), (10, 21, 22),
        (10, 22, 11), (11, 22, 23),
        (11, 23, 0), (0, 23, 12),
        # top
        (23, 18, 17), (23, 17, 12),
        (22, 18, 23), (22, 19, 18),
        (22, 21, 19), (21, 20, 19),
        (12, 17, 16), (12, 16, 13),
        (13, 16, 15), (13, 15, 14),
        # bottom
        (11,  5, 6), (11, 0, 5),
        (10, 11, 6), (10, 6, 7),
        (10,  7, 9), ( 9, 7, 8),
        ( 0,  4, 5), ( 0, 1, 4),
        ( 1,  3, 4), ( 1, 2, 3)
        ])

    return _build_mesh(vertices, faces)

def get_base(heigt):

    vertices = np.asarray([
        # top
        (  0, -50, -heigt),
        (400, -50, -heigt),
        (400, +50, -heigt),
        (  0, +50, -heigt),
        # bottom
        (  0, -50, 0),
        (400, -50, 0),
        (400, +50, 0),
        (  0, +50, 0)
    ])

    faces = np.asarray([
        (0,3,1),
        (1,3,2),
        (0,4,7),
        (0,7,3),
        (4,5,6),
        (4,6,7),
        (5,1,2),
        (5,2,6),
        (2,3,6),
        (3,7,6),
        (0,1,5),
        (0,5,4)
    ])

    return _build_mesh(vertices, faces)

def _build_mesh(vertices, faces):
    """Takes vertices and faces array and returns a mesh object"""
    m = mesh.Mesh(np.zeros(faces.shape[0], dtype=mesh.Mesh.dtype))   
    for i, f in enumerate(faces):
        for j in range(3):
            m.vectors[i][j] = vertices[f[j],:]

    return m