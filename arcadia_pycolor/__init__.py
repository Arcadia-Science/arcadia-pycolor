from arcadia_pycolor import colors, gradients, mpl, palettes, plot, styles

from .colors import *
from .gradient import *
from .hexcode import *
from .palette import *

__all__ = [
    "gradients",
    "mpl",
    "palettes",
    "plot",
]

colors_all = [name for name in dir(colors) if not name.startswith("_")]

__all__.extend(colors_all)
