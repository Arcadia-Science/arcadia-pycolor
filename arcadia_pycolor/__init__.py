from arcadia_pycolor import classes, colors, gradients, mpl, palettes, plot

from .classes import *
from .colors import *

__all__ = [
    "gradients",
    "mpl",
    "palettes",
    "plot",
]

classes_all = [name for name in dir(classes) if not name.startswith("_")]
colors_all = [name for name in dir(colors) if not name.startswith("_")]

__all__.extend(classes_all)
__all__.extend(colors_all)
