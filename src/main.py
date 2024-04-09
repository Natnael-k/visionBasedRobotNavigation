import cv2
import numpy as np
import Object_Detection
import Object_Tracking
import Robot_Arm_Control
import Visual_Servoing
import Calibration

class FSM_Controller:
    def __init__(self):
        
        self.state = "searching"
        self.object_detector = Object_Detection.YOLOObjectDetector()
        self.object_tracking = Object_Tracking.ObjectTracker()
        self.visual_servoing_controller = Visual_Servoing.VisualServoingController()
        self.robot_arm_controller = Robot_Arm_Control.RobotArmController()
        self.object_of_interest = 'object'  # Replace 'object' with your object of interest
    
    def run(self):
        
        #intialize the camera
        cap = cv2.VideoCapture(0)
        
        #caliberate the camera
        distance = Calibration.calculate_distance()
        
        #move_robot_to_Home_Position
        Robot_Arm_Control.move_robot_home()
        
        while True:
            
            ret, frame = cap.read()
            if not ret:
                break
            
            if self.state == "searching":
                
                # Search for object of interest
                object_detected, bbox = self.object_detector.detect_object_of_interest(frame)
                if object_detected:
                    self.state = "tracking"
                    break
            
            elif self.state == "tracking":
                
                # initialise object tracking
                self.object_Tracking.start_tracking(frame, bbox)
                # Implement Speed estimation
                centroid, self.speed = Object_Tracking.update(frame)
                # Perform Depth Estimation
                # Perform visual servoing to adjust robot arm motion
                control_signal = self.visual_servoing_controller.compute_control_signal(centroid, bbox)
                self.robot_arm_controller.move_to_pose(centroid)
                
                if self.robot_arm_controller.object_in_grab_zone():
                    self.state = "picking"
            
            elif self.state == "picking":
                # Move robot arm to pick up the object
                self.robot_arm_controller.grip_object()
                self.state = "placing"
            
            elif self.state == "placing":
                # Move robot arm to place the object in the bin
                self.robot_arm_controller.release_object()
                self.state = "searching"
                
            cv2.imshow('Frame', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        
        cap.release()
        cv2.destroyAllWindows()

def main():
    fsm = FSM_Controller()
    fsm.run()

if __name__ == "__main__":
    main()
