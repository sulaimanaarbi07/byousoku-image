# ui/app.py
import os
import customtkinter as ctk
from tkinter import messagebox

from locales.manager import language_manager
from ui import theme
from ui.top_bar import TopBar
from ui.bottom_bar import BottomBar
from ui.settings_panel import SettingsPanel, load_settings
from ui.tab_convert import TabConvert
from ui.tab_resize import TabResize
from ui.tab_compress import TabCompress
from ui.tab_heic import TabHeic
from ui.tab_batch import TabBatch
from core.batch_processor import BatchProcessor

class App(ctk.CTkFrame):
    """
    Main application orchestrator and coordinator.
    """
    def __init__(self, parent, **kwargs):
        super().__init__(
            parent,
            fg_color=theme.COLOR_BG,
            **kwargs
        )
        self.pack(fill="both", expand=True)
        
        # Load user configurations
        self.settings = load_settings()
        
        # Apply initial settings
        ctk.set_appearance_mode(self.settings.get("theme", "Dark"))
        language_manager.set_language(self.settings.get("language", "ja"))
        
        # Instantiate core processor
        self.processor = BatchProcessor()
        self.is_processing = False
        
        # --- UI LAYOUT ---
        # Column & Row configs
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=0) # Top Bar
        self.grid_rowconfigure(1, weight=0) # Tabs Selector
        self.grid_rowconfigure(2, weight=1) # Main Dynamic Panel
        self.grid_rowconfigure(3, weight=0) # Bottom Bar
        
        # 1. Header Top Bar
        self.top_bar = TopBar(self, on_settings_clicked=self.show_settings)
        self.top_bar.grid(row=0, column=0, sticky="ew", padx=10)
        
        # Divider Line
        self.divider = ctk.CTkFrame(self, height=2, fg_color=theme.COLOR_BORDER)
        self.divider.grid(row=0, column=0, sticky="ews", padx=30)
        
        # 2. Tabs Selector (Segmented Button)
        self.tab_keys = ["convert", "resize", "compress", "heic", "batch"]
        self.active_tab_key = "convert"
        
        self.tab_selector_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.tab_selector_frame.grid(row=1, column=0, sticky="ew", padx=30, pady=(15, 5))
        
        self.tabs_selector = ctk.CTkSegmentedButton(
            self.tab_selector_frame,
            values=[],
            font=theme.FONT_BODY_BOLD,
            selected_color=theme.COLOR_ACCENT,
            selected_hover_color=theme.COLOR_ACCENT_HOVER,
            command=self._on_tab_changed
        )
        self.tabs_selector.pack(fill="x")
        
        # 3. Dynamic Tab Container Frame
        self.tab_container = ctk.CTkFrame(self, fg_color="transparent")
        self.tab_container.grid(row=2, column=0, sticky="nsew", padx=30, pady=5)
        
        # Instantiate all 5 tab panels
        self.tab_convert = TabConvert(self.tab_container)
        self.tab_resize = TabResize(self.tab_container)
        self.tab_compress = TabCompress(self.tab_container)
        self.tab_heic = TabHeic(self.tab_container)
        self.tab_batch = TabBatch(self.tab_container)
        
        self.tabs = {
            "convert": self.tab_convert,
            "resize": self.tab_resize,
            "compress": self.tab_compress,
            "heic": self.tab_heic,
            "batch": self.tab_batch
        }
        
        # Show first tab by default
        self.show_tab("convert")
        
        # 4. Bottom action & progress bar
        self.bottom_bar = BottomBar(
            self,
            on_start_clicked=self.on_action_button_clicked,
            get_output_dir_fn=self.get_current_output_dir
        )
        self.bottom_bar.grid(row=3, column=0, sticky="ew", padx=10, pady=(0, 10))
        
        # 5. Settings Panel (Hidden overlay)
        self.settings_panel = None
        
        # Register locales listener
        language_manager.register_listener(self.update_texts)
        self.update_texts()
        
    def show_tab(self, tab_key):
        """Hides other tabs and packs the selected tab frame."""
        for key, tab_frame in self.tabs.items():
            if key == tab_key:
                tab_frame.pack(fill="both", expand=True)
            else:
                tab_frame.pack_forget()
        self.active_tab_key = tab_key
        
    def _on_tab_changed(self, selection):
        labels = self._get_tab_labels()
        if selection in labels:
            idx = labels.index(selection)
            self.show_tab(self.tab_keys[idx])
            
    def _get_tab_labels(self):
        return [
            language_manager.get("tab_convert"),
            language_manager.get("tab_resize"),
            language_manager.get("tab_compress"),
            language_manager.get("tab_heic"),
            language_manager.get("tab_batch")
        ]
        
    def get_current_output_dir(self):
        # Refresh settings and return save folder
        self.settings = load_settings()
        return self.settings["default_output_dir"]
        
    def show_settings(self):
        # Instantiate panel as a overlay filling entire window
        if not self.settings_panel:
            self.settings_panel = SettingsPanel(self, on_close_callback=self.hide_settings)
            self.settings_panel.place(relx=0.5, rely=0.5, relwidth=1.0, relheight=1.0, anchor="center")
            
    def hide_settings(self):
        if self.settings_panel:
            self.settings_panel.place_forget()
            self.settings_panel.destroy()
            self.settings_panel = None
            
            # Reload settings in case theme or language changed
            self.settings = load_settings()
            
            # Refresh tabs scanning in case extension targets changed
            self.tab_batch._scan_folder_threaded()
            
    def on_action_button_clicked(self):
        if self.is_processing:
            # If processing, the button serves as a Cancel trigger
            self.cancel_processing()
        else:
            self.start_processing()
            
    def start_processing(self):
        # Get active tab payload
        active_tab = self.tabs[self.active_tab_key]
        payload = active_tab.get_payload()
        
        files = payload.get("files", [])
        if not files:
            # Show warning message in status
            self.bottom_bar.show_message("err_no_files", text_color=theme.COLOR_ACCENT[1] if ctk.get_appearance_mode() == "Dark" else theme.COLOR_ACCENT[0])
            return
            
        operation = payload.get("operation")
        params = payload.get("params", {})
        
        # Fetch output folder
        dst_dir = self.get_current_output_dir()
        
        # Set states
        self.is_processing = True
        self.bottom_bar.btn_start.configure(
            text=language_manager.get("cancel"),
            fg_color=("#ff3b30", "#d03e56"),
            hover_color=("#d03e56", "#a01e30")
        )
        
        # Start core processing
        self.processor.start_batch(
            files,
            dst_dir,
            operation,
            params,
            progress_callback=self._on_batch_progress,
            complete_callback=self._on_batch_complete
        )
        
    def cancel_processing(self):
        self.processor.cancel()
        self.bottom_bar.show_message("cancel", text_color=theme.COLOR_TEXT_SECONDARY)
        
    def _on_batch_progress(self, current, total, success, error, current_filepath):
        # Safeguard main thread updates
        percent = int((current / total) * 100) if total > 0 else 0
        self.after(
            0,
            lambda: self.bottom_bar.set_progress(
                current,
                total,
                percent,
                status_key="status_processing",
                current=current,
                total=total,
                percent=percent
            )
        )
        
    def _on_batch_complete(self, success_count, error_count):
        self.after(0, lambda: self._handle_complete(success_count, error_count))
        
    def _handle_complete(self, success, error):
        self.is_processing = False
        
        # Reset BottomBar action button looks
        self.bottom_bar.btn_start.configure(
            text=language_manager.get("start_processing"),
            fg_color=theme.COLOR_ACCENT,
            hover_color=theme.COLOR_ACCENT_HOVER
        )
        
        # Show complete message
        if error > 0:
            self.bottom_bar.show_message(
                "status_done",
                text_color=theme.COLOR_TEXT_PRIMARY,
                total=success
            )
            # Show a pop-up alert
            messagebox.showwarning(
                language_manager.get("warning"),
                language_manager.get("err_process_failed")
            )
        else:
            self.bottom_bar.show_message(
                "status_done",
                text_color=theme.COLOR_SUCCESS[1] if ctk.get_appearance_mode() == "Dark" else theme.COLOR_SUCCESS[0],
                total=success
            )
            # Simple alert
            messagebox.showinfo(
                language_manager.get("success"),
                language_manager.get("processing_complete")
            )
            
        # Reset progress bar to full or let user see 100%
        self.bottom_bar.progress_bar.set(1.0)
        
        # Auto clear file list if completed without errors (improves workspace workflow)
        if error == 0:
            active_tab = self.tabs[self.active_tab_key]
            # Batch tab has no list to clear, others do
            if hasattr(active_tab, "clear_files"):
                active_tab.clear_files()
                
    def update_texts(self):
        # Refresh segmented button labels in translated language
        labels = self._get_tab_labels()
        self.tabs_selector.configure(values=labels)
        
        # Sync index selection
        self.tabs_selector.set(labels[self.tab_keys.index(self.active_tab_key)])
