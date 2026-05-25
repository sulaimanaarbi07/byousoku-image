# ui/widgets.py
import os
import sys
import tkinter as tk
import customtkinter as ctk
from PIL import Image

from locales.manager import language_manager
from ui import theme

# Safe import for tkinterdnd2
has_dnd = False
try:
    from tkinterdnd2 import DND_FILES
    has_dnd = True
except ImportError:
    pass

class DragDropFrame(ctk.CTkFrame):
    """
    A frame that supports Drag and Drop if tkinterdnd2 is available,
    otherwise shows a standard selection instruction.
    """
    def __init__(self, parent, on_files_dropped, **kwargs):
        super().__init__(
            parent,
            corner_radius=theme.RADIUS_LARGE,
            fg_color=theme.COLOR_SURFACE,
            border_color=theme.COLOR_BORDER,
            border_width=2,
            **kwargs
        )
        self.on_files_dropped = on_files_dropped
        
        # UI Elements inside DragDropFrame
        self.label = ctk.CTkLabel(
            self,
            text="",
            font=theme.FONT_SUBTITLE,
            text_color=theme.COLOR_TEXT_SECONDARY,
            justify="center"
        )
        self.label.pack(expand=True, fill="both", padx=20, pady=40)
        
        # Set up drag and drop if available
        if has_dnd:
            try:
                self.drop_target_register(DND_FILES)
                self.dnd_bind('<<Drop>>', self._on_drop)
                self.dnd_bind('<<DropEnter>>', self._on_drag_enter)
                self.dnd_bind('<<DropLeave>>', self._on_drag_leave)
            except Exception as e:
                print(f"Error setting up drag and drop in frame: {e}")
                
        # Register for translation updates
        language_manager.register_listener(self.update_texts)
        self.update_texts()
        
    def update_texts(self):
        text = language_manager.get("drag_drop_zone")
        if not has_dnd:
            # Modify text slightly if DND is not available
            text = text.replace("ドラッグ＆ドロップ", "").replace("Drag & Drop Images Here\nor ", "")
            text = text.strip("\n ")
        self.label.configure(text=text)
        
    def _on_drag_enter(self, event):
        self.configure(border_color=theme.COLOR_ACCENT[1] if ctk.get_appearance_mode() == "Dark" else theme.COLOR_ACCENT[0])
        
    def _on_drag_leave(self, event):
        self.configure(border_color=theme.COLOR_BORDER)
        
    def _on_drop(self, event):
        self.configure(border_color=theme.COLOR_BORDER)
        data = event.data
        files = []
        
        # TkinterDnD2 returns space-separated strings, but spaces inside filenames
        # are enclosed in curly braces, e.g., "{C:/my file.png} C:/file2.png"
        # We need a robust parser for this.
        if data:
            # RegEx to find items wrapped in braces or individual non-braced tokens
            pattern = re.compile(r'\{([^}]+)\}|(\S+)')
            for match in pattern.finditer(data):
                file_path = match.group(1) or match.group(2)
                if file_path:
                    files.append(os.path.abspath(file_path))
                    
        if files and self.on_files_dropped:
            self.on_files_dropped(files)

# Simple regex fallback just in case DND parser matches empty
import re


