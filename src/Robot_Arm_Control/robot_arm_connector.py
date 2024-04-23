from Robot_Arm_Control import EpsonRobotController

class RobotArmController:
    
    def __init__(self):
        # Initialize robot arm controller
        self.robot_connctor = EpsonRobotController("127.0.0.1", 2001)
        pass
    
    def grip_object(self, pose, grab_zone=False):
        # Perform gripping action
        if grab_zone:
            self.robot_connctor.grip("open")
        pass
    
    def release_object(self, drop_zone=False):
        # Perform releasing action
        if drop_zone:
            self.robot_connctor.grip("open")
        pass
    
    def move_to_home(self, home_pose):
        # Move the robot to home position where and wait for detection
        x , y , z = home_pose
        self.robot_connector.go(x, y, z, 0)
        pass
    
    def tracking(self, error_pose):
        #visual servoing
        x , y , z = error_pose
        self.robot_connector.go(x, y, z, 0)
        pass
    