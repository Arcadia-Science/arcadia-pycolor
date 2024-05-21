import matplotlib.colors as mcolors

from arcadia_pycolor.classes import Gradient, Palette


def to_cmap(palette: Palette):
    return mcolors.ListedColormap([color.hex_code for color in palette.colors], palette.name)


def to_linear_cmap(grad: Gradient):
    colors = [(value, color.hex_code) for value, color in zip(grad.values, grad.colors)]
    return mcolors.LinearSegmentedColormap.from_list(
        grad.name,
        colors=colors,
    )
