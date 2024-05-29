import os
import platform
from importlib import resources as impresources
from pathlib import Path

import matplotlib as mpl
import matplotlib.font_manager as font_manager
import matplotlib.pyplot as plt
import matplotlib.transforms as mtransforms
from matplotlib.legend import Legend
from matplotlib.lines import Line2D
from matplotlib.offsetbox import DrawingArea

import arcadia_pycolor.colors as colors
import arcadia_pycolor.gradients
import arcadia_pycolor.palettes
from arcadia_pycolor.gradient import Gradient
from arcadia_pycolor.palette import Palette

from . import mplstyles
from .styles import (
    FULL_S,
    FULL_W,
    HALF_S,
    SAVEFIG_PAD,
    THREEQ_S,
    THREEQ_W,
)

_DARWIN_FONT_FOLDER = "~/Library/Fonts"
_FONT_FILTER = "Suisse"
_MPL_STYLESHEET = impresources.files(mplstyles) / "arcadia_2024.mplstyle"
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
    "Set the font of the xtick labels to a monospace font."
    ax = _catch_axis(axis)

    xtick_labels = ax.get_xticklabels()
    [i.set_fontfamily(font) for i in xtick_labels]


def monospace_yticklabels(font: str = _MONOSPACE_FONT, axis=None):
    "Set the font of the ytick labels to a monospace font."
    ax = _catch_axis(axis)

    ytick_labels = ax.get_yticklabels()
    [i.set_fontfamily(font) for i in ytick_labels]


def capitalize_xticklabels(axis=None):
    "Capitalize the xtick labels."
    ax = _catch_axis(axis)

    xticklabels = [label.get_text().capitalize() for label in ax.get_xticklabels()]
    ax.set_xticklabels(xticklabels)


def capitalize_yticklabels(axis=None):
    "Capitalize the ytick labels."
    ax = _catch_axis(axis)

    yticklabels = [label.get_text().capitalize() for label in ax.get_yticklabels()]
    ax.set_yticklabels(yticklabels)


def capitalize_ticklabels(axis=None):
    "Capitalize both the x and y tick labels."
    ax = _catch_axis(axis)

    capitalize_yticklabels(ax)
    capitalize_xticklabels(ax)


def categorical_xaxis(axis=None):
    "Set the x-axis to a categorical axis, removing ticks and adjusting padding."
    ax = _catch_axis(axis)

    ax.tick_params(axis="x", which="both", pad=15, size=0)


def categorical_yaxis(axis=None):
    "Set the x-axis to a categorical axis, removing ticks and adjusting padding."
    ax = _catch_axis(axis)

    ax.tick_params(axis="y", which="both", pad=15, size=0)


def capitalize_ylabel(axis=None):
    "Capitalize the y-axis label."
    ax = _catch_axis(axis)

    ax.set_ylabel(ax.get_yaxis().get_label().get_text().capitalize())


def capitalize_xlabel(axis=None):
    "Capitalize the x-axis label."
    ax = _catch_axis(axis)

    ax.set_xlabel(ax.get_xaxis().get_label().get_text().capitalize())


def capitalize_axislabels(axis=None):
    "Capitalize both the x and y axis labels."
    ax = _catch_axis(axis)

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


def autostyle(axis=None, mono=None, cat=None):
    "Apply a set of style changes to the most recent figure."

    ax = _catch_axis(axis)
    capitalize_axislabels(ax)

    # Legend styling.
    leg = ax.get_legend()

    if leg is not None:
        capitalize_legend(leg)
        add_legend_line(leg)
        leg.set_title(leg.get_title()._text, prop=LEGEND_PARAMS["title_fontproperties"])
        leg.set(alignment="left")

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

    dispatch_mono = {
        "x": monospace_xticklabels,
        "y": monospace_yticklabels,
    }
    if mono == "both":
        for func in dispatch_mono.values():
            func()
    elif mono in dispatch_mono:
        dispatch_mono[mono]()
    elif mono is None:
        pass
    else:
        print(f"Invalid mono option. Please choose from {list(dispatch_mono.keys())}.")


def dimensions(size: str):
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


def _load_colors():
    colors = {color.name: color.hex_code for color in arcadia_pycolor.palettes.all.colors}
    mpl.cm.colors.get_named_colors_mapping().update(colors)


def _load_fonts(font_folder: str = None):
    if font_folder:
        font_dir = Path(font_folder)
    elif platform.system() == "Darwin":  # Darwin is the system name for macOS
        font_dir = Path(os.path.expanduser(_DARWIN_FONT_FOLDER))
    else:
        print("Unsupported system. Please specify the font folder manually.")
        raise NotImplementedError

    suisse_fonts = [i for i in os.listdir(font_dir) if _FONT_FILTER in i]

    if len(suisse_fonts) == 0:
        print(f"No {_FONT_FILTER} fonts found in {font_folder}.")
        print("Make sure you have fonts installed and try again.")
        raise FileNotFoundError

    for font in suisse_fonts:
        font_path = font_dir / font
        font_manager.fontManager.addfont(font_path)
        font_manager.FontProperties(fname=font_path)


def _load_gradients():
    for grad in dir(arcadia_pycolor.gradients):
        if isinstance(grad, Gradient):
            plt.register_cmap(name=grad.name, cmap=grad.to_mpl_linear_cmap())


def _load_palettes():
    for pal in dir(arcadia_pycolor.palettes):
        if isinstance(pal, Palette):
            plt.register_cmap(name=pal.name, cmap=pal.to_mpl_cmap())


def _load_styles(sheet: str = _MPL_STYLESHEET):
    plt.style.use(sheet)


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
