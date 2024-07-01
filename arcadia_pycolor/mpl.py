import logging
from typing import Any, Literal, Union, cast

import matplotlib as mpl
import matplotlib.font_manager as font_manager
import matplotlib.pyplot as plt
from matplotlib import colormaps as mpl_colormaps
from matplotlib.axis import XAxis, YAxis
from matplotlib.legend import Legend
from matplotlib.lines import Line2D
from matplotlib.offsetbox import DrawingArea
from matplotlib.pyplot import Axes  # type: ignore

import arcadia_pycolor.colors as colors
import arcadia_pycolor.gradients
import arcadia_pycolor.palettes
from arcadia_pycolor.gradient import Gradient
from arcadia_pycolor.palette import ColorSequence
from arcadia_pycolor.style_defaults import (
    ARCADIA_RC_PARAMS,
    BASE_DPI,
    CATEGORICAL_AXIS_TICKLENGTH,
    CATEGORICAL_AXIS_TICKPADDING,
    DEFAULT_FONT,
    FIGURE_PADDING_INCHES,
    FIGURE_SIZES,
    FONT_FILTER,
    LEGEND_SEPARATOR_LINEWIDTH,
    MONOSPACE_FONT,
    MONOSPACE_FONT_SIZE,
    PRINT_DPI,
)

# Disable matplotlib's very noisy warnings when the Arcadia fonts are not installed.
logging.getLogger("matplotlib.font_manager").setLevel(logging.ERROR)

LEGEND_PARAMS = dict(
    alignment="left",
    title_fontproperties={"weight": "semibold", "size": ARCADIA_RC_PARAMS["legend.title_fontsize"]},
)

SAVEFIG_KWARGS_WEB = dict(dpi=BASE_DPI, bbox_inches="tight", pad_inches=FIGURE_PADDING_INCHES)
SAVEFIG_KWARGS_PRINT = dict(dpi=PRINT_DPI, bbox_inches="tight", pad_inches=FIGURE_PADDING_INCHES)


def _find_axis(axis: Union[Axes, None] = None) -> Axes:
    "Convenience function to catch the current axis if none is provided."
    if axis is None:
        return plt.gca()
    else:
        return axis


def _arcadia_fonts_found() -> bool:
    "Check if the Arcadia fonts are available to matplotlib."
    arcadia_fonts = [
        font_name
        for font_name in font_manager.fontManager.get_font_names()
        if FONT_FILTER in font_name
    ]
    # TODO(KC): can we specify the number of fonts that should be found?
    return len(arcadia_fonts) > 0


def save_figure(fname: str, context: str = "web", **savefig_kwargs: dict[Any, Any]) -> None:
    "Save the current figure with the default settings for web."
    kwargs = SAVEFIG_KWARGS_WEB if context == "web" else SAVEFIG_KWARGS_PRINT
    kwargs.update(**savefig_kwargs)  # type: ignore
    plt.savefig(fname=fname, **kwargs)  # type: ignore


def set_yticklabel_font(
    axis: Union[Axes, None] = None, font: str = DEFAULT_FONT, font_size: Union[float, None] = None
) -> None:
    "Set the font of the x and y tick labels."
    ax = _find_axis(axis)

    ytick_labels = ax.get_yticklabels()  # type: ignore
    for label in ytick_labels:
        label.set_fontfamily(font)
    if font_size is not None:
        ax.yaxis.set_tick_params(labelsize=font_size)


def set_xticklabel_font(
    axis: Union[Axes, None] = None, font: str = DEFAULT_FONT, font_size: Union[float, None] = None
) -> None:
    "Set the font of the x and y tick labels."
    ax = _find_axis(axis)

    xtick_labels = ax.get_xticklabels()  # type: ignore
    for label in xtick_labels:
        label.set_fontfamily(font)
    if font_size is not None:
        ax.xaxis.set_tick_params(labelsize=font_size)


def set_ticklabel_font(
    axis: Union[Axes, None] = None, font: str = DEFAULT_FONT, font_size: Union[float, None] = None
) -> None:
    "Set the font of the x and y tick labels."
    ax = _find_axis(axis)

    set_xticklabel_font(ax, font, font_size)
    set_yticklabel_font(ax, font, font_size)


def set_xticklabel_monospaced(axis: Union[Axes, None] = None):
    "Set the font of the xtick labels to a monospace font."
    ax = _find_axis(axis)

    set_xticklabel_font(ax, MONOSPACE_FONT, MONOSPACE_FONT_SIZE)


def set_yticklabel_monospaced(axis: Union[Axes, None] = None):
    "Set the font of the ytick labels to a monospace font."
    ax = _find_axis(axis)

    set_yticklabel_font(ax, MONOSPACE_FONT, MONOSPACE_FONT_SIZE)


def set_ticklabel_monospaced(axis: Union[Axes, None] = None):
    "Set the font of both the x and y tick labels to a monospace font."
    ax = _find_axis(axis)

    set_xticklabel_monospaced(ax)
    set_yticklabel_monospaced(ax)


