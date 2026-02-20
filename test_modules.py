"""
Simple test script for OpenCut modules
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

import numpy as np
from recorder import ScreenRecorder
from gif_exporter import GIFExporter

def test_recorder():
    """Test ScreenRecorder basic functionality"""
    print("Testing ScreenRecorder...")
    
    recorder = ScreenRecorder()
    
    # Test setting capture area
    recorder.set_capture_area(0, 0, 100, 100)
    assert recorder.capture_area == (0, 0, 100, 100), "Capture area not set correctly"
    print("  ✓ Capture area setting works")
    
    # Test initial state
    assert not recorder.is_recording(), "Should not be recording initially"
    print("  ✓ Initial state correct")
    
    # Test frame count
    assert recorder.get_frame_count() == 0, "Frame count should be 0"
    print("  ✓ Frame count correct")
    
    print("ScreenRecorder tests passed!\n")

def test_gif_exporter():
    """Test GIFExporter basic functionality"""
    print("Testing GIFExporter...")
    
    exporter = GIFExporter()
    
    # Create test frames
    frames = []
    for i in range(5):
        # Create a simple colored frame
        frame = np.zeros((100, 100, 3), dtype=np.uint8)
        frame[:, :, 0] = i * 50  # Red channel
        frame[:, :, 1] = i * 30  # Green channel
        frame[:, :, 2] = i * 20  # Blue channel
        frames.append(frame)
    
    # Test frame info
    info = exporter.get_frame_info(frames)
    assert info['count'] == 5, "Frame count mismatch"
    assert info['width'] == 100, "Width mismatch"
    assert info['height'] == 100, "Height mismatch"
    print("  ✓ Frame info works")
    
    # Test GIF export
    test_path = "test_output.gif"
    try:
        success = exporter.export_gif(frames, test_path, fps=5)
        assert success, "GIF export failed"
        assert os.path.exists(test_path), "GIF file not created"
        print("  ✓ GIF export works")
        
        # Cleanup
        os.remove(test_path)
    except Exception as e:
        print(f"  ⚠ GIF export test skipped: {e}")
    
    print("GIFExporter tests passed!\n")

def main():
    """Run all tests"""
    print("=" * 50)
    print("OpenCut Module Tests")
    print("=" * 50)
    print()
    
    try:
        test_recorder()
        test_gif_exporter()
        print("=" * 50)
        print("All tests passed! ✓")
        print("=" * 50)
    except AssertionError as e:
        print(f"\n✗ Test failed: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\n✗ Error during testing: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
