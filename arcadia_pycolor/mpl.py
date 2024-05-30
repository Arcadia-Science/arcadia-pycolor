import matplotlib as mpl
import matplotlib.font_manager as font_manager
import matplotlib.pyplot as plt
import matplotlib.transforms as mtransforms
from matplotlib import colormaps
from matplotlib.legend import Legend
from matplotlib.lines import Line2D
from matplotlib.offsetbox import DrawingArea

import arcadia_pycolor.colors as colors
import arcadia_pycolor.gradients
import arcadia_pycolor.palettes
from arcadia_pycolor.gradient import Gradient
from arcadia_pycolor.palette import Palette
from arcadia_pycolor.style_defaults import ARCADIA_RC_PARAMS, FONT_FILTER, MONOSPACE_FONT

from .styles import (
    FULL_S,
    FULL_W,
    HALF_S,
    SAVEFIG_PAD,
    THREEQ_S,
    THREEQ_W,
)

LEGEND_PARAMS = dict(
    alignment="left",
    title_fontproperties={"weight": "semibold", "size": "26"},
)

SAVE_WEB = dict(dpi=72, bbox_inches="tight", pad_inches=0.41)
SAVE_PRINT = dict(dpi=300, bbox_inches="tight", pad_inches=0.41)


def _find_axis(axis=None):
    "Convenience function to catch the current axis if none is provided."
    if axis is None:
        return plt.gca()
    else:
        return axis


def monospace_xticklabels(font: str = MONOSPACE_FONT, axis=None):
    "Set the font of the xtick labels to a monospace font."
    ax = _find_axis(axis)

    xtick_labels = ax.get_xticklabels()
    [label.set_fontfamily(font) for label in xtick_labels]


def monospace_yticklabels(font: str = MONOSPACE_FONT, axis=None):
    "Set the font of the ytick labels to a monospace font."
    ax = _find_axis(axis)

    ytick_labels = ax.get_yticklabels()
    [label.set_fontfamily(font) for label in ytick_labels]


def monospace_ticklabels(font: str = MONOSPACE_FONT, axis=None):
    "Set the font of both the x and y tick labels to a monospace font."
    ax = _find_axis(axis)

    monospace_xticklabels(font, ax)
    monospace_yticklabels(font, ax)


def capitalize_xticklabels(axis=None):
    "Capitalize the xtick labels."
    ax = _find_axis(axis)

    xticklabels = [label.get_text().capitalize() for label in ax.get_xticklabels()]
    ax.set_xticklabels(xticklabels)


def capitalize_yticklabels(axis=None):
    "Capitalize the ytick labels."
    ax = _find_axis(axis)

    yticklabels = [label.get_text().capitalize() for label in ax.get_yticklabels()]
    ax.set_yticklabels(yticklabels)


def capitalize_ticklabels(axis=None):
    "Capitalize both the x and y tick labels."
    ax = _find_axis(axis)

    capitalize_yticklabels(ax)
    capitalize_xticklabels(ax)


def categorical_xaxis(axis=None):
    "Set the style of the x-axis to a categorical axis, removing ticks and adjusting padding."
    ax = _find_axis(axis)

    ax.tick_params(axis="x", which="both", pad=15, size=0)


def categorical_yaxis(axis=None):
    "Set the style of the x-axis to a categorical axis, removing ticks and adjusting padding."
    ax = _find_axis(axis)

    ax.tick_params(axis="y", which="both", pad=15, size=0)


def categorical_axes(axis=None):
    "Set the style of both the x and y axes to categorical axes."
    ax = _find_axis(axis)

    categorical_xaxis(ax)
    categorical_yaxis(ax)


def capitalize_ylabel(axis=None):
    "Capitalize the y-axis label."
    ax = _find_axis(axis)

    ax.set_ylabel(ax.get_yaxis().get_label().get_text().capitalize())


def capitalize_xlabel(axis=None):
    "Capitalize the x-axis label."
    ax = _find_axis(axis)

    ax.set_xlabel(ax.get_xaxis().get_label().get_text().capitalize())


