"""
Main entry point for Rust AI Player
Coordinates vision, decision making, and control systems.
"""

import time
import yaml
import cv2
from pathlib import Path
from typing import Dict, Any

from vision import ScreenCapture, ObjectDetector
from control import KeyboardController, MouseController
from ai import DecisionEngine, BehaviorTree, build_rust_ai_tree, NodeStatus


class RustAIPlayer:
    """Main AI player controller for Rust."""

    def __init__(self, config_path: str = "config.yaml"):
        """
        Initialize the AI player.

        Args:
            config_path: Path to configuration file
        """
        # Load configuration
        self.config = self._load_config(config_path)

        # Initialize components
        self.screen_capture = ScreenCapture(
            monitor_number=self.config.get('monitor', 1)
        )
        self.object_detector = ObjectDetector(
            model_path=self.config.get('model_path'),
            confidence_threshold=self.config.get('confidence_threshold', 0.5)
        )
        self.keyboard = KeyboardController(
            default_delay=self.config.get('key_delay', 0.05)
        )
        self.mouse = MouseController(
            sensitivity=self.config.get('mouse_sensitivity', 1.0)
        )

        # Initialize AI systems
        self.decision_engine = DecisionEngine(self.config)
        self.behavior_tree = build_rust_ai_tree({
            'keyboard': self.keyboard,
            'mouse': self.mouse
        })

        # Runtime state
        self.running = False
        self.frame_count = 0
        self.fps = 0
        self.debug_mode = self.config.get('debug_mode', False)

    def _load_config(self, config_path: str) -> Dict[str, Any]:
        """
        Load configuration from YAML file.

        Args:
            config_path: Path to config file

        Returns:
            Configuration dictionary
        """
        config_file = Path(config_path)

        if config_file.exists():
            with open(config_file, 'r') as f:
                return yaml.safe_load(f)
        else:
            print(f"Config file not found: {config_path}")
            print("Using default configuration")
            return self._get_default_config()

    @staticmethod
    def _get_default_config() -> Dict[str, Any]:
        """Get default configuration."""
        return {
            'monitor': 1,
            'confidence_threshold': 0.5,
            'key_delay': 0.05,
            'mouse_sensitivity': 1.0,
            'target_fps': 10,
            'debug_mode': False,
            'window_x': 0,
            'window_y': 0,
            'window_width': 1920,
            'window_height': 1080
        }

    def process_frame(self) -> Dict[str, Any]:
        """
        Process one frame: capture, detect, decide, act.

        Returns:
            Frame processing results
        """
        # Capture screen
        frame = self.screen_capture.capture_game_window(self.config)

        # Detect objects
        detections = self.object_detector.detect_objects(frame)

        # Prepare vision data for AI
        vision_data = {
            'detections': detections,
            'frame': frame,
            'frame_count': self.frame_count
        }

        # Update decision engine with vision data
        self.decision_engine.update_game_state(vision_data)

        # Make decision
        decision = self.decision_engine.make_decision()

        # Execute decision via behavior tree
        context = {
            'decision': decision,
            'vision_data': vision_data,
            'health': self.decision_engine.health,
            'threats': self.decision_engine.nearby_threats,
            'resources': self.decision_engine.nearby_resources
        }

        behavior_status = self.behavior_tree.tick(context)

        # Debug visualization
        if self.debug_mode:
            debug_frame = self.object_detector.draw_detections(frame, detections)
            self._show_debug_info(debug_frame, decision, behavior_status)

        return {
            'frame': frame,
            'detections': detections,
            'decision': decision,
            'behavior_status': behavior_status
        }

    def _show_debug_info(self, frame, decision, behavior_status):
        """
        Display debug information.

        Args:
            frame: Current frame
            decision: Current decision
            behavior_status: Behavior tree status
        """
        # Add text overlay
        debug_text = [
            f"FPS: {self.fps:.1f}",
            f"Frame: {self.frame_count}",
            f"State: {self.decision_engine.current_state.value}",
            f"Decision: {decision.action}",
            f"Priority: {decision.priority.name}",
            f"Health: {self.decision_engine.health}",
            f"Threats: {len(self.decision_engine.nearby_threats)}",
            f"Resources: {len(self.decision_engine.nearby_resources)}",
            f"Behavior: {behavior_status.value}"
        ]

        y_offset = 30
        for text in debug_text:
            cv2.putText(frame, text, (10, y_offset),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
            y_offset += 25

        # Show frame
        cv2.imshow('Rust AI Player - Debug', frame)
        cv2.waitKey(1)

    def run(self):
        """Main run loop."""
        print("Starting Rust AI Player...")
        print(f"Debug mode: {self.debug_mode}")
        print(f"Target FPS: {self.config.get('target_fps', 10)}")
        print("Press Ctrl+C to stop")

        self.running = True
        target_frame_time = 1.0 / self.config.get('target_fps', 10)

        try:
            while self.running:
                frame_start = time.time()

                # Process one frame
                self.process_frame()

                # Update counters
                self.frame_count += 1

                # Maintain target FPS
                elapsed = time.time() - frame_start
                sleep_time = max(0, target_frame_time - elapsed)
                time.sleep(sleep_time)

                # Calculate actual FPS
                actual_elapsed = time.time() - frame_start
                self.fps = 1.0 / actual_elapsed if actual_elapsed > 0 else 0

                # Print status every 100 frames
                if self.frame_count % 100 == 0:
                    print(f"Frame {self.frame_count} - FPS: {self.fps:.1f}")

        except KeyboardInterrupt:
            print("\nStopping AI player...")
        finally:
            self.cleanup()

    def cleanup(self):
        """Clean up resources."""
        print("Cleaning up...")
        self.screen_capture.close()
        if self.debug_mode:
            cv2.destroyAllWindows()
        print("Shutdown complete")

    def stop(self):
        """Stop the AI player."""
        self.running = False


def main():
    """Main entry point."""
    # Create AI player
    ai_player = RustAIPlayer(config_path="../config.yaml")

    # Run the AI
    ai_player.run()


if __name__ == "__main__":
    main()
