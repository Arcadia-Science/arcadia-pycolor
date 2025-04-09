from arcadia_pycolor import colors, cvd, gradients, mpl, palettes, plot, style_defaults
from arcadia_pycolor import plotly_utils as plotly

from .colors import *
from .gradient import Gradient
from .hexcode import HexCode
from .palette import Palette

# This is a placeholder that will be replaced by the version number at build time.
__version__ = "0.0.0"

__all__ = [
    "cvd",
    "Gradient",
    "gradients",
    "HexCode",
    "mpl",
    "Palette",
    "palettes",
    "plot",
    "plotly",
    "style_defaults",
]

colors_all = [name for name in dir(colors) if isinstance(getattr(colors, name), HexCode)]

__all__.extend(colors_all)  # type: ignore