def capitalize_xticklabels(axis: Union[Axes, None] = None):
    "Capitalize the xtick labels."
    ax = _find_axis(axis)

    xticklabels = [label.get_text().capitalize() for label in ax.get_xticklabels()]  # type: ignore
    ax.set_xticklabels(xticklabels)  # type: ignore


def capitalize_yticklabels(axis: Union[Axes, None] = None):
    "Capitalize the ytick labels."
    ax = _find_axis(axis)

    yticklabels = [label.get_text().capitalize() for label in ax.get_yticklabels()]  # type: ignore
    ax.set_yticklabels(yticklabels)  # type: ignore


def capitalize_ticklabels(axis: Union[Axes, None] = None):
    "Capitalize both the x and y tick labels."
    ax = _find_axis(axis)

    capitalize_yticklabels(ax)
    capitalize_xticklabels(ax)


def add_commas_to_axis_tick_labels(axis: Union[XAxis, YAxis]):
    """
    Add commas to the numbers used for axis tick labels.
    """
    axis.set_major_formatter(mpl.ticker.FuncFormatter(lambda x, _: format(int(x), ",")))  # type: ignore


def set_xaxis_categorical(axis: Union[Axes, None] = None):
    "Set the style of the x-axis to a categorical axis, removing ticks and adjusting padding."
    ax = _find_axis(axis)

    ax.tick_params(
        axis="x",
        which="both",
        pad=CATEGORICAL_AXIS_TICKPADDING,
        size=CATEGORICAL_AXIS_TICKLENGTH,
    )


def set_yaxis_categorical(axis: Union[Axes, None] = None):
    "Set the style of the x-axis to a categorical axis, removing ticks and adjusting padding."
    ax = _find_axis(axis)

    ax.tick_params(
        axis="y",
        which="both",
        pad=CATEGORICAL_AXIS_TICKPADDING,
        size=CATEGORICAL_AXIS_TICKLENGTH,
    )


def set_axes_categorical(axis: Union[Axes, None] = None):
    "Set the style of both the x and y axes to categorical axes."
    ax = _find_axis(axis)

    set_xaxis_categorical(ax)
    set_yaxis_categorical(ax)


def capitalize_ylabel(axis: Union[Axes, None] = None):
    "Capitalize the y-axis label."
    ax = _find_axis(axis)

    ax.set_ylabel(ax.get_yaxis().get_label().get_text().capitalize())


def capitalize_xlabel(axis: Union[Axes, None] = None):
    "Capitalize the x-axis label."
    ax = _find_axis(axis)

    ax.set_xlabel(ax.get_xaxis().get_label().get_text().capitalize())


def capitalize_axislabels(axis: Union[Axes, None] = None):
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


def capitalize_legend_text(legend: Legend):
    "Capitalize the legend title and entries."
    capitalize_legend_title(legend)
    capitalize_legend_entries(legend)


def justify_legend_text(legend: Legend):
    "Justify the legend to the left and change legend title font to Medium weight."
    legend.set_title(legend.get_title()._text, prop=LEGEND_PARAMS["title_fontproperties"])  # type: ignore
    legend.set(alignment="left")


def style_legend(legend: Legend):
    "Apply a set of style changes to a legend."
    capitalize_legend_text(legend)
    add_legend_line(legend)
    justify_legend_text(legend)


def set_colorbar_ticklabel_monospaced(axis: Union[Axes, None] = None):
    "Set the font of the colorbar tick labels to Suisse Int'l Mono."

    ax = _find_axis(axis)
    if cbar := ax.collections[0].colorbar:  # type: ignore
        set_ticklabel_monospaced(axis=cbar.ax)


def style_plot(
    axis: Union[Axes, None] = None,
    monospaced_axes: Literal["x", "y", "both", None] = None,
    categorical_axes: Literal["x", "y", "both", None] = None,
    colorbar_exists: bool = False,
) -> None:
    """Apply a set of style changes to a user-specified axis, or (if None), the most recent axis.

    Args:
        axis (matplotlib.axis.Axis or None): the axis to style
        monospaced_axes (str): which axes to set to a monospaced font,
            either 'x', 'y', 'both', or None
        categorical_axes (str): which axes to set to categorical,
            either 'x', 'y', 'both', or None
        colorbar_exists (bool): whether a colorbar exists on the axis
    """

    ax = _find_axis(axis)
    capitalize_axislabels(ax)

    # Legend styling.
    legend = ax.get_legend()

    if legend is not None:  # type: ignore
        style_legend(legend)

    if categorical_axes == "both":
        set_axes_categorical(axis)
        capitalize_ticklabels(axis)
    elif categorical_axes == "x":
        set_xaxis_categorical(axis)
        capitalize_xticklabels(axis)
    elif categorical_axes == "y":
        set_yaxis_categorical(axis)
        capitalize_yticklabels(axis)
    elif categorical_axes is None:
        pass
    else:
        print("Invalid categorical_axes option. Please choose from 'x', 'y', or 'both'.")

    if monospaced_axes == "both":
        set_ticklabel_monospaced(axis)
    elif monospaced_axes == "x":
        set_xticklabel_monospaced(axis)
    elif monospaced_axes == "y":
        set_yticklabel_monospaced(axis)
    elif monospaced_axes is None:
        pass
    else:
        print("Invalid monospaced_axes option. Please choose from 'x', 'y', or 'both'.")

    if colorbar_exists:
        set_colorbar_ticklabel_monospaced(ax)


