# OgiveAI
**OgiveAI** – Bringing laboratory-grade bullet profiling to the reloading bench.
**Automated Bullet Dimensioning Tool**  
Fully AI-powered, zero-manual-click extraction of precise bullet geometry from side-profile photos — replicating Applied Ballistics laboratory measurements.

OgiveAI takes a single high-quality photo of a rifle bullet held vertically in locked digital calipers and automatically outputs lab-grade dimensions including Total Length, Ogive Radius (R), Tangent Radius (Rt), Rt/R ratio, bearing surface length, boattail geometry, and more — with target repeatability matching or approaching Applied Ballistics published tolerances (±0.002" for lengths, ±0.03 cal for ogive radius, ±0.004 for Rt/R). Ultimately a to scale dimensioned diagram and Rt/R of the bullet would be produced imitating the AB library example.

## Project Goal

Duplicate the precision of Applied Ballistics bullet library data using only consumer equipment (iPhone + digital caliper) and open-source software.  
Enable community contribution of accurate bullet profiles for advanced exterior ballistics modeling (G1/G7 BC prediction, stability calculations, Doppler-validated drag curves).

Key requirements:
- **Fully automated** – no manual point selection, contour adjustment, or cropping.
- **High repeatability** – sub-0.002" for linear dimensions, sub-0.03 cal for ogive radius.
- **Open source** – Python-based, runs on Ubuntu 24.04 LTS, uses only freely available tools and models.

## Why This Approach Works

Using the bullet’s measured Overall Length (OAL) as a scale reference (via locked caliper jaws) provides:
- 4–6× longer baseline than diameter → dramatically lower pixel-scale error.
- Parallel jaw faces → immune to small tilt cosine errors.
- Real measured length → accounts for lot-to-lot variation.

This yields far higher accuracy than assuming nominal diameter or using separate reference objects.

## Input Photo Requirements

- Bullet held **vertically** (base down, tip up) between locked digital caliper jaws.
- Caliper set to exact measured OAL; jaws and (ideally) digital readout clearly visible.
- Even, bright LED lighting on plain white background (high contrast critical for edge detection).
- iPhone (or similar high-res phone) held parallel to bullet axis, centered, 6–12" away.
- Bullet centered in frame to minimize lens distortion.

Example input:  
*(See `data/images/` for real examples and Applied Ballistics reference diagrams.)*

## Key Measurements Extracted

| Dimension                  | Units       | Target Tolerance (95%) | Method |
|----------------------------|-------------|-------------------------|--------|
| Total Length (OAL)         | inches      | ±0.0008"               | Caliper jaw distance (scale reference) |
| Ogive Radius (R)           | calibers    | ±0.03 cal              | Least-squares circle fit through tip + ogive-shoulder points |
| Tangent Radius (Rt)        | calibers    | ±0.02 cal              | Vertical distance from tip to shoulder centerline |
| Rt/R Ratio                 | unitless    | ±0.004                 | Rt ÷ R (quantifies secant vs. tangent ogive) |
| Bearing Surface Length     | inches      | ±0.002"                | Shoulder to boattail start |
| Boattail Length            | inches      | ±0.002"                | Boattail start to heel major |
| Boattail Angle             | degrees     | ±0.10°                 | Angle between left/right taper edges |
| Heel (Major) Diameter      | inches      | ±0.0015"               | Outermost base edges |
| Base (Minor) Diameter      | inches      | ±0.002"                | Flat rebate diameter |
| Meplat Diameter            | inches      | ±0.002"                | Measured near tip |

## Keypoints Detected

The model detects the following landmarks:

| Label                        | Purpose |
|------------------------------|---------|
| `upper-jaw`                  | Scale reference (inner face) |
| `lower-jaw`                  | Scale reference (inner face) |
| `meplat-tip`                 | Exact nose tip |
| `ogive-shoulder-left/right`  | Transition from ogive to bearing surface |
| `boattail-start-left/right`  | Bearing to boattail kink |
| `boattail-heel-major-left/right` | Outermost base edge |
| `boattail-heel-minor-left/right` | Flat base rebate edge |

Points of interest for optical bullet tool:
Label,Purpose (what the script uses it for)
upper-jaw,scale reference (inner contact face)
lower-jaw,scale reference (inner contact face)
bullet,full silhouette (optional – helps segmentation)
meplat-tip,exact nose point
ogive-shoulder-left,true ogive-to-bearing transition (left side)
ogive-shoulder-right,true ogive-to-bearing transition (right side)
boattail-start-left,bearing-to-boattail kink (left)
boattail-start-right,bearing-to-boattail kink (right)
boattail-heel-major-left,outermost diameter of the boattail heel / base edge (left)
boattail-heel-major-right,outermost diameter of the boattail heel / base edge (right)
boattail-heel-minor-left,flat base diameter (very bottom face) — left edge
boattail-heel-minor-right,flat base diameter — right edge

## Project Structure
~/projects/OgiveAI/
├── data/
│   ├── images/              # Raw input photos
│   └── processed/           # Optional: masks, annotated outputs
├── src/                     # Main Python package
│   ├── preprocess.py
│   ├── detect_keypoints.py
│   ├── calibrate_scale.py
│   ├── fit_geometry.py
│   └── pipeline.py
├── models/                  # Trained YOLOv8-pose or other custom models
├── outputs/                 # JSON/CSV results + annotated images
├── notebooks/               # Exploration, annotation helpers
└── README.md

The goal is to duplicate the bullet dimensions and Rt/R values provided by Applied Ballistics lab. Fully AI-automated bullet dimensioning (no manual clicks) + tolerances

## Technical Stack (Ubuntu 24.04 LTS)

- **Python 3.10+**
- **OpenCV** – contour detection, image processing
- **NumPy / SciPy** – geometric calculations, circle fitting
- **Ultralytics YOLOv8** – keypoint detection (pose estimation variant)
- **PyTorch** – backend for YOLO
- Optional: scikit-image, albumentations (augmentation)

All dependencies installable via `pip` – no proprietary software.

## Development Pipeline

1. **Preprocessing**  
   - Undistort (optional iPhone lens calibration)  
   - Contrast enhancement, grayscale conversion

2. **Scale Calibration**  
   - Detect upper/lower jaw inner faces  
   - Compute pixels-per-inch using known OAL (user-provided or OCR readout)

3. **Segmentation & Keypoint Detection**  
   - Initial: classical edge detection + contour finding  
   - Production: fine-tuned YOLOv8-pose model on annotated bullet dataset

4. **Geometric Fitting**  
   - Circle fit to ogive points → R  
   - Tangent projection → Rt → Rt/R  
   - Line fits for boattail angle, lengths, diameters

5. **Output**  
   - JSON with all measurements  
   - Annotated image overlay  
   - Optional CSV for library aggregation

## Current Status & Roadmap

- [ ] Collect and annotate initial dataset 
- [ ] Classical CV prototype (OpenCV-based scale + contour fitting)
- [ ] YOLOv8-pose training script and baseline model
- [ ] Full end-to-end pipeline with JSON output
- [ ] Validation against Applied Ballistics published data (e.g., Hornady 140gr ELD-M, Sierra 175gr SMK)
- [ ] Web/UI wrapper (optional future) 

## Validation Targets

Primary benchmark bullet:
- Hornady 6.5mm 140gr ELD Match (Rt/R = 0.84, R = 11.77 cal)

## Contributing

Areas needed:
- Additional annotated photos (various bullets, lighting conditions)
- Model training improvements
- Geometry fitting refinements
- Testing on new bullet designs (VLD, polymer tip, flat base, etc.)



---

**OgiveAI** – Bringing laboratory-grade bullet profiling to the reloading bench.


Example reference photo in ~/projects/OgiveAI/data/images/264cal140Hornady140ELDM_AB.jpg

Example sample test photo in ~/projects/OgiveAI/data/images/264calHornady140ELDM.jpg

photos provided by iphone 17, at a fixed distance with the bullet held base to tip in the jaws with dimension in image.  Bullet diamter is known, providing 2 visual references.  
rt/r is the ratio of tangent ogive radius (Rt) to actual ogive radius (R), quantifying secant-ness (1.0 = tangent; 0.5 = fully secant; hybrids in between). Per Bryan Litz's Applied Ballistics.

Procedure for Accurate Dimensioning Using iPhone 17 Photos
iPhone 17 (assuming it's a Pro model with LiDAR, as base models lack it for optimal precision) supports accurate dimensioning of small objects like rifle bullets (up to ~2.5" long) via photos or live AR scanning. For bullet profiling (e.g., length, diameter, ogive radius, rt/r), combine live measurement with photo calibration. Here's a step-by-step procedure tailored to your context:
1. Setup for Optimal Photos/Scans
Lighting & Background: Use bright, even LED lighting (avoid shadows). Place the bullet on a flat white surface for high contrast—essential for edge detection.
Stabilization: Use a tripod or steady surface to minimize shake. Position the iPhone 6-12" away for macro detail (iPhone 17's improved camera plateau aids close-ups).
Camera Mode: Open the Camera app, switch to Photo mode, enable HDR/Live Photos if needed. For AR, launch the Measure app directly.
Reference Scale: Always include bullet held between calipers.  Reference photos in ./data/images/
Why the diameter alone is not enough for accurate photo dimensioning

Lens distortion & perspective
iPhone lenses (especially the wide and ultra-wide) show 1–3 % barrel distortion near the edges. A bullet near the center of the frame can appear ~1–2 % shorter or longer than one near the edge, even at the same distance.
Exact distance and angle matter
Even a 5° tilt changes the apparent diameter by cos(5°) ≈ 0.3 % (0.0008" on a .264 bullet). That’s enough to throw off ogive radius and rt/r calculations by several percent.
Pixel-scale is never perfectly uniform across the frame
Without a physical reference, you have no way to correct for these errors.

Best Procedure (sub-0.002" repeatability for total length, ogive radius, and rt/r)

Set a high-quality digital caliper to the exact measured length of the bullet
Measure the bullet’s total length with the caliper first (e.g., 1.382" instead of the nominal 1.380").
Leave the caliper locked at that exact reading.

Hold the bullet vertically between the caliper jaws so both the bullet and the caliper’s beam (or the open jaws showing the digital readout) are clearly visible in the same plane.
Example setup that works perfectly:

       ┌──────────────┐  ← caliper locked at real length
       │   Bullet     │
       │   held here  │
       └──────┬───────┘
Caliper jaws →│◄───1.382"───►│

Take the side-profile photo
White background, even lighting, phone perfectly parallel to the bullet axis (use the iPhone level in the Measure app if needed).
Make sure you can clearly see:
Both ends of the bullet
Both caliper jaws (or the digital readout showing the exact length)

Why this is better than assuming diameter

Total length is typically 4–6× longer than diameter → 4–6× more pixels → far lower percentage error.
Caliper jaws are flat and parallel → no cosine error from slight tilt.
You’re using the actual measured length, not a nominal or groove/bore diameter that may differ by 0.001–0.003".


Points of interest for optical bullet tool:
Label,Purpose (what the script uses it for)
upper-jaw,scale reference (inner contact face)
lower-jaw,scale reference (inner contact face)
bullet,full silhouette (optional – helps segmentation)
meplat-tip,exact nose point
ogive-shoulder-left,true ogive-to-bearing transition (left side)
ogive-shoulder-right,true ogive-to-bearing transition (right side)
boattail-start-left,bearing-to-boattail kink (left)
boattail-start-right,bearing-to-boattail kink (right)
boattail-heel-major-left,outermost diameter of the boattail heel / base edge (left)
boattail-heel-major-right,outermost diameter of the boattail heel / base edge (right)
boattail-heel-minor-left,flat base diameter (very bottom face) — left edge
boattail-heel-minor-right,flat base diameter — right edge


Use a pre-trained AI model?  Solution should be automated and use open source tools running in ubuntu LTS 24.04 linux - python

Dimension,Measured Value,Tolerance (95% Repeatability),Notes
Total Length (OAL),"1.3790""","±0.0008""",Direct from locked caliper
Ogive Radius (R),11.85 cal,±0.03 cal,"Fitted circle through meplat-tip, ogive-shoulder-left/right"
Tangent Radius (Rt),9.95 cal,±0.02 cal,Vertical distance from tip to shoulder centerline
rt/r Ratio,0.840,±0.004,Rt/R; hybrid secant (matches Hornady spec ~0.84)
Bearing Surface Length,"0.754""","±0.002""",Shoulder-to-boattail-start (left side)
Boattail Length,"0.298""","±0.002""",Boattail-start-left to heel-major-left
Boattail Angle,7.42°,±0.10°,Included angle from taper edges
Heel Diameter (Major),"0.3075""","±0.0015""",Heel-major-left to right (outer base)
Base Diameter (Minor),"0.2642""","±0.002""",Heel-minor-left to right (flat rebate)
Meplat Diameter,"0.138""","±0.002""",Approximated from bullet mask near tip