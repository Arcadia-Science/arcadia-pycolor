import logging
import re
import sys
from pathlib import Path
from typing import Any, Literal, Union, cast

import matplotlib as mpl
import matplotlib.font_manager as font_manager
import matplotlib.pyplot as plt
from matplotlib import colormaps as mpl_colormaps
from matplotlib.axis import XAxis, YAxis
from matplotlib.backend_bases import FigureCanvasBase
from matplotlib.legend import Legend
from matplotlib.lines import Line2D
from matplotlib.offsetbox import DrawingArea
from matplotlib.pyplot import Axes  # type: ignore
from matplotlib.transforms import Bbox  # type: ignore

import arcadia_pycolor.colors as colors
import arcadia_pycolor.gradients
import arcadia_pycolor.palettes
from arcadia_pycolor.gradient import Gradient
from arcadia_pycolor.palette import Palette
from arcadia_pycolor.style_defaults import (
    ARCADIA_MATPLOTLIB_RC_PARAMS,
    BASE_DPI,
    CATEGORICAL_AXIS_TICKLENGTH,
    CATEGORICAL_AXIS_TICKPADDING,
    DEFAULT_FONT,
    FIGURE_PADDING_INCHES,
    FIGURE_SIZES_IN_INCHES,
    FONT_FILTER,
    LEGEND_SEPARATOR_LINEWIDTH,
    MONOSPACE_FONT,
    MONOSPACE_FONT_SIZE,
    PRINT_DPI,
    FigureSize,
)

# Disable matplotlib's very noisy warnings when the Arcadia fonts are not installed.
logging.getLogger("matplotlib.font_manager").setLevel(logging.ERROR)

# Copied from `matplotlib.font_manager.OSXFontDirectories`. For reference, see:
# https://support.apple.com/guide/font-book/change-font-book-settings-fntbk1004/mac.
MACOS_FONT_DIRECTORIES = [
    "/Library/Fonts",
    "/Network/Library/Fonts",
    "/System/Library/Fonts",
    "/opt/local/share/fonts",
    str(Path.home() / "Library/Fonts"),
]

LEGEND_PARAMS = dict(
    alignment="left",
    title_fontproperties={
        "weight": "semibold",
        "size": ARCADIA_MATPLOTLIB_RC_PARAMS["legend.title_fontsize"],
    },
)

SAVEFIG_KWARGS_WEB = dict(dpi=BASE_DPI, pad_inches=FIGURE_PADDING_INCHES)
SAVEFIG_KWARGS_PRINT = dict(dpi=PRINT_DPI, pad_inches=FIGURE_PADDING_INCHES)


def _try_get_current_axes(axes: Union[Axes, None] = None) -> Axes:
    """Returns the current axes using `plt.gca()` if no axes are provided.

    Otherwise, returns the provided axes.
    """
    if axes is None:
        return plt.gca()
    else:
        return axes


def _is_arcadia_font_set_available() -> bool:
    """Returns True if the Arcadia fonts are available to matplotlib."""
    arcadia_fonts = [
        font_name
        for font_name in font_manager.fontManager.get_font_names()
        if FONT_FILTER in font_name
    ]
    # TODO(KC): can we specify the number of fonts that should be found?
    return len(arcadia_fonts) > 0


def _find_macos_arcadia_fonts() -> list[str]:
    """Searches for Arcadia fonts in the standard macOS font directories.

    Returns:
        list[str]: A list of paths to the Arcadia fonts.
    """
    font_paths = []
    for dirpath in MACOS_FONT_DIRECTORIES:
        if not Path(dirpath).exists():
            continue
        paths = [
            str(font_path)
            for font_path in Path(dirpath).glob("*.ttf")
            if FONT_FILTER.lower() in font_path.name.lower()
        ]
        font_paths.extend(paths)
    return font_paths


