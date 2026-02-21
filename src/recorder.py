"""
Screen Recorder Module
Handles screen capture and frame storage
"""

import threading
import time
from typing import Optional, Tuple, List, Callable
import mss
import mss.tools
import numpy as np


class ScreenRecorder:
    """Handles screen recording functionality"""
    
    def __init__(self):
        self.recording = False
        self.frames: List[np.ndarray] = []
        self.capture_area: Optional[Tuple[int, int, int, int]] = None
        self.fps = 15
        self.thread: Optional[threading.Thread] = None
        self.stop_event = threading.Event()
        self.frame_callback: Optional[Callable] = None
        self.frame_count = 0
        
    def set_capture_area(self, x: int, y: int, width: int, height: int):
        """Set the screen area to capture"""
        self.capture_area = (x, y, width, height)
        
    def start_recording(self, callback: Optional[Callable] = None):
        """Start recording the screen"""
        if self.recording:
            return False
            
        if self.capture_area is None:
            raise ValueError("Capture area not set")
            
        self.recording = True
        self.frames = []
        self.frame_count = 0
        self.stop_event.clear()
        self.frame_callback = callback
        
        self.thread = threading.Thread(target=self._capture_loop)
        self.thread.start()
        return True
        
    def stop_recording(self) -> List[np.ndarray]:
        """Stop recording and return captured frames"""
        if not self.recording:
            return []
            
        self.recording = False
        self.stop_event.set()
        
        if self.thread:
            self.thread.join(timeout=2.0)
            
        return self.frames.copy()
        
    def _capture_loop(self):
        """Main capture loop running in separate thread"""
        with mss.mss() as sct:
            x, y, width, height = self.capture_area
            monitor = {"left": x, "top": y, "width": width, "height": height}
            
            frame_interval = 1.0 / self.fps
            
            while self.recording and not self.stop_event.is_set():
                start_time = time.time()
                
                try:
                    # Capture screen
                    screenshot = sct.grab(monitor)
                    
                    # Convert to numpy array
                    img = np.array(screenshot)
                    
                    # 关键修改：去除 Alpha 透明通道，并将 BGR 反转为 RGB
                    img = img[:, :, :3][:, :, ::-1]
                    
                    self.frames.append(img)
                    self.frame_count += 1
                    
                    # Call callback if provided
                    if self.frame_callback:
                        self.frame_callback(self.frame_count)
                        
                except Exception as e:
                    print(f"Capture error: {e}")
                    
                # Maintain consistent frame rate
                elapsed = time.time() - start_time
                sleep_time = frame_interval - elapsed
                if sleep_time > 0:
                    time.sleep(sleep_time)
                    
    def is_recording(self) -> bool:
        """Check if currently recording"""
        return self.recording
        
    def get_frame_count(self) -> int:
        """Get number of captured frames"""
        return self.frame_count
        
    def clear_frames(self):
        """Clear captured frames"""
        self.frames = []
        self.frame_count = 0