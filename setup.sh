#!/bin/bash
# Setup script for OpenCut (Linux/macOS)

echo "Setting up OpenCut..."

# Check Python version
python_version=$(python3 --version 2>&1 | awk '{print $2}')
echo "Python version: $python_version"

# Create virtual environment
echo "Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip

# Install requirements
echo "Installing requirements..."
pip install -r requirements.txt

echo ""
echo "Setup complete!"
echo ""
echo "To run OpenCut:"
echo "  source venv/bin/activate"
echo "  python main.py"
echo ""
echo "To build executable:"
echo "  python build.py"
