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
                   quality: Optional[str] = None) -> bool:
        """
        Export frames as animated GIF with high quality color preservation
        
        Args:
            frames: List of numpy arrays (RGB images)
            output_path: Path to save the GIF
            fps: Frames per second (default: 15)
            quality: Quality preset - 'low', 'medium', 'high' (default: 'medium')
            
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
            
            # Convert frames to PIL Images and quantize for better colors
            pil_frames = []
            for frame in frames:
                if isinstance(frame, np.ndarray):
                    if frame.shape[2] == 3:  # RGB
                        img = Image.fromarray(frame, mode='RGB')
                    elif frame.shape[2] == 4:  # RGBA
                        img = Image.fromarray(frame, mode='RGBA').convert('RGB')
                    else:
                        img = Image.fromarray(frame)
                else:
                    img = frame
                pil_frames.append(img)
            
            # Generate optimized global palette from all frames
            # This ensures consistent colors across the animation
            global_palette_img = self._create_global_palette(pil_frames, quality)
            
            # Quantize all frames to use the global palette
            quantized_frames = []
            for img in pil_frames:
                quantized = img.quantize(
                    colors=256,
                    method=Image.Quantize.MEDIANCUT,
                    kmeans=1 if quality == 'low' else 2 if quality == 'medium' else 4,
                    palette=global_palette_img
                )
                quantized_frames.append(quantized)
            
            # Calculate duration between frames in milliseconds
            duration = int(1000 / fps)
            
            # Save optimized GIF
            if len(quantized_frames) > 1:
                first_frame = quantized_frames[0]
                
                # Optimization settings based on quality
                if quality == 'high':
                    optimize = False  # Don't optimize to preserve colors
                    disposal = 2  # Restore to background color
                elif quality == 'medium':
                    optimize = True
                    disposal = 2
                else:  # low
                    optimize = True
                    disposal = 2
                
                first_frame.save(
                    output_path,
                    save_all=True,
                    append_images=quantized_frames[1:],
                    duration=duration,
                    loop=0,
                    optimize=optimize,
                    disposal=disposal
                )
            else:
                quantized_frames[0].save(output_path, optimize=True)
                
            return True
            
        except Exception as e:
            print(f"GIF export error: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    def _create_global_palette(self, frames: List[Image.Image], quality: str) -> Image.Image:
        """
        Create a global color palette from all frames for consistent colors
        
        Args:
            frames: List of PIL Images
            quality: Quality preset
            
        Returns:
            PIL Image with palette
        """
        if len(frames) == 1:
            # Single frame - quantize directly
            kmeans = 1 if quality == 'low' else 2 if quality == 'medium' else 4
            return frames[0].quantize(colors=256, method=Image.Quantize.MEDIANCUT, kmeans=kmeans)
        
        # For multiple frames, sample frames to create a representative palette
        # Sample every Nth frame or up to 10 frames
        sample_interval = max(1, len(frames) // 10)
        sampled_frames = frames[::sample_interval][:10]
        
        # Create a composite image from samples (side by side)
        if len(sampled_frames) == 1:
            composite = sampled_frames[0]
        else:
            # Resize frames to smaller size for palette generation
            small_frames = []
            for f in sampled_frames:
                small = f.resize((f.width // 4, f.height // 4), Image.Resampling.LANCZOS)
                small_frames.append(small)
            
            # Create a grid of frames
            grid_w = min(4, len(small_frames))
            grid_h = (len(small_frames) + grid_w - 1) // grid_w
            
            thumb_w = small_frames[0].width
            thumb_h = small_frames[0].height
            
            composite = Image.new('RGB', (thumb_w * grid_w, thumb_h * grid_h))
            
            for i, frame in enumerate(small_frames):
                x = (i % grid_w) * thumb_w
                y = (i // grid_w) * thumb_h
                composite.paste(frame, (x, y))
        
        # Generate palette from composite
        kmeans = 1 if quality == 'low' else 2 if quality == 'medium' else 4
        palette_img = composite.quantize(
            colors=256,
            method=Image.Quantize.MEDIANCUT,
            kmeans=kmeans
        )
        
        return palette_img
    
    def export_gif_high_quality(self,
                                frames: List[np.ndarray],
                                output_path: str,
                                fps: Optional[int] = None) -> bool:
        """
        Export with maximum color quality using adaptive palette per frame
        Better for complex animations but larger file size
        
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
            os.makedirs(os.path.dirname(os.path.abspath(output_path)) or '.', exist_ok=True)
            
            pil_frames = []
            for frame in frames:
                if isinstance(frame, np.ndarray):
                    if frame.shape[2] == 3:
                        img = Image.fromarray(frame, mode='RGB')
                    elif frame.shape[2] == 4:
                        img = Image.fromarray(frame, mode='RGBA').convert('RGB')
                    else:
                        img = Image.fromarray(frame)
                else:
                    img = frame
                    
                # Quantize each frame individually with high quality
                quantized = img.quantize(
                    colors=256,
                    method=Image.Quantize.MEDIANCUT,
                    kmeans=4,
                    dither=Image.Dither.NONE  # No dithering for cleaner colors
                )
                pil_frames.append(quantized)
            
            duration = int(1000 / fps)
            
            if len(pil_frames) > 1:
                pil_frames[0].save(
                    output_path,
                    save_all=True,
                    append_images=pil_frames[1:],
                    duration=duration,
                    loop=0,
                    optimize=False,  # Don't optimize to preserve colors
                    disposal=1  # Do not dispose between frames
                )
            else:
                pil_frames[0].save(output_path)
                
            return True
            
        except Exception as e:
            print(f"High quality export error: {e}")
            return False
    
    def export_gif_imageio(self,
                          frames: List[np.ndarray],
                          output_path: str,
                          fps: Optional[int] = None,
                          quality: Optional[str] = None) -> bool:
        """
        Alternative export using imageio with better quality control
        
        Args:
            frames: List of numpy arrays (RGB images)
            output_path: Path to save the GIF
            fps: Frames per second (default: 15)
            quality: Quality preset
            
        Returns:
            bool: True if export successful
        """
        if not frames:
            raise ValueError("No frames to export")
            
        fps = fps or self.default_fps
        quality = quality or 'medium'
        
        try:
            os.makedirs(os.path.dirname(os.path.abspath(output_path)) or '.', exist_ok=True)
            
            # Convert frames to uint8 if needed
            processed_frames = []
            for frame in frames:
                if isinstance(frame, np.ndarray):
                    if frame.dtype != np.uint8:
                        frame = (frame * 255).astype(np.uint8)
                    if frame.shape[2] == 4:  # RGBA to RGB
                        frame = frame[:, :, :3]
                processed_frames.append(frame)
            
            duration = 1.0 / fps
            
            # ImageIO settings based on quality
            if quality == 'high':
                # Use imageio with higher quality settings
                imageio.mimsave(
                    output_path,
                    processed_frames,
                    duration=duration,
                    loop=0,
                    quantizer=2,  # Median cut
                    palettesize=256
                )
            else:
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
