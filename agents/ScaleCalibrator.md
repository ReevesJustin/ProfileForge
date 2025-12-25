# ScaleCalibrator

## Role
Subagent for detecting caliper jaws and computing scale from photos.

## Description
Uses edge detection and Hough lines to find caliper jaws, computes pixels-per-inch from known OAL or OCR readout. Handles tilt correction via symmetry. Outputs px_per_inch and corrected image.

## When to Invoke
- After preprocessing by PipelineOrchestrator
- If OAL not provided, attempts OCR

## Tools
- OpenCV for edge detection
- EasyOCR or Tesseract for readout
- Python modules: scale_calibration.py

## Configuration
- Temperature: 0
- Restricted tools: CV and OCR tools

## Dependencies
- OpenCV, easyocr, scipy