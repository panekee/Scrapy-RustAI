"""
Screen Capture Module
Handles real-time screen capture for the AI player.
"""

import mss
import numpy as np
from typing import Tuple, Optional
import cv2


class ScreenCapture:
    """Captures screen content for AI processing."""

    def __init__(self, monitor_number: int = 1):
        """
        Initialize screen capture.

        Args:
            monitor_number: Monitor to capture (1 = primary)
        """
        self.sct = mss.mss()
        self.monitor = self.sct.monitors[monitor_number]

    def capture_region(self, x: int, y: int, width: int, height: int) -> np.ndarray:
        """
        Capture a specific region of the screen.

        Args:
            x: Top-left x coordinate
            y: Top-left y coordinate
            width: Region width
            height: Region height

        Returns:
            numpy array containing the captured image
        """
        region = {
            "top": y,
            "left": x,
            "width": width,
            "height": height
        }

        screenshot = self.sct.grab(region)
        img = np.array(screenshot)

        # Convert BGRA to RGB
        img = cv2.cvtColor(img, cv2.COLOR_BGRA2RGB)

        return img

    def capture_full_screen(self) -> np.ndarray:
        """
        Capture the full screen.

        Returns:
            numpy array containing the captured image
        """
        screenshot = self.sct.grab(self.monitor)
        img = np.array(screenshot)

        # Convert BGRA to RGB
        img = cv2.cvtColor(img, cv2.COLOR_BGRA2RGB)

        return img

    def capture_game_window(self, config: dict) -> np.ndarray:
        """
        Capture the game window based on configuration.

        Args:
            config: Configuration dictionary with window coordinates

        Returns:
            numpy array containing the captured image
        """
        x = config.get('window_x', 0)
        y = config.get('window_y', 0)
        width = config.get('window_width', 1920)
        height = config.get('window_height', 1080)

        return self.capture_region(x, y, width, height)

    def get_screen_size(self) -> Tuple[int, int]:
        """
        Get the size of the current monitor.

        Returns:
            Tuple of (width, height)
        """
        return self.monitor['width'], self.monitor['height']

    def close(self):
        """Clean up resources."""
        self.sct.close()
