from arcadia_pycolor import colors, cvd, gradients, mpl, palettes, plot, style_defaults

from .colors import *
from .gradient import Gradient
from .hexcode import HexCode
from .palette import Palette

__all__ = [
    "cvd",
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
