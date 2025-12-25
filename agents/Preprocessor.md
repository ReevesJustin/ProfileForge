# Preprocessor

## Role
Subagent for loading and preprocessing bullet photos to improve detection quality.

## Description
Loads JPEG/PNG image, enhances contrast, undistorts if needed (using iPhone lens calibration), converts to grayscale, applies high-contrast masking. Outputs enhanced image.

## When to Invoke
- Automatically by PipelineOrchestrator at start of pipeline
- When image quality issues are detected

## Tools
- OpenCV-based functions for image processing
- Python modules: preprocessing.py

## Configuration
- Temperature: 0
- Restricted tools: Only image processing tools

## Dependencies
- OpenCV, NumPy