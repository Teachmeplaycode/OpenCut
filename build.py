"""
Build script for creating OpenCut executable
"""

import os
import sys
import subprocess
import shutil


def clean_build():
    """Clean previous build artifacts"""
    dirs_to_remove = ['build', 'dist', '__pycache__']
    for dir_name in dirs_to_remove:
        if os.path.exists(dir_name):
            print(f"Removing {dir_name}/...")
            shutil.rmtree(dir_name)
    
    # Remove .spec files
    for file in os.listdir('.'):
        if file.endswith('.spec'):
            print(f"Removing {file}...")
            os.remove(file)


def build_executable():
    """Build the executable using PyInstaller"""
    print("Building OpenCut executable...")
    
    # PyInstaller command - Linux uses : separator
    cmd = [
        'pyinstaller',
        '--onefile',
        '--windowed',
        '--name', 'OpenCut',
        '--add-data', 'src:src',  # Linux uses : separator
        '--hidden-import', 'tkinter',
        '--hidden-import', 'customtkinter',
        '--hidden-import', 'PIL',
        '--hidden-import', 'mss',
        '--hidden-import', 'imageio',
        '--hidden-import', 'numpy',
        '--collect-all', 'imageio',
        '--collect-all', 'mss',
        '--collect-all', 'customtkinter',
        'main.py'
    ]
    
    # Run PyInstaller
    result = subprocess.run(cmd, capture_output=False, text=True)
    
    if result.returncode == 0:
        print("\n✓ Build successful!")
        print("Executable location: dist/OpenCut.exe")
        return True
    else:
        print("\n✗ Build failed!")
        return False


def build_directory_mode():
    """Build in directory mode (faster startup, but not single file)"""
    print("Building OpenCut (directory mode)...")
    
    cmd = [
        'pyinstaller',
        '--windowed',
        '--name', 'OpenCut',
        '--add-data', 'src;src',
        '--hidden-import', 'tkinter',
        '--hidden-import', 'PIL',
        '--hidden-import', 'mss',
        '--hidden-import', 'imageio',
        '--hidden-import', 'numpy',
        '--collect-all', 'imageio',
        '--collect-all', 'mss',
        'main.py'
    ]
    
    result = subprocess.run(cmd, capture_output=False, text=True)
    
    if result.returncode == 0:
        print("\n✓ Build successful!")
        print("Executable location: dist/OpenCut/OpenCut.exe")
        return True
    else:
        print("\n✗ Build failed!")
        return False


def main():
    """Main build function"""
    print("=" * 50)
    print("OpenCut Build Script")
    print("=" * 50)
    
    # Check if PyInstaller is installed
    try:
        import PyInstaller
    except ImportError:
        print("PyInstaller not found. Installing...")
        subprocess.run([sys.executable, '-m', 'pip', 'install', 'pyinstaller'])
    
    # Parse arguments
    if len(sys.argv) > 1:
        if sys.argv[1] == '--clean':
            clean_build()
            return
        elif sys.argv[1] == '--dir':
            clean_build()
            build_directory_mode()
            return
    
    # Default: clean and build single file executable
    clean_build()
    build_executable()


if __name__ == "__main__":
    main()
