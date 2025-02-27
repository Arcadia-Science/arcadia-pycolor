from arcadia_pycolor import colors, cvd, gradients, mpl, palettes, plot, style_defaults

from .colors import *
from .display_plotly import display_all_colors
from .gradient import Gradient
from .hexcode import HexCode
from .palette import Palette

# This is a placeholder that will be replaced by the version number at build time.
__version__ = "0.0.0"

__all__ = [
    "cvd",
    "display_all_colors",
    "Gradient",
    "gradients",
    "HexCode",
    "mpl",
    "Palette",
    "palettes",
    "plot",
    "style_defaults",
]

colors_all = [name for name in dir(colors) if isinstance(getattr(colors, name), HexCode)]

__all__.extend(colors_all)  # type: ignore

# Update the reference to colors_all in display_plotly
from . import display_plotly

display_plotly.colors_all = colors_all
