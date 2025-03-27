from typing import Literal, Union

import plotly.graph_objects as go
import plotly.io as pio

from arcadia_pycolor.style_defaults import (
    ARCADIA_PLOTLY_TEMPLATE_LAYOUT,
    DEFAULT_FONT_PLOTLY,
    FIGURE_PADDING_PIXELS,
    FIGURE_SIZES_IN_PIXELS,
    MONOSPACE_FONT_PLOTLY,
    MONOSPACE_FONT_SIZE,
    TITLE_FONT_SIZE,
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


def set_colorbar_ticklabel_monospaced(
    fig: go.Figure, row: Union[int, None] = None, col: Union[int, None] = None
) -> None:
    """Sets the font of the colorbar ticklabels to a monospace font."""
    fig.update_coloraxes(
        tickfont_family=MONOSPACE_FONT_PLOTLY, tickfont_size=MONOSPACE_FONT_SIZE, row=row, col=col
    )


def set_ticklabel_monospaced(
    fig: go.Figure, row: Union[int, None] = None, col: Union[int, None] = None
) -> None:
    """Sets the font of both the x- and y-axis ticklabels to a monospace font."""
    set_xticklabel_monospaced(fig, row, col)
    set_yticklabel_monospaced(fig, row, col)


def capitalize_xticklabels(fig: go.Figure) -> None:
    """Capitalizes the x-axis ticklabels."""
    fig.update_xaxes(ticktext=fig.xaxes[0].ticktext.capitalize())  # type: ignore


def capitalize_yticklabels(fig: go.Figure) -> None:
    """Capitalizes the y-axis ticklabels."""
    fig.update_yaxes(ticktext=fig.yaxes[0].ticktext.capitalize())  # type: ignore


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


def set_xaxis_categorical(
    fig: go.Figure, row: Union[int, None] = None, col: Union[int, None] = None
) -> None:
    """Sets the style of the x-axis to a categorical axis, removing ticks and adjusting padding."""
    fig.update_xaxes(ticks="", row=row, col=col)


def set_yaxis_categorical(
    fig: go.Figure, row: Union[int, None] = None, col: Union[int, None] = None
) -> None:
    """Sets the style of the y-axis to a categorical axis, removing ticks and adjusting padding."""
    fig.update_yaxes(ticks="", row=row, col=col)


def set_axes_categorical(
    fig: go.Figure, row: Union[int, None] = None, col: Union[int, None] = None
) -> None:
    """Sets both the x- and y-axes to categorical axes, removing ticks and adjusting padding."""
    set_xaxis_categorical(fig, row, col)
    set_yaxis_categorical(fig, row, col)


def capitalize_ylabel(
    fig: go.Figure, row: Union[int, None] = None, col: Union[int, None] = None
) -> None:
    """Capitalizes the y-axis label."""
    fig.update_yaxes(title_text=fig.yaxes[0].title.text.capitalize(), row=row, col=col)  # type: ignore


def capitalize_xlabel(
    fig: go.Figure, row: Union[int, None] = None, col: Union[int, None] = None
) -> None:
    """Capitalizes the x-axis label."""
    fig.update_xaxes(title_text=fig.xaxes[0].title.text.capitalize(), row=row, col=col)  # type: ignore


def capitalize_axislabels(
    fig: go.Figure, row: Union[int, None] = None, col: Union[int, None] = None
) -> None:
    """Capitalizes both the x and y axis labels."""
    capitalize_xlabel(fig, row, col)
    capitalize_ylabel(fig, row, col)


def hide_xaxis_ticks(
    fig: go.Figure, row: Union[int, None] = None, col: Union[int, None] = None
) -> None:
    """Hides the ticks on the x-axis."""
    fig.update_xaxes(ticks="", showticklabels=False, row=row, col=col)


def hide_yaxis_ticks(
    fig: go.Figure, row: Union[int, None] = None, col: Union[int, None] = None
) -> None:
    """Hides the ticks on the y-axis."""
    fig.update_yaxes(ticks="", showticklabels=False, row=row, col=col)


def hide_ticks(fig: go.Figure, row: Union[int, None] = None, col: Union[int, None] = None) -> None:
    """Hides the ticks on both the x- and y-axes."""
    hide_xaxis_ticks(fig, row, col)
    hide_yaxis_ticks(fig, row, col)


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


def capitalize_legend_title(fig: go.Figure) -> None:
    """Capitalizes the legend title."""
    fig.update_layout(legend_title_text=fig.layout.legend.title.text.capitalize())  # type: ignore


def capitalize_legend_entries(fig: go.Figure) -> None:
    """Capitalizes the legend entries."""
    pass


def capitalize_legend_text(fig: go.Figure) -> None:
    """Capitalize the legend title and entries."""
    capitalize_legend_title(fig)
    capitalize_legend_entries(fig)


def justify_legend_text(fig: go.Figure) -> None:
    """Justify the legend to the left and change legend title font to Medium weight."""
    fig.update_layout(legend_title_font_weight=600, legend_title_font_size=TITLE_FONT_SIZE)


def style_legend(fig: go.Figure) -> None:
    """Styles the legend according to Arcadia's style guide."""
    capitalize_legend_text(fig)
    justify_legend_text(fig)


def style_plot(
    fig: go.Figure,
    monospaced_axes: Literal["x", "y", "both", None] = None,
    categorical_axes: Literal["x", "y", "both", None] = None,
    colorbar_exists: bool = False,
) -> None:
    """Styles the plot according to Arcadia's style guide.

    Args:
        axes (Axes, optional): The matplotlib Axes to modify.
            If None, uses the most recent Axes.
        monospaced_axes (str, optional): Which axes to set to a monospaced font.
            Either 'x', 'y', 'both', or None.
        categorical_axes (str, optional): Which axes to set to categorical.
            Either 'x', 'y', 'both', or None.
        colorbar_exists (bool): Whether a colorbar exists on the axis.
    """
    if monospaced_axes is not None:
        if monospaced_axes == "x":
            set_xticklabel_monospaced(fig)
        elif monospaced_axes == "y":
            set_yticklabel_monospaced(fig)
        elif monospaced_axes == "both":
            set_ticklabel_monospaced(fig)
        else:
            raise ValueError(
                "Invalid monospaced_axes option. Please choose from 'x', 'y', or 'both'."
            )
    if categorical_axes is not None:
        if categorical_axes == "x":
            set_xaxis_categorical(fig)
        elif categorical_axes == "y":
            set_yaxis_categorical(fig)
        elif categorical_axes == "both":
            set_axes_categorical(fig)
        else:
            raise ValueError(
                "Invalid categorical_axes option. Please choose from 'x', 'y', or 'both'."
            )
    if colorbar_exists:
        set_colorbar_ticklabel_monospaced(fig)


def set_figure_dimensions(fig: go.Figure, size: str) -> None:
    """Sets the width and height of a figure.

    Args:
        size (str): Figure size, which must be one of the following:
            - "full_wide"
            - "full_square"
            - "float_wide"
            - "float_square"
            - "half_square"

    Raises:
        ValueError: If the size is not one of the predefined sizes.
    """
    if size not in FIGURE_SIZES_IN_PIXELS.keys():
        raise ValueError(f"Size must be one of {list(FIGURE_SIZES_IN_PIXELS.keys())}.")

    width, height = FIGURE_SIZES_IN_PIXELS[size]
    fig.update_layout(
        width=width - 2 * FIGURE_PADDING_PIXELS,
        height=height - 2 * FIGURE_PADDING_PIXELS,
    )


def setup() -> None:
    """Loads all Arcadia colors, fonts, styles, and colormaps into Plotly."""
    arcadia_template = go.layout.Template(layout=ARCADIA_PLOTLY_TEMPLATE_LAYOUT)
    pio.templates["arcadia"] = arcadia_template
    pio.templates.default = "arcadia"
