# src/main.py

import customtkinter as ctk
from ui.components import ReportBuilderUI

if __name__ == "__main__":
    ctk.set_appearance_mode("light")  # or "dark"
    ctk.set_default_color_theme("blue")

    app = ReportBuilderUI()
    app.mainloop()
