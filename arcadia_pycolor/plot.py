from typing import Union

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
from colorspacious import cspace_converter

from arcadia_pycolor.gradient import Gradient


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
    grad_names = []

    if not isinstance(gradients, list):
        gradients = [gradients]

    for j, grad in enumerate(gradients):
        if isinstance(grad, str):
            name = grad
            if name not in mpl.colormaps:
                print(f"Colormap {name} not found in Matplotlib colormaps.")
                continue
            cmap = mpl.cm.get_cmap(name)
            colormap_as_rgb = mpl.colormaps[name](x)[np.newaxis, :, :3]
        elif isinstance(grad, Gradient):
            name = grad.name
            cmap = grad.to_mpl_cmap()
            colormap_as_rgb = cmap(x)[np.newaxis, :, :3]

        grad_names.append(name)

        # Get RGB values for colormap and convert the colormap in
        # CAM02-UCS colorspace.  lab[0, :, 0] is the lightness.
        colormap_as_lab = cspace_converter("sRGB1", "CAM02-UCS")(colormap_as_rgb)

        # Plot colormap L values.  Do separately for each category
        # so each plot can be pretty.  To make scatter markers change
        # color along plot:
        # https://stackoverflow.com/q/8202605/

        y_ = colormap_as_lab[0, :, 0]
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
