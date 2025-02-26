from typing import Union, cast

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
from colorspacious import cspace_converter  # type: ignore
from matplotlib.figure import Figure
from numpy.typing import NDArray

from arcadia_pycolor.gradient import Gradient
from arcadia_pycolor.gradients import all_gradients
from arcadia_pycolor.palettes import all_palettes


def plot_gradient_lightness(
    gradients: Union[Gradient, str, list[Gradient], list[str]],
    title: Union[str, None] = None,
    horizontal_spacing: float = 1.1,
    steps: int = 100,
    figsize: tuple[float, float] = (4, 4),
    cmap_type: str = "linear",
    tickrotation: float = 50,
    markersize: float = 300,
    return_fig: bool = False,
) -> Union[None, Figure]:
    """Plots the lightness of one or more color gradients to assess their uniformity.

    Args:
        gradients (list[Gradient] or list[str]):
            The list of gradients to plot, where each element is either a `Gradient` object
            or a string. If a string is provided, it is assumed to be a registered Matplotlib
            colormap.
        title (str):
            A title for the plot if desired.
        horizontal_spacing (float):
            The spacing between lines.
        steps (int):
            The number of steps along the gradient to generate.
        figsize (tuple):
            The width, height tuple of the figure size.
        cmap_type (str):
            'linear' if you want the label for the `cmap` to be at the end;
            anything else puts the label in the middle.
        tickrotation (int):
            The rotation of the label for each `cmap`.
        markersize (int):
            The size of the points that make up the gradient color line.
        return_fig (bool):
            Whether or not to return the figure as an object.

    Returns:
        Union[None, matplotlib.figure.Figure]:
            None if `return_fig` is False, otherwise a `matplotlib.figure.Figure` object.

    Raises:
        TypeError:
            If `gradients` is not a list of `Gradient` objects or strings.
    """

    fig, ax = plt.subplots(figsize=figsize, layout="constrained")  # type: ignore

    # Indices to step through colormap.
    x = np.linspace(0.0, 1.0, steps)

    xaxis_tick_labels: list[str] = []
    xaxis_tick_locations: list[float] = []

    # Check separately for single strings and single Gradient objects in order to avoid type errors.
    if isinstance(gradients, str):
        gradients = [gradients]
    elif isinstance(gradients, Gradient):
        gradients = [gradients]

    for ind, gradient in enumerate(gradients):
        if isinstance(gradient, str):
            gradient_name = gradient
            if gradient_name not in mpl.colormaps:  # type: ignore
                print(f"Colormap {gradient_name} not found in Matplotlib colormaps.")
                continue
            cmap = mpl.colormaps[gradient_name]
        elif isinstance(gradient, Gradient):
            gradient_name = gradient.name
            cmap = gradient.to_mpl_cmap()
        else:
            raise TypeError("gradients must be a list of Gradient objects or strings.")

        xaxis_tick_labels.append(gradient_name)
        cmap_as_rgb = cast(NDArray[np.float64], cmap(x)[np.newaxis, :, :3])
        cmap_as_lab = cast(NDArray[np.float64], cspace_converter("sRGB1", "CAM02-UCS")(cmap_as_rgb))

        # Plot colormap lightness values. Do this separately for each category
        # so each plot can be pretty.
        # Note: `lab[0, :, 0]` is the lightness.
        y_ = cmap_as_lab[0, :, 0]
        c_ = x

        x_offset = ind * horizontal_spacing

        # To make scatter markers change color along plot: https://stackoverflow.com/q/8202605/.
        ax.scatter(x + x_offset, y_, c=c_, cmap=cmap, s=markersize, linewidths=0.0)

        # Store locations for colormap labels.
        if cmap_type == "linear":
            xaxis_tick_locations.append(x[-1] + x_offset)
        else:
            xaxis_tick_locations.append(x[int(np.round(steps / 2))] + x_offset)

    # Lightness goes from 0 to 100.
    ax.set_ylim(0.0, 100.0)

    # Set up labels for colormaps.
    ax.xaxis.set_ticks_position("top")
    xaxis_tick_locator = mpl.ticker.FixedLocator(xaxis_tick_locations)  # type: ignore
    ax.xaxis.set_major_locator(xaxis_tick_locator)
    ax.xaxis.set_tick_params(rotation=tickrotation)
    ax.set_xticklabels(labels=xaxis_tick_labels)
    ax.set_ylabel("Lightness $L^*$", fontsize=12)

    if title is not None:
        ax.set_xlabel(title, fontsize=14)

    plt.show()  # type: ignore

    if return_fig:
        return fig


def display_all_gradients() -> None:
    """Displays all registered gradients."""
    for gradient in all_gradients:
        print(gradient.name)
        print(gradient.swatch())


def display_all_palettes() -> None:
    """Displays all registered palettes."""
    for palette in all_palettes:
        print(palette.name)
        print(palette.swatch())
