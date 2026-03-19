"""
Enhanced Video Editor - Main Application with Video Processing
"""

import os
import sys
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from pathlib import Path
import threading
from video_processor import VideoProcessor

class ProgressDialog:
    def __init__(self, parent, title):
        self.top = tk.Toplevel(parent)
        self.top.title(title)
        self.top.geometry("300x150")
        self.top.transient(parent)
        self.top.grab_set()
        
        # Center the dialog
        self.top.update_idletasks()
        x = parent.winfo_x() + (parent.winfo_width() // 2) - (300 // 2)
        y = parent.winfo_y() + (parent.winfo_height() // 2) - (150 // 2)
        self.top.geometry(f"+{x}+{y}")
        
        # Progress bar
        self.progress = ttk.Progressbar(
            self.top, 
            mode='determinate',
            length=250
        )
        self.progress.pack(pady=20)
        
        # Status label
        self.status_label = ttk.Label(self.top, text="Processing...")
        self.status_label.pack(pady=10)
        
        # Cancel button
        self.cancel_btn = ttk.Button(
            self.top,
            text="Cancel",
            command=self.cancel
        )
        self.cancel_btn.pack(pady=10)
        
        self.cancelled = False
    
    def update_progress(self, value, status=None):
        self.progress['value'] = value
        if status:
            self.status_label.config(text=status)
        self.top.update()
    
    def cancel(self):
        self.cancelled = True
        self.top.destroy()
    
    def close(self):
        self.top.destroy()

class VideoEditor:
     def apply_filter(self):
    """Apply visual filters to video"""
    if not self.input_file:
        messagebox.showerror("Error", "Please select an input video first!")
        return
    
    # Create filter dialog
    filter_window = tk.Toplevel(self.root)
    filter_window.title("Apply Filter")
    filter_window.geometry("400x500")
    filter_window.transient(self.root)
    filter_window.grab_set()
    
    ttk.Label(filter_window, text="Select Filter:").pack(pady=10)
    
    filter_var = tk.StringVar(value="grayscale")
    
    filters = [
        ("Grayscale", "grayscale"),
        ("Sepia", "sepia"),
        ("Negative", "negative"),
        ("Brightness", "brightness"),
        ("Contrast", "contrast"),
        ("Blur", "blur"),
        ("Sharpen", "sharpen"),
        ("Edge Detect", "edge_detect"),
        ("Pixelate", "pixelate"),
        ("Vintage", "vintage")
    ]
    
    # Filter selection
    filter_frame = ttk.Frame(filter_window)
    filter_frame.pack(pady=10)
    
    for i, (text, value) in enumerate(filters):
        col = i % 2
        row = i // 2
        ttk.Radiobutton(
            filter_frame,
            text=text,
            variable=filter_var,
            value=value
        ).grid(row=row, column=col, sticky=tk.W, padx=10, pady=2)
    
    # Intensity slider (for filters that support it)
    ttk.Label(filter_window, text="Intensity:").pack(pady=5)
    intensity_var = tk.DoubleVar(value=1.0)
    intensity_scale = ttk.Scale(
        filter_window,
        from_=0.0,
        to=2.0,
        orient=tk.HORIZONTAL,
        variable=intensity_var,
        length=200
    )
    intensity_scale.pack(pady=5)
    
    # Preview area (simplified)
    preview_frame = ttk.LabelFrame(filter_window, text="Preview", padding="5")
    preview_frame.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)
    
    preview_label = ttk.Label(
        preview_frame,
        text="Filter preview will appear here\n(coming soon)",
        background="#333333",
        foreground="white"
    )
    preview_label.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
    
    # Output location
    ttk.Label(
        filter_window,
        text="Output will be saved to 'outputs/filtered_video.mp4'"
    ).pack(pady=5)
    
    # Apply button
    ttk.Button(
        filter_window,
        text="Apply Filter",
        command=lambda: self.start_apply_filter(
            filter_var.get(),
            intensity_var.get(),
            filter_window
        )
    ).pack(pady=10)

def start_apply_filter(self, filter_type, intensity, window):
    """Start filter application in a separate thread"""
    window.destroy()
    
    # Set output file
    self.output_file = str(Path("outputs/filtered_video.mp4"))
    os.makedirs("outputs", exist_ok=True)
    self.output_label.config(text="filtered_video.mp4")
    
    # Show progress dialog
    progress = ProgressDialog(self.root, f"Applying {filter_type} Filter")
    
    def process():
        success, result = self.processor.apply_filter(
            self.input_file,
            self.output_file,
            filter_type,
            intensity,
            lambda v, s: progress.update_progress(v, s)
        )
        
        progress.close()
        
        if success:
            self.status_var.set(f"Filter applied: {os.path.basename(self.output_file)}")
            messagebox.showinfo("Success", f"Filter applied successfully!\nSaved to: {self.output_file}")
        else:
            self.status_var.set("Filter failed")
            messagebox.showerror("Error", f"Failed to apply filter: {result}")
    
    thread = threading.Thread(target=process)
    thread.start()

def add_transition(self):
    """Add transition between two videos"""
    # Create transition dialog
    transition_window = tk.Toplevel(self.root)
    transition_window.title("Add Transition")
    transition_window.geometry("500x400")
    transition_window.transient(self.root)
    transition_window.grab_set()
    
    ttk.Label(transition_window, text="Select two videos to add transition:").pack(pady=10)
    
    # Video selection
    video_frame = ttk.Frame(transition_window)
    video_frame.pack(pady=10)
    
    ttk.Label(video_frame, text="First Video:").grid(row=0, column=0, padx=5, pady=5)
    video1_label = ttk.Label(video_frame, text="Not selected", foreground="gray", width=30)
    video1_label.grid(row=0, column=1, padx=5, pady=5)
    
    def select_video1():
        filename = filedialog.askopenfilename(
            title="Select First Video",
            filetypes=[("Video files", "*.mp4 *.avi *.mov *.mkv")]
        )
        if filename:
            video1_label.config(text=os.path.basename(filename), foreground="black")
            video1_label.filename = filename
    
    ttk.Button(video_frame, text="Browse...", command=select_video1).grid(row=0, column=2, padx=5)
    
    ttk.Label(video_frame, text="Second Video:").grid(row=1, column=0, padx=5, pady=5
    def __init__(self, root):
        self.root = root
        self.root.title("Enhanced Video Editor")
        self.root.geometry("900x700")
        self.root.resizable(True, True)
        
        # Initialize processor
        self.processor = VideoProcessor()
        
        # Variables
        self.input_file = None
        self.output_file = None
        self.video_info = None
        
        # Setup UI
        self.setup_ui()
        
    def setup_ui(self):
        """Create the user interface"""
        # Main container
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Title
        title_label = ttk.Label(
            main_frame, 
            text="Enhanced Video Editor", 
            font=("Arial", 20, "bold")
        )
        title_label.pack(pady=10)
        
        # File selection frame
        self.create_file_selection(main_frame)
        
        # Video info frame
        self.create_info_frame(main_frame)
        
        # Operations frame
        self.create_operations(main_frame)
        
        # Status bar
        self.status_var = tk.StringVar()
        self.status_var.set("Ready")
        status_bar = ttk.Label(
            self.root, 
            textvariable=self.status_var, 
            relief=tk.SUNKEN, 
            anchor=tk.W
        )
        status_bar.pack(side=tk.BOTTOM, fill=tk.X)
    
    def create_file_selection(self, parent):
        """Create file selection section"""
        file_frame = ttk.LabelFrame(parent, text="File Selection", padding="10")
        file_frame.pack(fill=tk.X, pady=10)
        
        # Input file
        input_frame = ttk.Frame(file_frame)
        input_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(input_frame, text="Input Video:").pack(side=tk.LEFT, padx=5)
        self.input_label = ttk.Label(input_frame, text="No file selected", foreground="gray")
        self.input_label.pack(side=tk.LEFT, padx=5)
        
        ttk.Button(
            input_frame, 
            text="Browse...", 
            command=self.select_input_file
        ).pack(side=tk.RIGHT, padx=5)
        
        # Output file
        output_frame = ttk.Frame(file_frame)
        output_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(output_frame, text="Output Video:").pack(side=tk.LEFT, padx=5)
        self.output_label = ttk.Label(output_frame, text="Not specified", foreground="gray")
        self.output_label.pack(side=tk.LEFT, padx=5)
        
        ttk.Button(
            output_frame, 
            text="Browse...", 
            command=self.select_output_file
        ).pack(side=tk.RIGHT, padx=5)
    
    def create_info_frame(self, parent):
        """Create video info section"""
        self.info_frame = ttk.LabelFrame(parent, text="Video Information", padding="10")
        self.info_frame.pack(fill=tk.X, pady=10)
        
        self.info_text = tk.Text(self.info_frame, height=5, width=50)
        self.info_text.pack(fill=tk.X)
        self.info_text.insert(tk.END, "No video loaded")
        self.info_text.config(state=tk.DISABLED)
    
    def create_operations(self, parent):
        """Create operations section"""
        ops_frame = ttk.LabelFrame(parent, text="Operations", padding="10")
        ops_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Operation buttons
        button_frame = ttk.Frame(ops_frame)
        button_frame.pack(pady=10)
        
        operations = [
            ("Trim Video", self.trim_video),
            ("Merge Videos", self.merge_videos),
            ("Add Text", self.add_text),
            ("Add Audio", self.add_audio),
            ("Change Speed", self.change_speed),
            ("Extract Audio", self.extract_audio),
            ("Video Info", self.show_video_info),
            ("Export", self.export_video)
        ]
        
        for i, (text, command) in enumerate(operations):
            btn = ttk.Button(button_frame, text=text, command=command, width=15)
            btn.grid(row=i//3, column=i%3, padx=5, pady=5)
    
    def select_input_file(self):
        """Select input video file"""
        filename = filedialog.askopenfilename(
            title="Select Video File",
            filetypes=[
                ("Video files", "*.mp4 *.avi *.mov *.mkv *.flv *.wmv"),
                ("All files", "*.*")
            ]
        )
        if filename:
            self.input_file = filename
            self.input_label.config(text=os.path.basename(filename), foreground="black")
            self.status_var.set(f"Selected: {os.path.basename(filename)}")
            self.update_video_info()
    
    def select_output_file(self):
        """Select output file location"""
        filename = filedialog.asksaveasfilename(
            title="Save Output Video As",
            defaultextension=".mp4",
            filetypes=[
                ("MP4 files", "*.mp4"),
                ("AVI files", "*.avi"),
                ("MOV files", "*.mov"),
                ("All files", "*.*")
            ]
        )
        if filename:
            self.output_file = filename
            self.output_label.config(text=os.path.basename(filename), foreground="black")
    
    def update_video_info(self):
        """Update video information display"""
        if self.input_file:
            info = self.processor.get_video_info(self.input_file)
            if info:
                self.video_info = info
                self.info_text.config(state=tk.NORMAL)
                self.info_text.delete(1.0, tk.END)
                self.info_text.insert(tk.END, 
                    f"Duration: {info['duration']:.2f} seconds\n"
                    f"Resolution: {info['width']}x{info['height']}\n"
                    f"FPS: {info['fps']:.2f}\n"
                    f"Audio: {'Yes' if info['audio'] else 'No'}"
                )
                self.info_text.config(state=tk.DISABLED)
    
    def show_video_info(self):
        """Show video information in a dialog"""
        if not self.input_file:
            messagebox.showerror("Error", "Please select an input video first!")
            return
        
        if self.video_info:
            info = self.video_info
            messagebox.showinfo("Video Information",
                f"File: {os.path.basename(self.input_file)}\n"
                f"Duration: {info['duration']:.2f} seconds\n"
                f"Resolution: {info['width']}x{info['height']}\n"
                f"FPS: {info['fps']:.2f}\n"
                f"Audio Track: {'Yes' if info['audio'] else 'No'}"
            )
    
    def trim_video(self):
        """Trim video operation"""
        if not self.input_file:
            messagebox.showerror("Error", "Please select an input video first!")
            return
        
        # Create trim dialog
        trim_window = tk.Toplevel(self.root)
        trim_window.title("Trim Video")
        trim_window.geometry("400x250")
        trim_window.transient(self.root)
        trim_window.grab_set()
        
        ttk.Label(trim_window, text="Enter trim times (in seconds):").pack(pady=10)
        
        frame = ttk.Frame(trim_window)
        frame.pack(pady=10)
        
        ttk.Label(frame, text="Start:").grid(row=0, column=0, padx=5)
        start_entry = ttk.Entry(frame, width=10)
        start_entry.grid(row=0, column=1, padx=5)
        start_entry.insert(0, "0")
        
        ttk.Label(frame, text="End:").grid(row=1, column=0, padx=5)
        end_entry = ttk.Entry(frame, width=10)
        end_entry.grid(row=1, column=1, padx=5)
        
        if self.video_info:
            end_entry.insert(0, str(int(self.video_info['duration'])))
        
        ttk.Label(trim_window, text="Output will be saved to:\n'outputs/trimmed_video.mp4'").pack(pady=10)
        
        ttk.Button(
            trim_window, 
            text="Apply Trim", 
            command=lambda: self.start_trim(
                float(start_entry.get()), 
                float(end_entry.get()),
                trim_window
            )
        ).pack(pady=10)
    
    def start_trim(self, start_time, end_time, window):
        """Start trim operation in a separate thread"""
        window.destroy()
        
        # Set output file
        if not self.output_file:
            self.output_file = str(Path("outputs/trimmed_video.mp4"))
            os.makedirs("outputs", exist_ok=True)
            self.output_label.config(text="trimmed_video.mp4")
        
        # Show progress dialog
        progress = ProgressDialog(self.root, "Trimming Video")
        
        def process():
            success, result = self.processor.trim_video(
                self.input_file,
                self.output_file,
                start_time,
                end_time,
                lambda v, s: progress.update_progress(v, s)
            )
            
            progress.close()
            
            if success:
                self.status_var.set(f"Trim complete: {os.path.basename(self.output_file)}")
                messagebox.showinfo("Success", f"Video trimmed successfully!\nSaved to: {self.output_file}")
            else:
                self.status_var.set("Trim failed")
                messagebox.showerror("Error", f"Trim failed: {result}")
        
        thread = threading.Thread(target=process)
        thread.start()
    
    def merge_videos(self):
        """Merge multiple videos"""
        if not self.input_file:
            messagebox.showerror("Error", "Please select at least one video first!")
            return
        
        # Create merge dialog
        merge_window = tk.Toplevel(self.root)
        merge_window.title("Merge Videos")
        merge_window.geometry("500x400")
        merge_window.transient(self.root)
        merge_window.grab_set()
        
        ttk.Label(merge_window, text="Select videos to merge (in order):").pack(pady=10)
        
        # Listbox for videos
        list_frame = ttk.Frame(merge_window)
        list_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        scrollbar = ttk.Scrollbar(list_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        video_list = tk.Listbox(list_frame, yscrollcommand=scrollbar.set)
        video_list.pack(fill=tk.BOTH, expand=True)
        
        scrollbar.config(command=video_list.yview)
        
        # Add current video
        video_list.insert(tk.END, self.input_file)
        
        # Button frame
        btn_frame = ttk.Frame(merge_window)
        btn_frame.pack(pady=10)
        
        def add_video():
            filename = filedialog.askopenfilename(
                title="Select Video File",
                filetypes=[("Video files", "*.mp4 *.avi *.mov *.mkv")]
            )
            if filename:
                video_list.insert(tk.END, filename)
        
        def remove_selected():
            selection = video_list.curselection()
            if selection:
                video_list.delete(selection[0])
        
        def move_up():
            selection = video_list.curselection()
            if selection and selection[0] > 0:
                idx = selection[0]
                text = video_list.get(idx)
                video_list.delete(idx)
                video_list.insert(idx-1, text)
                video_list.selection_set(idx-1)
        
        def move_down():
            selection = video_list.curselection()
            if selection and selection[0] < video_list.size()-1:
                idx = selection[0]
                text = video_list.get(idx)
                video_list.delete(idx)
                video_list.insert(idx+1, text)
                video_list.selection_set(idx+1)
        
        ttk.Button(btn_frame, text="Add Video", command=add_video).grid(row=0, column=0, padx=5)
        ttk.Button(btn_frame, text="Remove", command=remove_selected).grid(row=0, column=1, padx=5)
        ttk.Button(btn_frame, text="Move Up", command=move_up).grid(row=0, column=2, padx=5)
        ttk.Button(btn_frame, text="Move Down", command=move_down).grid(row=0, column=3, padx=5)
        
        ttk.Label(merge_window, text="Output will be saved to 'outputs/merged_video.mp4'").pack(pady=5)
        
        ttk.Button(
            merge_window,
            text="Merge Videos",
            command=lambda: self.start_merge(video_list.get(0, tk.END), merge_window)
        ).pack(pady=10)
    
    def start_merge(self, video_paths, window):
        """Start merge operation in a separate thread"""
        window.destroy()
        
        # Set output file
        self.output_file = str(Path("outputs/merged_video.mp4"))
        os.makedirs("outputs", exist_ok=True)
        self.output_label.config(text="merged_video.mp4")
        
        # Show progress dialog
        progress = ProgressDialog(self.root, "Merging Videos")
        
        def process():
            success, result = self.processor.merge_videos(
                list(video_paths),
                self.output_file,
                lambda v, s: progress.update_progress(v, s)
            )
            
            progress.close()
            
            if success:
                self.status_var.set(f"Merge complete: {os.path.basename(self.output_file)}")
                messagebox.showinfo("Success", f"Videos merged successfully!\nSaved to: {self.output_file}")
            else:
                self.status_var.set("Merge failed")
                messagebox.showerror("Error", f"Merge failed: {result}")
        
        thread = threading.Thread(target=process)
        thread.start()
    
    def add_text(self):
        """Add text to video"""
        if not self.input_file:
            messagebox.showerror("Error", "Please select an input video first!")
            return
        
        # Create text dialog
        text_window = tk.Toplevel(self.root)
        text_window.title("Add Text to Video")
        text_window.geometry("400x350")
        text_window.transient(self.root)
        text_window.grab_set()
        
        ttk.Label(text_window, text="Enter text to overlay:").pack(pady=10)
        
        text_entry = tk.Text(text_window, height=3, width=40)
        text_entry.pack(pady=5)
        
        ttk.Label(text_window, text="Position:").pack(pady=5)
        position_var = tk.StringVar(value="center")
        
        position_frame = ttk.Frame(text_window)
        position_frame.pack(pady=5)
        
        positions = ['center', 'top', 'bottom', 'left', 'right']
        for pos in positions:
            ttk.Radiobutton(
                position_frame,
                text=pos.capitalize(),
                variable=position_var,
                value=pos
            ).pack(side=tk.LEFT, padx=5)
        
        ttk.Label(text_window, text="Font Size:").pack(pady=5)
        size_var = tk.IntVar(value=70)
        size_spin = ttk.Spinbox(text_window, from_=20, to=200, textvariable=size_var, width=10)
        size_spin.pack(pady=5)
        
        ttk.Label(text_window, text="Color:").pack(pady=5)
        color_var = tk.StringVar(value="white")
        color_combo = ttk.Combobox(text_window, textvariable=color_var, values=['white', 'black', 'red', 'blue', 'green', 'yellow'])
        color_combo.pack(pady=5)
        
        ttk.Label(text_window, text="Output will be saved to 'outputs/text_video.mp4'").pack(pady=10)
        
        ttk.Button(
            text_window,
            text="Add Text",
            command=lambda: self.start_add_text(
                text_entry.get("1.0", tk.END).strip(),
                position_var.get(),
                size_var.get(),
                color_var.get(),
                text_window
            )
        ).pack(pady=10)
    
    def start_add_text(self, text, position, fontsize, color, window):
        """Start add text operation in a separate thread"""
        if not text:
            messagebox.showerror("Error", "Please enter some text!")
            return
        
        window.destroy()
        
        # Set output file
        self.output_file = str(Path("outputs/text_video.mp4"))
        os.makedirs("outputs", exist_ok=True)
        self.output_label.config(text="text_video.mp4")
        
        # Show progress dialog
        progress = ProgressDialog(self.root, "Adding Text to Video")
        
        def process():
            success, result = self.processor.add_text_overlay(
                self.input_file,
                self.output_file,
                text,
                position,
                fontsize,
                color,
                callback=lambda v, s: progress.update_progress(v, s)
            )
            
            progress.close()
            
            if success:
                self.status_var.set(f"Text added: {os.path.basename(self.output_file)}")
                messagebox.showinfo("Success", f"Text added successfully!\nSaved to: {self.output_file}")
            else:
                self.status_var.set("Add text failed")
                messagebox.showerror("Error", f"Failed to add text: {result}")
        
        thread = threading.Thread(target=process)
        thread.start()
    
    def add_audio(self):
        """Add audio to video"""
        messagebox.showinfo("Info", "Add audio feature coming in next step!")
    
    def change_speed(self):
        """Change video speed"""
        if not self.input_file:
            messagebox.showerror("Error", "Please select an input video first!")
            return
        
        # Create speed dialog
        speed_window = tk.Toplevel(self.root)
        speed_window.title("Change Video Speed")
        speed_window.geometry("400x200")
        speed_window.transient(self.root)
        speed_window.grab_set()
        
        ttk.Label(speed_window, text="Select speed factor:").pack(pady=10)
        
        speed_var = tk.DoubleVar(value=1.0)
        
        speeds = [("0.25x (Slow)", 0.25), ("0.5x (Slow)", 0.5), ("0.75x", 0.75),
                  ("1.0x (Normal)", 1.0), ("1.5x", 1.5), ("2.0x (Fast)", 2.0)]
        
        for text, value in speeds:
            ttk.Radiobutton(
                speed_window,
                text=text,
                variable=speed_var,
                value=value
            ).pack(pady=2)
        
        ttk.Label(speed_window, text="Output will be saved to 'outputs/speed_changed.mp4'").pack(pady=10)
        
        ttk.Button(
            speed_window,
            text="Apply Speed",
            command=lambda: self.start_speed_change(speed_var.get(), speed_window)
        ).pack(pady=10)
    
    def start_speed_change(self, speed_factor, window):
        """Start speed change operation in a separate thread"""
        window.destroy()
        
        # Set output file
        self.output_file = str(Path("outputs/speed_changed.mp4"))
        os.makedirs("outputs", exist_ok=True)
        self.output_label.config(text="speed_changed.mp4")
        
        # Show progress dialog
        progress = ProgressDialog(self.root, "Changing Video Speed")
        
        def process():
            success, result = self.processor.change_speed(
                self.input_file,
                self.output_file,
                speed_factor,
                lambda v, s: progress.update_progress(v, s)
            )
            
            progress.close()
            
            if success:
                self.status_var.set(f"Speed changed: {os.path.basename(self.output_file)}")
                messagebox.showinfo("Success", f"Speed changed successfully!\nSaved to: {self.output_file}")
            else:
                self.status_var.set("Speed change failed")
                messagebox.showerror("Error", f"Failed to change speed: {result}")
        
        thread = threading.Thread(target=process)
        thread.start()
    
    def extract_audio(self):
        """Extract audio from video"""
        if not self.input_file:
            messagebox.showerror("Error", "Please select an input video first!")
            return
        
        # Set output file
        output_file = filedialog.asksaveasfilename(
            title="Save Audio As",
            defaultextension=".mp3",
            filetypes=[
                ("MP3 files", "*.mp3"),
                ("WAV files", "*.wav"),
                ("AAC files", "*.aac"),
                ("All files", "*.*")
            ]
        )
        
        if output_file:
            # Show progress dialog
            progress = ProgressDialog(self.root, "Extracting Audio")
            
            def process():
                success, result = self.processor.extract_audio(
                    self.input_file,
                    output_file,
                    lambda v, s: progress.update_progress(v, s)
                )
                
                progress.close()
                
                if success:
                    self.status_var.set(f"Audio extracted: {os.path.basename(output_file)}")
                    messagebox.showinfo("Success", f"Audio extracted successfully!\nSaved to: {output_file}")
                else:
                    self.status_var.set("Extract failed")
                    messagebox.showerror("Error", f"Failed to extract audio: {result}")
            
            thread = threading.Thread(target=process)
            thread.start()
    
    def export_video(self):
        """Export the video"""
        if not self.output_file:
            if not self.input_file:
                messagebox.showerror("Error", "No video to export!")
                return
            self.output_file = self.input_file
        
        if os.path.exists(self.output_file):
            messagebox.showinfo("Export", f"Video ready: {self.output_file}")
            self.status_var.set(f"Ready to use: {os.path.basename(self.output_file)}")
        else:
            messagebox.showerror("Error", "Output file not found!")

def main():
    """Main entry point"""
    root = tk.Tk()
    app = VideoEditor(root)
    root.mainloop()

if __name__ == "__main__":
    main()
