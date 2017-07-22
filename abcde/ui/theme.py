import tkinter.font as tk_font

class Theme():
    def __init__(self, theme = 'TedPy'):
        # The 'TedPy' theme:
        self.bg = '#222222'     # Background color
        self.fg = 'white'       # Foreground color
        self.insertbg = 'white' # Insertion cursor color
        self.selectbg = '#630'  # Select background color

        self.font_family = "courier new"
        self.font_size = 12

    def get_font(self):
        return tk_font.Font(family=self.font_family, size=self.font_size)
