# ui/settings_panel.py
import os
import json
import customtkinter as ctk
from tkinter import filedialog

from locales.manager import language_manager
from ui import theme
from ui.widgets import QualitySlider

SETTINGS_FILE = "settings.json"

def load_settings():
    """Load settings from JSON file. Returns dict of settings."""
    default_settings = {
        "language": "ja",
        "theme": "Dark",
        "default_quality": 85,
        "default_output_dir": ""
    }
    
    if os.path.exists(SETTINGS_FILE):
        try:
            with open(SETTINGS_FILE, "r", encoding="utf-8") as f:
                saved = json.load(f)
                default_settings.update(saved)
        except Exception as e:
            print(f"Error loading settings.json: {e}")
            
    # Default output dir fallback to user's Pictures folder if empty
    if not default_settings["default_output_dir"]:
        pictures_dir = os.path.join(os.path.expanduser("~"), "Pictures")
        if os.path.exists(pictures_dir):
            default_settings["default_output_dir"] = os.path.join(pictures_dir, "ByousokuConverted")
        else:
            default_settings["default_output_dir"] = os.path.join(os.path.expanduser("~"), "ByousokuConverted")
            
    return default_settings

def save_settings(settings):
    """Save settings dict to JSON file."""
    try:
        with open(SETTINGS_FILE, "w", encoding="utf-8") as f:
            json.dump(settings, f, ensure_ascii=False, indent=4)
    except Exception as e:
        print(f"Error saving settings.json: {e}")