class FileListRow(ctk.CTkFrame):
    """
    A single row in the FileListBox.
    """
    def __init__(self, parent, file_path, on_delete, **kwargs):
        super().__init__(
            parent,
            fg_color="transparent",
            height=40,
            **kwargs
        )
        self.file_path = file_path
        self.on_delete = on_delete
        
        self.grid_columnconfigure(0, weight=1) # File path
        self.grid_columnconfigure(1, weight=0) # File size
        self.grid_columnconfigure(2, weight=0) # Delete button
        
        # Icon / Thumbnail placeholder (represented as a text icon first)
        ext = os.path.splitext(file_path)[1].upper()
        
        # Safe display name (limit length if too long)
        display_name = os.path.basename(file_path)
        if len(display_name) > 40:
            display_name = display_name[:25] + "..." + display_name[-12:]
            
        self.lbl_name = ctk.CTkLabel(
            self,
            text=f"📄  {display_name}",
            font=theme.FONT_BODY,
            text_color=theme.COLOR_TEXT_PRIMARY,
            anchor="w"
        )
        self.lbl_name.grid(row=0, column=0, sticky="ew", padx=(10, 5), pady=5)
        
        # Display File Size
        try:
            size_bytes = os.path.getsize(file_path)
            if size_bytes < 1024 * 1024:
                size_str = f"{size_bytes / 1024:.1f} KB"
            else:
                size_str = f"{size_bytes / (1024 * 1024):.2f} MB"
        except Exception:
            size_str = "Unknown"
            
        self.lbl_size = ctk.CTkLabel(
            self,
            text=size_str,
            font=theme.FONT_SMALL,
            text_color=theme.COLOR_TEXT_SECONDARY,
            anchor="e"
        )
        self.lbl_size.grid(row=0, column=1, sticky="e", padx=10, pady=5)
        
        # Delete Button (Red cross button)
        self.btn_delete = ctk.CTkButton(
            self,
            text="✕",
            width=24,
            height=24,
            fg_color="transparent",
            text_color=theme.COLOR_TEXT_SECONDARY,
            hover_color=("#ffcccc", "#4a1c22"),
            corner_radius=6,
            command=self._delete
        )
        self.btn_delete.grid(row=0, column=2, sticky="e", padx=(0, 10), pady=5)
        
    def _delete(self):
        if self.on_delete:
            self.on_delete(self.file_path)


class FileListBox(ctk.CTkScrollableFrame):
    """
    A scrollable list of added files with their metadata and deletion triggers.
    """
    def __init__(self, parent, on_delete_item, **kwargs):
        super().__init__(
            parent,
            corner_radius=theme.RADIUS_MEDIUM,
            fg_color=theme.COLOR_SURFACE_ALT,
            label_text="",
            **kwargs
        )
        self.on_delete_item = on_delete_item
        self.rows = {}
        
    def set_files(self, files):
        """
        Populate the list with the given file list.
        """
        # Clear old rows
        for row in self.rows.values():
            row.destroy()
        self.rows.clear()
        
        for idx, file_path in enumerate(files):
            row = FileListRow(
                self,
                file_path=file_path,
                on_delete=self._delete_file_clicked
            )
            row.pack(fill="x", padx=5, pady=2)
            self.rows[file_path] = row
            
    def _delete_file_clicked(self, file_path):
        if self.on_delete_item:
            self.on_delete_item(file_path)


class QualitySlider(ctk.CTkFrame):
    """
    A slider for selecting image quality with a live numerical display.
    """
    def __init__(self, parent, label_key, default_value=85, min_val=1, max_val=100, step=1, **kwargs):
        super().__init__(parent, fg_color="transparent", **kwargs)
        self.label_key = label_key
        self.min_val = min_val
        self.max_val = max_val
        self.step = step
        
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=0)
        
        self.lbl_title = ctk.CTkLabel(
            self,
            text="",
            font=theme.FONT_BODY_BOLD,
            text_color=theme.COLOR_TEXT_PRIMARY,
            anchor="w"
        )
        self.lbl_title.grid(row=0, column=0, columnspan=2, sticky="ew", pady=(0, 5))
        
        self.slider = ctk.CTkSlider(
            self,
            from_=min_val,
            to=max_val,
            number_of_steps=int((max_val - min_val) / step),
            command=self._on_value_changed,
            button_color=theme.COLOR_ACCENT,
            button_hover_color=theme.COLOR_ACCENT_HOVER
        )
        self.slider.set(default_value)
        self.slider.grid(row=1, column=0, sticky="ew", padx=(0, 10))
        
        self.lbl_value = ctk.CTkLabel(
            self,
            text=f"{default_value}",
            font=theme.FONT_BODY_BOLD,
            text_color=theme.COLOR_ACCENT,
            width=40
        )
        self.lbl_value.grid(row=1, column=1, sticky="e")
        
        language_manager.register_listener(self.update_texts)
        self.update_texts()
        
    def _on_value_changed(self, value):
        val = int(float(value))
        self.lbl_value.configure(text=str(val))
        
    def get_value(self):
        return int(self.slider.get())
        
    def set_value(self, val):
        self.slider.set(val)
        self.lbl_value.configure(text=str(int(val)))
        
    def update_texts(self):
        self.lbl_title.configure(text=language_manager.get(self.label_key))
