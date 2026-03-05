import cv2
import numpy as np
import os

# Define the function to calculate the transformation matrix
def calculate_transform_matrix(marker_corner, poster):
    e = marker_corner[0][0]
    f = marker_corner[0][1]
    g = marker_corner[0][2]
    h = marker_corner[0][3]
    
    height, width, _ = poster.shape
    center_x, center_y = width / 2, height / 2
    
    small_width = width / 9
    small_height = height / 6
    a = (center_x - small_width / 2, center_y - small_height / 2)
    b = (center_x + small_width / 2, center_y - small_height / 2)
    c = (center_x + small_width / 2, center_y + small_height / 2)
    d = (center_x - small_width / 2, center_y + small_height / 2)
    
    input_corners = np.float32([a, b, c, d])
    output_corners = np.float32([e, f, g, h])
    return cv2.getPerspectiveTransform(input_corners, output_corners)

# Input and output folders
input_folder = "Assets"
output_folder = "Results"

# Create the output folder if it doesn't exist
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# Load the ArUco dictionary and parameters
aruco_dict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_6X6_250)
parameters = cv2.aruco.DetectorParameters()

# Create ArUco detector instance
detector = cv2.aruco.ArucoDetector(aruco_dict, parameters)

# Process each image in the input folder
for filename in os.listdir(input_folder):
    # Read the image
    image_path = os.path.join(input_folder, filename)
    classroom_image = cv2.imread(image_path)
    
    # ArUco marker detection
    aruco_corners, ids, _ = detector.detectMarkers(classroom_image)
    
    # Process the image if markers are detected
    if len(aruco_corners) > 0:
        for marker_corner in aruco_corners:
            # Load the poster image
            poster_path = "Poster.jpg"
            poster = cv2.imread(poster_path)
            
            # Calculate the transformation matrix
            M = calculate_transform_matrix(marker_corner, poster)
            
            # Apply perspective transformation to the poster
            transformed_poster = cv2.warpPerspective(poster, M, (classroom_image.shape[1], classroom_image.shape[0]), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT, borderValue=(0, 0, 1, 0))
            
            # Create a black image to use as a mask
            mask = np.zeros_like(classroom_image)
            
            # Fill the area of the transferred poster with white
            cv2.fillPoly(mask, [marker_corner.astype(int)], (255, 255, 255))
            
            # Invert the mask
            inverted_mask = cv2.bitwise_not(mask)
            
            # Exclude the area of the transferred poster from the classroom image
            classroom_without_poster = cv2.bitwise_and(classroom_image, inverted_mask)
            
            # Blend the poster with the classroom image using alpha blending
            alpha = 1  # Adjust the opacity as needed (0.0 - fully transparent, 1.0 - fully opaque)
            blended_image = cv2.addWeighted(transformed_poster, alpha, classroom_without_poster, 0, 1)
            
            # Create a copy of the classroom image
            classroom_copy = classroom_image.copy()
            
            # Integrate the blended image into the copy of the classroom image
            blended_image_gray = cv2.cvtColor(blended_image, cv2.COLOR_BGR2GRAY)
            _, mask = cv2.threshold(blended_image_gray, 1, 255, cv2.THRESH_BINARY)
            mask_inv = cv2.bitwise_not(mask)
            classroom_copy_bg = cv2.bitwise_or(classroom_copy, classroom_copy, mask=mask_inv)
            result = cv2.add(classroom_copy_bg, blended_image)
            
            # Save the result image
            output_image_path = os.path.join(output_folder, f'result_image_{filename}')
            cv2.imwrite(output_image_path, result )
    else:
        print(f"No markers detected in the image: {filename}")