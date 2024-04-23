import numpy as np
import cv2
import glob

class CameraCalibration:
    def __init__(self, chessboard_size=(16, 8), frame_size=(1440, 1080)):
        self.chessboard_size = chessboard_size
        self.frame_size = frame_size
        self.criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)
        self.objp = np.zeros((chessboard_size[0] * chessboard_size[1], 3), np.float32)
        self.objp[:, :2] = np.mgrid[0:chessboard_size[0], 0:chessboard_size[1]].T.reshape(-1, 2)
        self.obj_points = []  # 3D Points in real-world Space
        self.img_points = []  # 2D points in Image Plane
        self.camera_matrix = None
        self.dist_coefficients = None
        self.is_camera_caliberated = False  

    def find_chessboard_corners(self, image):
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        ret, corners = cv2.findChessboardCorners(gray, self.chessboard_size, None)
        return ret, corners, gray

    def calibrate_camera(self):
        images = glob.glob('*.png')

        for image_path in images:
            print(image_path)
            img = cv2.imread(image_path)
            ret, corners, gray = self.find_chessboard_corners(img)

            if ret:
                corners2 = cv2.cornerSubpix(gray, corners, (11, 11), (-1, -1), self.criteria)
                self.obj_points.append(self.objp)
                self.img_points.append(corners)

        ret, self.camera_matrix, self.dist_coefficients, _, _ = cv2.calibrateCamera(
            self.obj_points, self.img_points, self.frame_size, None, None)
        
        self.is_camera_caliberated = True
        
        print("Camera Calibrations: ", ret)
        print("\nCamera Matrix:\n", self.camera_matrix)
        print("\nDistortion Parameters:\n", self.dist_coefficients)

    def undistort_image(self, image_path, is_camera_claiberated):
        
        if is_camera_claiberated:
        
            img = cv2.imread(image_path)
            h, w = img.shape[:2]
            new_camera_matrix, roi = cv2.getOptimalCameraMatrix(self.camera_matrix, self.dist_coefficients,
                                                                (w, h), 1, (w, h))
            dst = cv2.undistort(img, self.camera_matrix, self.dist_coefficients, None, new_camera_matrix)
            x, y, w, h = roi
            undistorted_image = dst[y:y+h, x:x+w]
            
            return undistorted_image
        
        else:
            pass