# Quick Start Guide

## Installation

### Option 1: Using Setup Scripts

**Windows:**
```bash
setup.bat
```

**Linux/macOS:**
```bash
chmod +x setup.sh
./setup.sh
```

### Option 2: Manual Setup

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Linux/macOS:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

## Running OpenCut

```bash
# Activate virtual environment (if not already active)
source venv/bin/activate  # or venv\Scripts\activate on Windows

# Run the application
python main.py
```

## Building Executable

```bash
# Build single-file executable
python build.py

# Build directory version (faster startup)
python build.py --dir

# Clean build artifacts
python build.py --clean
```

The executable will be created in the `dist/` folder.

## Using the Application

1. **Select Area**: Click "Select Area" and drag to choose the screen region
2. **Start Recording**: Click "Start Recording" or press F9
3. **Stop Recording**: Click "Stop Recording" or press F9
4. **Export GIF**: Click "Export GIF" to save your recording

## Keyboard Shortcuts

- **F9**: Start/Stop Recording
- **ESC**: Cancel area selection

## Project Structure

```
OpenCut/
├── main.py              # Entry point
├── src/                 # Source modules
│   ├── recorder.py     # Screen capture
│   ├── gif_exporter.py # GIF generation
│   └── gui.py          # User interface
├── requirements.txt     # Dependencies
├── build.py            # Build script
├── setup.py            # Package setup
└── README.md           # Documentation
```
