# ProfileForge Execution Plan

Based on the goals and roadmap in README.md, here's the step-by-step execution plan to implement ProfileForge.

## High Priority Tasks

1. **Collect and Annotate Initial Dataset**
   - Gather bullet photos (e.g., from data/images/)
   - Annotate keypoints: upper-jaw, lower-jaw, meplat-tip, ogive-shoulder-left/right, boattail-start-left/right, boattail-heel-major-left/right, boattail-heel-minor-left/right
   - Use LabelStudio or Roboflow for annotation
   - Export to YOLO format for training

2. **Build Classical CV Prototype**
   - Implement scale calibration using OpenCV (jaw detection via Hough lines, OCR with easyocr)
   - Contour fitting for keypoints
   - Basic geometry computation (circle fit for R, line fits for angles)
   - Test on sample images

3. **Create YOLOv8-Pose Training Script and Baseline Model**
   - Write train_yolo.py (already in src/)
   - Train on annotated dataset
   - Save model to models/yolo_bullet_pose.pt

4. **Integrate Full End-to-End Pipeline**
   - Combine classical CV with YOLO detection
   - Add JSON output for dimensions: OAL, R, Rt, Rt/R, lengths, angles, diameters
   - Run pipeline.py with annotated images

5. **Validate Against Benchmarks**
   - Test on Hornady 140gr ELD-M (OAL=1.380", R=11.77 cal, Rt/R=0.84)
   - Test on Sierra 175gr SMK (OAL=1.240", R=7 cal, Rt/R=0.4)
   - Ensure tolerances: ±0.03 cal for R, ±0.004 for Rt/R, etc.

## Medium Priority Tasks

6. **Add Robustness Improvements**
   - Error handling for failures
   - Repeatability checks (run multiple times)
   - Tilt correction via symmetry
   - Suggest re-photo if tilt >5° or low confidence

7. **Implement Linting and Typechecking**
   - Add ruff for linting, mypy for typechecking
   - Set up in CI/CD (e.g., GitHub Actions)

8. **Test on Various Bullet Types**
   - VLD, polymer tip, flat base bullets
   - Different lighting conditions
   - Expand dataset and retrain if needed

## Low Priority Tasks

9. **Develop Web/UI Wrapper (Optional)**
   - Use Flask or Streamlit
   - Upload photo, input OAL, display results

## Recommended Pre-trained Models

Based on research for keypoint detection on custom objects like bullets:

- **Ultralytics YOLOv8-pose** (Primary): Pre-trained on COCO, fine-tunable for 11+ bullet keypoints. Supports custom training via Roboflow/trainYOLO. Recommended for speed and accuracy.
- **MMPose (OpenMMLab)**: Pre-trained models (e.g., HRNet) on COCO, adaptable for precision keypoint detection.
- **Detectron2 Keypoint R-CNN**: From Meta, pre-trained on COCO, extensible via Mask R-CNN for custom keypoints.
- **Roboflow Universe Models**: Pre-trained or custom-trained keypoint models for industrial objects.
- **Torchvision Keypoint R-CNN**: Pre-trained on COCO, suitable for fine-tuning.

For scale calibration OCR: EasyOCR (pre-trained on text) or Tesseract. No specific models for geometry fitting (use SciPy).

## Notes
- Run lint/typecheck after each code change
- Commit changes only after verification
- Start with high-priority tasks sequentially, then parallelize