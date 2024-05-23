from typing import TYPE_CHECKING

import matplotlib.colors as mcolors
import matplotlib.pyplot as plt
import matplotlib.transforms as mtransforms
from matplotlib.legend import Legend
from matplotlib.lines import Line2D
from matplotlib.offsetbox import DrawingArea

if TYPE_CHECKING:
    from arcadia_pycolor.classes import Gradient, Palette


import arcadia_pycolor.colors as colors

from .styles import (
    FULL_S,
    FULL_W,
    HALF_S,
    SAVEFIG_PAD,
    THREEQ_S,
    THREEQ_W,
)

_MONOSPACE_FONT = "Suisse Int'l Mono"
LEGEND_PARAMS = dict(
    alignment="left",
    title_fontproperties={"weight": "semibold", "size": "26"},
)

SAVE_WEB = dict(dpi=72, bbox_inches="tight", pad_inches=0.41)
SAVE_PRINT = dict(dpi=300, bbox_inches="tight", pad_inches=0.41)


def _catch_axis(axis=None):
    "Convenience function to catch the current axis if none is provided."
    if axis is None:
        return plt.gca()
    else:
        return axis


def monospace_xticklabels(font: str = _MONOSPACE_FONT, axis=None):
    ax = _catch_axis(axis)

    xtick_labels = ax.get_xticklabels()
    [i.set_fontfamily(font) for i in xtick_labels]


def monospace_yticklabels(font: str = _MONOSPACE_FONT, axis=None):
    ax = _catch_axis(axis)

    ytick_labels = ax.get_yticklabels()
    [i.set_fontfamily(font) for i in ytick_labels]


def capitalize_xticklabels(axis=None):
    ax = _catch_axis(axis)

    xticklabels = [label.get_text().capitalize() for label in ax.get_xticklabels()]
    ax.set_xticklabels(xticklabels)


def capitalize_yticklabels(axis=None):
    ax = _catch_axis(axis)

    yticklabels = [label.get_text().capitalize() for label in ax.get_yticklabels()]
    ax.set_yticklabels(yticklabels)


def capitalize_ticklabels(axis=None):
    ax = _catch_axis(axis)

    capitalize_yticklabels(ax)
    capitalize_xticklabels(ax)


def categorical_xaxis(axis=None):
    ax = _catch_axis(axis)

    ax.tick_params(axis="x", which="both", pad=15, size=0)


def categorical_yaxis(axis=None):
    ax = _catch_axis(axis)

    ax.tick_params(axis="y", which="both", pad=15, size=0)


def capitalize_ylabel(axis=None):
    ax = _catch_axis(axis)

    ax.set_ylabel(ax.get_yaxis().get_label().get_text().capitalize())


def capitalize_xlabel(axis=None):
    ax = _catch_axis(axis)

    ax.set_xlabel(ax.get_xaxis().get_label().get_text().capitalize())


def capitalize_axislabels(axis=None):
    ax = _catch_axis(axis)

    capitalize_xlabel(ax)
    capitalize_ylabel(ax)


def capitalize_legend_title(legend: Legend):
    legend.set_title(legend.get_title().get_text().capitalize())


def capitalize_legend_entries(legend: Legend):
    for text in legend.get_texts():
        text.set_text(text.get_text().capitalize())


def capitalize_legend(legend: Legend):
    capitalize_legend_title(legend)
    capitalize_legend_entries(legend)


def dimensions(size: str):
    dispatch_dict = {
        "full_w": FULL_W,
        "full_s": FULL_S,
        "threeq_w": THREEQ_W,
        "threeq_s": THREEQ_S,
        "half_s": HALF_S,
    }

    if size not in dispatch_dict:
        raise ValueError(f"Size must be one of {list(dispatch_dict.keys())}.")

    return tuple(x - 2 * SAVEFIG_PAD for x in dispatch_dict[size])


def add_legend_line(legend: Legend):
    # Written with assistance from ChatGPT-4
    # Determine the width of the legend in pixels

    x0 = legend._legend_handle_box.get_window_extent()._points[0][0]
    x1 = legend._legend_handle_box.get_window_extent()._points[1][0]
    bbox_length = abs(x1 - x0)

    # Create a horizontal line
    line = Line2D(
        [0, bbox_length],
        [0],
        color=colors.chateau,
        linewidth=2,
        linestyle="-",
        transform=mtransforms.IdentityTransform(),
    )
    line_area = DrawingArea(
        width=bbox_length, height=0, xdescent=0, ydescent=0
    )  # width and height in pixels
    line_area.add_artist(line)

    # Modify the transform of the line to match the DrawingArea's internal coordinate system
    line.set_transform(line_area.get_transform())

    # Insert the line as a new row just below the title
    legend_vpacker = legend._legend_handle_box.get_children()[0]
    legend_vpacker.get_children().insert(0, line_area)


def to_cmap(palette: "Palette"):
    return mcolors.ListedColormap([color.hex_code for color in palette.colors], palette.name)


def to_linear_cmap(gradient: "Gradient"):
    colors = [(value, color.hex_code) for value, color in zip(gradient.values, gradient.colors)]
    return mcolors.LinearSegmentedColormap.from_list(
        gradient.name,
        colors=colors,
    )