def _fix_svg_fonts_for_illustrator(filename: str) -> None:
    """Fixes CSS font styles in SVG exports for Adobe Illustrator.

    Adobe Illustrator cannot parse font weights in shorthand font styles like
    "font: 500 15px SuisseIntl, sans-serif;". The axis titles and legend title have font
    weights applied, and because of this, their fonts are not being rendered correctly
    in Illustrator.

    As a workaround, each CSS font property is explicitly set:

    ```html
    <text style="font-family: SuisseIntl, sans-serif; font-size: 15px; font-weight: 500;">
    ```

    Additionally, the font family is not being applied correctly in Illustrator
    when it is encoded as "&quot;Suisse Int&apos;l&quot;". To fix this, we replace
    all instances of this encoding with "SuisseIntl".

    For more context, see https://github.com/Arcadia-Science/arcadia-pycolor/issues/68.

    Args:
        filename (str): The path to the SVG file to fix.
    """
    with open(filename) as f:
        content = f.read()

    pattern = r'font:\s*(\d+)\s+(\d+)px\s+(.+),\s*([^"]+);'

    def replace_font_style(match):
        weight = match.group(1)
        size = match.group(2)
        font_family = match.group(3)
        fallback = match.group(4)
        return f"font-family: {font_family},{fallback}; font-size: {size}px; font-weight: {weight};"

    new_content = re.sub(pattern, replace_font_style, content)
    new_content = new_content.replace("&quot;Suisse Int&apos;l&quot;", "SuisseIntl")

    with open(filename, "w") as f:
        f.write(new_content)


def save_figure(
    filepath: str,
    size: FigureSize,
    filetypes: Union[list[str], None] = None,
    context: str = "web",
    **savefig_kwargs: dict[Any, Any],
) -> None:
    """Saves the current figure to a file using Arcadia's margin, padding, and dpi settings.

    Args:
        filepath (str): Path to save the figure to.
        size (FigureSize): The size of the figure to save.
        filetypes (list[str], optional): The file types(s) to save the figure to.
            If None, the original filetype of `filepath` is used.
            If the original filetype is not in `filetypes`, it is appended to the list.
        context (str): The context to save the figure in, either 'web' or 'print'.
        **savefig_kwargs: Additional keyword arguments to pass to `plt.savefig`.
    """
    width, height = FIGURE_SIZES_IN_INCHES[size]
    bbox_inches = Bbox.from_bounds(
        -FIGURE_PADDING_INCHES,
        -FIGURE_PADDING_INCHES,
        width,
        height,
    )

    kwargs = SAVEFIG_KWARGS_WEB if context == "web" else SAVEFIG_KWARGS_PRINT
    kwargs.update(**savefig_kwargs, bbox_inches=bbox_inches)  # type: ignore

    # Gets a list of valid filetypes for saving figures from matplotlib.
    valid_filetypes = list(FigureCanvasBase.get_supported_filetypes().keys())

    filename = Path(filepath).with_suffix("")
    filetype = Path(filepath).suffix[1:]

    # If no file types are provided, use the filetype from the file path.
    if filetypes is None:
        if not filetype:
            raise ValueError("The filename must include a filetype if no filetypes are provided.")
        filetypes = [filetype]
    else:
        filetypes.append(filetype)

    for ftype in filetypes:
        if ftype not in valid_filetypes:
            print(f"Invalid filetype '{ftype}'. Skipping.")
            continue

        plt.savefig(fname=f"{filename}.{ftype}", **kwargs)

        if ftype == "svg":
            _fix_svg_fonts_for_illustrator(f"{filename}.{ftype}")


def set_yticklabel_font(
    axes: Union[Axes, None] = None, font: str = DEFAULT_FONT, font_size: Union[float, None] = None
) -> None:
    """Sets the font and font size of the y-axis tick labels.

    Args:
        axes (Axes, optional): The matplotlib axes to modify.
            If None, uses the current axes.
        font (str): The font family to use for the tick labels.
        font_size (float, optional): The font size to use for the tick labels.
            If None, keeps current size.
    """
    ax = _try_get_current_axes(axes)

    ytick_labels = ax.get_yticklabels()
    for label in ytick_labels:
        label.set_fontfamily(font)
    if font_size is not None:
        ax.yaxis.set_tick_params(labelsize=font_size)


def set_xticklabel_font(
    axes: Union[Axes, None] = None, font: str = DEFAULT_FONT, font_size: Union[float, None] = None
) -> None:
    """Sets the font and font size of the x-axis tick labels.

    Args:
        axes (Axes, optional): The matplotlib axes to modify.
            If None, uses the current axes.
        font (str): The font family to use for the tick labels.
        font_size (float, optional): The font size to use for the tick labels.
            If None, keeps current size.
    """
    ax = _try_get_current_axes(axes)

    xtick_labels = ax.get_xticklabels()
    for label in xtick_labels:
        label.set_fontfamily(font)
    if font_size is not None:
        ax.xaxis.set_tick_params(labelsize=font_size)


