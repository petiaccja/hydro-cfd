#!/usr/bin/bash

./cleanAll.sh
./runMeshing.sh

# Run simulation
mpirun -np 8 rhoSimpleFoam -parallel
