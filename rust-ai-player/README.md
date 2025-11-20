# Rust AI Player

An intelligent AI player for the game Rust, using computer vision, machine learning, and behavior trees to play autonomously.

## Features

### Phase 1 - Core AI Player
- **Computer Vision**: Real-time screen capture and object detection using YOLOv8
- **Intelligent Decision Making**: Multi-layered AI with decision engine and behavior trees
- **Precise Control**: Human-like keyboard and mouse control
- **Adaptive Behavior**: Dynamic decision making based on game state
- **Resource Management**: Automatic gathering, crafting, and inventory management
- **Combat AI**: Threat detection, engagement decisions, and combat execution
- **Survival Mechanics**: Health monitoring, hunger management, and self-preservation

### Phase 2 - Voice Chat (Planned)
- **Text-to-Speech**: Natural voice communication with other players
- **Contextual Responses**: AI-driven conversational abilities
- **Multiple TTS Engines**: Support for pyttsx3, ElevenLabs, and OpenAI

## Architecture

```
rust-ai-player/
├── src/
│   ├── vision/              # Computer vision modules
│   │   ├── screen_capture.py    # Screen capture using mss
│   │   └── object_detection.py  # YOLOv8 object detection
│   ├── control/             # Input control modules
│   │   ├── keyboard_controller.py  # Keyboard input simulation
│   │   └── mouse_controller.py     # Mouse input simulation
│   ├── ai/                  # AI decision making
│   │   ├── decision_engine.py   # High-level decision making
│   │   └── behavior_tree.py     # Behavior tree implementation
│   └── main.py             # Main entry point
├── models/                 # Trained models
├── config.yaml            # Configuration file
└── requirements.txt       # Python dependencies
```

## Installation

### Prerequisites
- Python 3.8 or higher
- CUDA-capable GPU (recommended for better performance)
- Windows/Linux operating system

### Setup

1. Clone the repository:
```bash
git clone <repository-url>
cd rust-ai-player
```

2. Create a virtual environment:
```bash
python -m venv venv

# On Windows
venv\Scripts\activate

# On Linux/Mac
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Download YOLOv8 model (happens automatically on first run):
```bash
python -c "from ultralytics import YOLO; YOLO('yolov8n.pt')"
```

## Configuration

Edit `config.yaml` to customize the AI behavior:

```yaml
# Display settings
monitor: 1
window_width: 1920
window_height: 1080

# Vision settings
confidence_threshold: 0.5

# Performance
target_fps: 10
debug_mode: false

# AI behavior
decision_engine:
  critical_health_threshold: 20
  low_health_threshold: 50
```

## Usage

### Basic Usage

Run the AI player:
```bash
cd src
python main.py
```

### Debug Mode

Enable debug visualization in `config.yaml`:
```yaml
debug_mode: true
```

This will show:
- Detected objects with bounding boxes
- Current AI state and decisions
- FPS and performance metrics
- Health, threats, and resources

### Custom Model Training

To train a custom YOLO model for Rust-specific objects:

1. Collect and label training data
2. Create a dataset YAML file
3. Run training:
```python
from vision import ObjectDetector

