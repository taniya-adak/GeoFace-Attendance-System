"""
Custom UI styles for GeoFace Attendance System
"""

# ================ COLOR PALETTE ================
class Colors:
    PRIMARY = "#2563EB"  # Vibrant blue
    SECONDARY = "#7C3AED"  # Purple
    BACKGROUND = "#F9FAFB"  # Light gray
    CARD = "#FFFFFF"  # White
    TEXT = "#1F2937"  # Dark gray
    TEXT_LIGHT = "#6B7280"  # Gray
    SUCCESS = "#10B981"  # Green
    WARNING = "#F59E0B"  # Amber
    ERROR = "#EF4444"  # Red
    BORDER = "#E5E7EB"  # Light border

# ================ FONT SETTINGS ================
class Fonts:
    TITLE = ("Segoe UI", 20, "bold")
    HEADING = ("Segoe UI", 14, "bold")
    BODY = ("Segoe UI", 11)
    SMALL = ("Segoe UI", 9)
    MONOSPACE = ("Consolas", 10)

# ================ TTK THEME CONFIG ================
def configure_styles():
    """Apply custom styles to all ttk widgets"""
    import tkinter.ttk as ttk
    
    style = ttk.Style()
    
    # ----- General Theme Settings -----
    style.theme_create("geoface", parent="clam", settings={
        ".": {
            "configure": {
                "background": Colors.BACKGROUND,
                "foreground": Colors.TEXT,
                "font": Fonts.BODY,
                "borderwidth": 1,
                "relief": "flat"
            }
        },
        
        # ----- Button Styles -----
        "TButton": {
            "configure": {
                "padding": 8,
                "anchor": "center",
                "background": Colors.PRIMARY,
                "foreground": "white",
                "font": Fonts.BODY
            },
            "map": {
                "background": [("active", Colors.SECONDARY)],
                "foreground": [("active", "white")]
            }
        },
        
        # ----- Entry/Combobox -----
        "TEntry": {
            "configure": {
                "fieldbackground": "white",
                "borderwidth": 1,
                "relief": "solid"
            }
        },
        
        # ----- Frame Styles -----
        "TFrame": {
            "configure": {
                "background": Colors.BACKGROUND
            }
        },
        
        # ----- Label Styles -----
        "TLabel": {
            "configure": {
                "background": Colors.BACKGROUND,
                "foreground": Colors.TEXT
            }
        },
        
        # ----- Notebook (Tabs) -----
        "TNotebook.Tab": {
            "configure": {
                "padding": [12, 6],
                "background": Colors.BACKGROUND,
                "foreground": Colors.TEXT_LIGHT
            },
            "map": {
                "background": [("selected", Colors.PRIMARY)],
                "foreground": [("selected", "white")]
            }
        }
    })
    
    style.theme_use("geoface")

# ================ DARK MODE (Optional) ================
DARK_MODE = {
    "BACKGROUND": "#1E1E1E",
    "CARD": "#2D2D2D",
    "TEXT": "#E0E0E0",
    "PRIMARY": "#3B82F6",
    "BORDER": "#444444"
}