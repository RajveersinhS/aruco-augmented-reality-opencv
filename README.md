# aruco-augmented-reality-opencv

# ArUco Augmented Reality Poster Overlay using OpenCV

This project demonstrates a simple **Augmented Reality (AR) system using ArUco markers and computer vision techniques**.  
The system detects ArUco markers in an image and overlays a poster onto the detected marker surface using **homography-based perspective transformation**.

The implementation is developed using **Python, OpenCV, and NumPy**, and was created as part of the **Computer Vision course at Ravensburg-Weingarten University of Applied Sciences (RWU)**.

---

## Project Overview

Augmented Reality systems often rely on visual markers to determine the position and orientation of objects in the real world.

In this project:

1. **ArUco markers** are detected in the scene.
2. The marker corners are used to estimate the **geometric transformation**.
3. A poster image is **warped to match the perspective** of the detected marker.
4. The transformed poster is **blended into the scene**, creating an AR effect.

The final result is a realistic **poster overlay aligned with the physical marker in the image**.

---

## Algorithm Pipeline

The system follows the steps below:

### 1. ArUco Marker Detection
- Detect markers in the image using OpenCV's `cv2.aruco.detectMarkers()` function.
- Marker IDs and corner coordinates are extracted.

### 2. Quadrilateral Mapping
- The poster image is mapped to a smaller quadrilateral region.
- Poster dimensions are scaled using predefined ratios.

### 3. Homography Estimation
- Corresponding points between the poster and marker corners are used.
- The transformation matrix is computed using:

### 4. Perspective Transformation
- The poster is warped to match the perspective of the marker using:

### 5. Image Blending
- A mask is created to isolate the marker region.
- Bitwise operations merge the poster with the original scene.

This results in a **natural-looking augmented poster embedded in the environment**.

---

## Example Output

| Input Image | AR Output |
|-------------|-----------|
| ![](https://github.com/RajveersinhS/aruco-augmented-reality-opencv/blob/main/Assets/Image_1.jpg) | ![](results/sample_outputs/output1.jpg) |

*(Replace these images with your own examples from the results folder.)*

---

## Project Structure
aruco-augmented-reality-opencv
│
├── src
│ └── main.py
│
├── assets
│ ├── posters
│ └── sample_inputs
│
├── results
│ └── sample_outputs
│
├── report
│ └── Project_Report_Task1_Augmented_Reality.pdf
│
├── requirements.txt
├── README.md
└── .gitignore


---

## Installation

Clone the repository: https://github.com/RajveersinhS/aruco-augmented-reality-opencv.git
