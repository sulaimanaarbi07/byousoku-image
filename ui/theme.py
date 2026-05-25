# ui/theme.py
import sys

# Platform specific font family
if sys.platform.startswith('win'):
    FONT_FAMILY = "Yu Gothic UI"
else:
    FONT_FAMILY = "Segoe UI"

# Colors: tuple format for CustomTkinter (Light, Dark)
COLOR_BG = ("#f5f5f7", "#121222")          # Core background
COLOR_SURFACE = ("#ffffff", "#1a1a2e")     # Card/Panel background
COLOR_SURFACE_ALT = ("#eaeaea", "#24243e") # Subtle alt background
COLOR_ACCENT = ("#007aff", "#e94560")      # Vibrant blue / hot pink highlight
COLOR_ACCENT_HOVER = ("#0056b3", "#d03e56")
COLOR_SUCCESS = ("#34c759", "#4caf50")
COLOR_TEXT_PRIMARY = ("#1c1c1e", "#ffffff")
COLOR_TEXT_SECONDARY = ("#8e8e93", "#a0a5c0")
COLOR_BORDER = ("#e5e5e7", "#2a2a40")

# Corner Radii
RADIUS_LARGE = 16
RADIUS_MEDIUM = 12
RADIUS_SMALL = 8

# Fonts
FONT_TITLE = (FONT_FAMILY, 22, "bold")
FONT_SUBTITLE = (FONT_FAMILY, 16, "bold")
FONT_HEADER = (FONT_FAMILY, 14, "bold")
FONT_BODY = (FONT_FAMILY, 12)
FONT_BODY_BOLD = (FONT_FAMILY, 12, "bold")
FONT_SMALL = (FONT_FAMILY, 10)
FONT_SMALL_BOLD = (FONT_FAMILY, 10, "bold")
