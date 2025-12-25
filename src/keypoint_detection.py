from ultralytics import YOLO
import cv2
import numpy as np

def load_yolo_model(model_path='models/yolo_bullet_pose.pt'):
    """Load YOLOv8-pose model."""
    return YOLO(model_path)

def detect_keypoints_yolo(image, model):
    """Run YOLO detection."""
    results = model(image)
    if results:
        keypoints = results[0].keypoints.xy.cpu().numpy()
        return keypoints
    return None

def detect_keypoints_fallback(gray_image):
    """Fallback using contours and edges."""
    contours, _ = cv2.findContours(gray_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    # Simplified: assume largest contour is bullet
    if contours:
        cnt = max(contours, key=cv2.contourArea)
        # Extract keypoints manually - this is placeholder
        return np.array([[0,0]] * 11)  # dummy
    return None

def detect_keypoints(image, model=None, confidence_thresh=0.5):
    """Detect keypoints with fallback."""
    if model:
        kps = detect_keypoints_yolo(image, model)
        if kps is not None and len(kps) > 0 and np.mean(kps[:,2]) > confidence_thresh:
            return kps[:,:2]  # x,y only
    # Fallback
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) if len(image.shape) == 3 else image
    return detect_keypoints_fallback(gray)