import cv2
import numpy as np
from scipy.spatial.distance import euclidean

def detect_jaws(gray_image):
    """Detect caliper jaws using edge detection and Hough lines."""
    edges = cv2.Canny(gray_image, 50, 150)
    lines = cv2.HoughLinesP(edges, 1, np.pi/180, 50, minLineLength=50, maxLineGap=10)
    if lines is None:
        return []
    # Filter horizontal lines (angle close to 0 or 180)
    horizontal_lines = []
    for line in lines:
        x1, y1, x2, y2 = line[0]
        angle = np.abs(np.arctan2(y2 - y1, x2 - x1) * 180 / np.pi)
        if angle < 10 or angle > 170:  # horizontal
            horizontal_lines.append(line[0])
    # Assume top two horizontal lines are jaws (sort by y)
    horizontal_lines.sort(key=lambda l: l[1])
    return horizontal_lines[:2]  # upper and lower

def compute_pixels_per_inch(jaw_lines, known_oal_inches):
    """Compute px/inch from jaw distance."""
    if len(jaw_lines) == 2:
        dist_px = abs(jaw_lines[0][0][1] - jaw_lines[1][0][1])
        return dist_px / known_oal_inches
    return None

def ocr_readout(gray_image):
    """OCR caliper readout using easyocr."""
    import easyocr
    reader = easyocr.Reader(['en'])
    result = reader.readtext(gray_image)
    # Extract numeric value
    for detection in result:
        text = detection[1]
        try:
            return float(text)
        except ValueError:
            continue
    return None

def calibrate_scale(gray_image, known_oal=None):
    """Full scale calibration."""
    jaws = detect_jaws(gray_image)
    if known_oal:
        px_per_inch = compute_pixels_per_inch(jaws, known_oal)
    else:
        oal = ocr_readout(gray_image)
        if oal:
            px_per_inch = compute_pixels_per_inch(jaws, oal)
        else:
            return None, "OCR failed"
    return px_per_inch, jaws