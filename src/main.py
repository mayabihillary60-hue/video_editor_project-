"""
Enhanced Video Editor - Main Application
"""

import os
import sys
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from pathlib import Path

class VideoEditor:
    def __init__(self, root):
        self.root = root
        self.root.title("Enhanced Video Editor")
        self.root.geometry("800x600")
        self.root.resizable(True, True)
        
        # Variables
        self.input_file = None
        self.output_file = None
        
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
        file_frame = ttk.LabelFrame(main_frame, text="File Selection", padding="10")
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
        
        # Operations frame
        ops_frame = ttk.LabelFrame(main_frame, text="Operations", padding="10")
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
            ("Export", self.export_video)
        ]
        
        for i, (text, command) in enumerate(operations):
            btn = ttk.Button(button_frame, text=text, command=command, width=15)
            btn.grid(row=i//3, column=i%3, padx=5, pady=5)
        
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
    
    def select_input_file(self):
        """Select input video file"""
        filename = filedialog.askopenfilename(
            title="Select Video File",
            filetypes=[
                ("Video files", "*.mp4 *.avi *.mov *.mkv *.flv"),
                ("All files", "*.*")
            ]
        )
        if filename:
            self.input_file = filename
            self.input_label.config(text=os.path.basename(filename), foreground="black")
            self.status_var.set(f"Selected: {os.path.basename(filename)}")
    
    def select_output_file(self):
        """Select output file location"""
        filename = filedialog.asksaveasfilename(
            title="Save Output Video As",
            defaultextension=".mp4",
            filetypes=[
                ("MP4 files", "*.mp4"),
                ("AVI files", "*.avi"),
                ("All files", "*.*")
            ]
        )
        if filename:
            self.output_file = filename
            self.output_label.config(text=os.path.basename(filename), foreground="black")
    
    def trim_video(self):
        """Trim video operation"""
        if not self.input_file:
            messagebox.showerror("Error", "Please select an input video first!")
            return
        
        # Create trim dialog
        trim_window = tk.Toplevel(self.root)
        trim_window.title("Trim Video")
        trim_window.geometry("400x200")
        
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
        end_entry.insert(0, "10")
        
        ttk.Button(
            trim_window, 
            text="Apply Trim", 
            command=lambda: self.apply_trim(
                float(start_entry.get()), 
                float(end_entry.get()),
                trim_window
            )
        ).pack(pady=20)
    
    def apply_trim(self, start_time, end_time, window):
        """Apply the trim operation"""
        if not self.output_file:
            self.output_file = str(Path("outputs/trimmed_video.mp4"))
            self.output_label.config(text="trimmed_video.mp4")
        
        self.status_var.set(f"Trimming video from {start_time}s to {end_time}s...")
        window.destroy()
        
        # Here we'll add the actual video processing
        messagebox.showinfo("Info", f"Would trim from {start_time}s to {end_time}s\n\n(Processing will be added in next step)")
    
    def merge_videos(self):
        """Merge multiple videos"""
        messagebox.showinfo("Info", "Merge videos feature coming in next step!")
    
    def add_text(self):
        """Add text to video"""
        messagebox.showinfo("Info", "Add text feature coming in next step!")
    
    def add_audio(self):
        """Add audio to video"""
        messagebox.showinfo("Info", "Add audio feature coming in next step!")
    
    def change_speed(self):
        """Change video speed"""
        messagebox.showinfo("Info", "Change speed feature coming in next step!")
    
    def export_video(self):
        """Export the video"""
        if not self.output_file:
            messagebox.showerror("Error", "No output file specified!")
            return
        self.status_var.set(f"Exporting to {os.path.basename(self.output_file)}...")
        messagebox.showinfo("Info", f"Would export to {self.output_file}\n\n(Export will be added in next step)")

def main():
    """Main entry point"""
    root = tk.Tk()
    app = VideoEditor(root)
    root.mainloop()

if __name__ == "__main__":
    main()