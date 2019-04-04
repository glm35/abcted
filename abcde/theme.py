import tkinter.font as tk_font

class Theme():
    def __init__(self, theme = 'desert'):
        # The 'desert' theme:
        # (https://www.vim.org/scripts/script.php?script_id=105)

        # Edit zone foreground and background
        self.bg = '#333333'  # Background color (~ black)
        self.fg = '#ffffff'  # Foreground color (white)

        # Insertion cursor color
        self.insertfg = '#708090'  # ~ grey (used for text under solid cursor)
        self.insertbg = '#f0e68c'  # ~ yellow

        # Cursor line
        self.cursorlinebg = '#666666'  # ~ grey

        # Selection foreground and background
        self.selectfg = '#f0e68c'  # ~ yellow
        self.selectbg = '#6b8e23'  # ~ olive green

        # Search result foreground and background
        self.hlsearchfg = '#f5deb3'  # ~ light orange
        self.hlsearchbg = '#cd853f'  # ~ darker orange

        self.font_family = "courier new"
        self.font_size = 12

    def get_font(self):
        return tk_font.Font(family=self.font_family, size=self.font_size)
