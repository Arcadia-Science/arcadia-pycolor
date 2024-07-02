from arcadia_pycolor import colors, cvd, gradients, mpl, palettes, plot, style_defaults

from .colors import *
from .gradient import *
from .hexcode import *
from .palette import *

__all__ = [
    "cvd",
    "gradients",
    "mpl",
    "palettes",
    "plot",
    "style_defaults",
]

colors_all = [name for name in dir(colors) if not name.startswith("_")]

__all__.extend(colors_all)  # type: ignore
