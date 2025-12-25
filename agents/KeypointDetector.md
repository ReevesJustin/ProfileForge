# KeypointDetector

## Role
Subagent for detecting keypoints on bullet profiles using AI and fallback CV.

## Description
Runs YOLOv8-pose model fine-tuned on bullet dataset to detect 11+ keypoints (jaws, meplat, ogive, boattail). Falls back to contours/edge finding if confidence low. Outputs keypoints JSON.

## When to Invoke
- After scale calibration
- If confidence < threshold, retries with enhanced image

## Tools
- Ultralytics YOLOv8
- OpenCV fallback
- Python modules: keypoint_detection.py

## Configuration
- Temperature: 0
- Restricted tools: Detection tools

## Dependencies
- ultralytics, opencv, numpy