def set_ticklabel_font(
    axes: Union[Axes, None] = None, font: str = DEFAULT_FONT, font_size: Union[float, None] = None
) -> None:
    """Sets the font and font size of the ticklabels for the given axes.

    Args:
        axes (Axes, optional): The matplotlib axes to modify.
            If None, uses the current axes.
        font (str, optional): The font family to use for the ticklabels.
        font_size (float, optional): The font size to use for the ticklabels.
            If None, keeps current size.
    """
    ax = _try_get_current_axes(axes)

    set_xticklabel_font(ax, font, font_size)
    set_yticklabel_font(ax, font, font_size)


def set_xticklabel_monospaced(axes: Union[Axes, None] = None) -> None:
    """Sets the font of the x-axis ticklabels to a monospace font."""
    ax = _try_get_current_axes(axes)
    set_xticklabel_font(ax, MONOSPACE_FONT, MONOSPACE_FONT_SIZE)


def set_yticklabel_monospaced(axes: Union[Axes, None] = None) -> None:
    """Sets the font of the y-axis ticklabels to a monospace font."""
    ax = _try_get_current_axes(axes)
    set_yticklabel_font(ax, MONOSPACE_FONT, MONOSPACE_FONT_SIZE)


def set_ticklabel_monospaced(axes: Union[Axes, None] = None) -> None:
    """Sets the font of both the x- and y-axis ticklabels to a monospace font."""
    ax = _try_get_current_axes(axes)

    set_xticklabel_monospaced(ax)
    set_yticklabel_monospaced(ax)


def capitalize_xticklabels(axes: Union[Axes, None] = None) -> None:
    """Capitalizes the x-axis ticklabels if all letters are lowercase."""
    ax = _try_get_current_axes(axes)

    xticklabels = [
        label.get_text().capitalize() if label.get_text().islower() else label.get_text()
        for label in ax.get_xticklabels()
    ]
    ax.set_xticks(ax.get_xticks())
    ax.set_xticklabels(xticklabels)


def capitalize_yticklabels(axes: Union[Axes, None] = None) -> None:
    """Capitalizes the y-axis ticklabels if all letters are lowercase."""
    ax = _try_get_current_axes(axes)

    yticklabels = [
        label.get_text().capitalize() if label.get_text().islower() else label.get_text()
        for label in ax.get_yticklabels()
    ]
    ax.set_yticks(ax.get_yticks())
    ax.set_yticklabels(yticklabels)


def capitalize_ticklabels(axes: Union[Axes, None] = None) -> None:
    """Capitalizes both the x- and y-axis ticklabels if all letters are lowercase."""
    ax = _try_get_current_axes(axes)

    capitalize_yticklabels(ax)
    capitalize_xticklabels(ax)


def add_commas_to_axis_tick_labels(axes: Union[XAxis, YAxis]) -> None:
    """Adds commas to the numbers used for axis ticklabels.

    For example, transform 1000000 to 1,000,000.
    """
    axes.set_major_formatter(mpl.ticker.FuncFormatter(lambda x, _: format(int(x), ",")))  # type: ignore


def set_xaxis_categorical(axes: Union[Axes, None] = None) -> None:
    """Sets the style of the x-axis to a categorical axis, removing ticks and adjusting padding."""
    ax = _try_get_current_axes(axes)

    ax.tick_params(
        axis="x",
        which="both",
        pad=CATEGORICAL_AXIS_TICKPADDING,
        size=CATEGORICAL_AXIS_TICKLENGTH,
    )


def set_yaxis_categorical(axes: Union[Axes, None] = None) -> None:
    """Sets the style of the y-axis to a categorical axis, removing ticks and adjusting padding."""
    ax = _try_get_current_axes(axes)

    ax.tick_params(
        axis="y",
        which="both",
        pad=CATEGORICAL_AXIS_TICKPADDING,
        size=CATEGORICAL_AXIS_TICKLENGTH,
    )


