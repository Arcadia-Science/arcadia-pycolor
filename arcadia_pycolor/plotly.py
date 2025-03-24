from typing import Union

import plotly.graph_objects as go
import plotly.io as pio

from arcadia_pycolor.style_defaults import (
    ARCADIA_PLOTLY_TEMPLATE_LAYOUT,
    DEFAULT_FONT_PLOTLY,
    FIGURE_PADDING_PIXELS,
    FIGURE_WIDTHS_IN_PIXELS,
    MONOSPACE_FONT_PLOTLY,
    MONOSPACE_FONT_SIZE,
)


def set_yticklabel_font(
    fig: go.Figure, font: str = DEFAULT_FONT_PLOTLY, font_size: Union[float, None] = None
) -> None:
    """Sets the font and font size of the y-axis tick labels for a Plotly figure.

    Args:
        fig (go.Figure): The Plotly figure to modify.
        font (str): The font family to use for the tick labels.
        font_size (float, optional): The font size to use for the tick labels.
            If None, keeps current size.
    """
    fig.update_layout(yaxis=dict(tickfont=dict(family=font)))
    if font_size is not None:
        fig.update_layout(yaxis=dict(tickfont=dict(size=font_size)))


def set_xticklabel_font(
    fig: go.Figure, font: str = DEFAULT_FONT_PLOTLY, font_size: Union[float, None] = None
) -> None:
    """Sets the font and font size of the x-axis tick labels for a Plotly figure.

    Args:
        fig (go.Figure): The Plotly figure to modify.
        font (str): The font family to use for the tick labels.
        font_size (float, optional): The font size to use for the tick labels.
            If None, keeps current size.
    """
    fig.update_layout(xaxis=dict(tickfont=dict(family=font)))
    if font_size is not None:
        fig.update_layout(xaxis=dict(tickfont=dict(size=font_size)))


def set_ticklabel_font(
    fig: go.Figure, font: str = DEFAULT_FONT_PLOTLY, font_size: Union[float, None] = None
) -> None:
    """Sets the font and font size of the ticklabels for the given axes.

    Args:
        fig (go.Figure): The Plotly figure to modify.
        font (str, optional): The font family to use for the ticklabels.
        font_size (float, optional): The font size to use for the ticklabels.
            If None, keeps current size.
    """
    set_xticklabel_font(fig, font, font_size)
    set_yticklabel_font(fig, font, font_size)


def set_xticklabel_monospaced(fig: go.Figure) -> None:
    """Sets the font of the x-axis ticklabels to a monospace font."""
    set_xticklabel_font(fig, MONOSPACE_FONT_PLOTLY, font_size=MONOSPACE_FONT_SIZE)


def set_yticklabel_monospaced(fig: go.Figure) -> None:
    """Sets the font of the y-axis ticklabels to a monospace font."""
    set_yticklabel_font(fig, MONOSPACE_FONT_PLOTLY, font_size=MONOSPACE_FONT_SIZE)


def set_ticklabel_monospaced(fig: go.Figure) -> None:
    """Sets the font of both the x- and y-axis ticklabels to a monospace font."""
    set_xticklabel_monospaced(fig)
    set_yticklabel_monospaced(fig)


def add_commas_to_axis_tick_labels(fig: go.Figure) -> None:
    """Adds commas to the numbers used for axis ticklabels.

    For example, transform 1000000 to 1,000,000.
    """
    fig.update_layout(xaxis=dict(tickformat=","))
    fig.update_layout(yaxis=dict(tickformat=","))


def set_figure_width(fig: go.Figure, width: str) -> None:
    """Sets the width of a figure.

    Args:
        width (str): Figure width, which must be one of the following:
            - "full_wide"
            - "full_square"
            - "float_wide"
            - "float_square"
            - "half_square"

    Raises:
        ValueError: If the width is not one of the predefined sizes.
    """
    if width not in FIGURE_WIDTHS_IN_PIXELS.keys():
        raise ValueError(f"Width must be one of {list(FIGURE_WIDTHS_IN_PIXELS.keys())}.")

    fig.update_layout(width=FIGURE_WIDTHS_IN_PIXELS[width] - 2 * FIGURE_PADDING_PIXELS)


def setup() -> None:
    """Loads all Arcadia colors, fonts, styles, and colormaps into Plotly."""
    arcadia_template = go.layout.Template(layout=ARCADIA_PLOTLY_TEMPLATE_LAYOUT)
    pio.templates["arcadia"] = arcadia_template
    pio.templates.default = "arcadia"
