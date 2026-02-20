"""
Modern GUI Module for OpenCut
Using customtkinter for a modern, adaptive interface
"""

import customtkinter as ctk
from customtkinter import CTk, CTkFrame, CTkButton, CTkLabel, CTkSwitch, CTkSlider, CTkToplevel
from tkinter import filedialog, messagebox
import threading
import os
import platform
from datetime import datetime
import tkinter as tk

# Import recorder modules
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from src.recorder import ScreenRecorder
from src.gif_exporter import GIFExporter


# Set customtkinter theme
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


class ModernAreaSelector:
    """Modern fullscreen overlay for selecting screen area"""
    
    def __init__(self, callback):
        self.callback = callback
        self.root = tk.Toplevel()
        self.root.attributes('-fullscreen', True)
        self.root.attributes('-alpha', 0.4)
        self.root.attributes('-topmost', True)
        self.root.configure(bg='#1a1a2e')
        
        self.canvas = tk.Canvas(self.root, cursor='cross', bg='#1a1a2e', highlightthickness=0)
        self.canvas.pack(fill=tk.BOTH, expand=True)
        
        self.start_x = None
        self.start_y = None
        self.rect = None
        
        # Get screen dimensions
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        
        # Modern styled instructions
        self.canvas.create_text(
            screen_width // 2,
            screen_height // 2 - 60,
            text="🖱️ 拖拽选择录制区域",
            fill='#00d4ff',
            font=('Microsoft YaHei', 32, 'bold')
        )
        self.canvas.create_text(
            screen_width // 2,
            screen_height // 2,
            text="按 ESC 取消",
            fill='#888888',
            font=('Microsoft YaHei', 18)
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
            outline='#00d4ff', width=3, fill='#00d4ff'
        )
        # Update dimensions text
        width = abs(event.x - self.start_x)
        height = abs(event.y - self.start_y)
        if hasattr(self, 'dim_text'):
            self.canvas.delete(self.dim_text)
        self.dim_text = self.canvas.create_text(
            (self.start_x + event.x) // 2,
            (self.start_y + event.y) // 2,
            text=f"{width} x {height}",
            fill='white',
            font=('Microsoft YaHei', 14, 'bold')
        )
        
    def on_release(self, event):
        if self.start_x and self.start_y:
            x1 = min(self.start_x, event.x)
            y1 = min(self.start_y, event.y)
            x2 = max(self.start_x, event.x)
            y2 = max(self.start_y, event.y)
            
            width = x2 - x1
            height = y2 - y1
            
            if width > 50 and height > 50:
                self.callback(x1, y1, width, height)
            else:
                messagebox.showwarning("区域太小", "请选择更大的区域！")
                
        self.root.destroy()
        
    def on_cancel(self, event=None):
        self.root.destroy()


