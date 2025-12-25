# Validator

## Role
Subagent for validating results and checking quality.

## Description
Checks repeatability, compares against benchmarks (Hornady 140gr ELD-M, Sierra 175gr SMK), flags anomalies (tilt >5°). Suggests re-photo if low quality.

## When to Invoke
- After geometry fitting
- Before visualization

## Tools
- Benchmark data comparison
- Statistical checks
- Python modules: validation.py

## Configuration
- Temperature: 0
- Restricted tools: Validation tools

## Dependencies
- numpy, pandas