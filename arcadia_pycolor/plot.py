from typing import Union

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
from colorspacious import cspace_converter  # type: ignore

from arcadia_pycolor.gradient import Gradient
from arcadia_pycolor.gradients import all_gradients
from arcadia_pycolor.palettes import all_palettes


def plot_gradient_lightness(
    gradients: Union["Gradient", str, list["Gradient"], list[str]],
    title: Union[str, None] = None,
    horizontal_spacing: float = 1.1,
    steps: int = 100,
    figsize: tuple[float, float] = (4, 4),
    cmap_type: str = "linear",
    tickrotation: float = 50,
    markersize: float = 300,
    return_fig: bool = False,
):
    """
    Plots the lightness of one or more color gradients
        to assess the uniformity of their lightnesses.

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

    # Indices to step through colormap.
    x = np.linspace(0.0, 1.0, steps)

    locs = []  # Locations for text labels.

    fig, ax = plt.subplots(figsize=figsize, layout="constrained")
    gradient_names = []

    # Check separately for single strings and single Gradient objects in order to avoid type errors.
    if isinstance(gradients, str):
        gradients = [gradients]
    elif isinstance(gradients, Gradient):
        gradients = [gradients]

    for ind, gradient in enumerate(gradients):
        if isinstance(gradient, str):
            name = gradient
            if name not in mpl.colormaps:  # type: ignore
                print(f"Colormap {name} not found in Matplotlib colormaps.")
                continue
            cmap = mpl.cm.get_cmap(name)  # type: ignore
            colormap_as_rgb = mpl.colormaps[name](x)[np.newaxis, :, :3]  # type: ignore
        elif isinstance(gradient, Gradient):  # type: ignore
            name = gradient.name
            cmap = gradient.to_mpl_cmap()
            colormap_as_rgb = cmap(x)[np.newaxis, :, :3]
        else:
            raise TypeError("gradients must be a list of Gradient objects or strings.")

        gradient_names.append(name)

        # Get RGB values for colormap and convert the colormap in
        # CAM02-UCS colorspace.  lab[0, :, 0] is the lightness.
        colormap_as_lab = cspace_converter("sRGB1", "CAM02-UCS")(colormap_as_rgb)

        # Plot colormap L values.  Do separately for each category
        # so each plot can be pretty.  To make scatter markers change
        # color along plot:
        # https://stackoverflow.com/q/8202605/

        y_ = colormap_as_lab[0, :, 0]
        c_ = x

        x_offset = ind * horizontal_spacing
        ax.scatter(x + x_offset, y_, c=c_, cmap=cmap, s=markersize, linewidths=0.0)

        if cmap_type == "linear":
            # Store locations for colormap labels.
            locs.append(x[-1] + x_offset)
        else:
            locs.append(x[int(np.round(steps / 2))] + x_offset)

    # Lightness goes from 0 to 100.
    ax.set_ylim(0.0, 100.0)

    # Set up labels for colormaps
    ax.xaxis.set_ticks_position("top")
    ticker = mpl.ticker.FixedLocator(locs)  # type: ignore
    ax.xaxis.set_major_locator(ticker)
    ax.xaxis.set_tick_params(rotation=tickrotation)
    ax.set_xticklabels(labels=gradient_names)
    ax.set_ylabel("Lightness $L^*$", fontsize=12)

    if title is not None:
        ax.set_xlabel(title, fontsize=14)

    if return_fig:
        return fig

    plt.show()


def display_all_gradients():
    for gradient in all_gradients:
        print(gradient.name)
        print(gradient.swatch())


def display_all_palettes():
    for palette in all_palettes:
        print(palette.name)
        print(palette.swatch())
