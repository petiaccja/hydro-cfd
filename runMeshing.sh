#!/usr/bin/bash

# Run meshing
blockMesh
surfaceFeatures
decomposePar
mpirun -np 8 snappyHexMesh -parallel

# Copy mesh
cp ./2/polyMesh/* ./constant/polyMesh