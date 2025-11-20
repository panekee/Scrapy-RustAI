"""
Keyboard Controller Module
Handles keyboard input simulation for the AI player.
"""

from pynput.keyboard import Controller, Key
import time
from typing import Union, List


class KeyboardController:
    """Simulates keyboard inputs for game control."""

    def __init__(self, default_delay: float = 0.05):
        """
        Initialize keyboard controller.

        Args:
            default_delay: Default delay between key actions (seconds)
        """
        self.keyboard = Controller()
        self.default_delay = default_delay

    def press_key(self, key: Union[str, Key], duration: float = 0.1):
        """
        Press and hold a key for specified duration.

        Args:
            key: Key to press (string or Key enum)
            duration: How long to hold the key (seconds)
        """
        self.keyboard.press(key)
        time.sleep(duration)
        self.keyboard.release(key)

    def tap_key(self, key: Union[str, Key]):
        """
        Quick tap of a key.

        Args:
            key: Key to tap
        """
        self.keyboard.press(key)
        time.sleep(self.default_delay)
        self.keyboard.release(key)

    def type_text(self, text: str, delay: float = 0.05):
        """
        Type a string of text.

        Args:
            text: Text to type
            delay: Delay between characters (seconds)
        """
        for char in text:
            self.keyboard.press(char)
            self.keyboard.release(char)
            time.sleep(delay)

    def press_combination(self, keys: List[Union[str, Key]], duration: float = 0.1):
        """
        Press multiple keys simultaneously.

        Args:
            keys: List of keys to press together
            duration: How long to hold the combination (seconds)
        """
        # Press all keys
        for key in keys:
            self.keyboard.press(key)

        time.sleep(duration)

        # Release in reverse order
        for key in reversed(keys):
            self.keyboard.release(key)

    def hold_key(self, key: Union[str, Key]):
        """
        Start holding a key (must call release_key later).

        Args:
            key: Key to hold
        """
        self.keyboard.press(key)

    def release_key(self, key: Union[str, Key]):
        """
        Release a held key.

        Args:
            key: Key to release
        """
        self.keyboard.release(key)

    # Game-specific movement methods for Rust
    def move_forward(self, duration: float = 1.0):
        """Move forward (W key)."""
        self.press_key('w', duration)

    def move_backward(self, duration: float = 1.0):
        """Move backward (S key)."""
        self.press_key('s', duration)

    def move_left(self, duration: float = 1.0):
        """Move left (A key)."""
        self.press_key('a', duration)

    def move_right(self, duration: float = 1.0):
        """Move right (D key)."""
        self.press_key('d', duration)

    def jump(self):
        """Jump (Space key)."""
        self.tap_key(Key.space)

    def crouch(self, duration: float = 0.5):
        """Crouch (Ctrl key)."""
        self.press_key(Key.ctrl, duration)

    def sprint(self, duration: float = 1.0):
        """Sprint (Shift key)."""
        self.press_key(Key.shift, duration)

    def reload(self):
        """Reload weapon (R key)."""
        self.tap_key('r')

    def interact(self):
        """Interact with object (E key)."""
        self.tap_key('e')

    def open_inventory(self):
        """Open inventory (Tab key)."""
        self.tap_key(Key.tab)

    def open_map(self):
        """Open map (G key in Rust)."""
        self.tap_key('g')

    def select_hotbar_slot(self, slot: int):
        """
        Select a hotbar slot.

        Args:
            slot: Slot number (1-6)
        """
        if 1 <= slot <= 6:
            self.tap_key(str(slot))

    def use_voice_chat(self, duration: float = 2.0):
        """
        Activate voice chat (V key in Rust).

        Args:
            duration: How long to hold the voice key (seconds)
        """
        self.press_key('v', duration)
