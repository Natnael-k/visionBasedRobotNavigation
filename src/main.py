import cv2
import numpy as np
import Object_Detection
import Object_Tracking
import Robot_Arm_Control
import Visual_Servoing
import Calibration
import os
import time

class FSM_Controller:
    def __init__(self):
        
        self.state = "calibrating"
        self.object_detector = Object_Detection.YOLOObjectDetector()
        self.object_tracking = Object_Tracking.ObjectTracker()
        self.visual_servoing_controller = Visual_Servoing.VisualServoingController()
        self.robot_arm_controller = Robot_Arm_Control.RobotArmController()
        self.object_of_interest = 'object'  # Replace 'object' with your object of interest
        
         # Initialize camera and calibration
        self.cap = cv2.VideoCapture(0)
        self.calibration = Calibration.CameraCalibration()
        self.desired_bbox = None
        self.desired_centroid = None
        
        # Path to folder to save calibration images
        self.calibration_image_folder = 'calibration_images'
        
        # Create folder if it doesn't exist
        if not os.path.exists(self.calibration_image_folder):
            os.makedirs(self.calibration_image_folder)
        
        #caliberation image initalisation
        self.calibration_images_taken = 0
        
        #object detection output initialisation
        self.object_detected = False
        self.bbox = None
        
        #object tracking output initialisation
        self.speed = 0
        self.centroid = None
    
    def run(self):
        
        #move_robot_to_Home_Position
        Robot_Arm_Control.move_robot_home()
        
        while True:
            
            ret, frame = self.cap.read()
            if not ret:
                break
             # Undistort the frame
            frame_undistorted = self.calibration.undistort_image(frame)
            
            if self.state == "calibrating":
                #initialise time
                start_time = time.time()
                cv2.putText(frame, "Place chessboard in different orientations and press 's' to capture calibration image.",
                            (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                cv2.imshow('Frame', frame)
                
                key = cv2.waitKey(1) & 0xFF
                if key == ord('s'):
                    # Save calibration image
                    image_filename = os.path.join(self.calibration_image_folder, f'calibration_image_{self.calibration_images_taken}.png')
                    cv2.imwrite(image_filename, frame)
                    self.calibration_images_taken += 1
                    print(f"Calibration image {self.calibration_images_taken} captured.")
                
                if self.calibration_images_taken >= 5:
                    print("Calibration images captured. Starting calibration process...")
                    # Perform camera calibration
                    self.calibration.calibrate_camera(self.calibration_image_folder)
                    self.state = "detection_and_tracking"
                    
                    end_time = time.time()
                    print(f"Camera calibration completed. This took {end_time - start_time} seconds")  

            elif self.state == "caliberating_pickup_depth":
                 
                # Capture an image
                cv2.putText(frame_undistorted, "Place object of interest 10cm away from the camera in BeV oritentation and press 's' to capture calibration image.",
                            (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                cv2.imshow('Frame', )
                
                key = cv2.waitKey(1) & 0xFF
                if key == ord('s'):
                    # Save calibration image
                    image_filename = os.path.join(self.calibration_image_folder, f'pickup_depth_calibration_image.png')
                    cv2.imwrite(image_filename, frame_undistorted)

                # Perform object detection
                detected_object, self.desired_bbox = self.object_detector.detect_object_of_interest(frame_undistorted)
                if detected_object:
                    # Calculate centroid
                    centroid_x = (self.desired_bbox[0] + self.desired_bbox[2]) // 2
                    centroid_y = (self.desired_bbox[1] + self.desired_bbox[3]) // 2
                    self.desired_centroid = (centroid_x, centroid_y)
            
            # Other states and operations
            elif self.state == "detection_and_tracking":
                 #initialise time
                start_time = time.time()
                # Search for object of interest
                object_detected, self.bbox = self.object_detector.detect_object_of_interest(frame_undistorted)
                if object_detected:
                    # initialise object tracking
                    self.object_Tracking.start_tracking(frame_undistorted , self.bbox)
                    # Implement Speed estimation
                    self.centroid, self.speed = Object_Tracking.update(frame_undistorted)
                    # Perform visual servoing to adjust robot arm motion
                    control_signal = self.visual_servoing_controller(start_time, self.speed, self.centroid, self.bbox, self.desired_centroid, self.desired_bbox)
                    self.robot_arm_controller.move_to_pose(control_signal)
                    
                    if self.robot_arm_controller.object_in_grab_zone():
                        self.state = "picking"
            
            elif self.state == "picking":
                # Move robot arm to pick up the object
                self.robot_arm_controller.grip_object(self.speed, self.centroid)
                self.state = "placing"
            
            elif self.state == "placing":
                # Move robot arm to place the object in the bin
                self.robot_arm_controller.release_object()
                self.state = "searching"
                
            cv2.imshow('Frame', frame_undistorted)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        
        self.cap.release()
        cv2.destroyAllWindows()

def main():
    fsm = FSM_Controller()
    fsm.run()

if __name__ == "__main__":
    main()
