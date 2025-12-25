# DatasetManager

## Role
Subagent for managing training data annotation.

## Description
Semi-automated annotation of new images for YOLO training, manages Roboflow/LabelStudio exports.

## When to Invoke
- When adding new training data
- For dataset expansion

## Tools
- Annotation tools
- Export functions
- Python modules: dataset_management.py

## Configuration
- Temperature: 0.5 (creative for annotation suggestions)
- Restricted tools: Data management tools

## Dependencies
- label-studio, roboflow