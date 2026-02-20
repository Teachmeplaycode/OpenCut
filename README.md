# OpenCut - Screen to GIF Recorder

A simple, user-friendly screen recording application that captures video and exports it as animated GIF files.

![Python Version](https://img.shields.io/badge/python-3.8+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

## Features

- 🖥️ **Screen Area Selection** - Select any portion of your screen to record
- 🎬 **Record/Stop Controls** - Simple controls to start and stop recording
- 🎞️ **Export to GIF** - Automatically converts captured frames to animated GIF
- 🖱️ **Simple GUI** - Clean, intuitive interface using tkinter
- ⚡ **Fast Capture** - Optimized screen capture using mss

## Screenshots

*(Screenshots will be added after initial release)*

## Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package installer)

### Setup

1. Clone the repository:
```bash
git clone https://github.com/yourusername/OpenCut.git
cd OpenCut
```

2. Create and activate a virtual environment:
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Running from Source

```bash
python main.py
```

### Using the Application

1. **Select Area**: Click "Select Area" to draw a rectangle on your screen
2. **Start Recording**: Click "Start Recording" to begin capturing
3. **Stop Recording**: Click "Stop Recording" when finished
4. **Export GIF**: The GIF will be automatically saved, or use "Export GIF" to choose a location

### Keyboard Shortcuts

- `F9` - Start/Stop Recording
- `ESC` - Cancel area selection

## Building Executable

To create a standalone .exe file:

```bash
# Install PyInstaller
pip install pyinstaller

# Build executable
pyinstaller --onefile --windowed --name OpenCut main.py

# Or use the build script
python build.py
```

The executable will be created in the `dist` folder.

## Project Structure

```
OpenCut/
├── main.py              # Main application entry point
├── requirements.txt     # Python dependencies
├── setup.py            # Package setup configuration
├── build.py            # Build script for executable
├── README.md           # This file
├── .gitignore          # Git ignore rules
├── assets/             # Application assets
│   └── icon.ico       # Application icon
└── src/               # Source code modules
    ├── __init__.py
    ├── recorder.py    # Screen recording logic
    ├── gif_exporter.py # GIF generation
    └── gui.py         # GUI components
```

## Dependencies

- **tkinter** - GUI framework (included with Python)
- **mss** - Multi-screen shot for fast screen capture
- **Pillow** - Image processing library
- **imageio** - GIF generation
- **numpy** - Numerical operations for image processing
- **pyinstaller** - Executable packaging (development)

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- [mss](https://github.com/BoboTiG/python-mss) - Ultra fast cross-platform multiple screenshots module
- [imageio](https://imageio.readthedocs.io/) - Python library for reading and writing image data
- [Pillow](https://python-pillow.org/) - Python Imaging Library fork

## Support

If you encounter any issues or have questions, please [open an issue](https://github.com/yourusername/OpenCut/issues) on GitHub.

---

Made with ❤️ by the OpenCut Team