def get_figure_dimensions(size: str) -> tuple[float, ...]:
    "Return the dimensions of a figure given a size, subtracting the spacing needed for margins."

    if size not in FIGURE_SIZES:
        raise ValueError(f"Size must be one of {list(FIGURE_SIZES.keys())}.")

    return tuple(x - 2 * FIGURE_PADDING_INCHES for x in FIGURE_SIZES[size])


def add_legend_line(legend: Legend, linewidth: float = LEGEND_SEPARATOR_LINEWIDTH):
    "Add a horizontal line with 'chateau' color below the legend title."
    # Determine the width of the legend in pixels

    legend_line_color = colors.chateau

    x0 = legend._legend_handle_box.get_window_extent()._points[0][0]  # type: ignore
    x1 = legend._legend_handle_box.get_window_extent()._points[1][0]  # type: ignore
    bbox_length = abs(cast(float, x1 - x0))

    # We must create a drawing area to insert the line into the legend,
    # otherwise we encounter issues at draw time.
    line_area = DrawingArea(width=bbox_length, height=0, xdescent=0, ydescent=0)

    # Create a horizontal line.
    line = Line2D(
        [0, bbox_length],  # length
        [0],  # height
        color=legend_line_color,
        linewidth=linewidth,
        linestyle="-",
        transform=line_area.get_transform(),
    )
    line_area.add_artist(line)

    # Insert the line as a new row just below the title.
    # First, get the _legend_handle_box (an HPacker object) which wraps all the legend entries.
    # Then, get the children of that box, which returns a list of VPacker objects.
    # Get the first object, which is a VPacker containing the legend entries.
    # TODO: Check if there are more objects in the case of a multi-column legend.
    legend_vpacker = legend._legend_handle_box.get_children()[0]  # type: ignore

    # The children of the VPacker object are HPacker objects wrapping the legend handle and text.
    entries = legend_vpacker.get_children()  # type: ignore

    # Check that we haven't already put a drawing area within the legend.
    # This should catch if we've already added the legend line
    # through a different call to this function, e.g. calling "style_plot".
    # This won't catch if the DrawingArea is added by a user otherwise,
    # but most users shouldn't be adding new DrawingAreas to the legend.
    if not isinstance(entries[0], DrawingArea):
        # Insert the line inside a DrawingArea as the first entry.
        entries.insert(0, line_area)


def load_colors():
    "Load Arcadia's colors into the matplotlib list of named colors with the prefix 'apc:'."
    colors = {
        "apc:" + color.name: color.hex_code for color in arcadia_pycolor.palettes.all_colors.colors
    }
    mpl.cm.colors.get_named_colors_mapping().update(colors)  # type: ignore


def load_fonts(font_folder: Union[str, None] = None) -> None:
    """
    Detect and load Suisse-family fonts installed on the system into matplotlib.

    Args:
        font_folder (str, optional): the folder to search for fonts in.
            Uses the default system font folder if None.
    """
    for fontpath in font_manager.findSystemFonts(fontpaths=font_folder, fontext="ttf"):
        if FONT_FILTER.lower() in fontpath.lower():
            font_manager.fontManager.addfont(fontpath)
            font_manager.FontProperties(fname=fontpath)

    if not _arcadia_fonts_found():
        print(
            "Warning: The Arcadia fonts were not found. "
            "The default matplotlib fonts will be used instead."
        )


def load_colormaps() -> None:
    """
    Load Arcadia's palettes and gradients into the matplotlib list of named colormaps
    with the prefix 'apc:'.
    """
    arcadia_colormaps = [
        object
        for object in (
            list(arcadia_pycolor.palettes.__dict__.values())
            + list(arcadia_pycolor.gradients.__dict__.values())
        )
        if isinstance(object, ColorSequence)
    ]

    for arcadia_colormap in arcadia_colormaps:
        if (colormap_name := f"apc:{arcadia_colormap.name}") not in mpl_colormaps:
            mpl.colormaps.register(name=colormap_name, cmap=arcadia_colormap.to_mpl_cmap())
        # Register the reversed version of gradients but not palettes
        # to be consistent with matplotlib.
        if isinstance(arcadia_colormap, Gradient):
            if (colormap_name := f"apc:{arcadia_colormap.name}_r") not in mpl_colormaps:
                mpl.colormaps.register(
                    name=colormap_name, cmap=arcadia_colormap.reverse().to_mpl_cmap()
                )


def load_styles() -> None:
    "Load Arcadia's default style settings into matplotlib rcParams."
    plt.rcParams.update(ARCADIA_RC_PARAMS)


def setup(font_folder: Union[str, None] = None) -> None:
    "Load all Arcadia colors, fonts, styles, and colormaps into matplotlib."
    load_colors()
    load_fonts(font_folder)
    load_colormaps()
    load_styles()
