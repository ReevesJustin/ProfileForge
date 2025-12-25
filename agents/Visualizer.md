# Visualizer

## Role
Subagent for generating annotated output images.

## Description
Draws keypoints, fitted curves, labels on image; saves annotated version.

## When to Invoke
- At end of pipeline
- After validation

## Tools
- OpenCV for drawing
- Python modules: visualization.py

## Configuration
- Temperature: 0
- Restricted tools: Drawing tools

## Dependencies
- opencv, numpy