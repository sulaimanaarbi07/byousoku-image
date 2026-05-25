# main.py
import sys
import os
import customtkinter as ctk

# Safe import for tkinterdnd2
has_dnd = False
try:
    from tkinterdnd2 import TkinterDnD
    has_dnd = True
except ImportError:
    pass

# Custom Tkinter root class wrapped with TkinterDnD support if available
if has_dnd:
    class RootWindow(ctk.CTk, TkinterDnD.DnDWrapper):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            try:
                self.TkdndVersion = TkinterDnD._require(self)
            except Exception as e:
                print(f"Error loading tkdnd package: {e}")
                self.TkdndVersion = None
else:
    class RootWindow(ctk.CTk):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)

def main():
    # Setup customtkinter appearance
    ctk.set_appearance_mode("Dark")
    ctk.set_default_color_theme("blue")
    
    # Initialize main window
    root = RootWindow()
    root.title("秒速画像変換 — Byousoku Image Converter")
    
    # Set window size and center on screen
    window_width = 860
    window_height = 640
    
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    
    x = int((screen_width - window_width) / 2)
    y = int((screen_height - window_height) / 2)
    
    root.geometry(f"{window_width}x{window_height}+{x}+{y}")
    root.minsize(800, 600)
    
    # Check for icon
    icon_path_png = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets", "icon.png")
    icon_path_ico = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets", "icon.ico")
    
    if os.path.exists(icon_path_png):
        try:
            from PIL import Image, ImageTk
            img = Image.open(icon_path_png)
            # Resize for window icon standard size if needed
            img_resized = img.resize((32, 32), Image.Resampling.LANCZOS)
            photo = ImageTk.PhotoImage(img_resized)
            root.wm_iconphoto(True, photo)
        except Exception as e:
            print(f"Error loading PNG icon: {e}")
    elif os.path.exists(icon_path_ico):
        try:
            root.iconbitmap(icon_path_ico)
        except Exception as e:
            print(f"Error loading ICO icon: {e}")
            
    # Instantiate Main Application Frame
    from ui.app import App
    app = App(root)
    
    root.mainloop()

if __name__ == "__main__":
    main()
