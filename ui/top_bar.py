# ui/top_bar.py
import customtkinter as ctk
from locales.manager import language_manager
from ui import theme

class TopBar(ctk.CTkFrame):
    """
    Top header bar with App Title on the left and Settings gear on the right.
    """
    def __init__(self, parent, on_settings_clicked, **kwargs):
        super().__init__(
            parent,
            fg_color="transparent",
            height=60,
            **kwargs
        )
        self.on_settings_clicked = on_settings_clicked
        
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=0)
        
        # App Title & Subtitle in a container
        self.title_container = ctk.CTkFrame(self, fg_color="transparent")
        self.title_container.grid(row=0, column=0, sticky="w", padx=20, pady=10)
        
        self.lbl_title = ctk.CTkLabel(
            self.title_container,
            text="",
            font=theme.FONT_TITLE,
            text_color=theme.COLOR_TEXT_PRIMARY,
            anchor="w"
        )
        self.lbl_title.pack(anchor="w")
        
        # Settings Gear Button
        # We can use a UTF-8 cog symbol ⚙ or gear text if no image.
        # CustomTkinter supports text nicely and ⚙ displays beautiful in Yu Gothic UI!
        self.btn_settings = ctk.CTkButton(
            self,
            text="⚙️",
            font=(theme.FONT_FAMILY, 20),
            width=40,
            height=40,
            fg_color=theme.COLOR_SURFACE,
            text_color=theme.COLOR_TEXT_PRIMARY,
            hover_color=theme.COLOR_SURFACE_ALT,
            border_color=theme.COLOR_BORDER,
            border_width=1,
            corner_radius=theme.RADIUS_SMALL,
            command=self.on_settings_clicked
        )
        self.btn_settings.grid(row=0, column=1, sticky="e", padx=20, pady=10)
        
        language_manager.register_listener(self.update_texts)
        self.update_texts()
        
    def update_texts(self):
        self.lbl_title.configure(text=language_manager.get("app_title"))
