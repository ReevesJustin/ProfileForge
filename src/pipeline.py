import argparse
import json
import cv2
from src.preprocessing import preprocess_image
from src.scale_calibration import calibrate_scale
from src.keypoint_detection import detect_keypoints, load_yolo_model
from src.geometry_fitting import compute_dimensions
from src.validation import validate_results
from src.visualization import annotate_image, save_annotated

def main(image_path, oal=None, output_dir='outputs/'):
    # Preprocess
    gray, mask = preprocess_image(image_path)

    # Scale
    px_per_inch, jaws = calibrate_scale(gray, oal)
    if px_per_inch is None:
        print("Scale calibration failed. Provide OAL.")
        return

    # Keypoints
    model = load_yolo_model()
    img = cv2.imread(image_path)  # for YOLO
    keypoints = detect_keypoints(img, model)

    # Geometry
    dimensions = compute_dimensions(keypoints, px_per_inch)

    # Validate
    tilt_ok, errors = validate_results(dimensions, keypoints)

    # Visualize
    annotated = annotate_image(img, keypoints, dimensions)
    save_annotated(annotated, f"{output_dir}/annotated_{image_path.split('/')[-1]}")

    # Output JSON
    result = {'dimensions': dimensions, 'errors': errors, 'tilt_ok': tilt_ok}
    with open(f"{output_dir}/result.json", 'w') as f:
        json.dump(result, f)

    print("Pipeline completed.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--image', required=True)
    parser.add_argument('--oal', type=float)
    args = parser.parse_args()
    main(args.image, args.oal)