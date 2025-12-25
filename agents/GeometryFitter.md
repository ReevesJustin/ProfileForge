# GeometryFitter

## Role
Subagent for fitting geometric models to keypoints and computing dimensions.

## Description
Fits circles (least-squares for ogive R), lines (boattail angle), computes Rt, Rt/R, lengths, diameters, angles using SciPy optimize. Outputs measurements JSON.

## When to Invoke
- After keypoint detection

## Tools
- SciPy optimization
- NumPy for calculations
- Python modules: geometry_fitting.py

## Configuration
- Temperature: 0
- Restricted tools: Math/compute tools

## Dependencies
- scipy, numpy