"""
Decision Engine Module
Makes high-level decisions based on game state.
"""

from typing import Dict, List, Optional, Any
from enum import Enum
import numpy as np


class GameState(Enum):
    """Possible game states."""
    EXPLORING = "exploring"
    GATHERING = "gathering"
    BUILDING = "building"
    COMBAT = "combat"
    FLEEING = "fleeing"
    LOOTING = "looting"
    CRAFTING = "crafting"
    IDLE = "idle"


class Priority(Enum):
    """Priority levels for decisions."""
    CRITICAL = 5
    HIGH = 4
    MEDIUM = 3
    LOW = 2
    MINIMAL = 1


class Decision:
    """Represents a decision with priority and context."""

    def __init__(self, action: str, priority: Priority, context: Dict[str, Any]):
        """
        Create a decision.

        Args:
            action: Action to take
            priority: Priority level
            context: Additional context for the decision
        """
        self.action = action
        self.priority = priority
        self.context = context

    def __repr__(self):
        return f"Decision(action={self.action}, priority={self.priority.name})"


class DecisionEngine:
    """Makes strategic decisions for the AI player."""

    def __init__(self, config: Dict[str, Any]):
        """
        Initialize decision engine.

        Args:
            config: Configuration dictionary
        """
        self.config = config
        self.current_state = GameState.IDLE
        self.health = 100
        self.hunger = 100
        self.inventory = []
        self.nearby_threats = []
        self.nearby_resources = []

    def update_game_state(self, vision_data: Dict[str, Any]):
        """
        Update internal game state based on vision data.

        Args:
            vision_data: Data from vision system (detections, etc.)
        """
        detections = vision_data.get('detections', [])

        # Update threats
        self.nearby_threats = [
            d for d in detections
            if d['class_name'] in ['player', 'bear', 'wolf', 'scientist']
        ]

        # Update resources
        self.nearby_resources = [
            d for d in detections
            if d['class_name'] in ['tree', 'stone', 'ore', 'hemp', 'crate']
        ]

        # Update health/hunger if available
        self.health = vision_data.get('health', self.health)
        self.hunger = vision_data.get('hunger', self.hunger)

    def make_decision(self) -> Decision:
        """
        Make a decision based on current game state.

        Returns:
            Decision object with action and priority
        """
        # Critical decisions (survival)
        if self.health < 20:
            return Decision(
                action="heal",
                priority=Priority.CRITICAL,
                context={'health': self.health}
            )

        if self.nearby_threats:
            threat = self.nearby_threats[0]
            if self.health < 50:
                return Decision(
                    action="flee",
                    priority=Priority.CRITICAL,
                    context={'threat': threat}
                )
            else:
                return Decision(
                    action="combat",
                    priority=Priority.HIGH,
                    context={'threat': threat}
                )

        # High priority decisions
        if self.hunger < 30:
            return Decision(
                action="find_food",
                priority=Priority.HIGH,
                context={'hunger': self.hunger}
            )

        # Medium priority decisions
        if self.nearby_resources:
            resource = self._select_best_resource()
            return Decision(
                action="gather_resource",
                priority=Priority.MEDIUM,
                context={'resource': resource}
            )

        # Low priority decisions
        if len(self.inventory) < 5:
            return Decision(
                action="explore",
                priority=Priority.LOW,
                context={'goal': 'find_resources'}
            )

        # Default: explore
        return Decision(
            action="explore",
            priority=Priority.MINIMAL,
            context={'goal': 'general_exploration'}
        )

    def evaluate_threat_level(self, threat: Dict[str, Any]) -> float:
        """
        Evaluate how dangerous a threat is.

        Args:
            threat: Threat detection data

        Returns:
            Threat level (0.0 to 1.0)
        """
        threat_ratings = {
            'player': 0.9,
            'bear': 0.95,
            'wolf': 0.7,
            'scientist': 0.85,
            'boar': 0.3
        }

        base_threat = threat_ratings.get(threat['class_name'], 0.5)

        # Adjust based on distance (closer = more threatening)
        bbox = threat['bbox']
        size = (bbox[2] - bbox[0]) * (bbox[3] - bbox[1])
        distance_factor = min(1.0, size / 10000)  # Normalize

        return min(1.0, base_threat * (1 + distance_factor))

    def _select_best_resource(self) -> Optional[Dict[str, Any]]:
        """
        Select the best resource to gather.

        Returns:
            Resource detection data
        """
        if not self.nearby_resources:
            return None

        # Priority: ore > stone > tree > hemp
        priority_order = ['ore', 'stone', 'tree', 'hemp', 'crate']

        for resource_type in priority_order:
            for resource in self.nearby_resources:
                if resource['class_name'] == resource_type:
                    return resource

        return self.nearby_resources[0]

    def should_engage_combat(self, threat: Dict[str, Any]) -> bool:
        """
        Decide whether to engage in combat.

        Args:
            threat: Threat detection data

        Returns:
            True if should engage, False if should flee
        """
        threat_level = self.evaluate_threat_level(threat)

        # Don't engage if low health
        if self.health < 40:
            return False

        # Don't engage if threat is too dangerous
        if threat_level > 0.8 and self.health < 70:
            return False

        # Engage if we have good health and threat is manageable
        return self.health > 60 and threat_level < 0.7

    def calculate_flee_direction(self, threat: Dict[str, Any]) -> str:
        """
        Calculate best direction to flee.

        Args:
            threat: Threat detection data

        Returns:
            Direction to flee ('left', 'right', 'forward', 'backward')
        """
        center_x, center_y = threat['center']

        # Flee away from threat
        if center_x < 960:  # Threat on left
            return 'right'
        else:  # Threat on right
            return 'left'

    def set_state(self, state: GameState):
        """
        Set current game state.

        Args:
            state: New game state
        """
        self.current_state = state

    def get_state(self) -> GameState:
        """Get current game state."""
        return self.current_state
