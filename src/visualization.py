import cv2
import numpy as np

def draw_keypoints(image, keypoints):
    """Draw keypoints on image."""
    for kp in keypoints:
        cv2.circle(image, tuple(kp.astype(int)), 5, (0,255,0), -1)
    return image

def draw_fitted_curves(image, circle_params, line_params):
    """Draw fitted circle and lines."""
    xc, yc, r = circle_params
    cv2.circle(image, (int(xc), int(yc)), int(r), (255,0,0), 2)
    # Draw line if needed
    return image

def annotate_image(image, keypoints, dimensions):
    """Full annotation."""
    img = draw_keypoints(image.copy(), keypoints)
    # Assume circle params from fitting
    # img = draw_fitted_curves(img, ...)
    # Add text labels
    y_offset = 30
    for key, val in dimensions.items():
        cv2.putText(img, f"{key}: {val:.3f}", (10, y_offset), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,255), 1)
        y_offset += 20
    return img

def save_annotated(image, output_path):
    """Save annotated image."""
    cv2.imwrite(output_path, image)