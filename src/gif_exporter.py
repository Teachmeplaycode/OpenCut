"""
GIF Exporter Module
Handles conversion of frames to animated GIF
"""

import os
from typing import List, Optional
import numpy as np
from PIL import Image
import imageio


class GIFExporter:
    """Handles GIF export functionality"""
    
    def __init__(self):
        self.default_fps = 15
        self.default_quality = 10  # Lower is better quality (1-100)
        
    def export_gif(self, 
                   frames: List[np.ndarray], 
                   output_path: str, 
                   fps: Optional[int] = None,
                   quality: Optional[int] = None) -> bool:
        """
        Export frames as animated GIF
        
        Args:
            frames: List of numpy arrays (RGB images)
            output_path: Path to save the GIF
            fps: Frames per second (default: 15)
            quality: Quality setting 1-100, lower is better (default: 10)
            
        Returns:
            bool: True if export successful
        """
        if not frames:
            raise ValueError("No frames to export")
            
        fps = fps or self.default_fps
        quality = quality or self.default_quality
        
        try:
            # Ensure output directory exists
            os.makedirs(os.path.dirname(os.path.abspath(output_path)) or '.', exist_ok=True)
            
            # Convert frames to PIL Images
            pil_frames = []
            for frame in frames:
                if frame.shape[2] == 3:  # RGB
                    img = Image.fromarray(frame, mode='RGB')
                elif frame.shape[2] == 4:  # RGBA
                    img = Image.fromarray(frame, mode='RGBA')
                else:
                    img = Image.fromarray(frame)
                pil_frames.append(img)
            
            # Calculate duration between frames in milliseconds
            duration = int(1000 / fps)
            
            # Optimize palette for all frames
            if len(pil_frames) > 1:
                # Use the first frame's palette as base
                first_frame = pil_frames[0]
                
                # Save optimized GIF
                first_frame.save(
                    output_path,
                    save_all=True,
                    append_images=pil_frames[1:],
                    duration=duration,
                    loop=0,  # Loop forever
                    optimize=True,
                    quality=quality
                )
            else:
                # Single frame
                pil_frames[0].save(output_path, optimize=True, quality=quality)
                
            return True
            
        except Exception as e:
            print(f"GIF export error: {e}")
            return False
            
    def export_gif_imageio(self,
                          frames: List[np.ndarray],
                          output_path: str,
                          fps: Optional[int] = None) -> bool:
        """
        Alternative export using imageio (better quality control)
        
        Args:
            frames: List of numpy arrays (RGB images)
            output_path: Path to save the GIF
            fps: Frames per second (default: 15)
            
        Returns:
            bool: True if export successful
        """
        if not frames:
            raise ValueError("No frames to export")
            
        fps = fps or self.default_fps
        
        try:
            # Ensure output directory exists
            os.makedirs(os.path.dirname(os.path.abspath(output_path)) or '.', exist_ok=True)
            
            # Convert frames to uint8 if needed
            processed_frames = []
            for frame in frames:
                if frame.dtype != np.uint8:
                    frame = (frame * 255).astype(np.uint8)
                processed_frames.append(frame)
            
            # Calculate duration
            duration = 1.0 / fps
            
            # Save using imageio
            imageio.mimsave(
                output_path,
                processed_frames,
                duration=duration,
                loop=0
            )
            
            return True
            
        except Exception as e:
            print(f"ImageIO export error: {e}")
            return False
            
    def get_frame_info(self, frames: List[np.ndarray]) -> dict:
        """Get information about the frames"""
        if not frames:
            return {}
            
        first_frame = frames[0]
        return {
            'count': len(frames),
            'width': first_frame.shape[1],
            'height': first_frame.shape[0],
            'channels': first_frame.shape[2] if len(first_frame.shape) > 2 else 1,
            'duration_seconds': len(frames) / self.default_fps
        }