def set_axes_categorical(axes: Union[Axes, None] = None) -> None:
    """Sets the style of both the x and y axes to categorical axes."""
    ax = _try_get_current_axes(axes)

    set_xaxis_categorical(ax)
    set_yaxis_categorical(ax)


def capitalize_ylabel(axes: Union[Axes, None] = None) -> None:
    """Capitalizes the y-axis label if all letters are lowercase."""
    ax = _try_get_current_axes(axes)

    ylabel = ax.get_yaxis().get_label().get_text()
    if ylabel.islower():
        ax.set_ylabel(ylabel.capitalize())


def capitalize_xlabel(axes: Union[Axes, None] = None) -> None:
    """Capitalizes the x-axis label if all letters are lowercase."""
    ax = _try_get_current_axes(axes)

    xlabel = ax.get_xaxis().get_label().get_text()
    if xlabel.islower():
        ax.set_xlabel(xlabel.capitalize())


def capitalize_axislabels(axes: Union[Axes, None] = None) -> None:
    """Capitalizes both the x and y axis labels if all letters are lowercase."""
    ax = _try_get_current_axes(axes)

    capitalize_xlabel(ax)
    capitalize_ylabel(ax)


def capitalize_legend_title(legend: Legend) -> None:
    """Capitalizes the legend title if all letters are lowercase."""
    title = legend.get_title().get_text()
    if title.islower():
        legend.set_title(title.capitalize())


def capitalize_legend_entries(legend: Legend) -> None:
    """Capitalizes the legend entries if all letters are lowercase."""
    for text in legend.get_texts():
        text_content = text.get_text()
        if text_content.islower():
            text.set_text(text_content.capitalize())


def capitalize_legend_text(legend: Legend) -> None:
    """Capitalizes the legend title and entries if all letters are lowercase."""
    capitalize_legend_title(legend)
    capitalize_legend_entries(legend)


def justify_legend_text(legend: Legend) -> None:
    """Justify the legend to the left and change legend title font to Medium weight."""
    legend.set_title(legend.get_title()._text, prop=LEGEND_PARAMS["title_fontproperties"])  # type: ignore
    legend.set(alignment="left")


def style_legend(legend: Legend) -> None:
    """Styles the legend according to Arcadia's style guide."""
    capitalize_legend_text(legend)
    add_legend_line(legend)
    justify_legend_text(legend)


def set_colorbar_ticklabel_monospaced(axes: Union[Axes, None] = None) -> None:
    """Set the font of the colorbar tick labels to Suisse Int'l Mono."""
    ax = _try_get_current_axes(axes)
    if cbar := ax.collections[0].colorbar:  # type: ignore
        set_ticklabel_monospaced(axes=cbar.ax)


def style_plot(
    axes: Union[Axes, None] = None,
    monospaced_axes: Literal["x", "y", "both", "all", None] = None,
    categorical_axes: Literal["x", "y", "both", "all", None] = None,
    colorbar_exists: bool = False,
) -> None:
    """Styles the plot according to Arcadia's style guide.

    Args:
        axes (Axes, optional): The matplotlib Axes to modify.
            If None, uses the most recent Axes.
        monospaced_axes (str, optional): Which axes to set to the default monospaced font.
            Either 'x', 'y', 'both', 'all', or None ('both' and 'all' are equivalent).
        categorical_axes (str, optional): Which axes to set to categorical.
            Either 'x', 'y', 'both', 'all', or None ('both' and 'all' are equivalent).
        colorbar_exists (bool): Whether a colorbar exists on the axis.
    """

    ax = _try_get_current_axes(axes)
    capitalize_axislabels(ax)

    # Legend styling.
    legend = ax.get_legend()

    if legend is not None:
        style_legend(legend)

    if categorical_axes in ("both", "all"):
        set_axes_categorical(ax)
        capitalize_ticklabels(ax)
    elif categorical_axes == "x":
        set_xaxis_categorical(ax)
        capitalize_xticklabels(ax)
    elif categorical_axes == "y":
        set_yaxis_categorical(ax)
        capitalize_yticklabels(ax)
    elif categorical_axes is None:
        pass
    else:
        raise ValueError(
            "Invalid categorical_axes option. Please choose from 'x', 'y', 'both', or 'all'."
        )

    if monospaced_axes in ("both", "all"):
        set_ticklabel_monospaced(ax)
    elif monospaced_axes == "x":
        set_xticklabel_monospaced(ax)
    elif monospaced_axes == "y":
        set_yticklabel_monospaced(ax)
    elif monospaced_axes is None:
        pass
    else:
        raise ValueError(
            "Invalid monospaced_axes option. Please choose from 'x', 'y', 'both', or 'all'."
        )

    if colorbar_exists:
        set_colorbar_ticklabel_monospaced(ax)


