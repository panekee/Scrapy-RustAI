"""
Object Detection Module
Uses YOLO for detecting game objects.
"""

import cv2
import numpy as np
from ultralytics import YOLO
from typing import List, Dict, Tuple, Optional
import os


class ObjectDetector:
    """Detects objects in game frames using YOLO."""

    def __init__(self, model_path: Optional[str] = None, confidence_threshold: float = 0.5):
        """
        Initialize object detector.

        Args:
            model_path: Path to custom YOLO model (uses YOLOv8n by default)
            confidence_threshold: Minimum confidence for detections
        """
        self.confidence_threshold = confidence_threshold

        if model_path and os.path.exists(model_path):
            self.model = YOLO(model_path)
        else:
            # Use pre-trained YOLOv8 nano model
            self.model = YOLO('yolov8n.pt')

    def detect_objects(self, frame: np.ndarray) -> List[Dict]:
        """
        Detect objects in a frame.

        Args:
            frame: Input image as numpy array

        Returns:
            List of detected objects with bounding boxes and labels
        """
        results = self.model(frame, conf=self.confidence_threshold, verbose=False)

        detections = []
        for result in results:
            boxes = result.boxes

            for box in boxes:
                detection = {
                    'class_id': int(box.cls[0]),
                    'class_name': self.model.names[int(box.cls[0])],
                    'confidence': float(box.conf[0]),
                    'bbox': box.xyxy[0].tolist(),  # [x1, y1, x2, y2]
                    'center': self._get_bbox_center(box.xyxy[0].tolist())
                }
                detections.append(detection)

        return detections

    def detect_specific_object(self, frame: np.ndarray, target_class: str) -> Optional[Dict]:
        """
        Detect a specific object class.

        Args:
            frame: Input image
            target_class: Name of the class to detect (e.g., 'person', 'car')

        Returns:
            Detection dict or None if not found
        """
        detections = self.detect_objects(frame)

        for detection in detections:
            if detection['class_name'] == target_class:
                return detection

        return None

    def find_all_of_class(self, frame: np.ndarray, target_class: str) -> List[Dict]:
        """
        Find all instances of a specific class.

        Args:
            frame: Input image
            target_class: Name of the class to detect

        Returns:
            List of all detections matching the class
        """
        detections = self.detect_objects(frame)
        return [d for d in detections if d['class_name'] == target_class]

    def draw_detections(self, frame: np.ndarray, detections: List[Dict]) -> np.ndarray:
        """
        Draw bounding boxes on frame.

        Args:
            frame: Input image
            detections: List of detections to draw

        Returns:
            Frame with drawn detections
        """
        output_frame = frame.copy()

        for detection in detections:
            x1, y1, x2, y2 = map(int, detection['bbox'])
            label = f"{detection['class_name']}: {detection['confidence']:.2f}"

            # Draw bounding box
            cv2.rectangle(output_frame, (x1, y1), (x2, y2), (0, 255, 0), 2)

            # Draw label
            cv2.putText(output_frame, label, (x1, y1 - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

            # Draw center point
            center_x, center_y = detection['center']
            cv2.circle(output_frame, (int(center_x), int(center_y)), 5, (0, 0, 255), -1)

        return output_frame

    @staticmethod
    def _get_bbox_center(bbox: List[float]) -> Tuple[float, float]:
        """
        Calculate center of bounding box.

        Args:
            bbox: [x1, y1, x2, y2]

        Returns:
            (center_x, center_y)
        """
        x1, y1, x2, y2 = bbox
        center_x = (x1 + x2) / 2
        center_y = (y1 + y2) / 2
        return center_x, center_y

    def train_custom_model(self, data_yaml: str, epochs: int = 100):
        """
        Train a custom YOLO model for game-specific objects.

        Args:
            data_yaml: Path to dataset configuration YAML
            epochs: Number of training epochs
        """
        self.model.train(data=data_yaml, epochs=epochs, imgsz=640)