def capitalize_axislabels(axis=None):
    "Capitalize both the x and y axis labels."
    ax = _find_axis(axis)

    capitalize_xlabel(ax)
    capitalize_ylabel(ax)


def capitalize_legend_title(legend: Legend):
    "Capitalize the legend title."
    legend.set_title(legend.get_title().get_text().capitalize())


def capitalize_legend_entries(legend: Legend):
    "Capitalize the legend entries."
    for text in legend.get_texts():
        text.set_text(text.get_text().capitalize())


def capitalize_legend(legend: Legend):
    "Capitalize the legend title and entries."
    capitalize_legend_title(legend)
    capitalize_legend_entries(legend)


def justify_legend(legend: Legend):
    legend.set_title(legend.get_title()._text, prop=LEGEND_PARAMS["title_fontproperties"])
    legend.set(alignment="left")


def style_legend(legend: Legend):
    "Apply a set of style changes to a legend."
    capitalize_legend(legend)
    add_legend_line(legend)
    justify_legend(legend)


def monospace_colorbar(axis=None):
    ax = _find_axis(axis)
    if cbar := ax.collections[0].colorbar:
        monospace_ticklabels(axis=cbar.ax)


def autostyle(axis=None, mono=None, cat=None, cbar=False):
    "Apply a set of style changes to the most recent figure."

    ax = _find_axis(axis)
    capitalize_axislabels(ax)

    # Legend styling.
    leg = ax.get_legend()

    if leg is not None:
        style_legend(leg)

    dispatch_cat = {
        "x": [categorical_xaxis, capitalize_xticklabels],
        "y": [categorical_yaxis, capitalize_yticklabels],
    }
    if cat == "both":
        for func in dispatch_cat.values():
            for f in func:
                f()
    elif cat in dispatch_cat:
        for f in dispatch_cat[cat]:
            f()
    elif cat is None:
        pass
    else:
        print(f"Invalid cat option. Please choose from {list(dispatch_cat.keys())}.")

    if mono == "both":
        monospace_ticklabels(axis)
    elif mono == "x":
        monospace_xticklabels(axis)
    elif mono == "y":
        monospace_yticklabels(axis)
    else:
        print("Invalid mono option. Please choose from 'x', 'y', or 'both'.")

    if cbar:
        monospace_colorbar(ax)


def get_figure_dimensions(size: str):
    "Return the dimensions of a figure given a size."
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
    "Add a horizontal line with 'chateau' color below the legend title."
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

    # TODO: Don't make the line if there's already a line in the second position.


def _load_colors():
    colors = {"apc:" + color.name: color.hex_code for color in arcadia_pycolor.palettes.all.colors}
    mpl.cm.colors.get_named_colors_mapping().update(colors)


def _load_fonts(font_folder: str = None):
    for fontpath in font_manager.findSystemFonts(fontpaths=font_folder, fontext="ttf"):
        if FONT_FILTER.lower() in fontpath.lower():
            font_manager.fontManager.addfont(fontpath)
            font_manager.FontProperties(fname=fontpath)


def _load_gradients():
    for object in arcadia_pycolor.gradients.__dict__.values():
        if isinstance(object, Gradient):
            if (gradient_name := f"apc:{object.name}") not in colormaps:
                plt.register_cmap(name=gradient_name, cmap=object.to_mpl_linear_cmap())


def _load_palettes():
    for object in arcadia_pycolor.palettes.__dict__.values():
        if isinstance(object, Palette):
            if (palette_name := f"apc:{object.name}") not in colormaps:
                plt.register_cmap(name=palette_name, cmap=object.to_mpl_cmap())


def _load_styles():
    plt.rcParams.update(ARCADIA_RC_PARAMS)


def setup(mode: str = "all", font_folder: str = None):
    dispatch = {
        "colors": _load_colors,
        "fonts": lambda: _load_fonts(font_folder),
        "gradients": _load_gradients,
        "palettes": _load_palettes,
        "styles": _load_styles,
    }

    if mode == "all":
        for func in dispatch.values():
            func()
    elif mode in dispatch:
        dispatch[mode]()
    else:
        print(f"""Invalid mode. Please choose from "all", {list(dispatch.keys())}.""")
