# ui/tab_heic.py
import os
import customtkinter as ctk
from tkinter import filedialog

from locales.manager import language_manager
from ui import theme
from ui.widgets import DragDropFrame, FileListBox
from core.heic_converter import has_heif

class TabHeic(ctk.CTkFrame):
    """
    Tab for HEIC to JPG/PNG conversion.
    """
    def __init__(self, parent, **kwargs):
        super().__init__(
            parent,
            fg_color="transparent",
            **kwargs
        )
        self.files = []
        
        # Grid Layout
        self.grid_columnconfigure(0, weight=3) # File list
        self.grid_columnconfigure(1, weight=2) # Options
        self.grid_rowconfigure(0, weight=1)
        
        # --- LEFT SIDE: FILES ---
        self.left_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.left_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 10), pady=10)
        
        self.drag_drop = DragDropFrame(self.left_frame, on_files_dropped=self.add_files)
        self.drag_drop.pack(fill="x", pady=(0, 10))
        
        self.file_list = FileListBox(self.left_frame, on_delete_item=self.remove_file, height=220)
        self.file_list.pack(fill="both", expand=True)
        
        # --- RIGHT SIDE: SETTINGS ---
        self.right_frame = ctk.CTkFrame(
            self,
            fg_color=theme.COLOR_SURFACE,
            corner_radius=theme.RADIUS_LARGE,
            border_color=theme.COLOR_BORDER,
            border_width=1
        )
        self.right_frame.grid(row=0, column=1, sticky="nsew", padx=(10, 0), pady=10)
        
        self.settings_container = ctk.CTkFrame(self.right_frame, fg_color="transparent")
        self.settings_container.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Title
        self.lbl_opt_title = ctk.CTkLabel(
            self.settings_container,
            text="",
            font=theme.FONT_SUBTITLE,
            text_color=theme.COLOR_TEXT_PRIMARY,
            anchor="w"
        )
        self.lbl_opt_title.pack(anchor="w", pady=(0, 10))
        
        # Explanation
        self.lbl_explain = ctk.CTkLabel(
            self.settings_container,
            text="",
            font=theme.FONT_SMALL,
            text_color=theme.COLOR_TEXT_SECONDARY,
            justify="left",
            wraplength=200
        )
        self.lbl_explain.pack(anchor="w", pady=(0, 15))
        
        # Target format selection
        self.lbl_target = ctk.CTkLabel(
            self.settings_container,
            text="",
            font=theme.FONT_BODY_BOLD,
            text_color=theme.COLOR_TEXT_PRIMARY,
            anchor="w"
        )
        self.lbl_target.pack(anchor="w", pady=(10, 2))
        
        self.fmt_var = ctk.StringVar(value="JPG")
        
        self.radio_jpg = ctk.CTkRadioButton(
            self.settings_container,
            text="JPG (JPEG)",
            variable=self.fmt_var,
            value="JPG",
            font=theme.FONT_BODY,
            hover_color=theme.COLOR_ACCENT,
            fg_color=theme.COLOR_ACCENT
        )
        self.radio_jpg.pack(anchor="w", pady=(5, 5))
        
        self.radio_png = ctk.CTkRadioButton(
            self.settings_container,
            text="PNG",
            variable=self.fmt_var,
            value="PNG",
            font=theme.FONT_BODY,
            hover_color=theme.COLOR_ACCENT,
            fg_color=theme.COLOR_ACCENT
        )
        self.radio_png.pack(anchor="w", pady=(0, 15))
        
        # Auto rotate
        self.chk_rotate = ctk.CTkCheckBox(
            self.settings_container,
            text="",
            font=theme.FONT_BODY,
            hover_color=theme.COLOR_ACCENT,
            fg_color=theme.COLOR_ACCENT
        )
        self.chk_rotate.select()
        self.chk_rotate.pack(anchor="w", pady=(10, 20))
        
        # Warnings for missing dependencies
        self.lbl_heif_warning = ctk.CTkLabel(
            self.settings_container,
            text="⚠️ pillow-heif is not installed!\nHEIC conversion will fail.",
            font=theme.FONT_SMALL_BOLD,
            text_color="#ff3b30",
            justify="left",
            wraplength=200
        )
        if not has_heif:
            self.lbl_heif_warning.pack(anchor="w", pady=(5, 10))
            
        # --- ACTION BUTTONS ---
        self.buttons_frame = ctk.CTkFrame(self.settings_container, fg_color="transparent")
        self.buttons_frame.pack(fill="x", side="bottom")
        
        self.btn_add_files = ctk.CTkButton(
            self.buttons_frame,
            text="",
            font=theme.FONT_BODY_BOLD,
            fg_color=theme.COLOR_SURFACE_ALT,
            text_color=theme.COLOR_TEXT_PRIMARY,
            hover_color=theme.COLOR_BORDER,
            border_color=theme.COLOR_BORDER,
            border_width=1,
            command=self._browse_files
        )
        self.btn_add_files.pack(fill="x", pady=(0, 8))
        
        self.btn_clear = ctk.CTkButton(
            self.buttons_frame,
            text="",
            font=theme.FONT_BODY_BOLD,
            fg_color="transparent",
            text_color=theme.COLOR_TEXT_SECONDARY,
            hover_color=("#ffdfdf", "#2c151a"),
            command=self.clear_files
        )
        self.btn_clear.pack(fill="x")
        
        # Localisation
        language_manager.register_listener(self.update_texts)
        self.update_texts()
        
    def add_files(self, file_paths):
        # Accepts ONLY HEIC/HEIF files (case-insensitive)
        valid_extensions = ('.heic', '.heif')
        for path in file_paths:
            if os.path.isfile(path) and path.lower().endswith(valid_extensions):
                if path not in self.files:
                    self.files.append(path)
        self.file_list.set_files(self.files)
        
    def remove_file(self, file_path):
        if file_path in self.files:
            self.files.remove(file_path)
            self.file_list.set_files(self.files)
            
    def clear_files(self):
        self.files.clear()
        self.file_list.set_files(self.files)
        
    def _browse_files(self):
        file_types = [("HEIC/HEIF Images", "*.heic;*.heif"), ("All Files", "*.*")]
        selected = filedialog.askopenfilenames(filetypes=file_types)
        if selected:
            self.add_files([os.path.abspath(f) for f in selected])
            
    def get_payload(self):
        """Returns payload for HEIC processor."""
        return {
            "files": self.files.copy(),
            "operation": "heic",
            "params": {
                "target_format": self.fmt_var.get(),
                "auto_rotate": bool(self.chk_rotate.get())
            }
        }
        
    def update_texts(self):
        self.lbl_opt_title.configure(text=language_manager.get("tab_heic"))
        self.lbl_explain.configure(text=language_manager.get("heic_explain"))
        self.lbl_target.configure(text=language_manager.get("heic_target_format"))
        self.chk_rotate.configure(text=language_manager.get("auto_rotate"))
        self.btn_add_files.configure(text=language_manager.get("add_files"))
        self.btn_clear.configure(text=language_manager.get("clear_list"))
