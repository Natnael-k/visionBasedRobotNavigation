import cv2
import numpy as np
import time



class ObjectTracker:
    
    """Object tracker with Speed Calculator"""
    
    def __init__(self, tracker_type="CSRT"):
        self.tracker = None
        self.prev_centroid = None
        self.prev_time = None
        self.speed = None

    def start_tracking(self, frame, bbox):
        self.tracker = cv2.TrackerCSRT_create()
        self.tracker.init(frame, bbox)
        self.prev_centroid = None
        self.prev_time = None

    def update(self, frame):
        if self.tracker:
            success, bbox = self.tracker.update(frame)
            if success:
                left, top, width, height = [int(i) for i in bbox]
                centroid = (left + width // 2, top + height // 2)
                if self.prev_centroid is not None:
                    displacement = np.sqrt((centroid[0] - self.prev_centroid[0])**2 + (centroid[1] - self.prev_centroid[1])**2)
                    if self.prev_time is not None:
                        time_interval = time.time() - self.prev_time
                        self.speed = displacement / time_interval
                    else:
                        self.speed = None
                else:
                    self.speed = None
                self.prev_centroid = centroid
                self.prev_time = time.time()
                return centroid, bbox, self.speed

        return None, None, None

