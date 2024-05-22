from typing import TYPE_CHECKING, Optional, Union

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
from colorspacious import cspace_converter

if TYPE_CHECKING:
    from arcadia_pycolor.classes import Gradient, HexCode

from arcadia_pycolor.mpl import to_linear_cmap


def swatch(color: "HexCode", width: int = 2, min_name_width: int = None):
    """
    Returns a color swatch with the specified width and color name.

    Args:
        color (HexCode): the HexCode object to display
        width (int): the width of the color swatch
        min_name_width (int): the desired width of the color name;
            pads the name with spaces if necessary.
            If not specified, text will not display in a fixed width.

    Based on colorir's swatch function:
    https://github.com/aleferna12/colorir/blob/master/colorir/utils.py#L59
    """
    # Add padding to the color name if necessary.
    # Used when displaying multiple colors in a palette.
    if min_name_width:
        color_name = color.name.ljust(min_name_width)
    else:
        color_name = color.name

    # Creates a block of color with the specified width in monospace characters.
    swatch_text = " " * width
    output = colorize(swatch_text, bg_color=color)

    output += colorize(f" {color_name} {color.hex_code}", fg_color=color)

    return output


def gradient_swatch(gradient: "Gradient", steps=21):
    from arcadia_pycolor.classes import HexCode

    """
    Returns a gradient swatch with the specified number of steps.

    Args:
        gradient (Gradient): the Gradient object to display
        steps (int): the number of swatches to display in the gradient

    """
    # Calculate the color for each step in the gradient
    cmap = to_linear_cmap(gradient)

    # Get the color for each step in the gradient
    colors = [HexCode(i, cmap(i / steps)) for i in range(steps)]

    swatches = [colorize(" ", bg_color=c) for c in colors]

    return "".join(swatches)


def plot_gradient_lightness(
    gradients: Union["Gradient", str, list[Union["Gradient", str]]],
    title: str = None,
    horizontal_spacing: float = 1.1,
    steps: int = 100,
    figsize: tuple[float, float] = (4, 4),
    cmap_type: str = "linear",
    tickrotation: float = 50,
    markersize: float = 300,
    return_fig: bool = False,
):
    """
    Displays color gradients as lines based on lightness, for looking at uniformity of lightness.

    Expects a dictionary, where each entry has the name of the color palette
        as its key and the value as:
        - the string name of the registered Matplotlib colormap OR
        - a Matplotlib ListedColormap object for the colormap

    Args:
        gradients (list of Gradient or str): list of gradients to plot.
            If `str` is provided, it is assumed to be a registered Matplotlib colormap.
        title (str): a title for the plot if desired
        horizontal_spacing (float): the spacing between lines
        steps (int): the number of steps along the gradient to generate
        figsize (tuple): the width, height tuple of the figure size
        cmap_type (str): 'linear' if you want the label for the cmap to be at the end;
            anything else puts the label in the middle.
        tickrotation (int): rotation of the label for each cmap
        markersize (int): the size of the points that make up the gradient color line
        return_fig (bool): whether or not to return the figure as an object
    """
    from arcadia_pycolor.classes import Gradient

    # Indices to step through colormap.
    x = np.linspace(0.0, 1.0, steps)

    locs = []  # Locations for text labels.

    fig, ax = plt.subplots(figsize=figsize, layout="constrained")
    grad_names = []

    if not isinstance(gradients, list):
        gradients = [gradients]

    for j, grad in enumerate(gradients):
        if isinstance(grad, str):
            name = grad
            try:
                cmap = mpl.cm.get_cmap(name)
            except ValueError:
                print(f"Colormap {name} not found in Matplotlib colormaps.")
                continue
        elif isinstance(grad, Gradient):
            name = grad.name
            cmap = to_linear_cmap(grad)

        grad_names.append(name)

        # Get RGB values for colormap and convert the colormap in
        # CAM02-UCS colorspace.  lab[0, :, 0] is the lightness.
        if name in mpl.colormaps:
            rgb = mpl.colormaps[name](x)[np.newaxis, :, :3]
        else:
            rgb = cmap(x)[np.newaxis, :, :3]
        lab = cspace_converter("sRGB1", "CAM02-UCS")(rgb)

        # Plot colormap L values.  Do separately for each category
        # so each plot can be pretty.  To make scatter markers change
        # color along plot:
        # https://stackoverflow.com/q/8202605/

        y_ = lab[0, :, 0]
        c_ = x

        dc = horizontal_spacing  # cmaps horizontal spacing
        ax.scatter(x + j * dc, y_, c=c_, cmap=cmap, s=markersize, linewidths=0.0)

        if cmap_type == "linear":
            # Store locations for colormap labels
            locs.append(x[-1] + j * dc)
        else:
            locs.append(x[int(np.round(steps / 2))] + j * dc)

    # Lightness goes from 0 to 100.
    ax.set_ylim(0.0, 100.0)

    # Set up labels for colormaps
    ax.xaxis.set_ticks_position("top")
    ticker = mpl.ticker.FixedLocator(locs)
    ax.xaxis.set_major_locator(ticker)
    ax.xaxis.set_tick_params(rotation=tickrotation)
    ax.set_xticklabels(labels=grad_names)
    ax.set_ylabel("Lightness $L^*$", fontsize=12)

    if title is not None:
        ax.set_xlabel(title, fontsize=14)

    if return_fig:
        return fig

    plt.show()


def colorize(
    string: str,
    fg_color: Optional["HexCode"] = None,
    bg_color: Optional["HexCode"] = None,
):
    """
    Colorizes a string with the specified foreground and background colors.

    Args:
        string (str): the string to colorize
        fg_color (HexCode): the foreground color
        bg_color (HexCode): the background color

    Based on colorir's color_str function:
    https://github.com/aleferna12/colorir/blob/master/colorir/utils.py#L370

    Relies on ANSI escape codes for colorization.
    See https://gist.github.com/fnky/458719343aabd01cfb17a3a4f7296797
    """
    if fg_color:
        rgb = fg_color.to_rgb()
        string = f"\033[38;2;{rgb[0]};{rgb[1]};{rgb[2]}m" + string + "\33[0m"

    if bg_color:
        bg_rgb = bg_color.to_rgb()
        string = f"\033[48;2;{bg_rgb[0]};{bg_rgb[1]};{bg_rgb[2]}m" + string + "\33[0m"

    return string
