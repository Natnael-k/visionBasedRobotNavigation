from epson_robot_connector import EpsonRobotController

class RobotArmController:
    
    def __init__(self):
        # Initialize robot arm controller
        self.robotconnctor = EpsonRobotController()
        pass
    
    def move_to_pose_depth_detection(self, pose):
        # Move the robot arm to the specified pose
        pass
    
    def move_to_pose_speed_estim(self, pose):
        # Move the robot arm to the specified pose
        pass
    
    def grip_object(self, pose, grab_zone=False):
        # Perform gripping action
        pass
    
    def release_object(self, pose):
        # Perform releasing action
        pass
    
    def move_to_home(self, pose):
        # Move the robot to home position where and wait for detection
        pass
    
    def tracking(self, pose):
        #visual servoing
        pass
    
    def object_in_grab_zone(self, depth, error ):
        #is object in grab zone
        pass