class SettingsPanel(ctk.CTkFrame):
    """
    A full-window modal-like settings overlay frame.
    """
    def __init__(self, parent, on_close_callback, **kwargs):
        super().__init__(
            parent,
            fg_color=theme.COLOR_BG,
            **kwargs
        )
        self.on_close_callback = on_close_callback
        self.settings = load_settings()
        
        # Header
        self.header_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.header_frame.pack(fill="x", padx=30, pady=(30, 20))
        
        self.lbl_title = ctk.CTkLabel(
            self.header_frame,
            text="",
            font=theme.FONT_TITLE,
            text_color=theme.COLOR_TEXT_PRIMARY,
            anchor="w"
        )
        self.lbl_title.pack(side="left")
        
        # Form Container (Centered Card)
        self.card = ctk.CTkFrame(
            self,
            fg_color=theme.COLOR_SURFACE,
            corner_radius=theme.RADIUS_LARGE,
            border_color=theme.COLOR_BORDER,
            border_width=1
        )
        self.card.pack(fill="both", expand=True, padx=30, pady=(0, 20))
        
        # Settings Content Layout
        self.form_frame = ctk.CTkFrame(self.card, fg_color="transparent")
        self.form_frame.pack(fill="both", expand=True, padx=25, pady=25)
        
        # Row 1: Language
        self.lbl_lang = ctk.CTkLabel(
            self.form_frame,
            text="",
            font=theme.FONT_BODY_BOLD,
            text_color=theme.COLOR_TEXT_PRIMARY,
            anchor="w"
        )
        self.lbl_lang.pack(anchor="w", pady=(10, 2))
        
        self.opt_lang = ctk.CTkOptionMenu(
            self.form_frame,
            values=["日本語 (Japanese)", "English"],
            fg_color=theme.COLOR_SURFACE_ALT,
            button_color=theme.COLOR_SURFACE_ALT,
            text_color=theme.COLOR_TEXT_PRIMARY,
            dropdown_fg_color=theme.COLOR_SURFACE,
            dropdown_text_color=theme.COLOR_TEXT_PRIMARY,
            command=self._on_language_menu_select
        )
        self.opt_lang.pack(fill="x", pady=(0, 15))
        
        # Row 2: Theme
        self.lbl_theme = ctk.CTkLabel(
            self.form_frame,
            text="",
            font=theme.FONT_BODY_BOLD,
            text_color=theme.COLOR_TEXT_PRIMARY,
            anchor="w"
        )
        self.lbl_theme.pack(anchor="w", pady=(10, 2))
        
        self.opt_theme = ctk.CTkOptionMenu(
            self.form_frame,
            values=[],
            fg_color=theme.COLOR_SURFACE_ALT,
            button_color=theme.COLOR_SURFACE_ALT,
            text_color=theme.COLOR_TEXT_PRIMARY,
            dropdown_fg_color=theme.COLOR_SURFACE,
            dropdown_text_color=theme.COLOR_TEXT_PRIMARY
        )
        self.opt_theme.pack(fill="x", pady=(0, 15))
        
        # Row 3: Quality
        self.quality_slider = QualitySlider(
            self.form_frame,
            label_key="default_quality",
            default_value=self.settings["default_quality"]
        )
        self.quality_slider.pack(fill="x", pady=(10, 15))
        
        # Row 4: Default save folder
        self.lbl_save_folder = ctk.CTkLabel(
            self.form_frame,
            text="",
            font=theme.FONT_BODY_BOLD,
            text_color=theme.COLOR_TEXT_PRIMARY,
            anchor="w"
        )
        self.lbl_save_folder.pack(anchor="w", pady=(10, 2))
        
        self.folder_frame = ctk.CTkFrame(self.form_frame, fg_color="transparent")
        self.folder_frame.pack(fill="x", pady=(0, 20))
        
        self.entry_folder = ctk.CTkEntry(
            self.folder_frame,
            fg_color=theme.COLOR_SURFACE_ALT,
            text_color=theme.COLOR_TEXT_PRIMARY,
            border_color=theme.COLOR_BORDER
        )
        self.entry_folder.pack(side="left", fill="x", expand=True, padx=(0, 10))
        self.entry_folder.insert(0, self.settings["default_output_dir"])
        
        self.btn_browse = ctk.CTkButton(
            self.folder_frame,
            text="",
            font=theme.FONT_BODY,
            width=80,
            fg_color=theme.COLOR_SURFACE_ALT,
            text_color=theme.COLOR_TEXT_PRIMARY,
            hover_color=theme.COLOR_BORDER,
            border_color=theme.COLOR_BORDER,
            border_width=1,
            command=self._browse_folder
        )
        self.btn_browse.pack(side="right")
        
        # Bottom Buttons
        self.buttons_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.buttons_frame.pack(fill="x", padx=30, pady=(0, 30))
        
        self.btn_cancel = ctk.CTkButton(
            self.buttons_frame,
            text="",
            font=theme.FONT_BODY_BOLD,
            fg_color="transparent",
            text_color=theme.COLOR_TEXT_PRIMARY,
            hover_color=theme.COLOR_SURFACE,
            border_color=theme.COLOR_BORDER,
            border_width=1,
            command=self._cancel
        )
        self.btn_cancel.pack(side="left", padx=(0, 10))
        
        self.btn_save = ctk.CTkButton(
            self.buttons_frame,
            text="",
            font=theme.FONT_BODY_BOLD,
            fg_color=theme.COLOR_ACCENT,
            hover_color=theme.COLOR_ACCENT_HOVER,
            command=self._save
        )
        self.btn_save.pack(side="right", padx=(10, 0))
        
        # Set dropdown initial values based on loaded settings
        lang_display = "日本語 (Japanese)" if self.settings["language"] == "ja" else "English"
        self.opt_lang.set(lang_display)
        
        # Register for translation
        language_manager.register_listener(self.update_texts)
        self.update_texts()
        
    def update_texts(self):
        # Update UI labels on translations switch
        self.lbl_title.configure(text=language_manager.get("settings_title"))
        self.lbl_lang.configure(text=language_manager.get("language"))
        self.lbl_theme.configure(text=language_manager.get("theme"))
        self.lbl_save_folder.configure(text=language_manager.get("default_output_dir"))
        self.btn_browse.configure(text=language_manager.get("select_dir"))
        self.btn_cancel.configure(text=language_manager.get("cancel"))
        self.btn_save.configure(text=language_manager.get("save"))
        
        # Update theme menu choices
        themes = [
            language_manager.get("theme_dark"),
            language_manager.get("theme_light"),
            language_manager.get("theme_system")
        ]
        self.opt_theme.configure(values=themes)
        
        # Map current theme state to localization display
        theme_map = {
            "Dark": language_manager.get("theme_dark"),
            "Light": language_manager.get("theme_light"),
            "System": language_manager.get("theme_system")
        }
        self.opt_theme.set(theme_map.get(self.settings["theme"], theme_map["Dark"]))
        
    def _on_language_menu_select(self, val):
        # Preview language immediately
        lang_code = "ja" if "日本語" in val else "en"
        language_manager.set_language(lang_code)
        
    def _browse_folder(self):
        folder = filedialog.askdirectory(initialdir=self.entry_folder.get())
        if folder:
            # Standardize paths to backslashes on windows
            folder = os.path.abspath(folder)
            self.entry_folder.delete(0, "end")
            self.entry_folder.insert(0, folder)
            
    def _cancel(self):
        # Revert language preview to original saved state
        language_manager.set_language(self.settings["language"])
        if self.on_close_callback:
            self.on_close_callback()
            
    def _save(self):
        # Extract selections and save to json
        selected_lang_text = self.opt_lang.get()
        selected_lang = "ja" if "日本語" in selected_lang_text else "en"
        
        selected_theme_text = self.opt_theme.get()
        theme_rev_map = {
            language_manager.get("theme_dark"): "Dark",
            language_manager.get("theme_light"): "Light",
            language_manager.get("theme_system"): "System"
        }
        selected_theme = theme_rev_map.get(selected_theme_text, "Dark")
        
        self.settings["language"] = selected_lang
        self.settings["theme"] = selected_theme
        self.settings["default_quality"] = self.quality_slider.get_value()
        self.settings["default_output_dir"] = self.entry_folder.get()
        
        save_settings(self.settings)
        
        # Apply theme and notify
        ctk.set_appearance_mode(selected_theme)
        language_manager.set_language(selected_lang)
        
        if self.on_close_callback:
            self.on_close_callback()
