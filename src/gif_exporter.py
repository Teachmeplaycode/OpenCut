"""
GIF Exporter Module - Improved Color Quality
Handles conversion of frames to animated GIF with better color preservation
"""

import os
from typing import List, Optional
import numpy as np
from PIL import Image
import imageio


class GIFExporter:
    """Handles GIF export functionality with improved color quality"""
    
    def __init__(self):
        self.default_fps = 15
        
    def export_gif(self, 
                   frames: List[np.ndarray], 
                   output_path: str, 
                   fps: Optional[int] = None,
                   quality: Optional[str] = None,
                   color_mode: str = 'RGB') -> bool:
        """
        Export frames as animated GIF with high quality color preservation
        
        Args:
            frames: List of numpy arrays (RGB images)
            output_path: Path to save the GIF
            fps: Frames per second (default: 15)
            quality: Quality preset - 'low', 'medium', 'high' (default: 'medium')
            color_mode: Input color mode - 'RGB' or 'BGR'
            
        Returns:
            bool: True if export successful
        """
        if not frames:
            raise ValueError("No frames to export")
            
        fps = fps or self.default_fps
        quality = quality or 'medium'
        
        try:
            # Ensure output directory exists
            os.makedirs(os.path.dirname(os.path.abspath(output_path)) or '.', exist_ok=True)
            
            # Convert frames to PIL Images
            pil_frames = []
            for frame in frames:
                if isinstance(frame, np.ndarray):
                    # Handle different data types
                    if frame.dtype != np.uint8:
                        frame = (frame * 255).astype(np.uint8)
                    
                    # Convert BGR to RGB if necessary
                    if color_mode == 'BGR':
                        frame = frame[:, :, ::-1]  # Reverse channel order
                    
                    if frame.shape[2] == 3:  # RGB
                        img = Image.fromarray(frame, mode='RGB')
                    elif frame.shape[2] == 4:  # RGBA
                        img = Image.fromarray(frame, mode='RGBA').convert('RGB')
                    else:
                        img = Image.fromarray(frame)
                else:
                    img = frame
                pil_frames.append(img)
            
            # Calculate duration between frames in milliseconds
            duration = int(1000 / fps)
            
            # Directly save without complex quantization that might cause color shifts
            if len(pil_frames) > 1:
                # Try to avoid quantization by using existing color information more effectively
                # Use adaptive palette per frame instead of global palette
                processed_frames = []
                for img in pil_frames:
                    # Convert to P mode with adaptive palette, but preserve original colors as much as possible
                    if img.mode != 'P':
                        # Convert with adaptive palette to maintain color accuracy
                        palette_img = img.convert('P', palette=Image.Palette.ADAPTIVE, colors=256)
                        processed_frames.append(palette_img)
                    else:
                        processed_frames.append(img)
                
                processed_frames[0].save(
                    output_path,
                    save_all=True,
                    append_images=processed_frames[1:],
                    duration=duration,
                    loop=0,
                    optimize=True,
                    disposal=2  # Restore to background
                )
            else:
                # Single frame
                if pil_frames[0].mode == 'P':
                    pil_frames[0].save(output_path, optimize=True)
                else:
                    # Convert to palette mode with adaptive palette
                    palette_img = pil_frames[0].convert('P', palette=Image.Palette.ADAPTIVE, colors=256)
                    palette_img.save(output_path, optimize=True)
                
            return True
            
        except Exception as e:
            print(f"GIF export error: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    def export_gif_simple(self,
                         frames: List[np.ndarray],
                         output_path: str,
                         fps: Optional[int] = None,
                         color_mode: str = 'RGB') -> bool:
        """
        Simple export method that preserves colors as much as possible
        
        Args:
            frames: List of numpy arrays (RGB images)
            output_path: Path to save the GIF
            fps: Frames per second (default: 15)
            color_mode: Input color mode - 'RGB' or 'BGR'
            
        Returns:
            bool: True if export successful
        """
        if not frames:
            raise ValueError("No frames to export")
            
        fps = fps or self.default_fps
        
        try:
            os.makedirs(os.path.dirname(os.path.abspath(output_path)) or '.', exist_ok=True)
            
            # Convert frames to PIL Images
            pil_frames = []
            for frame in frames:
                if isinstance(frame, np.ndarray):
                    # Handle different data types
                    if frame.dtype != np.uint8:
                        frame = (frame * 255).astype(np.uint8)
                    
                    # Convert BGR to RGB if necessary
                    if color_mode == 'BGR':
                        frame = frame[:, :, ::-1]  # Reverse channel order
                    
                    if frame.shape[2] == 3:  # RGB
                        img = Image.fromarray(frame, mode='RGB')
                    elif frame.shape[2] == 4:  # RGBA
                        img = Image.fromarray(frame, mode='RGBA').convert('RGB')
                    else:
                        img = Image.fromarray(frame)
                else:
                    img = frame
                pil_frames.append(img)
            
            duration = int(1000 / fps)
            
            # For simple export, just convert each frame individually with minimal processing
            converted_frames = []
            for img in pil_frames:
                # Convert to palette mode using median cut to preserve color integrity
                if img.mode != 'P':
                    # Use a simple conversion without aggressive optimization
                    converted = img.quantize(method=Image.Quantize.MEDIANCUT, colors=256, kmeans=0)
                    converted_frames.append(converted)
                else:
                    converted_frames.append(img)
            
            if len(converted_frames) > 1:
                converted_frames[0].save(
                    output_path,
                    save_all=True,
                    append_images=converted_frames[1:],
                    duration=duration,
                    loop=0,
                    optimize=False  # Disable optimization to prevent color shifts
                )
            else:
                converted_frames[0].save(output_path, optimize=False)
                
            return True
            
        except Exception as e:
            print(f"Simple GIF export error: {e}")
            return False
    
    def export_gif_with_manual_palette(self,
                                      frames: List[np.ndarray],
                                      output_path: str,
                                      fps: Optional[int] = None,
                                      color_mode: str = 'RGB') -> bool:
        """
        Export using manually created palette from first frame to ensure color consistency
        
        Args:
            frames: List of numpy arrays (RGB images)
            output_path: Path to save the GIF
            fps: Frames per second (default: 15)
            color_mode: Input color mode - 'RGB' or 'BGR'
            
        Returns:
            bool: True if export successful
        """
        if not frames:
            raise ValueError("No frames to export")
            
        fps = fps or self.default_fps
        
        try:
            os.makedirs(os.path.dirname(os.path.abspath(output_path)) or '.', exist_ok=True)
            
            # Convert frames to PIL Images
            pil_frames = []
            for frame in frames:
                if isinstance(frame, np.ndarray):
                    # Handle different data types
                    if frame.dtype != np.uint8:
                        frame = (frame * 255).astype(np.uint8)
                    
                    # Convert BGR to RGB if necessary
                    if color_mode == 'BGR':
                        frame = frame[:, :, ::-1]  # Reverse channel order
                    
                    if frame.shape[2] == 3:  # RGB
                        img = Image.fromarray(frame, mode='RGB')
                    elif frame.shape[2] == 4:  # RGBA
                        img = Image.fromarray(frame, mode='RGBA').convert('RGB')
                    else:
                        img = Image.fromarray(frame)
                else:
                    img = frame
                pil_frames.append(img)
            
            # Create a combined palette from the first few frames to capture the overall color range
            if len(pil_frames) == 1:
                # Single frame - just quantize it
                palette_img = pil_frames[0].quantize(method=Image.Quantize.MEDIANCUT, colors=256)
                final_frames = [palette_img]
            else:
                # Create palette from first few frames
                sample_size = min(5, len(pil_frames))
                sample_frames = pil_frames[:sample_size]
                
                # Combine a few frames to create a comprehensive palette
                combined_width = sum(frame.width for frame in sample_frames[:3])
                max_height = max(frame.height for frame in sample_frames[:3])
                
                # Create a wide composite image to capture all colors
                composite = Image.new('RGB', (combined_width, max_height))
                x_offset = 0
                for frame in sample_frames[:3]:
                    # Resize frame to reduce memory usage while preserving color info
                    resized_frame = frame.resize((frame.width // 4, frame.height // 4), Image.Resampling.NEAREST)
                    composite.paste(resized_frame, (x_offset, 0))
                    x_offset += resized_frame.width
                
                # Generate the palette from the composite
                master_palette = composite.quantize(method=Image.Quantize.MEDIANCUT, colors=256)
                
                # Apply this palette to all frames
                final_frames = []
                for img in pil_frames:
                    # Apply the master palette to each frame
                    # First convert to RGB to ensure compatibility
                    rgb_img = img.convert('RGB')
                    # Then map to the master palette
                    palette_mapped = rgb_img.im.convert('P', 0, master_palette.im)
                    result_img = img.copy()
                    result_img.im = palette_mapped
                    final_frames.append(result_img)
            
            duration = int(1000 / fps)
            
            if len(final_frames) > 1:
                final_frames[0].save(
                    output_path,
                    save_all=True,
                    append_images=final_frames[1:],
                    duration=duration,
                    loop=0,
                    optimize=False  # Avoid optimization that may change colors
                )
            else:
                final_frames[0].save(output_path, optimize=False)
                
            return True
            
        except Exception as e:
            print(f"GIF export with manual palette error: {e}")
            return False
    
    def export_gif_imageio(self,
                          frames: List[np.ndarray],
                          output_path: str,
                          fps: Optional[int] = None,
                          quality: Optional[str] = None,
                          color_mode: str = 'RGB') -> bool:
        """
        Alternative export using imageio with better quality control
        
        Args:
            frames: List of numpy arrays (RGB images)
            output_path: Path to save the GIF
            fps: Frames per second (default: 15)
            quality: Quality preset
            color_mode: Input color mode - 'RGB' or 'BGR'
            
        Returns:
            bool: True if export successful
        """
        if not frames:
            raise ValueError("No frames to export")
            
        fps = fps or self.default_fps
        quality = quality or 'medium'
        
        try:
            os.makedirs(os.path.dirname(os.path.abspath(output_path)) or '.', exist_ok=True)
            
            # Convert frames to uint8 if needed and handle color mode
            processed_frames = []
            for frame in frames:
                if isinstance(frame, np.ndarray):
                    # Make sure we have correct dtype
                    if frame.dtype != np.uint8:
                        frame = (frame * 255).astype(np.uint8)
                    
                    # Convert BGR to RGB if necessary
                    if color_mode == 'BGR':
                        frame = frame[:, :, ::-1]  # Reverse channel order
                    
                    if frame.shape[2] == 4:  # RGBA to RGB
                        frame = frame[:, :, :3]
                processed_frames.append(frame)
            
            duration = 1.0 / fps
            
            # Use imageio with specific parameters to maintain color fidelity
            imageio.mimsave(
                output_path,
                processed_frames,
                duration=duration,
                loop=0,
                subrectangles=False  # Avoid subrectangle optimization that can cause color issues
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
            'dtype': str(first_frame.dtype),
            'duration_seconds': len(frames) / self.default_fps
        }