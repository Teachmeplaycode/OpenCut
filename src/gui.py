"""
GUI Module
Main application interface using tkinter
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import threading
import os
import platform
from datetime import datetime

from recorder import ScreenRecorder
from gif_exporter import GIFExporter


class AreaSelector:
    """Fullscreen overlay for selecting screen area"""
    
    def __init__(self, callback):
        self.callback = callback
        self.root = tk.Toplevel()
        self.root.attributes('-fullscreen', True)
        self.root.attributes('-alpha', 0.3)
        self.root.attributes('-topmost', True)
        self.root.configure(bg='gray')
        
        self.canvas = tk.Canvas(self.root, cursor='cross', bg='gray')
        self.canvas.pack(fill=tk.BOTH, expand=True)
        
        self.start_x = None
        self.start_y = None
        self.rect = None
        
        # Instructions
        self.canvas.create_text(
            self.root.winfo_screenwidth() // 2,
            self.root.winfo_screenheight() // 2 - 50,
            text="Click and drag to select area\nPress ESC to cancel",
            fill='white',
            font=('Arial', 20, 'bold')
        )
        
        # Bindings
        self.canvas.bind('<Button-1>', self.on_click)
        self.canvas.bind('<B1-Motion>', self.on_drag)
        self.canvas.bind('<ButtonRelease-1>', self.on_release)
        self.root.bind('<Escape>', self.on_cancel)
        
    def on_click(self, event):
        self.start_x = event.x
        self.start_y = event.y
        
    def on_drag(self, event):
        if self.rect:
            self.canvas.delete(self.rect)
        self.rect = self.canvas.create_rectangle(
            self.start_x, self.start_y, event.x, event.y,
            outline='red', width=2, fill='lightblue'
        )
        
    def on_release(self, event):
        if self.start_x and self.start_y:
            x1 = min(self.start_x, event.x)
            y1 = min(self.start_y, event.y)
            x2 = max(self.start_x, event.x)
            y2 = max(self.start_y, event.y)
            
            width = x2 - x1
            height = y2 - y1
            
            if width > 10 and height > 10:  # Minimum size
                self.callback(x1, y1, width, height)
            else:
                messagebox.showwarning("Invalid Selection", "Selected area too small!")
                
        self.root.destroy()
        
    def on_cancel(self, event=None):
        self.root.destroy()


class OpenCutApp:
    """Main application class"""
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("OpenCut - Screen to GIF Recorder")
        self.root.geometry("500x400")
        self.root.minsize(400, 300)
        
        # Center window
        self.center_window()
        
        # Initialize components
        self.recorder = ScreenRecorder()
        self.exporter = GIFExporter()
        
        # State
        self.capture_area = None
        self.is_recording = False
        self.last_gif_path = None
        
        # Create UI
        self.create_ui()
        
        # Update timer
        self.update_status()
        
    def center_window(self):
        """Center the window on screen"""
        self.root.update_idletasks()
        width = 500
        height = 400
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
        
    def create_ui(self):
        """Create the user interface"""
        # Main frame
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Title
        title_label = ttk.Label(
            main_frame, 
            text="OpenCut", 
            font=('Arial', 24, 'bold')
        )
        title_label.pack(pady=(0, 5))
        
        subtitle_label = ttk.Label(
            main_frame,
            text="Screen to GIF Recorder",
            font=('Arial', 12)
        )
        subtitle_label.pack(pady=(0, 20))
        
        # Status frame
        status_frame = ttk.LabelFrame(main_frame, text="Status", padding="10")
        status_frame.pack(fill=tk.X, pady=(0, 15))
        
        self.status_label = ttk.Label(
            status_frame, 
            text="Ready - Please select capture area",
            font=('Arial', 10)
        )
        self.status_label.pack()
        
        self.area_label = ttk.Label(
            status_frame,
            text="Area: Not selected",
            font=('Arial', 9)
        )
        self.area_label.pack(pady=(5, 0))
        
        # Recording info frame
        info_frame = ttk.LabelFrame(main_frame, text="Recording Info", padding="10")
        info_frame.pack(fill=tk.X, pady=(0, 15))
        
        self.frame_label = ttk.Label(
            info_frame,
            text="Frames: 0",
            font=('Arial', 10)
        )
        self.frame_label.pack(anchor=tk.W)
        
        self.duration_label = ttk.Label(
            info_frame,
            text="Duration: 0.0s",
            font=('Arial', 10)
        )
        self.duration_label.pack(anchor=tk.W)
        
        # Buttons frame
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.select_btn = ttk.Button(
            button_frame,
            text="📷 Select Area",
            command=self.select_area,
            width=20
        )
        self.select_btn.pack(pady=5)
        
        self.record_btn = ttk.Button(
            button_frame,
            text="🔴 Start Recording",
            command=self.toggle_recording,
            width=20,
            state=tk.DISABLED
        )
        self.record_btn.pack(pady=5)
        
        self.export_btn = ttk.Button(
            button_frame,
            text="💾 Export GIF",
            command=self.export_gif,
            width=20,
            state=tk.DISABLED
        )
        self.export_btn.pack(pady=5)
        
        # Settings frame
        settings_frame = ttk.LabelFrame(main_frame, text="Settings", padding="10")
        settings_frame.pack(fill=tk.X, pady=(0, 10))
        
        # FPS setting
        fps_frame = ttk.Frame(settings_frame)
        fps_frame.pack(fill=tk.X, pady=2)
        
        ttk.Label(fps_frame, text="FPS:").pack(side=tk.LEFT)
        self.fps_var = tk.IntVar(value=15)
        fps_spin = ttk.Spinbox(
            fps_frame, 
            from_=5, 
            to=30, 
            textvariable=self.fps_var,
            width=5
        )
        fps_spin.pack(side=tk.LEFT, padx=(5, 0))
        
        # Keyboard shortcuts info
        shortcuts_frame = ttk.LabelFrame(main_frame, text="Shortcuts", padding="5")
        shortcuts_frame.pack(fill=tk.X)
        
        ttk.Label(
            shortcuts_frame,
            text="F9: Start/Stop Recording | ESC: Cancel selection",
            font=('Arial', 9)
        ).pack()
        
        # Bind F9 key
        self.root.bind('<F9>', lambda e: self.toggle_recording())
        
    def select_area(self):
        """Open area selector"""
        if self.is_recording:
            return
            
        self.root.iconify()  # Minimize window
        self.root.after(500, lambda: AreaSelector(self.on_area_selected))
        
    def on_area_selected(self, x, y, width, height):
        """Callback when area is selected"""
        self.root.deiconify()  # Restore window
        self.capture_area = (x, y, width, height)
        self.recorder.set_capture_area(x, y, width, height)
        
        self.area_label.config(text=f"Area: {width}x{height} at ({x}, {y})")
        self.record_btn.config(state=tk.NORMAL)
        self.status_label.config(text="Area selected - Ready to record")
        
    def toggle_recording(self):
        """Toggle recording state"""
        if not self.is_recording:
            self.start_recording()
        else:
            self.stop_recording()
            
    def start_recording(self):
        """Start screen recording"""
        if self.capture_area is None:
            messagebox.showwarning("No Area", "Please select a capture area first!")
            return
            
        self.is_recording = True
        self.recorder.fps = self.fps_var.get()
        
        self.record_btn.config(text="⏹ Stop Recording")
        self.select_btn.config(state=tk.DISABLED)
        self.export_btn.config(state=tk.DISABLED)
        self.status_label.config(text="🔴 Recording...", foreground='red')
        
        # Start recording in thread
        self.recorder.start_recording(callback=self.on_frame_captured)
        
    def stop_recording(self):
        """Stop screen recording"""
        if not self.is_recording:
            return
            
        self.is_recording = False
        frames = self.recorder.stop_recording()
        
        self.record_btn.config(text="🔴 Start Recording")
        self.select_btn.config(state=tk.NORMAL)
        self.export_btn.config(state=tk.NORMAL)
        self.status_label.config(text="Recording stopped - Ready to export", foreground='black')
        
        messagebox.showinfo("Recording Complete", 
                          f"Captured {len(frames)} frames\nClick 'Export GIF' to save")
        
    def on_frame_captured(self, frame_count):
        """Callback when frame is captured"""
        self.frame_label.config(text=f"Frames: {frame_count}")
        duration = frame_count / self.fps_var.get()
        self.duration_label.config(text=f"Duration: {duration:.1f}s")
        
    def export_gif(self):
        """Export captured frames as GIF"""
        frames = self.recorder.frames
        if not frames:
            messagebox.showwarning("No Frames", "No frames to export!")
            return
            
        # Generate default filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        default_name = f"OpenCut_Recording_{timestamp}.gif"
        
        # Ask for save location
        file_path = filedialog.asksaveasfilename(
            defaultextension=".gif",
            filetypes=[("GIF files", "*.gif"), ("All files", "*.*")],
            initialfile=default_name
        )
        
        if not file_path:
            return
            
        # Show progress
        self.status_label.config(text="Exporting GIF...")
        self.root.update()
        
        try:
            success = self.exporter.export_gif(
                frames, 
                file_path, 
                fps=self.fps_var.get()
            )
            
            if success:
                self.last_gif_path = file_path
                file_size = os.path.getsize(file_path) / 1024  # KB
                self.status_label.config(
                    text=f"✓ Saved: {os.path.basename(file_path)} ({file_size:.1f} KB)"
                )
                messagebox.showinfo("Export Complete", 
                                  f"GIF saved to:\n{file_path}\n\nSize: {file_size:.1f} KB")
            else:
                self.status_label.config(text="Export failed")
                messagebox.showerror("Export Failed", "Failed to export GIF")
                
        except Exception as e:
            self.status_label.config(text=f"Export error: {str(e)}")
            messagebox.showerror("Export Error", str(e))
            
    def update_status(self):
        """Update status periodically"""
        if self.is_recording:
            frame_count = self.recorder.get_frame_count()
            self.frame_label.config(text=f"Frames: {frame_count}")
            duration = frame_count / self.fps_var.get()
            self.duration_label.config(text=f"Duration: {duration:.1f}s")
            
        self.root.after(100, self.update_status)
        
    def run(self):
        """Start the application"""
        self.root.mainloop()
