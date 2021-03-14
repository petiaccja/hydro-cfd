#!/usr/bin/bash
ls . | grep -E processor[0-9]+ | xargs rm -r
ls . | grep -E [1-9]+[0-9]* | xargs rm -r
find . -name *.eMesh | xargs rm
rm -r ./constant/polyMesh/*
rm -r ./constant/extendedFeatureEdgeMesh/*