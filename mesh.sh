#!/usr/bin/bash

# Run meshing
surfaceFeatures
blockMesh
#decomposePar
#mpirun -np 4 snappyHexMesh -overwrite -parallel
snappyHexMesh -overwrite

# Copy mesh
# cp ./2/polyMesh/* ./constant/polyMesh