def get_figure_dimensions(size: FigureSize) -> tuple[float, float]:
    """Returns the dimensions of a figure given a predefined size.

    The dimensions are calculated by subtracting the spacing needed for padding
    from the width and height of the predefined size.

    Args:
        size (FigureSize): The size of the figure, which must be one of the following:
            - "full_wide"
            - "full_square"
            - "float_wide"
            - "float_square"
            - "half_square"

    Returns:
        tuple[float, float]: The width and height of the figure in inches.

    Raises:
        ValueError: If the size is not one of the predefined sizes.
    """
    if size not in FIGURE_SIZES_IN_INCHES:
        raise ValueError(f"Size must be one of {list(FIGURE_SIZES_IN_INCHES.keys())}.")

    width, height = FIGURE_SIZES_IN_INCHES[size]
    return (width - 2 * FIGURE_PADDING_INCHES, height - 2 * FIGURE_PADDING_INCHES)


def add_legend_line(legend: Legend, linewidth: float = LEGEND_SEPARATOR_LINEWIDTH):
    """Adds a horizontal line with 'chateau' color below the legend title.

    Args:
        legend (Legend): The legend to add the line to.
        linewidth (float): The width of the line.
    """
    legend_line_color = colors.chateau

    # Determine the width of the legend in pixels.
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


def load_colors() -> None:
    """Loads Arcadia's colors into the matplotlib list of named colors with the prefix 'apc:'."""
    colors = {
        "apc:" + color.name: color.hex_code for color in arcadia_pycolor.palettes.all_colors.colors
    }
    mpl.cm.colors.get_named_colors_mapping().update(colors)  # type: ignore


def load_fonts(font_dirpath: Union[str, None] = None) -> None:
    """Detects the Suisse-family fonts installed on the system and loads them into matplotlib.

    Args:
        font_dirpath (str, optional): Path to the directory to search for fonts in.
            If None, searches the expected system font directories.
    """
    arcadia_font_paths = []

    # On macOS, look in the standard font directories first.
    # This is faster than matplotlib's font search implementation.
    # See https://github.com/Arcadia-Science/arcadia-pycolor/pull/58.
    if font_dirpath is None and sys.platform == "darwin":
        arcadia_font_paths.extend(_find_macos_arcadia_fonts())

    # If no fonts are found, fallback to full system search.
    if not arcadia_font_paths:
        for font_path in font_manager.findSystemFonts(fontpaths=font_dirpath, fontext="ttf"):
            if FONT_FILTER.lower() in font_path.lower():
                arcadia_font_paths.append(font_path)

    for font_path in arcadia_font_paths:
        font_manager.fontManager.addfont(font_path)
        font_manager.FontProperties(fname=font_path)

    if not _is_arcadia_font_set_available():
        print(
            "Warning: The Arcadia fonts were not found. "
            "The default matplotlib fonts will be used instead."
        )


def load_colormaps() -> None:
    """Loads Arcadia's palettes and gradients into matplotlib.

    The colormaps are loaded into matplotlib's list of named colormaps
    with the prefix 'apc:'.
    """
    arcadia_colormaps = [
        object
        for object in (
            list(arcadia_pycolor.palettes.__dict__.values())
            + list(arcadia_pycolor.gradients.__dict__.values())
        )
        if isinstance(object, (Palette, Gradient))
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
    """Updates matplotlib's runtime configuration parameters with Arcadia's style settings."""
    plt.rcParams.update(ARCADIA_MATPLOTLIB_RC_PARAMS)


def setup(font_dirpath: Union[str, None] = None) -> None:
    """Loads all Arcadia colors, fonts, styles, and colormaps into matplotlib."""
    load_colors()
    load_fonts(font_dirpath)
    load_colormaps()
    load_styles()
