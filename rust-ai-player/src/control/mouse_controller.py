"""
Mouse Controller Module
Handles mouse input simulation for the AI player.
"""

from pynput.mouse import Controller, Button
import time
from typing import Tuple
import math


class MouseController:
    """Simulates mouse inputs for game control."""

    def __init__(self, sensitivity: float = 1.0):
        """
        Initialize mouse controller.

        Args:
            sensitivity: Mouse sensitivity multiplier
        """
        self.mouse = Controller()
        self.sensitivity = sensitivity

    def get_position(self) -> Tuple[int, int]:
        """
        Get current mouse position.

        Returns:
            Tuple of (x, y) coordinates
        """
        return self.mouse.position

    def move_to(self, x: int, y: int, smooth: bool = False, duration: float = 0.2):
        """
        Move mouse to absolute position.

        Args:
            x: Target x coordinate
            y: Target y coordinate
            smooth: Whether to move smoothly (human-like)
            duration: Duration of smooth movement (seconds)
        """
        if smooth:
            self._smooth_move(x, y, duration)
        else:
            self.mouse.position = (x, y)

    def move_relative(self, dx: int, dy: int):
        """
        Move mouse relative to current position.

        Args:
            dx: Change in x
            dy: Change in y
        """
        current_x, current_y = self.mouse.position
        self.mouse.position = (
            current_x + int(dx * self.sensitivity),
            current_y + int(dy * self.sensitivity)
        )

    def click(self, button: Button = Button.left, clicks: int = 1):
        """
        Click mouse button.

        Args:
            button: Which button to click
            clicks: Number of clicks
        """
        for _ in range(clicks):
            self.mouse.click(button)
            time.sleep(0.05)

    def left_click(self):
        """Perform a left click."""
        self.click(Button.left)

    def right_click(self):
        """Perform a right click."""
        self.click(Button.right)

    def double_click(self):
        """Perform a double click."""
        self.click(Button.left, clicks=2)

    def press(self, button: Button = Button.left):
        """
        Press and hold mouse button.

        Args:
            button: Which button to press
        """
        self.mouse.press(button)

    def release(self, button: Button = Button.left):
        """
        Release mouse button.

        Args:
            button: Which button to release
        """
        self.mouse.release(button)

    def drag(self, x: int, y: int, button: Button = Button.left):
        """
        Drag mouse to position.

        Args:
            x: Target x coordinate
            y: Target y coordinate
            button: Which button to hold while dragging
        """
        self.press(button)
        time.sleep(0.1)
        self.move_to(x, y, smooth=True)
        time.sleep(0.1)
        self.release(button)

    def scroll(self, dy: int):
        """
        Scroll mouse wheel.

        Args:
            dy: Scroll amount (positive = up, negative = down)
        """
        self.mouse.scroll(0, dy)

    # Game-specific methods
    def aim_at_target(self, target_x: int, target_y: int, smooth: bool = True):
        """
        Aim at a target location.

        Args:
            target_x: Target x coordinate
            target_y: Target y coordinate
            smooth: Whether to move smoothly
        """
        self.move_to(target_x, target_y, smooth=smooth, duration=0.15)

    def shoot(self, duration: float = 0.1):
        """
        Shoot weapon (hold left click).

        Args:
            duration: How long to hold fire (seconds)
        """
        self.press(Button.left)
        time.sleep(duration)
        self.release(Button.left)

    def aim_down_sights(self, duration: float = 1.0):
        """
        Aim down sights (hold right click).

        Args:
            duration: How long to aim (seconds)
        """
        self.press(Button.right)
        time.sleep(duration)
        self.release(Button.right)

    def quick_shoot(self, target_x: int, target_y: int):
        """
        Quick aim and shoot at target.

        Args:
            target_x: Target x coordinate
            target_y: Target y coordinate
        """
        self.aim_at_target(target_x, target_y, smooth=True)
        time.sleep(0.1)
        self.shoot(0.1)

    def spray_control(self, pattern: list, fire_duration: float = 1.0):
        """
        Apply spray pattern control while shooting.

        Args:
            pattern: List of (dx, dy) mouse movements for recoil compensation
            fire_duration: Total duration of fire (seconds)
        """
        self.press(Button.left)

        if pattern:
            step_duration = fire_duration / len(pattern)
            for dx, dy in pattern:
                self.move_relative(dx, dy)
                time.sleep(step_duration)

        self.release(Button.left)

    def look_around(self, degrees: float, duration: float = 0.5):
        """
        Look around horizontally.

        Args:
            degrees: Degrees to turn (positive = right, negative = left)
            duration: Duration of turn (seconds)
        """
        # Approximate conversion: depends on game sensitivity
        # This is a rough estimate and should be calibrated per game
        pixels_per_degree = 2.5
        total_dx = int(degrees * pixels_per_degree)

        steps = int(duration / 0.01)
        dx_per_step = total_dx / steps

        for _ in range(steps):
            self.move_relative(dx_per_step, 0)
            time.sleep(0.01)

    def _smooth_move(self, target_x: int, target_y: int, duration: float):
        """
        Move mouse smoothly to target using easing.

        Args:
            target_x: Target x coordinate
            target_y: Target y coordinate
            duration: Duration of movement (seconds)
        """
        start_x, start_y = self.mouse.position
        dx = target_x - start_x
        dy = target_y - start_y

        steps = int(duration / 0.01)

        for i in range(steps):
            # Ease-out cubic easing
            t = (i + 1) / steps
            eased_t = 1 - math.pow(1 - t, 3)

            new_x = start_x + dx * eased_t
            new_y = start_y + dy * eased_t

            self.mouse.position = (int(new_x), int(new_y))
            time.sleep(0.01)

        # Ensure we reach the exact target
        self.mouse.position = (target_x, target_y)

    def set_sensitivity(self, sensitivity: float):
        """
        Update mouse sensitivity.

        Args:
            sensitivity: New sensitivity multiplier
        """
        self.sensitivity = sensitivity
