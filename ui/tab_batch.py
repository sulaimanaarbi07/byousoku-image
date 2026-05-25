# ui/tab_batch.py
import os
import threading
import customtkinter as ctk
from tkinter import filedialog

from locales.manager import language_manager
from ui import theme
from ui.widgets import QualitySlider

class TabBatch(ctk.CTkFrame):
    """
    Tab for bulk/batch folder processing with customizable operations.
    """
    def __init__(self, parent, **kwargs):
        super().__init__(
            parent,
            fg_color="transparent",
            **kwargs
        )
        self.selected_folder = ""
        self.matching_files = []
        
        # Grid Layout
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        # --- LEFT SIDE: FOLDER SELECTION & SCANNING ---
        self.left_frame = ctk.CTkFrame(
            self,
            fg_color=theme.COLOR_SURFACE,
            corner_radius=theme.RADIUS_LARGE,
            border_color=theme.COLOR_BORDER,
            border_width=1
        )
        self.left_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 10), pady=10)
        
        self.left_container = ctk.CTkFrame(self.left_frame, fg_color="transparent")
        self.left_container.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Folder picker
        self.lbl_folder_title = ctk.CTkLabel(
            self.left_container,
            text="",
            font=theme.FONT_SUBTITLE,
            text_color=theme.COLOR_TEXT_PRIMARY,
            anchor="w"
        )
        self.lbl_folder_title.pack(anchor="w", pady=(0, 10))
        
        self.folder_input_frame = ctk.CTkFrame(self.left_container, fg_color="transparent")
        self.folder_input_frame.pack(fill="x", pady=(0, 15))
        
        self.entry_folder = ctk.CTkEntry(
            self.folder_input_frame,
            fg_color=theme.COLOR_SURFACE_ALT,
            text_color=theme.COLOR_TEXT_PRIMARY,
            border_color=theme.COLOR_BORDER
        )
        self.entry_folder.pack(side="left", fill="x", expand=True, padx=(0, 10))
        self.entry_folder.bind("<KeyRelease>", lambda e: self._on_folder_path_typed())
        
        self.btn_browse = ctk.CTkButton(
            self.folder_input_frame,
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
        
        # Batch options checkboxes
        self.chk_recursive = ctk.CTkCheckBox(
            self.left_container,
            text="",
            font=theme.FONT_BODY,
            hover_color=theme.COLOR_ACCENT,
            fg_color=theme.COLOR_ACCENT,
            command=self._scan_folder_threaded
        )
        self.chk_recursive.pack(anchor="w", pady=(5, 10))
        
        self.chk_preserve = ctk.CTkCheckBox(
            self.left_container,
            text="",
            font=theme.FONT_BODY,
            hover_color=theme.COLOR_ACCENT,
            fg_color=theme.COLOR_ACCENT
        )
        self.chk_preserve.select()
        self.chk_preserve.pack(anchor="w", pady=(5, 15))
        
        # Folder scanner status card
        self.status_card = ctk.CTkFrame(
            self.left_container,
            fg_color=theme.COLOR_SURFACE_ALT,
            corner_radius=theme.RADIUS_MEDIUM
        )
        self.status_card.pack(fill="both", expand=True, pady=10)
        
        self.lbl_scan_status = ctk.CTkLabel(
            self.status_card,
            text="-",
            font=theme.FONT_BODY,
            text_color=theme.COLOR_TEXT_SECONDARY,
            justify="center"
        )
        self.lbl_scan_status.pack(expand=True, fill="both", padx=15, pady=15)
        
        # --- RIGHT SIDE: OPERATIONS & PARAMETERS ---
        self.right_frame = ctk.CTkFrame(
            self,
            fg_color=theme.COLOR_SURFACE,
            corner_radius=theme.RADIUS_LARGE,
            border_color=theme.COLOR_BORDER,
            border_width=1
        )
        self.right_frame.grid(row=0, column=1, sticky="nsew", padx=(10, 0), pady=10)
        
        self.right_container = ctk.CTkFrame(self.right_frame, fg_color="transparent")
        self.right_container.pack(fill="both", expand=True, padx=20, pady=20)
        
        self.lbl_action_title = ctk.CTkLabel(
            self.right_container,
            text="",
            font=theme.FONT_SUBTITLE,
            text_color=theme.COLOR_TEXT_PRIMARY,
            anchor="w"
        )
        self.lbl_action_title.pack(anchor="w", pady=(0, 10))
        
        self.opt_action = ctk.CTkOptionMenu(
            self.right_container,
            values=["Convert", "Resize", "Compress", "HEIC to JPG/PNG"],
            fg_color=theme.COLOR_SURFACE_ALT,
            button_color=theme.COLOR_SURFACE_ALT,
            text_color=theme.COLOR_TEXT_PRIMARY,
            dropdown_fg_color=theme.COLOR_SURFACE,
            dropdown_text_color=theme.COLOR_TEXT_PRIMARY,
            command=self._on_action_changed
        )
        self.opt_action.pack(fill="x", pady=(0, 15))
        
        # Sub-parameters frame
        self.params_frame = ctk.CTkFrame(self.right_container, fg_color="transparent")
        self.params_frame.pack(fill="both", expand=True, pady=(5, 10))
        
        # Dynamic Op Subpanels
        # Subpanel 1: Convert Option
        self.sub_convert = ctk.CTkFrame(self.params_frame, fg_color="transparent")
        self.lbl_conv_fmt = ctk.CTkLabel(self.sub_convert, text="Output Format", font=theme.FONT_BODY_BOLD)
        self.lbl_conv_fmt.pack(anchor="w")
        self.opt_conv_fmt = ctk.CTkOptionMenu(
            self.sub_convert,
            values=["PNG", "JPG", "WEBP"],
            fg_color=theme.COLOR_SURFACE_ALT,
            button_color=theme.COLOR_SURFACE_ALT,
            text_color=theme.COLOR_TEXT_PRIMARY
        )
        self.opt_conv_fmt.pack(fill="x", pady=(2, 5))
        
        # Subpanel 2: Resize Option
        self.sub_resize = ctk.CTkFrame(self.params_frame, fg_color="transparent")
        self.lbl_res_mode = ctk.CTkLabel(self.sub_resize, text="Resize Mode", font=theme.FONT_BODY_BOLD)
        self.lbl_res_mode.pack(anchor="w")
        self.opt_res_mode = ctk.CTkOptionMenu(
            self.sub_resize,
            values=["Percentage", "Preset (1920x1080)"],
            fg_color=theme.COLOR_SURFACE_ALT,
            button_color=theme.COLOR_SURFACE_ALT,
            text_color=theme.COLOR_TEXT_PRIMARY,
            command=self._on_res_mode_changed
        )
        self.opt_res_mode.pack(fill="x", pady=(2, 5))
        
        # Nested resize slider/preset select
        self.sub_resize_percent = ctk.CTkFrame(self.sub_resize, fg_color="transparent")
        self.lbl_res_p_val = ctk.CTkLabel(self.sub_resize_percent, text="50%", font=theme.FONT_SMALL_BOLD, text_color=theme.COLOR_ACCENT)
        self.lbl_res_p_val.pack(anchor="e")
        self.slider_res_p = ctk.CTkSlider(self.sub_resize_percent, from_=10, to=200, number_of_steps=19, button_color=theme.COLOR_ACCENT, command=self._on_res_p_changed)
        self.slider_res_p.set(50)
        self.slider_res_p.pack(fill="x")
        
        self.sub_resize_preset = ctk.CTkFrame(self.sub_resize, fg_color="transparent")
        self.opt_res_presets = ctk.CTkOptionMenu(
            self.sub_resize_preset,
            values=["SNS (1200x630)", "Blog (800x600)", "Email (640x480)", "Wallpaper (1920x1080)"],
            fg_color=theme.COLOR_SURFACE_ALT,
            button_color=theme.COLOR_SURFACE_ALT,
            text_color=theme.COLOR_TEXT_PRIMARY
        )
        self.opt_res_presets.pack(fill="x")
        
        # Subpanel 3: Compress Option
        self.sub_compress = ctk.CTkFrame(self.params_frame, fg_color="transparent")
        self.comp_slider = QualitySlider(self.sub_compress, label_key="compress_quality", default_value=80)
        self.comp_slider.pack(fill="x")
        
        # Subpanel 4: HEIC Option
        self.sub_heic = ctk.CTkFrame(self.params_frame, fg_color="transparent")
        self.lbl_heic_fmt = ctk.CTkLabel(self.sub_heic, text="Format", font=theme.FONT_BODY_BOLD)
        self.lbl_heic_fmt.pack(anchor="w")
        self.opt_heic_fmt = ctk.CTkOptionMenu(
            self.sub_heic,
            values=["JPG", "PNG"],
            fg_color=theme.COLOR_SURFACE_ALT,
            button_color=theme.COLOR_SURFACE_ALT,
            text_color=theme.COLOR_TEXT_PRIMARY
        )
        self.opt_heic_fmt.pack(fill="x", pady=(2, 5))
        
        # Rename pattern box
        self.lbl_rename = ctk.CTkLabel(
            self.right_container,
            text="",
            font=theme.FONT_BODY_BOLD,
            text_color=theme.COLOR_TEXT_PRIMARY,
            anchor="w"
        )
        self.lbl_rename.pack(anchor="w", pady=(10, 2))
        
        self.entry_rename = ctk.CTkEntry(
            self.right_container,
            placeholder_text="e.g. prefix_{name}_suffix",
            fg_color=theme.COLOR_SURFACE_ALT,
            text_color=theme.COLOR_TEXT_PRIMARY,
            border_color=theme.COLOR_BORDER
        )
        self.entry_rename.pack(fill="x", pady=(0, 5))
        
        self.lbl_rename_note = ctk.CTkLabel(
            self.right_container,
            text="Note: {name} will be replaced by original file name.",
            font=theme.FONT_SMALL,
            text_color=theme.COLOR_TEXT_SECONDARY,
            anchor="w"
        )
        self.lbl_rename_note.pack(anchor="w", pady=(0, 20))
        
        # Metadata check (global for batch)
        self.chk_metadata = ctk.CTkCheckBox(
            self.right_container,
            text="",
            font=theme.FONT_BODY,
            hover_color=theme.COLOR_ACCENT,
            fg_color=theme.COLOR_ACCENT
        )
        self.chk_metadata.select()
        self.chk_metadata.pack(anchor="w", pady=(0, 10))
        
        # Localisation
        language_manager.register_listener(self.update_texts)
        self.update_texts()
        
        # Set up default subpanel layouts
        self._on_action_changed(self.opt_action.get())
        self._on_res_mode_changed(self.opt_res_mode.get())
        
    def _browse_folder(self):
        folder = filedialog.askdirectory(initialdir=self.entry_folder.get() or "~")
        if folder:
            folder = os.path.abspath(folder)
            self.entry_folder.delete(0, "end")
            self.entry_folder.insert(0, folder)
            self.selected_folder = folder
            self._scan_folder_threaded()
            
    def _on_folder_path_typed(self):
        path = self.entry_folder.get().strip()
        if os.path.isdir(path):
            self.selected_folder = os.path.abspath(path)
            self._scan_folder_threaded()
            
    def _scan_folder_threaded(self):
        # Async folder scan
        if not self.selected_folder or not os.path.isdir(self.selected_folder):
            self.lbl_scan_status.configure(text="-")
            return
        threading.Thread(target=self._run_scan, daemon=True).start()
        
    def _run_scan(self):
        folder = self.selected_folder
        recursive = bool(self.chk_recursive.get())
        
        # Determine valid extensions based on the selected action
        action_text = self.opt_action.get()
        if action_text == "HEIC to JPG/PNG" or action_text == language_manager.get("tab_heic"):
            exts = ('.heic', '.heif')
        else:
            exts = ('.png', '.jpg', '.jpeg', '.webp')
            
        found = []
        try:
            if recursive:
                for root, dirs, files in os.walk(folder):
                    for file in files:
                        if file.lower().endswith(exts):
                            found.append(os.path.join(root, file))
            else:
                for file in os.listdir(folder):
                    if file.lower().endswith(exts) and os.path.isfile(os.path.join(folder, file)):
                        found.append(os.path.join(folder, file))
        except Exception as e:
            print(f"Error scanning folder: {e}")
            
        self.matching_files = found
        
        # Compile summary details
        summary_text = f"📂  {os.path.basename(folder)}\n\n"
        summary_text += f"{len(found)} {language_manager.get('found_files')}.\n\n"
        
        ext_counts = {}
        for f in found:
            ext = os.path.splitext(f)[1].upper()
            ext_counts[ext] = ext_counts.get(ext, 0) + 1
            
        for ext, count in sorted(ext_counts.items()):
            summary_text += f"• {ext}: {count}枚\n"
            
        self.after(0, lambda: self.lbl_scan_status.configure(text=summary_text))
        
    def _on_res_p_changed(self, val):
        self.lbl_res_p_val.configure(text=f"{int(float(val))}%")
        
    def _on_res_mode_changed(self, val):
        self.sub_resize_percent.pack_forget()
        self.sub_resize_preset.pack_forget()
        
        if val == "Percentage" or val == language_manager.get("resize_percent"):
            self.sub_resize_percent.pack(fill="x", pady=5)
        else:
            self.sub_resize_preset.pack(fill="x", pady=5)
            
    def _on_action_changed(self, val):
        # Hide all option panels first
        self.sub_convert.pack_forget()
        self.sub_resize.pack_forget()
        self.sub_compress.pack_forget()
        self.sub_heic.pack_forget()
        
        lbl_convert = language_manager.get("tab_convert")
        lbl_resize = language_manager.get("tab_resize")
        lbl_compress = language_manager.get("tab_compress")
        lbl_heic = language_manager.get("tab_heic")
        
        if val == "Convert" or val == lbl_convert:
            self.sub_convert.pack(fill="x", pady=5)
        elif val == "Resize" or val == lbl_resize:
            self.sub_resize.pack(fill="x", pady=5)
        elif val == "Compress" or val == lbl_compress:
            self.sub_compress.pack(fill="x", pady=5)
        elif val == "HEIC to JPG/PNG" or val == lbl_heic:
            self.sub_heic.pack(fill="x", pady=5)
            
        # Rescan because extension filters changed (HEIC vs normal images)
        self._scan_folder_threaded()
        
    def get_payload(self):
        """Returns payload for batch processes."""
        val = self.opt_action.get()
        lbl_convert = language_manager.get("tab_convert")
        lbl_resize = language_manager.get("tab_resize")
        lbl_compress = language_manager.get("tab_compress")
        
        rename_patt = self.entry_rename.get().strip()
        preserve_meta = bool(self.chk_metadata.get())
        
        operation = ""
        params = {
            "rename_pattern": rename_patt,
            "preserve_metadata": preserve_meta
        }
        
        if val == "Convert" or val == lbl_convert:
            operation = "convert"
            params["target_format"] = self.opt_conv_fmt.get()
            
        elif val == "Resize" or val == lbl_resize:
            operation = "resize"
            res_sel = self.opt_res_mode.get()
            if res_sel == "Percentage" or res_sel == language_manager.get("resize_percent"):
                params["mode"] = "percentage"
                params["resize_params"] = {"percent": int(self.slider_res_p.get())}
            else:
                params["mode"] = "presets"
                preset_text = self.opt_res_presets.get()
                import re
                match = re.search(r'(\d+)x(\d+)', preset_text)
                if match:
                    w, h = int(match.group(1)), int(match.group(2))
                else:
                    w, h = 800, 600
                params["resize_params"] = {"width": w, "height": h}
            params["keep_aspect"] = True
            
        elif val == "Compress" or val == lbl_compress:
            operation = "compress"
            params["quality"] = self.comp_slider.get_value()
            params["lossless"] = False
            
        else: # HEIC
            operation = "heic"
            params["target_format"] = self.opt_heic_fmt.get()
            params["auto_rotate"] = True
            
        return {
            "files": self.matching_files.copy(),
            "operation": operation,
            "params": params,
            "preserve_originals": bool(self.chk_preserve.get())
        }
        
    def update_texts(self):
        self.lbl_folder_title.configure(text=language_manager.get("batch_folder_select"))
        self.btn_browse.configure(text=language_manager.get("select_dir"))
        self.chk_recursive.configure(text=language_manager.get("recursive_search"))
        self.chk_preserve.configure(text=language_manager.get("preserve_originals"))
        self.lbl_action_title.configure(text=language_manager.get("batch_operation"))
        self.lbl_rename.configure(text=language_manager.get("rename_pattern"))
        self.chk_metadata.configure(text=language_manager.get("preserve_metadata"))
        
        # Rebuild option values
        actions = [
            language_manager.get("tab_convert"),
            language_manager.get("tab_resize"),
            language_manager.get("tab_compress"),
            language_manager.get("tab_heic")
        ]
        
        prev_act = self.opt_action.get()
        self.opt_action.configure(values=actions)
        if prev_act in actions:
            self.opt_action.set(prev_act)
        else:
            self.opt_action.set(actions[0])
            
        # Rebuild resize modes
        res_modes = [
            language_manager.get("resize_percent"),
            language_manager.get("resize_presets")
        ]
        prev_res = self.opt_res_mode.get()
        self.opt_res_mode.configure(values=res_modes)
        if prev_res in res_modes:
            self.opt_res_mode.set(prev_res)
        else:
            self.opt_res_mode.set(res_modes[0])
            
        self._on_action_changed(self.opt_action.get())
        self._on_res_mode_changed(self.opt_res_mode.get())
