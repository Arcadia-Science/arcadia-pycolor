from pathlib import Path
from typing import Any, Literal, Union

import plotly.graph_objects as go
import plotly.io as pio

from arcadia_pycolor.style_defaults import (
    ARCADIA_PLOTLY_TEMPLATE_LAYOUT,
    DEFAULT_FONT_PLOTLY,
    FIGURE_SIZES_IN_PIXELS,
    MONOSPACE_FONT_PLOTLY,
    MONOSPACE_FONT_SIZE,
    FigureSize,
)


def save_figure(
    fig: go.Figure,
    filepath: str,
    size: FigureSize,
    filetypes: Union[list[str], None] = None,
    **write_image_kwargs: dict[Any, Any],
) -> None:
    """Saves the current figure to a file without any margins or padding.

    Args:
        fig (go.Figure): The figure to save.
        filepath (str): The path to save the figure to.
        size (FigureSize): The size of the figure.
        filetypes (list[str], optional): The file types(s) to save the figure to.
            If None, the original filetype of `filepath` is used.
            If the original filetype is not in `filetypes`, it is appended to the list.
        **write_image_kwargs: Additional keyword arguments to pass to `fig.write_image`.
    """
    # By default, our Plotly template attempts to add 40 pixels of margin on all sides.
    # However, due to Plotly's internal automargin strategy, the margin is not always
    # applied correctly, resulting in a figure that is not the correct size.
    #
    # For exports, we want to remove the margins and update the figure dimensions
    # so that the correct margins can be applied in Adobe Illustrator.
    # TODO(#69): Write a custom function to apply the margins.
    updated_margins = dict(l=0, r=0, t=0, b=0)
    updated_width = FIGURE_SIZES_IN_PIXELS[size][0] - 80
    updated_height = FIGURE_SIZES_IN_PIXELS[size][1] - 80

    # For some reason, the axis linewidths (which are set to 1 px) are being rendered as
    # 1 pt in Illustrator. Manually setting these to 0.75 px renders them as 0.75 pt.
    updated_axis_linewidth = 0.75

    fig_export = go.Figure(fig)
    fig_export.update_layout(
        margin=updated_margins,
        width=updated_width,
        height=updated_height,
        xaxis=dict(linewidth=updated_axis_linewidth),
        yaxis=dict(linewidth=updated_axis_linewidth),
    )

    # If no file types are provided, use the filetype from the file path.
    valid_filetypes = ["png", "jpg", "jpeg", "webp", "svg", "pdf"]

    filename = Path(filepath).with_suffix("")
    filetype = Path(filepath).suffix[1:]

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
        fig_export.write_image(f"{filename}.{ftype}", **write_image_kwargs)


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
        row (int, optional): The row index of the subplot to modify.
        col (int, optional): The column index of the subplot to modify.
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
        row (int, optional): The row index of the subplot to modify.
        col (int, optional): The column index of the subplot to modify.
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
        row (int, optional): The row index of the subplot to modify.
        col (int, optional): The column index of the subplot to modify.
    """
    set_xticklabel_font(fig, font, font_size, row, col)
    set_yticklabel_font(fig, font, font_size, row, col)


def set_xticklabel_monospaced(
    fig: go.Figure, row: Union[int, None] = None, col: Union[int, None] = None
) -> None:
    """Sets the font of the x-axis ticklabels to the default monospace font.

    Args:
        fig (go.Figure): The Plotly figure to modify.
        row (int, optional): The row index of the subplot to modify.
        col (int, optional): The column index of the subplot to modify.
    """
    set_xticklabel_font(fig, MONOSPACE_FONT_PLOTLY, font_size=MONOSPACE_FONT_SIZE, row=row, col=col)


def set_yticklabel_monospaced(
    fig: go.Figure, row: Union[int, None] = None, col: Union[int, None] = None
) -> None:
    """Sets the font of the y-axis ticklabels to the default monospace font.

    Args:
        fig (go.Figure): The Plotly figure to modify.
        row (int, optional): The row index of the subplot to modify.
        col (int, optional): The column index of the subplot to modify.
    """
    set_yticklabel_font(fig, MONOSPACE_FONT_PLOTLY, font_size=MONOSPACE_FONT_SIZE, row=row, col=col)


def set_colorbar_ticklabel_monospaced(
    fig: go.Figure, row: Union[int, None] = None, col: Union[int, None] = None
) -> None:
    """Sets the font of the colorbar ticklabels to the default monospace font.

    Args:
        fig (go.Figure): The Plotly figure to modify.
        row (int, optional): The row index of the subplot to modify.
        col (int, optional): The column index of the subplot to modify.
    """
    fig.update_coloraxes(
        tickfont_family=MONOSPACE_FONT_PLOTLY, tickfont_size=MONOSPACE_FONT_SIZE, row=row, col=col
    )


def set_ticklabel_monospaced(
    fig: go.Figure, row: Union[int, None] = None, col: Union[int, None] = None
) -> None:
    """Sets the font of both the x- and y-axis ticklabels to the default monospace font.

    Args:
        fig (go.Figure): The Plotly figure to modify.
        row (int, optional): The row index of the subplot to modify.
        col (int, optional): The column index of the subplot to modify.
    """
    set_xticklabel_monospaced(fig, row, col)
    set_yticklabel_monospaced(fig, row, col)


def capitalize_xticklabels(
    fig: go.Figure, row: Union[int, None] = None, col: Union[int, None] = None
) -> None:
    """Capitalizes the x-axis ticklabels.

    Args:
        fig (go.Figure): The Plotly figure to modify.
        row (int, optional): The row index of the subplot to modify.
        col (int, optional): The column index of the subplot to modify.
    """
    fig.update_xaxes(ticktext=fig.xaxes[0].ticktext.capitalize(), row=row, col=col)  # type: ignore


def capitalize_yticklabels(
    fig: go.Figure, row: Union[int, None] = None, col: Union[int, None] = None
) -> None:
    """Capitalizes the y-axis ticklabels.

    Args:
        fig (go.Figure): The Plotly figure to modify.
        row (int, optional): The row index of the subplot to modify.
        col (int, optional): The column index of the subplot to modify.
    """
    fig.update_yaxes(ticktext=fig.yaxes[0].ticktext.capitalize(), row=row, col=col)  # type: ignore


def capitalize_ticklabels(
    fig: go.Figure, row: Union[int, None] = None, col: Union[int, None] = None
) -> None:
    """Capitalizes both the x- and y-axis ticklabels.

    Args:
        fig (go.Figure): The Plotly figure to modify.
        row (int, optional): The row index of the subplot to modify.
        col (int, optional): The column index of the subplot to modify.
    """
    capitalize_xticklabels(fig, row, col)
    capitalize_yticklabels(fig, row, col)


def add_commas_to_axis_tick_labels(fig: go.Figure) -> None:
    """Adds commas to the numbers used for axis ticklabels.

    For example, transform 1000000 to 1,000,000.
    """
    fig.update_layout(xaxis=dict(tickformat=","))
    fig.update_layout(yaxis=dict(tickformat=","))


def set_xaxis_categorical(
    fig: go.Figure, row: Union[int, None] = None, col: Union[int, None] = None
) -> None:
    """Sets the style of the x-axis to a categorical axis by removing ticks.

    Args:
        fig (go.Figure): The Plotly figure to modify.
        row (int, optional): The row index of the subplot to modify.
        col (int, optional): The column index of the subplot to modify.
    """
    # TODO: We should also adjust the margins between the ticklabels and the axis labels.
    fig.update_xaxes(ticks="", row=row, col=col)


def set_yaxis_categorical(
    fig: go.Figure, row: Union[int, None] = None, col: Union[int, None] = None
) -> None:
    """Sets the style of the y-axis to a categorical axis by removing ticks.

    Args:
        fig (go.Figure): The Plotly figure to modify.
        row (int, optional): The row index of the subplot to modify.
        col (int, optional): The column index of the subplot to modify.
    """
    # TODO: We should also adjust the margins between the ticklabels and the axis labels.
    fig.update_yaxes(ticks="", row=row, col=col)


def set_axes_categorical(
    fig: go.Figure, row: Union[int, None] = None, col: Union[int, None] = None
) -> None:
    """Sets both the x- and y-axes to categorical axes by removing ticks.

    Args:
        fig (go.Figure): The Plotly figure to modify.
        row (int, optional): The row index of the subplot to modify.
        col (int, optional): The column index of the subplot to modify.
    """
    set_xaxis_categorical(fig, row, col)
    set_yaxis_categorical(fig, row, col)


def capitalize_ylabel(
    fig: go.Figure, row: Union[int, None] = None, col: Union[int, None] = None
) -> None:
    """Capitalizes the y-axis label.

    Args:
        fig (go.Figure): The Plotly figure to modify.
        row (int, optional): The row index of the subplot to modify.
        col (int, optional): The column index of the subplot to modify.
    """
    fig.update_yaxes(title_text=fig.yaxes[0].title.text.capitalize(), row=row, col=col)  # type: ignore


def capitalize_xlabel(
    fig: go.Figure, row: Union[int, None] = None, col: Union[int, None] = None
) -> None:
    """Capitalizes the x-axis label.

    Args:
        fig (go.Figure): The Plotly figure to modify.
        row (int, optional): The row index of the subplot to modify.
        col (int, optional): The column index of the subplot to modify.
    """
    fig.update_xaxes(title_text=fig.xaxes[0].title.text.capitalize(), row=row, col=col)  # type: ignore


def capitalize_axislabels(
    fig: go.Figure, row: Union[int, None] = None, col: Union[int, None] = None
) -> None:
    """Capitalizes both the x and y axis labels.

    Args:
        fig (go.Figure): The Plotly figure to modify.
        row (int, optional): The row index of the subplot to modify.
        col (int, optional): The column index of the subplot to modify.
    """
    capitalize_xlabel(fig, row, col)
    capitalize_ylabel(fig, row, col)


def hide_yaxis_ticks(
    fig: go.Figure, row: Union[int, None] = None, col: Union[int, None] = None
) -> None:
    """Hides the ticks and ticklabels on the y-axis.

    Args:
        fig (go.Figure): The Plotly figure to modify.
        row (int, optional): The row index of the subplot to modify.
        col (int, optional): The column index of the subplot to modify.
    """
    fig.update_yaxes(ticks="", showticklabels=False, row=row, col=col)


def hide_xaxis_ticks(
    fig: go.Figure, row: Union[int, None] = None, col: Union[int, None] = None
) -> None:
    """Hides the ticks and ticklabelson the x-axis.

    Args:
        fig (go.Figure): The Plotly figure to modify.
        row (int, optional): The row index of the subplot to modify.
        col (int, optional): The column index of the subplot to modify.
    """
    fig.update_xaxes(ticks="", showticklabels=False, row=row, col=col)


def hide_ticks(fig: go.Figure, row: Union[int, None] = None, col: Union[int, None] = None) -> None:
    """Hides the ticks and ticklabels on both the x- and y-axes.

    Args:
        fig (go.Figure): The Plotly figure to modify.
        row (int, optional): The row index of the subplot to modify.
        col (int, optional): The column index of the subplot to modify.
    """
    hide_xaxis_ticks(fig, row, col)
    hide_yaxis_ticks(fig, row, col)


def hide_yaxis_line(
    fig: go.Figure, row: Union[int, None] = None, col: Union[int, None] = None
) -> None:
    """Hides the y-axis line.

    Args:
        fig (go.Figure): The Plotly figure to modify.
        row (int, optional): The row index of the subplot to modify.
        col (int, optional): The column index of the subplot to modify.
    """
    fig.update_yaxes(showline=False, row=row, col=col)


def hide_xaxis_line(
    fig: go.Figure, row: Union[int, None] = None, col: Union[int, None] = None
) -> None:
    """Hides the x-axis line.

    Args:
        fig (go.Figure): The Plotly figure to modify.
        row (int, optional): The row index of the subplot to modify.
        col (int, optional): The column index of the subplot to modify.
    """
    fig.update_xaxes(showline=False, row=row, col=col)


def hide_axis_lines(
    fig: go.Figure, row: Union[int, None] = None, col: Union[int, None] = None
) -> None:
    """Hides the x-axis and y-axis lines.

    Args:
        fig (go.Figure): The Plotly figure to modify.
        row (int, optional): The row index of the subplot to modify.
        col (int, optional): The column index of the subplot to modify.
    """
    hide_yaxis_line(fig, row, col)
    hide_xaxis_line(fig, row, col)


def capitalize_legend_title(fig: go.Figure) -> None:
    """Capitalizes the legend title.

    Plotly does have the `legend_font_textcase` attribute, but the CSS styles are not
    applied correctly in SVG exports, so we manually mutate the legend entries instead.
    """
    legend_title_text = fig.layout.legend.title.text  # type: ignore
    if legend_title_text and not legend_title_text.isupper():
        fig.update_layout(legend_title_text=legend_title_text.capitalize())


def capitalize_legend_entries(fig: go.Figure) -> None:
    """Capitalizes the legend entries.

    Plotly does have the `legend_font_textcase` attribute, but the CSS styles are not
    applied correctly in SVG exports, so we manually mutate the legend entries instead.
    """
    for trace in fig.data:
        if trace.name and not trace.name.isupper():
            trace.name = trace.name.capitalize()


def get_arcadia_styles() -> dict[str, Any]:
    """Returns the Arcadia Plotly layout template as a dictionary."""
    return ARCADIA_PLOTLY_TEMPLATE_LAYOUT.to_plotly_json()


def style_legend(fig: go.Figure) -> None:
    """Styles the legend according to Arcadia's style guide."""
    capitalize_legend_title(fig)
    capitalize_legend_entries(fig)


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
        monospaced_axes (str, optional): Which axes to set to the default monospaced font.
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


def set_figure_dimensions(fig: go.Figure, size: FigureSize) -> None:
    """Sets the width and height of a figure.

    Args:
        fig (go.Figure): The figure to modify.
        size (FigureSize): The size of the figure, which must be one of the following:
            - "full_wide"
            - "full_square"
            - "float_wide"
            - "float_square"
            - "half_square"

    Raises:
        ValueError: If the size is not one of the predefined panel sizes.
    """
    if size not in FIGURE_SIZES_IN_PIXELS:
        raise ValueError(f"Size must be one of {list(FIGURE_SIZES_IN_PIXELS.keys())}.")

    width, height = FIGURE_SIZES_IN_PIXELS[size]
    fig.update_layout(width=width, height=height)


def setup() -> None:
    """Loads Arcadia fonts and styles into Plotly."""
    arcadia_template = go.layout.Template(layout=ARCADIA_PLOTLY_TEMPLATE_LAYOUT)
    pio.templates["arcadia"] = arcadia_template
    pio.templates.default = "arcadia"
