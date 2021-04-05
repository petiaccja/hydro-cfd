import numpy as np

force = np.array([[0,0,1]])
centers = np.array([[0,1,0]])
areas = np.array([1])

torque = np.sum(np.cross(centers, force) * areas, axis=0)

print(torque)