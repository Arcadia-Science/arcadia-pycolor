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
    fig: go.Figure,
    font: str = DEFAULT_FONT_PLOTLY,
    font_size: Union[float, None] = None,
    row: Union[int, None] = None,
    col: Union[int, None] = None,
) -> None:
    """Sets the font and font size of the y-axis tick labels for a Plotly figure.

    Args:
        fig (go.Figure): The Plotly figure to modify.
        font (str): The font family to use for the tick labels.
        font_size (float, optional): The font size to use for the tick labels.
            If None, keeps current size.
    """
    fig.update_yaxes(tickfont_family=font, row=row, col=col)
    if font_size is not None:
        fig.update_yaxes(tickfont_size=font_size, row=row, col=col)


def set_xticklabel_font(
    fig: go.Figure,
    font: str = DEFAULT_FONT_PLOTLY,
    font_size: Union[float, None] = None,
    row: Union[int, None] = None,
    col: Union[int, None] = None,
) -> None:
    """Sets the font and font size of the x-axis tick labels for a Plotly figure.

    Args:
        fig (go.Figure): The Plotly figure to modify.
        font (str): The font family to use for the tick labels.
        font_size (float, optional): The font size to use for the tick labels.
            If None, keeps current size.
    """
    fig.update_xaxes(tickfont_family=font, row=row, col=col)
    if font_size is not None:
        fig.update_xaxes(tickfont_size=font_size, row=row, col=col)


def set_ticklabel_font(
    fig: go.Figure,
    font: str = DEFAULT_FONT_PLOTLY,
    font_size: Union[float, None] = None,
    row: Union[int, None] = None,
    col: Union[int, None] = None,
) -> None:
    """Sets the font and font size of the ticklabels for the given axes.

    Args:
        fig (go.Figure): The Plotly figure to modify.
        font (str, optional): The font family to use for the ticklabels.
        font_size (float, optional): The font size to use for the ticklabels.
            If None, keeps current size.
    """
    set_xticklabel_font(fig, font, font_size, row, col)
    set_yticklabel_font(fig, font, font_size, row, col)


def set_xticklabel_monospaced(
    fig: go.Figure, row: Union[int, None] = None, col: Union[int, None] = None
) -> None:
    """Sets the font of the x-axis ticklabels to a monospace font."""
    set_xticklabel_font(fig, MONOSPACE_FONT_PLOTLY, font_size=MONOSPACE_FONT_SIZE, row=row, col=col)


def set_yticklabel_monospaced(
    fig: go.Figure, row: Union[int, None] = None, col: Union[int, None] = None
) -> None:
    """Sets the font of the y-axis ticklabels to a monospace font."""
    set_yticklabel_font(fig, MONOSPACE_FONT_PLOTLY, font_size=MONOSPACE_FONT_SIZE, row=row, col=col)


def set_ticklabel_monospaced(
    fig: go.Figure, row: Union[int, None] = None, col: Union[int, None] = None
) -> None:
    """Sets the font of both the x- and y-axis ticklabels to a monospace font."""
    set_xticklabel_monospaced(fig, row, col)
    set_yticklabel_monospaced(fig, row, col)


def add_commas_to_axis_tick_labels(fig: go.Figure) -> None:
    """Adds commas to the numbers used for axis ticklabels.

    For example, transform 1000000 to 1,000,000.
    """
    fig.update_layout(xaxis=dict(tickformat=","))
    fig.update_layout(yaxis=dict(tickformat=","))


def hide_yaxis_line(
    fig: go.Figure, row: Union[int, None] = None, col: Union[int, None] = None
) -> None:
    """Hides the line on the y-axis."""
    fig.update_yaxes(showline=False, row=row, col=col)


def hide_xaxis_line(
    fig: go.Figure, row: Union[int, None] = None, col: Union[int, None] = None
) -> None:
    """Hides the line on the x-axis."""
    fig.update_xaxes(showline=False, row=row, col=col)


def hide_axis_lines(
    fig: go.Figure, row: Union[int, None] = None, col: Union[int, None] = None
) -> None:
    """Hides the lines on both the x- and y-axes."""
    hide_yaxis_line(fig, row, col)
    hide_xaxis_line(fig, row, col)


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
