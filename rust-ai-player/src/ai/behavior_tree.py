"""
Behavior Tree Module
Implements behavior tree for complex AI decision making.
"""

from abc import ABC, abstractmethod
from enum import Enum
from typing import Dict, List, Optional, Any, Callable


class NodeStatus(Enum):
    """Possible states of a behavior tree node."""
    SUCCESS = "success"
    FAILURE = "failure"
    RUNNING = "running"


class BehaviorNode(ABC):
    """Base class for all behavior tree nodes."""

    def __init__(self, name: str):
        """
        Initialize node.

        Args:
            name: Name of the node
        """
        self.name = name
        self.status = NodeStatus.FAILURE

    @abstractmethod
    def tick(self, context: Dict[str, Any]) -> NodeStatus:
        """
        Execute this node.

        Args:
            context: Current game context

        Returns:
            Node status after execution
        """
        pass

    def reset(self):
        """Reset node to initial state."""
        self.status = NodeStatus.FAILURE


class ActionNode(BehaviorNode):
    """Leaf node that performs an action."""

    def __init__(self, name: str, action: Callable[[Dict[str, Any]], NodeStatus]):
        """
        Initialize action node.

        Args:
            name: Name of the action
            action: Function to execute
        """
        super().__init__(name)
        self.action = action

    def tick(self, context: Dict[str, Any]) -> NodeStatus:
        """Execute the action."""
        self.status = self.action(context)
        return self.status


class ConditionNode(BehaviorNode):
    """Leaf node that checks a condition."""

    def __init__(self, name: str, condition: Callable[[Dict[str, Any]], bool]):
        """
        Initialize condition node.

        Args:
            name: Name of the condition
            condition: Function that returns True/False
        """
        super().__init__(name)
        self.condition = condition

    def tick(self, context: Dict[str, Any]) -> NodeStatus:
        """Check the condition."""
        result = self.condition(context)
        self.status = NodeStatus.SUCCESS if result else NodeStatus.FAILURE
        return self.status


class SequenceNode(BehaviorNode):
    """Composite node that executes children in sequence."""

    def __init__(self, name: str, children: Optional[List[BehaviorNode]] = None):
        """
        Initialize sequence node.

        Args:
            name: Name of the sequence
            children: Child nodes
        """
        super().__init__(name)
        self.children = children or []
        self.current_child_index = 0

    def add_child(self, child: BehaviorNode):
        """Add a child node."""
        self.children.append(child)

    def tick(self, context: Dict[str, Any]) -> NodeStatus:
        """
        Execute children in sequence.
        Returns SUCCESS if all children succeed.
        Returns FAILURE if any child fails.
        """
        while self.current_child_index < len(self.children):
            child = self.children[self.current_child_index]
            status = child.tick(context)

            if status == NodeStatus.FAILURE:
                self.current_child_index = 0
                self.status = NodeStatus.FAILURE
                return self.status

            if status == NodeStatus.RUNNING:
                self.status = NodeStatus.RUNNING
                return self.status

            # SUCCESS: move to next child
            self.current_child_index += 1

        # All children succeeded
        self.current_child_index = 0
        self.status = NodeStatus.SUCCESS
        return self.status

    def reset(self):
        """Reset this node and all children."""
        super().reset()
        self.current_child_index = 0
        for child in self.children:
            child.reset()


class SelectorNode(BehaviorNode):
    """Composite node that tries children until one succeeds."""

    def __init__(self, name: str, children: Optional[List[BehaviorNode]] = None):
        """
        Initialize selector node.

        Args:
            name: Name of the selector
            children: Child nodes
        """
        super().__init__(name)
        self.children = children or []
        self.current_child_index = 0

    def add_child(self, child: BehaviorNode):
        """Add a child node."""
        self.children.append(child)

    def tick(self, context: Dict[str, Any]) -> NodeStatus:
        """
        Execute children until one succeeds.
        Returns SUCCESS if any child succeeds.
        Returns FAILURE if all children fail.
        """
        while self.current_child_index < len(self.children):
            child = self.children[self.current_child_index]
            status = child.tick(context)

            if status == NodeStatus.SUCCESS:
                self.current_child_index = 0
                self.status = NodeStatus.SUCCESS
                return self.status

            if status == NodeStatus.RUNNING:
                self.status = NodeStatus.RUNNING
                return self.status

            # FAILURE: move to next child
            self.current_child_index += 1

        # All children failed
        self.current_child_index = 0
        self.status = NodeStatus.FAILURE
        return self.status

    def reset(self):
        """Reset this node and all children."""
        super().reset()
        self.current_child_index = 0
        for child in self.children:
            child.reset()


