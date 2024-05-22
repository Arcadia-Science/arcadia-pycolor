from typing import TYPE_CHECKING

import matplotlib.colors as mcolors

if TYPE_CHECKING:
    from arcadia_pycolor.classes import Gradient, Palette


def to_cmap(palette: "Palette"):
    return mcolors.ListedColormap([color.hex_code for color in palette.colors], palette.name)


def to_linear_cmap(gradient: "Gradient"):
    colors = [(value, color.hex_code) for value, color in zip(gradient.values, gradient.colors)]
    return mcolors.LinearSegmentedColormap.from_list(
        gradient.name,
        colors=colors,
    )