detector = ObjectDetector()
detector.train_custom_model('data.yaml', epochs=100)
```

## Modules

### Vision Module

**ScreenCapture**: Fast screen capture using mss
- `capture_full_screen()`: Capture entire screen
- `capture_region()`: Capture specific region
- `capture_game_window()`: Capture game window based on config

**ObjectDetector**: YOLOv8-based object detection
- `detect_objects()`: Detect all objects in frame
- `detect_specific_object()`: Find specific object type
- `draw_detections()`: Visualize detections

### Control Module

**KeyboardController**: Keyboard input simulation
- Game-specific methods: `move_forward()`, `jump()`, `reload()`, etc.
- Generic methods: `press_key()`, `tap_key()`, `press_combination()`

**MouseController**: Mouse input simulation
- `aim_at_target()`: Smooth aiming
- `shoot()`: Weapon firing
- `spray_control()`: Recoil compensation
- `look_around()`: Camera control

### AI Module

**DecisionEngine**: High-level decision making
- State evaluation and priority assessment
- Threat analysis and resource selection
- Combat engagement decisions

**BehaviorTree**: Hierarchical behavior organization
- Composite nodes: Sequence, Selector, Parallel
- Action nodes: Executable behaviors
- Condition nodes: State checks

## AI Behavior

### Decision Priority

1. **Critical** - Survival (low health, immediate threats)
2. **High** - Combat, hunger management
3. **Medium** - Resource gathering
4. **Low** - Exploration, base building
5. **Minimal** - Idle behavior

### Behavior States

- **EXPLORING**: Looking for resources and threats
- **GATHERING**: Collecting resources
- **BUILDING**: Construction activities
- **COMBAT**: Engaging threats
- **FLEEING**: Escaping from danger
- **LOOTING**: Collecting loot
- **CRAFTING**: Creating items

## Performance

### Optimization Tips

1. Lower `target_fps` for less CPU usage
2. Use smaller YOLO model (yolov8n) for speed
3. Reduce `window_width` and `window_height` for faster processing
4. Disable `debug_mode` in production

### Recommended Settings

**High Performance (Gaming PC)**:
- target_fps: 10-15
- confidence_threshold: 0.5
- Model: yolov8n or yolov8s

**Balanced (Mid-range PC)**:
- target_fps: 5-10
- confidence_threshold: 0.6
- Model: yolov8n

**Low Performance (Laptop)**:
- target_fps: 3-5
- confidence_threshold: 0.7
- Model: yolov8n with reduced resolution

## Development

### Project Structure

- `vision/`: All computer vision related code
- `control/`: Input simulation and control
- `ai/`: Decision making and behavior logic
- `models/`: Trained ML models
- `config.yaml`: Configuration management

### Adding New Behaviors

1. Create action function in appropriate controller
2. Add decision logic to DecisionEngine
3. Integrate into BehaviorTree structure

Example:
```python
def custom_action(context):
    # Your custom logic here
    return NodeStatus.SUCCESS

# Add to behavior tree
custom_node = ActionNode("Custom Action", custom_action)
sequence.add_child(custom_node)
```

## Roadmap

### Phase 1 (Current)
- [x] Screen capture system
- [x] Object detection
- [x] Keyboard/mouse control
- [x] Decision engine
- [x] Behavior trees
- [ ] Combat optimization
- [ ] Resource gathering AI
- [ ] Base building logic

### Phase 2 (Planned)
- [ ] Voice chat integration
- [ ] TTS with multiple engines
- [ ] Contextual conversation AI
- [ ] Team coordination

### Phase 3 (Future)
- [ ] Reinforcement learning
- [ ] Strategy optimization
- [ ] Multi-agent coordination
- [ ] Advanced combat techniques

## Safety and Ethics

This project is for educational and research purposes. Please note:

- Ensure compliance with game terms of service
- Use responsibly and ethically
- Respect other players
- May violate anti-cheat systems
- Not recommended for competitive play

## Troubleshooting

### Common Issues

**"Module not found" errors**:
```bash
pip install -r requirements.txt
```

**Screen capture not working**:
- Check monitor number in config
- Verify screen coordinates
- Run with administrator privileges (Windows)

**Low FPS**:
- Reduce target_fps
- Use smaller YOLO model
- Lower screen resolution

**Detection not working**:
- Adjust confidence_threshold
- Check if game window is visible
- Train custom model for Rust objects

## Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

This project is for educational purposes only. Use at your own risk.

## Acknowledgments

- YOLOv8 by Ultralytics
- pynput for input control
- mss for screen capture
- OpenCV for image processing

## Contact

For questions, issues, or suggestions, please open an issue on GitHub.
