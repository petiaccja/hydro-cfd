#!/usr/bin/bash

decomposePar
mpirun -np 4 rhoSimpleFoam -parallel
reconstructPar
#rhoSimpleFoam
