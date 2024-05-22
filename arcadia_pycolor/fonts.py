import os

_MONOSPACE_FONT = "Suisse Int'l Mono"

_FONT_FOLDER = "~/Library/Fonts"
_EXPANDED_FONT_FOLDER = os.path.expanduser(_FONT_FOLDER)

_SUISSE_FONTS = [i for i in os.listdir(_EXPANDED_FONT_FOLDER) if "Suisse" in i]
