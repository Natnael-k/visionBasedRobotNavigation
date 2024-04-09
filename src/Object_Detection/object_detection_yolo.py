import cv2
from ultratics import YOLO


class YOLOObjectDetector:
    def __init__(self, model_config_path, model_weights_path, labels_path, object_of_interest, confidence_threshold=0.5, nms_threshold=0.4):
        self.net = cv2.dnn.readNetFromDarknet(model_config_path, model_weights_path)
        self.labels = open(labels_path).read().strip().split('\n')
        self.object_of_interest = object_of_interest
        self.confidence_threshold = confidence_threshold
        self.nms_threshold = nms_threshold

    def detect_object_of_interest(self, frame):
        h, w = frame.shape[:2]
        blob = cv2.dnn.blobFromImage(frame, 1/255.0, (416, 416), swapRB=True, crop=False)
        self.net.setInput(blob)
        layer_names = self.net.getLayerNames()
        output_layers = [layer_names[i[0] - 1] for i in self.net.getUnconnectedOutLayers()]
        detections = self.net.forward(output_layers)

        for detection in detections:
            for obj in detection:
                scores = obj[5:]
                class_id = np.argmax(scores)
                confidence = scores[class_id]
                if confidence > self.confidence_threshold and self.labels[class_id] == self.object_of_interest:
                    center_x = int(obj[0] * w)
                    center_y = int(obj[1] * h)
                    width = int(obj[2] * w)
                    height = int(obj[3] * h)
                    left = int(center_x - width / 2)
                    top = int(center_y - height / 2)
                    return True, (left, top, width, height)

        return False, None