# Define known dimensions of the marker (in meters)
marker_width = 0.1  # Example: 10 cm

# Function to calculate distance from camera to marker
def calculate_distance(marker_corners):
    # Assume marker_corners contains the pixel coordinates of the marker corners
    # Use perspective transformation to get real-world coordinates of marker corners
    marker_corners = np.array(marker_corners, dtype=np.float32).reshape(-1, 1, 2)
    marker_corners_distorted = cv2.undistortPoints(marker_corners, mtx, dist)

    # Calculate distance using known marker dimensions and camera intrinsic parameters
    _, rvec, tvec = cv2.solvePnP(marker_width, marker_corners_distorted, mtx, dist)
    distance = np.linalg.norm(tvec)  # Euclidean distance from camera to marker

    return distance