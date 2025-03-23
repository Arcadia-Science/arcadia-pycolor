from typing import Union

import plotly.graph_objects as go
import plotly.io as pio

from arcadia_pycolor.style_defaults import (
    ARCADIA_PLOTLY_TEMPLATE_LAYOUT,
    DEFAULT_FONT_PLOTLY,
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


def capitalize_xticklabels(fig: go.Figure) -> None:
    """Capitalizes the x-axis ticklabels."""
    fig.update_layout(xaxis=dict(tickfont=dict(variant="small-caption")))


def capitalize_yticklabels(fig: go.Figure) -> None:
    """Capitalizes the y-axis ticklabels."""
    fig.update_layout(yaxis=dict(tickfont=dict(variant="small-caption")))


def capitalize_ticklabels(fig: go.Figure) -> None:
    """Capitalizes both the x- and y-axis ticklabels."""
    capitalize_xticklabels(fig)
    capitalize_yticklabels(fig)


def add_commas_to_axis_tick_labels(fig: go.Figure) -> None:
    """Adds commas to the numbers used for axis ticklabels.

    For example, transform 1000000 to 1,000,000.
    """
    fig.update_layout(xaxis=dict(tickformat=","))
    fig.update_layout(yaxis=dict(tickformat=","))


def set_xaxis_categorical(fig: go.Figure) -> None:
    """Sets the style of the x-axis to a categorical axis, removing ticks and adjusting padding."""
    fig.update_layout(xaxis=dict(tickmode="array", tickvals=[]))
    fig.update_layout(xaxis=dict(tickmode="array", tickvals=[], ticktext=[]))


def set_yaxis_categorical(fig: go.Figure) -> None:
    """Sets the style of the y-axis to a categorical axis, removing ticks and adjusting padding."""
    fig.update_layout(yaxis=dict(tickmode="array", tickvals=[]))
    fig.update_layout(yaxis=dict(tickmode="array", tickvals=[], ticktext=[]))


def set_axes_categorical(fig: go.Figure) -> None:
    """Sets the style of both the x and y axes to categorical axes."""
    fig.update_layout(xaxis=dict(tickmode="array", tickvals=[]))
    fig.update_layout(yaxis=dict(tickmode="array", tickvals=[]))
    set_xaxis_categorical(fig)
    set_yaxis_categorical(fig)


def capitalize_ylabel(fig: go.Figure) -> None:
    """Capitalizes the y-axis label."""
    print(fig)
    pass


def capitalize_xlabel(fig: go.Figure) -> None:
    """Capitalizes the x-axis label."""
    print(fig)
    pass


def capitalize_axislabels(fig: go.Figure) -> None:
    """Capitalizes both the x and y axis labels."""
    capitalize_xlabel(fig)
    capitalize_ylabel(fig)


def setup() -> None:
    """Loads all Arcadia colors, fonts, styles, and colormaps into Plotly."""
    arcadia_template = go.layout.Template(layout=ARCADIA_PLOTLY_TEMPLATE_LAYOUT)
    pio.templates["arcadia"] = arcadia_template
    pio.templates.default = "arcadia"
