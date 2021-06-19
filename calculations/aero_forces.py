import numpy as np
import openfoamparser as ofp
import itertools
import math

def triangulate_face(face):
    tris = []
    for i in range(1, len(face)-1):
        tris.append([face[0], face[i], face[i+1]])
    return tris

def triangle_normal(triangle):
    v1 = triangle[0] - triangle[1]
    v2 = triangle[0] - triangle[2]
    normal = np.cross(v1, v2)
    return normal / (np.linalg.norm(normal) + 1e-308)

def triangle_area(triangle):
    v1 = triangle[0] - triangle[1]
    v2 = triangle[0] - triangle[2]
    v3 = triangle[1] - triangle[2]
    a2 = np.dot(v1, v1)
    b2 = np.dot(v2, v2)
    c2 = np.dot(v3, v3)
    # Heron's formula:
    return math.sqrt(max(1e-50, 4*a2*b2 - (a2 + b2 - c2)**2))/4

def triangle_center(triangle):
    points = np.array(triangle)
    s = np.sum(points, axis=0)
    return s / 3


#meshPath = "D:\\OpenFOAM\\cases\\squareBend"
#pressurePath = "D:\\OpenFOAM\\cases\\squareBend\\163\\p"
#pressureOffset = 110000
meshPath = "D:\\OpenFOAM\\cases\\hydro"
pressurePath = "D:\\OpenFOAM\\cases\\hydro\\200\\p"
pressureOffset = 101325
boundaryName = b"model"
float_formatter = "{:.3f}".format
np.set_printoptions(formatter={'float_kind':float_formatter})


# Load mesh
pressureData = ofp.parse_internal_field(pressurePath)
mesh = ofp.FoamMesh(meshPath)

# Get boundary we want forces on
wallBoundary = mesh.boundary[boundaryName]
wallFaces = mesh.faces[wallBoundary.start:(wallBoundary.start + wallBoundary.num)]
wallFaceOwners = mesh.owner[wallBoundary.start:(wallBoundary.start + wallBoundary.num)]

# Derive normals and areas
wallTris = list(map(triangulate_face, wallFaces))
wallTriOwners = list(map(lambda pair : [pair[1]]*len(pair[0]), zip(wallTris, wallFaceOwners)))

tris = list(itertools.chain(*wallTris))
numTris = len(tris)

owners = list(itertools.chain(*wallTriOwners))
points = list(map(lambda indices : [mesh.points[i] for i in indices], tris))
normals = np.array(list(map(triangle_normal, points)))
areas = np.array(list(map(triangle_area, points))).reshape((numTris, 1))
centers = np.array(list(map(triangle_center, points)))

print("Integrate areas:   ", np.sum(areas))
print("Integrate normals: ", np.sum(normals * areas, axis=0))
print("Integrate coords:  ", np.sum(centers * areas, axis=0))

# Load pressure values
pressure = np.array(pressureData[owners]).reshape((numTris, 1)) - pressureOffset
force = normals * pressure
lift = np.sum(force * areas, axis=0)
torque = np.sum(np.cross(centers, force*np.array([[0,0,1]])) * areas, axis=0)

print("Lift =           ", lift, " N")
print("zTorque =        ", torque, " Nm")