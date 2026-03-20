"""
Keyframe Dialog - UI for editing keyframe animations
"""

import tkinter as tk
from tkinter import ttk
from timeline_editor import Keyframe

class KeyframeDialog:
    def __init__(self, parent, keyframe=None, on_save=None):
        self.parent = parent
        self.keyframe = keyframe or Keyframe(time=0, position=(0,0), scale=1.0, rotation=0, opacity=1.0)
        self.on_save = on_save
        self.result = None
        
        self.create_dialog()
    
    def create_dialog(self):
        """Create keyframe edit dialog"""
        self.dialog = tk.Toplevel(self.parent)
        self.dialog.title("Edit Keyframe")
        self.dialog.geometry("400x500")
        self.dialog.transient(self.parent)
        self.dialog.grab_set()
        
        # Center the dialog
        self.dialog.update_idletasks()
        x = self.parent.winfo_x() + (self.parent.winfo_width() // 2) - (400 // 2)
        y = self.parent.winfo_y() + (self.parent.winfo_height() // 2) - (500 // 2)
        self.dialog.geometry(f"+{x}+{y}")
        
        # Time
        ttk.Label(self.dialog, text="Time (seconds):").pack(pady=5)
        self.time_var = tk.DoubleVar(value=self.keyframe.time)
        time_spin = ttk.Spinbox(
            self.dialog,
            from_=0,
            to=999,
            increment=0.1,
            textvariable=self.time_var,
            width=10
        )
        time_spin.pack(pady=5)
        
        # Position
        pos_frame = ttk.LabelFrame(self.dialog, text="Position", padding="10")
        pos_frame.pack(pady=10, padx=10, fill=tk.X)
        
        pos_inner = ttk.Frame(pos_frame)
        pos_inner.pack()
        
        ttk.Label(pos_inner, text="X:").grid(row=0, column=0, padx=5)
        self.pos_x_var = tk.DoubleVar(value=self.keyframe.position[0])
        pos_x_spin = ttk.Spinbox(pos_inner, from_=-1000, to=1000, textvariable=self.pos_x_var, width=8)
        pos_x_spin.grid(row=0, column=1, padx=5)
        
        ttk.Label(pos_inner, text="Y:").grid(row=0, column=2, padx=5)
        self.pos_y_var = tk.DoubleVar(value=self.keyframe.position[1])
        pos_y_spin = ttk.Spinbox(pos_inner, from_=-1000, to=1000, textvariable=self.pos_y_var, width=8)
        pos_y_spin.grid(row=0, column=3, padx=5)
        
        # Scale
        scale_frame = ttk.LabelFrame(self.dialog, text="Scale", padding="10")
        scale_frame.pack(pady=10, padx=10, fill=tk.X)
        
        ttk.Label(scale_frame, text="Scale factor:").pack()
        self.scale_var = tk.DoubleVar(value=self.keyframe.scale)
        scale_scale = ttk.Scale(
            scale_frame,
            from_=0.1,
            to=3.0,
            orient=tk.HORIZONTAL,
            variable=self.scale_var,
            length=200
        )
        scale_scale.pack(pady=5)
        scale_label = ttk.Label(scale_frame, textvariable=self.scale_var)
        scale_label.pack()
        
        # Rotation
        rotation_frame = ttk.LabelFrame(self.dialog, text="Rotation", padding="10")
        rotation_frame.pack(pady=10, padx=10, fill=tk.X)
        
        ttk.Label(rotation_frame, text="Degrees:").pack()
        self.rotation_var = tk.DoubleVar(value=self.keyframe.rotation)
        rotation_scale = ttk.Scale(
            rotation_frame,
            from_=-180,
            to=180,
            orient=tk.HORIZONTAL,
            variable=self.rotation_var,
            length=200
        )
        rotation_scale.pack(pady=5)
        rotation_label = ttk.Label(rotation_frame, textvariable=self.rotation_var)
        rotation_label.pack()
        
        # Opacity
        opacity_frame = ttk.LabelFrame(self.dialog, text="Opacity", padding="10")
        opacity_frame.pack(pady=10, padx=10, fill=tk.X)
        
        ttk.Label(opacity_frame, text="Opacity (0-1):").pack()
        self.opacity_var = tk.DoubleVar(value=self.keyframe.opacity)
        opacity_scale = ttk.Scale(
            opacity_frame,
            from_=0.0,
            to=1.0,
            orient=tk.HORIZONTAL,
            variable=self.opacity_var,
            length=200
        )
        opacity_scale.pack(pady=5)
        opacity_label = ttk.Label(opacity_frame, textvariable=self.opacity_var)
        opacity_label.pack()
        
        # Easing
        easing_frame = ttk.LabelFrame(self.dialog, text="Easing", padding="10")
        easing_frame.pack(pady=10, padx=10, fill=tk.X)
        
        self.easing_var = tk.StringVar(value=self.keyframe.easing)
        easings = ['linear', 'ease_in', 'ease_out', 'ease_in_out', 'bounce']
        easing_combo = ttk.Combobox(easing_frame, textvariable=self.easing_var, values=easings)
        easing_combo.pack()
        
        # Buttons
        button_frame = ttk.Frame(self.dialog)
        button_frame.pack(pady=20)
        
        ttk.Button(button_frame, text="Save", command=self.save).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Cancel", command=self.dialog.destroy).pack(side=tk.LEFT, padx=5)
    
    def save(self):
        """Save keyframe and close dialog"""
        self.result = Keyframe(
            time=self.time_var.get(),
            position=(self.pos_x_var.get(), self.pos_y_var.get()),
            scale=self.scale_var.get(),
            rotation=self.rotation_var.get(),
            opacity=self.opacity_var.get(),
            easing=self.easing_var.get()
        )
        if self.on_save:
            self.on_save(self.result)
        self.dialog.destroy()
    
    def show(self):
        """Show dialog and return result"""
        self.dialog.wait_window()
        return self.result