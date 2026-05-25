# ui/tab_resize.py
import os
import customtkinter as ctk
from tkinter import filedialog

from locales.manager import language_manager
from ui import theme
from ui.widgets import DragDropFrame, FileListBox

class TabResize(ctk.CTkFrame):
    """
    Tab for resizing images (percentage, pixels, or standard presets).
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
        
        # Resize Mode Selector
        self.lbl_mode = ctk.CTkLabel(
            self.settings_container,
            text="",
            font=theme.FONT_BODY_BOLD,
            text_color=theme.COLOR_TEXT_PRIMARY,
            anchor="w"
        )
        self.lbl_mode.pack(anchor="w", pady=(5, 2))
        
        self.opt_mode = ctk.CTkOptionMenu(
            self.settings_container,
            values=[],
            fg_color=theme.COLOR_SURFACE_ALT,
            button_color=theme.COLOR_SURFACE_ALT,
            text_color=theme.COLOR_TEXT_PRIMARY,
            dropdown_fg_color=theme.COLOR_SURFACE,
            dropdown_text_color=theme.COLOR_TEXT_PRIMARY,
            command=self._on_mode_changed
        )
        self.opt_mode.pack(fill="x", pady=(0, 15))
        
        # Aspect Ratio Toggles / Checkboxes
        self.chk_aspect = ctk.CTkCheckBox(
            self.settings_container,
            text="",
            font=theme.FONT_BODY,
            hover_color=theme.COLOR_ACCENT,
            fg_color=theme.COLOR_ACCENT
        )
        self.chk_aspect.select()
        self.chk_aspect.pack(anchor="w", pady=(5, 10))
        
        # Metadata Toggle
        self.chk_metadata = ctk.CTkCheckBox(
            self.settings_container,
            text="",
            font=theme.FONT_BODY,
            hover_color=theme.COLOR_ACCENT,
            fg_color=theme.COLOR_ACCENT
        )
        self.chk_metadata.select()
        self.chk_metadata.pack(anchor="w", pady=(0, 15))
        
        # --- DYNAMIC CONFIGURATION CONTAINER ---
        self.config_frame = ctk.CTkFrame(self.settings_container, fg_color="transparent")
        self.config_frame.pack(fill="both", expand=True, pady=(5, 5))
        
        # Mode 1: Percentage Subframe
        self.frame_percent = ctk.CTkFrame(self.config_frame, fg_color="transparent")
        self.lbl_percent_val = ctk.CTkLabel(
            self.frame_percent,
            text="100%",
            font=theme.FONT_BODY_BOLD,
            text_color=theme.COLOR_ACCENT
        )
        self.lbl_percent_val.pack(anchor="e")
        
        self.slider_percent = ctk.CTkSlider(
            self.frame_percent,
            from_=10,
            to=200,
            number_of_steps=19,
            button_color=theme.COLOR_ACCENT,
            button_hover_color=theme.COLOR_ACCENT_HOVER,
            command=self._on_percent_changed
        )
        self.slider_percent.set(100)
        self.slider_percent.pack(fill="x")
        
        # Mode 2: Dimensions (W x H) Subframe
        self.frame_pixels = ctk.CTkFrame(self.config_frame, fg_color="transparent")
        
        self.lbl_w = ctk.CTkLabel(self.frame_pixels, text="", font=theme.FONT_SMALL_BOLD)
        self.lbl_w.pack(anchor="w", pady=(2, 0))
        self.entry_w = ctk.CTkEntry(self.frame_pixels, fg_color=theme.COLOR_SURFACE_ALT, border_color=theme.COLOR_BORDER)
        self.entry_w.insert(0, "1920")
        self.entry_w.pack(fill="x", pady=(0, 8))
        
        self.lbl_h = ctk.CTkLabel(self.frame_pixels, text="", font=theme.FONT_SMALL_BOLD)
        self.lbl_h.pack(anchor="w", pady=(2, 0))
        self.entry_h = ctk.CTkEntry(self.frame_pixels, fg_color=theme.COLOR_SURFACE_ALT, border_color=theme.COLOR_BORDER)
        self.entry_h.insert(0, "1080")
        self.entry_h.pack(fill="x")
        
        # Mode 3: Presets Subframe
        self.frame_presets = ctk.CTkFrame(self.config_frame, fg_color="transparent")
        self.opt_presets = ctk.CTkOptionMenu(
            self.frame_presets,
            values=["SNS (1200x630)", "Blog (800x600)", "Email (640x480)", "Wallpaper (1920x1080)", "Icon (256x256)"],
            fg_color=theme.COLOR_SURFACE_ALT,
            button_color=theme.COLOR_SURFACE_ALT,
            text_color=theme.COLOR_TEXT_PRIMARY,
            dropdown_fg_color=theme.COLOR_SURFACE,
            dropdown_text_color=theme.COLOR_TEXT_PRIMARY
        )
        self.opt_presets.pack(fill="x")
        
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
        
        # Default layout display
        self._on_mode_changed(self.opt_mode.get())
        
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
            
    def _on_percent_changed(self, val):
        self.lbl_percent_val.configure(text=f"{int(float(val))}%")
        
    def _on_mode_changed(self, selection):
        # Hide all subframes first
        self.frame_percent.pack_forget()
        self.frame_pixels.pack_forget()
        self.frame_presets.pack_forget()
        
        # Map selections back to logical modes
        mode_percent = language_manager.get("resize_percent")
        mode_pixels = language_manager.get("resize_pixels")
        mode_presets = language_manager.get("resize_presets")
        
        if selection == mode_percent:
            self.frame_percent.pack(fill="x", pady=10)
            self.chk_aspect.pack_forget() # aspect ratio doesn't apply to percent scale
        elif selection == mode_pixels:
            self.frame_pixels.pack(fill="x", pady=10)
            self.chk_aspect.pack(anchor="w", after=self.opt_mode, pady=(5, 10))
        elif selection == mode_presets:
            self.frame_presets.pack(fill="x", pady=10)
            self.chk_aspect.pack_forget() # presets have fixed dimensions
            
    def get_payload(self):
        """Returns payload for resizer processing."""
        selection = self.opt_mode.get()
        mode_percent = language_manager.get("resize_percent")
        mode_pixels = language_manager.get("resize_pixels")
        
        if selection == mode_percent:
            mode = "percentage"
            resize_params = {"percent": int(self.slider_percent.get())}
        elif selection == mode_pixels:
            mode = "dimensions"
            try:
                w = int(self.entry_w.get())
                h = int(self.entry_h.get())
            except ValueError:
                w, h = 800, 600
            resize_params = {"width": w, "height": h}
        else: # presets
            mode = "presets"
            preset_text = self.opt_presets.get()
            # Extract numbers like 'SNS (1200x630)' -> w=1200, h=630
            import re
            match = re.search(r'(\d+)x(\d+)', preset_text)
            if match:
                w, h = int(match.group(1)), int(match.group(2))
            else:
                w, h = 800, 600
            resize_params = {"width": w, "height": h}
            
        return {
            "files": self.files.copy(),
            "operation": "resize",
            "params": {
                "mode": mode,
                "keep_aspect": bool(self.chk_aspect.get()),
                "preserve_metadata": bool(self.chk_metadata.get()),
                "resize_params": resize_params
            }
        }
        
    def update_texts(self):
        self.lbl_opt_title.configure(text=language_manager.get("tab_resize"))
        self.lbl_mode.configure(text=language_manager.get("resize_mode"))
        self.chk_aspect.configure(text=language_manager.get("aspect_ratio"))
        self.chk_metadata.configure(text=language_manager.get("preserve_metadata"))
        self.btn_add_files.configure(text=language_manager.get("add_files"))
        self.btn_clear.configure(text=language_manager.get("clear_list"))
        
        self.lbl_w.configure(text=language_manager.get("width"))
        self.lbl_h.configure(text=language_manager.get("height"))
        
        # Update modes dropdown choices
        modes = [
            language_manager.get("resize_percent"),
            language_manager.get("resize_pixels"),
            language_manager.get("resize_presets")
        ]
        
        # Save previous selection index or default
        prev_sel = self.opt_mode.get()
        self.opt_mode.configure(values=modes)
        
        if prev_sel:
            # Map index
            if prev_sel in modes:
                self.opt_mode.set(prev_sel)
            else:
                self.opt_mode.set(modes[0])
        else:
            self.opt_mode.set(modes[0])
            
        self._on_mode_changed(self.opt_mode.get())
