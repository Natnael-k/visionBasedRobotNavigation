import time


class VisualServoingController:
    def __init__(self, start_time, object_speed, centroid, bbox, desired_centroid, desired_bbox, gain_x=1.2, gain_y=1.4, gain_z=1.2):
       
        self.desired_centroid = desired_centroid
        self.object_centroid = centroid
        self.object_speed = object_speed
        self.desired_bbox = desired_bbox
        self.bbox = bbox
        self.gain_x = gain_x
        self.gain_y = gain_y
        self.gain_z = gain_z
        self.start_time = start_time
    
    def update_object_info(self, centroid, speed, depth):
        self.object_centroid = centroid
        self.object_speed = speed
        self.depth = depth
    
    def calculate_trajectory(self):
        # Calculate error between current and desired centroid
        error_x = self.desired_centroid[0] - self.object_centroid[0]
        error_y = self.desired_centroid[1] - self.object_centroid[1]
        
        # Compute control signals (proportional control)
        control_signal_x = error_x * self.gain_x
        control_signal_y = error_y * self.gain_y
        
        # Calculate depth error based on bounding box size
        desired_bbox_area = (self.desired_bbox[2] - self.desired_bbox[0]) * (self.desired_bbox[3] - self.desired_bbox[1])
        bbox_area = (self.bbox[2] - self.bbox[0]) * (self.bbox[3] - self.bbox[1])
        
        # Compute control signal for depth (proportional control)
        error_z = desired_bbox_area - bbox_area
        control_signal_z = error_z * self.gain_z
        
        # Update current distance based on object speed and depth
        dt= time.time() - self.start_time
        error_x += self.object_speed * dt
        
        # Return desired position and velocity for robot gripper
        desired_position = [error_x, error_y, error_z]
       
        return desired_position