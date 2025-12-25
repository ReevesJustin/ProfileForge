import numpy as np

BENCHMARKS = {
    'Hornady 140gr ELD-M': {'OAL': 1.380, 'R': 6.5, 'Rt/R': 0.35},
    'Sierra 175gr SMK': {'OAL': 1.240, 'R': 7, 'Rt/R': 0.4}
}

def validate_dimensions(dimensions, benchmark_key=None):
    """Validate against benchmarks."""
    if benchmark_key in BENCHMARKS:
        bench = BENCHMARKS[benchmark_key]
        errors = {}
        for key in bench:
            if key in dimensions:
                errors[key] = abs(dimensions[key] - bench[key])
        return errors
    return {}

def check_tilt(keypoints):
    """Check for tilt >5°."""
    # Placeholder: check symmetry
    return abs(np.mean(keypoints[:,0]) - np.median(keypoints[:,0])) < 10  # dummy

def validate_results(dimensions, keypoints):
    """Full validation."""
    tilt_ok = check_tilt(keypoints)
    errors = validate_dimensions(dimensions, 'Hornady 140gr ELD-M')  # default
    return tilt_ok, errors