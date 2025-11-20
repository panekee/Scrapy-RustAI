# 🤖 Scrapy - Autonomous Rust AI Player

<div align="center">

![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)
![Status](https://img.shields.io/badge/Status-In%20Development-yellow.svg)

An autonomous AI agent that plays Rust using computer vision and virtual input control.

[Features](#-features) • [Installation](#-installation) • [Usage](#-usage) • [Roadmap](#-roadmap)

</div>

---

## 📖 About

Scrapy is an artificial intelligence system designed to play Rust autonomously. It uses computer vision to analyze the game screen in real-time, makes decisions based on what it sees, and executes actions through virtual keyboard and mouse inputs.

**🎯 Project Goals:**
- Learn and implement computer vision techniques
- Explore AI decision-making systems
- Create an autonomous game-playing agent
- Document the development process for educational purposes

## ✨ Features

### Current (v0.1)
- ⚡ Real-time screen capture and analysis
- 👁️ Basic object detection using OpenCV
- 🎮 Virtual keyboard and mouse control
- 🧠 Simple decision-making engine

### Planned
- 🎯 Advanced object detection with YOLOv8
- 🗺️ Navigation and pathfinding
- 📦 Resource gathering automation
- 🏗️ Building system integration
- 🎤 Voice communication (TTS integration)
- 🤖 Reinforcement learning capabilities

## 🛠️ Tech Stack

- **Python 3.9+** - Core language
- **OpenCV** - Computer vision and image processing
- **YOLOv8** - Object detection
- **pynput** - Virtual keyboard/mouse control
- **mss** - Fast screen capture
- **NumPy** - Numerical operations

## 📦 Installation

### Prerequisites
- Python 3.9 or higher
- Rust game installed
- Windows/Linux/MacOS

### Setup

1. Clone the repository
```bash
git clone https://github.com/yourusername/scrapy-rust-ai.git
cd scrapy-rust-ai
```

2. Create a virtual environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies
```bash
pip install -r requirements.txt
```

4. Configure settings
```bash
cp config.example.yaml config.yaml
# Edit config.yaml with your settings
```

## 🚀 Usage

### Basic Usage
```bash
python src/main.py
```

### Training Mode
```bash
python src/main.py --mode train
```

### Configuration
Edit `config.yaml` to customize:
- Screen capture region
- Detection sensitivity
- Action delays
- Behavior parameters

## 🏗️ Project Structure

```
scrapy-rust-ai/
├── src/
│   ├── vision/
│   │   ├── screen_capture.py    # Screen capture module
│   │   └── object_detection.py  # Object detection and analysis
│   ├── control/
│   │   ├── keyboard_controller.py  # Virtual keyboard input
│   │   └── mouse_controller.py     # Virtual mouse input
│   ├── ai/
│   │   ├── decision_engine.py   # Decision-making logic
│   │   └── behavior_tree.py     # Behavior tree system
│   └── main.py                  # Main entry point
├── models/                       # Trained models
├── tests/                        # Unit tests
├── docs/                         # Documentation
├── config.yaml                   # Configuration file
├── requirements.txt              # Python dependencies
└── README.md
```

## 🗺️ Roadmap

- [x] Project setup and basic structure
- [x] Screen capture implementation
- [x] Virtual input control
- [ ] Object detection integration
- [ ] Basic movement and navigation
- [ ] Resource gathering logic
- [ ] Inventory management
- [ ] Building system
- [ ] Voice communication
- [ ] Machine learning integration

## 🎥 Demo

*Coming soon - Video demonstration will be available on YouTube*

## ⚠️ Disclaimer

This project is for **educational purposes only**. 

- Always respect game Terms of Service
- Use only on private servers or with permission
- Not intended for gaining unfair advantages
- The developer is not responsible for any misuse

## 🤝 Contributing

Contributions are welcome! Feel free to:
- Report bugs
- Suggest features
- Submit pull requests

Please read [CONTRIBUTING.md](CONTRIBUTING.md) before contributing.

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👤 Author

**SPUFF**
- GitHub: [@yourusername](https://github.com/yourusername)
- YouTube: [Your Channel]

## 🙏 Acknowledgments

- Rust game by Facepunch Studios
- OpenCV community
- Ultralytics YOLOv8

---

<div align="center">
Made with ❤️ and Python | ⭐ Star this repo if you find it interesting!
</div>
