# ui/bottom_bar.py
import customtkinter as ctk
import subprocess
import os

from locales.manager import language_manager
from ui import theme

class BottomBar(ctk.CTkFrame):
    """
    Bottom bar with progress bar, status text, "Start" action button,
    and "Open Output Directory" button.
    """
    def __init__(self, parent, on_start_clicked, get_output_dir_fn, **kwargs):
        super().__init__(
            parent,
            fg_color="transparent",
            height=80,
            **kwargs
        )
        self.on_start_clicked = on_start_clicked
        self.get_output_dir_fn = get_output_dir_fn
        
        self.grid_columnconfigure(0, weight=1) # Status & progress bar
        self.grid_columnconfigure(1, weight=0) # Action buttons
        
        # Left Side: Progress & Status Container
        self.progress_container = ctk.CTkFrame(self, fg_color="transparent")
        self.progress_container.grid(row=0, column=0, sticky="ew", padx=20, pady=10)
        
        self.lbl_status = ctk.CTkLabel(
            self.progress_container,
            text="",
            font=theme.FONT_BODY_BOLD,
            text_color=theme.COLOR_TEXT_PRIMARY,
            anchor="w"
        )
        self.lbl_status.pack(anchor="w", pady=(0, 4))
        
        self.progress_bar = ctk.CTkProgressBar(
            self.progress_container,
            height=8,
            progress_color=theme.COLOR_ACCENT,
            corner_radius=theme.RADIUS_SMALL
        )
        self.progress_bar.set(0.0)
        self.progress_bar.pack(fill="x")
        
        # Right Side: Buttons Container
        self.buttons_container = ctk.CTkFrame(self, fg_color="transparent")
        self.buttons_container.grid(row=0, column=1, sticky="e", padx=20, pady=10)
        
        self.btn_open_folder = ctk.CTkButton(
            self.buttons_container,
            text="",
            font=theme.FONT_BODY_BOLD,
            width=140,
            height=36,
            fg_color=theme.COLOR_SURFACE,
            text_color=theme.COLOR_TEXT_PRIMARY,
            hover_color=theme.COLOR_SURFACE_ALT,
            border_color=theme.COLOR_BORDER,
            border_width=1,
            corner_radius=theme.RADIUS_MEDIUM,
            command=self._open_output_folder
        )
        self.btn_open_folder.pack(side="left", padx=(0, 10))
        
        self.btn_start = ctk.CTkButton(
            self.buttons_container,
            text="",
            font=theme.FONT_BODY_BOLD,
            width=140,
            height=36,
            fg_color=theme.COLOR_ACCENT,
            text_color="#ffffff",
            hover_color=theme.COLOR_ACCENT_HOVER,
            corner_radius=theme.RADIUS_MEDIUM,
            command=self.on_start_clicked
        )
        self.btn_start.pack(side="right")
        
        # Localisation
        language_manager.register_listener(self.update_texts)
        self.update_texts()
        
    def set_progress(self, current, total, percent, status_key=None, **kwargs):
        """Updates progress bar and status text safely."""
        progress_val = float(current) / float(total) if total > 0 else 0.0
        self.progress_bar.set(progress_val)
        
        if status_key:
            # Pass localization parameters if any
            status_text = language_manager.get(status_key, current=current, total=total, percent=percent, **kwargs)
        else:
            status_text = language_manager.get("status_processing", current=current, total=total, percent=percent)
            
        self.lbl_status.configure(text=status_text)
        
    def reset(self):
        self.progress_bar.set(0.0)
        self.lbl_status.configure(text=language_manager.get("status_idle"))
        self.btn_start.configure(state="normal")
        
    def show_message(self, key, text_color=None, **kwargs):
        text = language_manager.get(key, **kwargs)
        self.lbl_status.configure(text=text)
        if text_color:
            self.lbl_status.configure(text_color=text_color)
            
    def _open_output_folder(self):
        out_dir = self.get_output_dir_fn()
        if not os.path.exists(out_dir):
            try:
                os.makedirs(out_dir, exist_ok=True)
            except Exception:
                return
                
        # Windows Explorer opening
        try:
            if os.name == 'nt':
                os.startfile(out_dir)
            elif sys.platform == 'darwin':
                subprocess.Popen(['open', out_dir])
            else:
                subprocess.Popen(['xdg-open', out_dir])
        except Exception as e:
            print(f"Error opening folder: {e}")
            
    def update_texts(self):
        self.btn_open_folder.configure(text=language_manager.get("open_output"))
        self.btn_start.configure(text=language_manager.get("start_processing"))
        
        # If progress is idle/not started
        if self.progress_bar.get() == 0.0:
            self.lbl_status.configure(text=language_manager.get("status_idle"))
