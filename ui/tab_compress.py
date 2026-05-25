# ui/tab_compress.py
import os
import threading
import customtkinter as ctk
from tkinter import filedialog

from locales.manager import language_manager
from ui import theme
from ui.widgets import DragDropFrame, FileListBox, QualitySlider
from core.compressor import estimate_compressed_size

class TabCompress(ctk.CTkFrame):
    """
    Tab for image compression with live file size reduction estimates.
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
        
        # Quality Slider Component
        # We hook into slider value changes to update size estimation!
        self.quality_slider = QualitySlider(
            self.settings_container,
            label_key="compress_quality",
            default_value=80
        )
        # Bind slider changes to re-trigger estimation
        self.quality_slider.slider.configure(command=self._on_slider_changed)
        self.quality_slider.pack(fill="x", pady=(10, 15))
        
        # Lossless Checkbox
        self.chk_lossless = ctk.CTkCheckBox(
            self.settings_container,
            text="",
            font=theme.FONT_BODY,
            hover_color=theme.COLOR_ACCENT,
            fg_color=theme.COLOR_ACCENT,
            command=self._trigger_estimation
        )
        self.chk_lossless.pack(anchor="w", pady=(5, 20))
        
        # --- ESTIMATION CARD PANEL ---
        self.est_card = ctk.CTkFrame(
            self.settings_container,
            fg_color=theme.COLOR_SURFACE_ALT,
            corner_radius=theme.RADIUS_MEDIUM
        )
        self.est_card.pack(fill="x", pady=(10, 20))
        
        self.lbl_est_title = ctk.CTkLabel(
            self.est_card,
            text="",
            font=theme.FONT_BODY_BOLD,
            text_color=theme.COLOR_TEXT_PRIMARY
        )
        self.lbl_est_title.pack(anchor="w", padx=15, pady=(10, 5))
        
        self.lbl_sizes_before = ctk.CTkLabel(
            self.est_card,
            text="Original: -",
            font=theme.FONT_SMALL,
            text_color=theme.COLOR_TEXT_SECONDARY
        )
        self.lbl_sizes_before.pack(anchor="w", padx=15)
        
        self.lbl_sizes_after = ctk.CTkLabel(
            self.est_card,
            text="Estimated: -",
            font=theme.FONT_SMALL,
            text_color=theme.COLOR_TEXT_SECONDARY
        )
        self.lbl_sizes_after.pack(anchor="w", padx=15, pady=(0, 10))
        
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
        valid_extensions = ('.png', '.jpg', '.jpeg', '.webp')
        for path in file_paths:
            if os.path.isfile(path) and path.lower().endswith(valid_extensions):
                if path not in self.files:
                    self.files.append(path)
        self.file_list.set_files(self.files)
        self._trigger_estimation()
        
    def remove_file(self, file_path):
        if file_path in self.files:
            self.files.remove(file_path)
            self.file_list.set_files(self.files)
            self._trigger_estimation()
            
    def clear_files(self):
        self.files.clear()
        self.file_list.set_files(self.files)
        self._trigger_estimation()
        
    def _browse_files(self):
        file_types = [("Image Files", "*.png;*.jpg;*.jpeg;*.webp"), ("All Files", "*.*")]
        selected = filedialog.askopenfilenames(filetypes=file_types)
        if selected:
            self.add_files([os.path.abspath(f) for f in selected])
            
    def _on_slider_changed(self, val):
        # Update slider UI label first
        self.quality_slider._on_value_changed(val)
        # Trigger re-estimation
        self._trigger_estimation()
        
    def _trigger_estimation(self):
        if not self.files:
            self.lbl_sizes_before.configure(text=f"{language_manager.get('before_size')}: -")
            self.lbl_sizes_after.configure(text=f"{language_manager.get('after_size')}: -")
            return
            
        # Run in a background thread to prevent UI freezing
        threading.Thread(target=self._run_estimation, daemon=True).start()
        
    def _run_estimation(self):
        quality = self.quality_slider.get_value()
        lossless = bool(self.chk_lossless.get())
        
        total_original = 0
        total_estimated = 0
        
        # Lock files local reference
        files_to_est = self.files.copy()
        
        for path in files_to_est:
            try:
                orig_size = os.path.getsize(path)
                total_original += orig_size
                
                # Estimate output size
                est_size = estimate_compressed_size(path, quality, lossless)
                total_estimated += est_size
            except Exception:
                pass
                
        # Format sizes nicely
        def format_size(s):
            if s < 1024 * 1024:
                return f"{s / 1024:.1f} KB"
            return f"{s / (1024 * 1024):.2f} MB"
            
        orig_str = format_size(total_original)
        est_str = format_size(total_estimated)
        
        reduction = 0
        if total_original > 0:
            reduction = max(0.0, (total_original - total_estimated) / total_original * 100.0)
            
        # Safe main-thread UI update
        self.after(0, lambda: self._update_estimation_ui(orig_str, est_str, reduction))
        
    def _update_estimation_ui(self, orig_str, est_str, reduction):
        lbl_orig = language_manager.get("before_size")
        lbl_est = language_manager.get("after_size")
        self.lbl_sizes_before.configure(text=f"{lbl_orig}: {orig_str}")
        self.lbl_sizes_after.configure(text=f"{lbl_est}: {est_str} (-{reduction:.1f}%)")
        
    def get_payload(self):
        """Returns the processing payload for compression."""
        return {
            "files": self.files.copy(),
            "operation": "compress",
            "params": {
                "quality": self.quality_slider.get_value(),
                "lossless": bool(self.chk_lossless.get())
            }
        }
        
    def update_texts(self):
        self.lbl_opt_title.configure(text=language_manager.get("tab_compress"))
        self.chk_lossless.configure(text=language_manager.get("lossless_compress"))
        self.lbl_est_title.configure(text=language_manager.get("est_size"))
        self.btn_add_files.configure(text=language_manager.get("add_files"))
        self.btn_clear.configure(text=language_manager.get("clear_list"))
        
        self._trigger_estimation()
