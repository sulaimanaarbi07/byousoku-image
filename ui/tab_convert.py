# ui/tab_convert.py
import os
import customtkinter as ctk
from tkinter import filedialog

from locales.manager import language_manager
from ui import theme
from ui.widgets import DragDropFrame, FileListBox

class TabConvert(ctk.CTkFrame):
    """
    Tab for image format conversion (PNG, JPG, WebP).
    """
    def __init__(self, parent, **kwargs):
        super().__init__(
            parent,
            fg_color="transparent",
            **kwargs
        )
        self.files = []
        
        # 2-Column Grid Layout
        self.grid_columnconfigure(0, weight=3) # File area
        self.grid_columnconfigure(1, weight=2) # Settings area
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
        
        # Option Title
        self.lbl_opt_title = ctk.CTkLabel(
            self.settings_container,
            text="",
            font=theme.FONT_SUBTITLE,
            text_color=theme.COLOR_TEXT_PRIMARY,
            anchor="w"
        )
        self.lbl_opt_title.pack(anchor="w", pady=(0, 15))
        
        # Format Dropdown
        self.lbl_format = ctk.CTkLabel(
            self.settings_container,
            text="",
            font=theme.FONT_BODY_BOLD,
            text_color=theme.COLOR_TEXT_PRIMARY,
            anchor="w"
        )
        self.lbl_format.pack(anchor="w", pady=(10, 2))
        
        self.opt_format = ctk.CTkOptionMenu(
            self.settings_container,
            values=["PNG", "JPG", "WEBP"],
            fg_color=theme.COLOR_SURFACE_ALT,
            button_color=theme.COLOR_SURFACE_ALT,
            text_color=theme.COLOR_TEXT_PRIMARY,
            dropdown_fg_color=theme.COLOR_SURFACE,
            dropdown_text_color=theme.COLOR_TEXT_PRIMARY
        )
        self.opt_format.pack(fill="x", pady=(0, 20))
        
        # Metadata Checkbox
        self.chk_metadata = ctk.CTkCheckBox(
            self.settings_container,
            text="",
            font=theme.FONT_BODY,
            hover_color=theme.COLOR_ACCENT,
            fg_color=theme.COLOR_ACCENT
        )
        self.chk_metadata.select()
        self.chk_metadata.pack(anchor="w", pady=(10, 20))
        
        # Manual Add Buttons
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
        
        # Register Translation
        language_manager.register_listener(self.update_texts)
        self.update_texts()
        
    def add_files(self, file_paths):
        valid_extensions = ('.png', '.jpg', '.jpeg', '.webp')
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
        file_types = [("Image Files", "*.png;*.jpg;*.jpeg;*.webp"), ("All Files", "*.*")]
        selected = filedialog.askopenfilenames(filetypes=file_types)
        if selected:
            self.add_files([os.path.abspath(f) for f in selected])
            
    def get_payload(self):
        """Returns the processing payload for converter."""
        return {
            "files": self.files.copy(),
            "operation": "convert",
            "params": {
                "target_format": self.opt_format.get(),
                "preserve_metadata": bool(self.chk_metadata.get())
            }
        }
        
    def update_texts(self):
        self.lbl_opt_title.configure(text=language_manager.get("output_format"))
        self.lbl_format.configure(text=language_manager.get("output_format"))
        self.chk_metadata.configure(text=language_manager.get("preserve_metadata"))
        self.btn_add_files.configure(text=language_manager.get("add_files"))
        self.btn_clear.configure(text=language_manager.get("clear_list"))
