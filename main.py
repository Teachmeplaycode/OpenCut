"""
OpenCut - Screen to GIF Recorder
Main application entry point
"""

import sys
import os

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from gui import OpenCutApp

def main():
    """Main entry point for the application"""
    app = OpenCutApp()
    app.run()

if __name__ == "__main__":
    main()
