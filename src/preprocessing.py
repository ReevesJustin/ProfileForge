import cv2
import numpy as np

def load_image(image_path):
    """Load image from path."""
    return cv2.imread(image_path)

def enhance_contrast(image):
    """Enhance contrast using CLAHE."""
    lab = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)
    clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8,8))
    lab[:,:,0] = clahe.apply(lab[:,:,0])
    return cv2.cvtColor(lab, cv2.COLOR_LAB2BGR)

def undistort_image(image, camera_matrix=None, dist_coeffs=None):
    """Undistort using camera calibration if available."""
    if camera_matrix is not None and dist_coeffs is not None:
        h, w = image.shape[:2]
        new_camera_matrix, roi = cv2.getOptimalNewCameraMatrix(camera_matrix, dist_coeffs, (w,h), 1, (w,h))
        return cv2.undistort(image, camera_matrix, dist_coeffs, None, new_camera_matrix)
    return image

def to_grayscale(image):
    """Convert to grayscale."""
    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

def high_contrast_mask(image):
    """Apply high contrast masking."""
    gray = to_grayscale(image)
    _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    return thresh

def preprocess_image(image_path):
    """Full preprocessing pipeline."""
    img = load_image(image_path)
    img = enhance_contrast(img)
    img = undistort_image(img)
    gray = to_grayscale(img)
    mask = high_contrast_mask(img)
    return gray, mask