class OpenCutModernApp:
    """Modern main application class"""
    
    def __init__(self):
        self.root = CTk()
        self.root.title("OpenCut - 屏幕录制转GIF")
        self.root.geometry("700x500")
        self.root.minsize(600, 400)
        
        # Configure grid for responsive layout
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_rowconfigure(0, weight=1)
        
        # Initialize components
        self.recorder = ScreenRecorder()
        self.exporter = GIFExporter()
        
        # State
        self.capture_area = None
        self.is_recording = False
        self.last_gif_path = None
        
        # Create UI
        self.create_modern_ui()
        
        # Start update loop
        self.update_status()
        
    def create_modern_ui(self):
        """Create modern user interface"""
        # Main container
        self.main_frame = CTkFrame(self.root, fg_color="transparent")
        self.main_frame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
        self.main_frame.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_rowconfigure(1, weight=1)
        
        # Header
        self.create_header()
        
        # Content area (split into left and right panels)
        self.create_content_area()
        
        # Footer
        self.create_footer()
        
    def create_header(self):
        """Create modern header"""
        header = CTkFrame(self.main_frame, fg_color="transparent")
        header.grid(row=0, column=0, sticky="ew", pady=(0, 20))
        header.grid_columnconfigure(0, weight=1)
        
        # Logo and title
        title_frame = CTkFrame(header, fg_color="transparent")
        title_frame.grid(row=0, column=0, sticky="w")
        
        logo_label = CTkLabel(
            title_frame,
            text="⏺️",
            font=("Microsoft YaHei", 40)
        )
        logo_label.pack(side="left", padx=(0, 10))
        
        text_frame = CTkFrame(title_frame, fg_color="transparent")
        text_frame.pack(side="left")
        
        title = CTkLabel(
            text_frame,
            text="OpenCut",
            font=("Microsoft YaHei", 28, "bold"),
            text_color="#00d4ff"
        )
        title.pack(anchor="w")
        
        subtitle = CTkLabel(
            text_frame,
            text="屏幕录制转GIF工具",
            font=("Microsoft YaHei", 14),
            text_color="#888888"
        )
        subtitle.pack(anchor="w")
        
        # Settings button (top right)
        settings_btn = CTkButton(
            header,
            text="⚙️",
            width=40,
            height=40,
            font=("Microsoft YaHei", 16),
            fg_color="transparent",
            hover_color="#333333",
            command=self.show_settings
        )
        settings_btn.grid(row=0, column=1, sticky="e")
        
    def create_content_area(self):
        """Create main content area with left and right panels"""
        content = CTkFrame(self.main_frame, fg_color="transparent")
        content.grid(row=1, column=0, sticky="nsew", pady=10)
        content.grid_columnconfigure(0, weight=3)
        content.grid_columnconfigure(1, weight=2)
        content.grid_rowconfigure(0, weight=1)
        
        # Left panel - Main controls
        left_panel = CTkFrame(content, fg_color="#1e1e2e", corner_radius=15)
        left_panel.grid(row=0, column=0, padx=(0, 10), sticky="nsew")
        left_panel.grid_columnconfigure(0, weight=1)
        
        # Status section
        status_section = CTkFrame(left_panel, fg_color="transparent")
        status_section.pack(fill="x", padx=20, pady=20)
        
        self.status_indicator = CTkLabel(
            status_section,
            text="●",
            font=("Microsoft YaHei", 24),
            text_color="#4ade80"  # Green
        )
        self.status_indicator.pack(side="left", padx=(0, 10))
        
        self.status_text = CTkLabel(
            status_section,
            text="准备就绪",
            font=("Microsoft YaHei", 18, "bold")
        )
        self.status_text.pack(side="left")
        
        # Area info
        self.area_info = CTkLabel(
            left_panel,
            text="未选择录制区域",
            font=("Microsoft YaHei", 14),
            text_color="#888888"
        )
        self.area_info.pack(pady=10)
        
        # Recording stats
        stats_frame = CTkFrame(left_panel, fg_color="#252535", corner_radius=10)
        stats_frame.pack(fill="x", padx=20, pady=10)
        
        self.frames_label = CTkLabel(
            stats_frame,
            text="🎞️ 帧数: 0",
            font=("Microsoft YaHei", 14)
        )
        self.frames_label.pack(pady=5)
        
        self.duration_label = CTkLabel(
            stats_frame,
            text="⏱️ 时长: 0.0s",
            font=("Microsoft YaHei", 14)
        )
        self.duration_label.pack(pady=5)
        
        # Main action buttons
        btn_frame = CTkFrame(left_panel, fg_color="transparent")
        btn_frame.pack(fill="x", padx=20, pady=20)
        btn_frame.grid_columnconfigure(0, weight=1)
        btn_frame.grid_columnconfigure(1, weight=1)
        
        self.select_btn = CTkButton(
            btn_frame,
            text="📷 选择区域",
            font=("Microsoft YaHei", 16, "bold"),
            height=50,
            fg_color="#3b82f6",
            hover_color="#2563eb",
            command=self.select_area
        )
        self.select_btn.grid(row=0, column=0, padx=5, sticky="ew")
        
        self.record_btn = CTkButton(
            btn_frame,
            text="🔴 开始录制",
            font=("Microsoft YaHei", 16, "bold"),
            height=50,
            fg_color="#ef4444",
            hover_color="#dc2626",
            command=self.toggle_recording,
            state="disabled"
        )
        self.record_btn.grid(row=0, column=1, padx=5, sticky="ew")
        
        self.export_btn = CTkButton(
            left_panel,
            text="💾 导出 GIF",
            font=("Microsoft YaHei", 16, "bold"),
            height=50,
            fg_color="#10b981",
            hover_color="#059669",
            command=self.export_gif,
            state="disabled"
        )
        self.export_btn.pack(fill="x", padx=20, pady=(0, 20))
        
        # Right panel - Settings and preview
        right_panel = CTkFrame(content, fg_color="#1e1e2e", corner_radius=15)
        right_panel.grid(row=0, column=1, sticky="nsew")
        
        settings_title = CTkLabel(
            right_panel,
            text="⚙️ 设置",
            font=("Microsoft YaHei", 18, "bold")
        )
        settings_title.pack(pady=20)
        
        # FPS setting
        fps_frame = CTkFrame(right_panel, fg_color="transparent")
        fps_frame.pack(fill="x", padx=20, pady=10)
        
        fps_label = CTkLabel(
            fps_frame,
            text="帧率 (FPS)",
            font=("Microsoft YaHei", 14)
        )
        fps_label.pack(anchor="w")
        
        self.fps_var = ctk.IntVar(value=15)
        self.fps_slider = CTkSlider(
            fps_frame,
            from_=5,
            to=30,
            number_of_steps=25,
            variable=self.fps_var,
            command=self.on_fps_change
        )
        self.fps_slider.pack(fill="x", pady=5)
        
        self.fps_value_label = CTkLabel(
            fps_frame,
            text="15 FPS",
            font=("Microsoft YaHei", 12),
            text_color="#00d4ff"
        )
        self.fps_value_label.pack(anchor="e")
        
        # Quality setting
        quality_frame = CTkFrame(right_panel, fg_color="transparent")
        quality_frame.pack(fill="x", padx=20, pady=10)
        
        quality_label = CTkLabel(
            quality_frame,
            text="导出质量",
            font=("Microsoft YaHei", 14)
        )
        quality_label.pack(anchor="w")
        
        self.quality_var = ctk.StringVar(value="medium")
        quality_options = ["低 (文件小)", "中 (推荐)", "高 (清晰)"]
        self.quality_menu = ctk.CTkOptionMenu(
            quality_frame,
            values=quality_options,
            variable=self.quality_var,
            font=("Microsoft YaHei", 12)
        )
        self.quality_menu.pack(fill="x", pady=5)
        
        # Shortcuts info
        shortcuts_frame = CTkFrame(right_panel, fg_color="#252535", corner_radius=10)
        shortcuts_frame.pack(fill="x", padx=20, pady=20, side="bottom")
        
        shortcuts_title = CTkLabel(
            shortcuts_frame,
            text="⌨️ 快捷键",
            font=("Microsoft YaHei", 14, "bold")
        )
        shortcuts_title.pack(pady=10)
        
        shortcuts_text = CTkLabel(
            shortcuts_frame,
            text="F9 - 开始/停止录制\nESC - 取消选择",
            font=("Microsoft YaHei", 12),
            text_color="#888888"
        )
        shortcuts_text.pack(pady=5)
        
    def create_footer(self):
        """Create footer with progress/status"""
        footer = CTkFrame(self.main_frame, fg_color="transparent")
        footer.grid(row=2, column=0, sticky="ew", pady=(20, 0))
        
        self.progress_label = CTkLabel(
            footer,
            text="",
            font=("Microsoft YaHei", 12),
            text_color="#888888"
        )
        self.progress_label.pack(side="left")
        
        version_label = CTkLabel(
            footer,
            text="v1.0.0",
            font=("Microsoft YaHei", 12),
            text_color="#555555"
        )
        version_label.pack(side="right")
        
    def on_fps_change(self, value):
        """Update FPS label when slider changes"""
        self.fps_value_label.configure(text=f"{int(value)} FPS")
        
    def show_settings(self):
        """Show settings dialog"""
        # Could add more settings here
        pass
        
    def select_area(self):
        """Open area selector"""
        if self.is_recording:
            return
        self.root.withdraw()  # Hide main window
        self.root.after(500, lambda: ModernAreaSelector(self.on_area_selected))
        
    def on_area_selected(self, x, y, width, height):
        """Callback when area is selected"""
        self.root.deiconify()  # Show main window
        self.capture_area = (x, y, width, height)
        self.recorder.set_capture_area(x, y, width, height)
        
        self.area_info.configure(
            text=f"📐 录制区域: {width} × {height} 像素",
            text_color="#00d4ff"
        )
        self.record_btn.configure(state="normal")
        self.status_text.configure(text="区域已选择")
        self.status_indicator.configure(text_color="#fbbf24")  # Yellow
        
    def toggle_recording(self):
        """Toggle recording state"""
        if not self.is_recording:
            self.start_recording()
        else:
            self.stop_recording()
            
    def start_recording(self):
        """Start screen recording"""
        if self.capture_area is None:
            messagebox.showwarning("提示", "请先选择录制区域！")
            return
            
        self.is_recording = True
        self.recorder.fps = self.fps_var.get()
        
        self.record_btn.configure(text="⏹ 停止录制")
        self.select_btn.configure(state="disabled")
        self.export_btn.configure(state="disabled")
        self.status_text.configure(text="🔴 正在录制...")
        self.status_indicator.configure(text_color="#ef4444")  # Red
        
        # Start recording in thread
        self.recorder.start_recording(callback=self.on_frame_captured)
        
    def stop_recording(self):
        """Stop screen recording"""
        if not self.is_recording:
            return
            
        self.is_recording = False
        frames = self.recorder.stop_recording()
        
        self.record_btn.configure(text="🔴 开始录制")
        self.select_btn.configure(state="normal")
        self.export_btn.configure(state="normal")
        self.status_text.configure(text="录制完成，可导出")
        self.status_indicator.configure(text_color="#4ade80")  # Green
        
        messagebox.showinfo("完成", f"已捕获 {len(frames)} 帧\n点击'导出GIF'保存文件")
        
    def on_frame_captured(self, frame_count):
        """Callback when frame is captured"""
        self.frames_label.configure(text=f"🎞️ 帧数: {frame_count}")
        duration = frame_count / self.fps_var.get()
        self.duration_label.configure(text=f"⏱️ 时长: {duration:.1f}s")
        
    def export_gif(self):
        """Export captured frames as GIF"""
        frames = self.recorder.frames
        if not frames:
            messagebox.showwarning("提示", "没有可导出的帧！")
            return
            
        # Generate default filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        default_name = f"OpenCut_{timestamp}.gif"
        
        # Ask for save location
        file_path = filedialog.asksaveasfilename(
            defaultextension=".gif",
            filetypes=[("GIF files", "*.gif"), ("All files", "*.*")],
            initialfile=default_name
        )
        
        if not file_path:
            return
            
        # Show progress
        self.progress_label.configure(text="⏳ 正在导出 GIF...")
        self.root.update()
        
        try:
            # Get quality setting
            quality_map = {"低 (文件小)": "low", "中 (推荐)": "medium", "高 (清晰)": "high"}
            quality = quality_map.get(self.quality_var.get(), "medium")
            
            success = self.exporter.export_gif(
                frames, 
                file_path, 
                fps=self.fps_var.get(),
                quality=quality
            )
            
            if success:
                self.last_gif_path = file_path
                file_size = os.path.getsize(file_path) / 1024
                self.progress_label.configure(
                    text=f"✅ 已保存: {os.path.basename(file_path)} ({file_size:.1f} KB)"
                )
                messagebox.showinfo("导出成功", 
                                  f"文件已保存到:\n{file_path}\n\n大小: {file_size:.1f} KB")
            else:
                self.progress_label.configure(text="❌ 导出失败")
                messagebox.showerror("错误", "GIF导出失败")
                
        except Exception as e:
            self.progress_label.configure(text=f"❌ 错误: {str(e)}")
            messagebox.showerror("错误", str(e))
            
    def update_status(self):
        """Update status periodically"""
        if self.is_recording:
            frame_count = self.recorder.get_frame_count()
            self.frames_label.configure(text=f"🎞️ 帧数: {frame_count}")
            duration = frame_count / self.fps_var.get()
            self.duration_label.configure(text=f"⏱️ 时长: {duration:.1f}s")
            
        self.root.after(100, self.update_status)
        
    def run(self):
        """Start the application"""
        # Bind F9 key
        self.root.bind('<F9>', lambda e: self.toggle_recording())
        self.root.mainloop()


# For backward compatibility
OpenCutApp = OpenCutModernApp