class ParallelNode(BehaviorNode):
    """Composite node that executes all children simultaneously."""

    def __init__(self, name: str, children: Optional[List[BehaviorNode]] = None,
                 success_threshold: int = 1):
        """
        Initialize parallel node.

        Args:
            name: Name of the parallel node
            children: Child nodes
            success_threshold: Number of children that must succeed
        """
        super().__init__(name)
        self.children = children or []
        self.success_threshold = success_threshold

    def add_child(self, child: BehaviorNode):
        """Add a child node."""
        self.children.append(child)

    def tick(self, context: Dict[str, Any]) -> NodeStatus:
        """
        Execute all children in parallel.
        Returns SUCCESS if success_threshold children succeed.
        Returns FAILURE if too many children fail.
        """
        success_count = 0
        failure_count = 0
        running_count = 0

        for child in self.children:
            status = child.tick(context)

            if status == NodeStatus.SUCCESS:
                success_count += 1
            elif status == NodeStatus.FAILURE:
                failure_count += 1
            else:
                running_count += 1

        # Check if we've met success threshold
        if success_count >= self.success_threshold:
            self.status = NodeStatus.SUCCESS
            return self.status

        # Check if too many have failed
        remaining = len(self.children) - failure_count
        if remaining < self.success_threshold:
            self.status = NodeStatus.FAILURE
            return self.status

        # Still running
        self.status = NodeStatus.RUNNING
        return self.status

    def reset(self):
        """Reset this node and all children."""
        super().reset()
        for child in self.children:
            child.reset()


class BehaviorTree:
    """Main behavior tree controller."""

    def __init__(self, root: BehaviorNode):
        """
        Initialize behavior tree.

        Args:
            root: Root node of the tree
        """
        self.root = root

    def tick(self, context: Dict[str, Any]) -> NodeStatus:
        """
        Execute one tick of the behavior tree.

        Args:
            context: Current game context

        Returns:
            Status of the root node
        """
        return self.root.tick(context)

    def reset(self):
        """Reset the entire tree."""
        self.root.reset()


# Example: Build a simple Rust AI behavior tree
def build_rust_ai_tree(controllers: Dict[str, Any]) -> BehaviorTree:
    """
    Build a behavior tree for Rust AI.

    Args:
        controllers: Dictionary containing keyboard and mouse controllers

    Returns:
        Configured behavior tree
    """
    keyboard = controllers.get('keyboard')
    mouse = controllers.get('mouse')

    # Root selector: try different strategies
    root = SelectorNode("Root Strategy")

    # 1. Survival behavior (highest priority)
    survival = SequenceNode("Survival")
    survival.add_child(ConditionNode(
        "Low Health?",
        lambda ctx: ctx.get('health', 100) < 30
    ))
    survival.add_child(ActionNode(
        "Find Cover",
        lambda ctx: NodeStatus.SUCCESS  # Implement cover finding
    ))
    survival.add_child(ActionNode(
        "Heal",
        lambda ctx: NodeStatus.SUCCESS  # Implement healing
    ))

    # 2. Combat behavior
    combat = SequenceNode("Combat")
    combat.add_child(ConditionNode(
        "Enemy Nearby?",
        lambda ctx: len(ctx.get('threats', [])) > 0
    ))
    combat.add_child(ActionNode(
        "Aim at Enemy",
        lambda ctx: NodeStatus.SUCCESS  # Implement aiming
    ))
    combat.add_child(ActionNode(
        "Shoot",
        lambda ctx: NodeStatus.SUCCESS  # Implement shooting
    ))

    # 3. Gathering behavior
    gathering = SequenceNode("Gathering")
    gathering.add_child(ConditionNode(
        "Resource Nearby?",
        lambda ctx: len(ctx.get('resources', [])) > 0
    ))
    gathering.add_child(ActionNode(
        "Move to Resource",
        lambda ctx: NodeStatus.SUCCESS  # Implement movement
    ))
    gathering.add_child(ActionNode(
        "Gather",
        lambda ctx: NodeStatus.SUCCESS  # Implement gathering
    ))

    # 4. Exploration behavior (default)
    exploration = ActionNode(
        "Explore",
        lambda ctx: NodeStatus.SUCCESS  # Implement exploration
    )

    # Add all behaviors to root
    root.add_child(survival)
    root.add_child(combat)
    root.add_child(gathering)
    root.add_child(exploration)

    return BehaviorTree(root)
