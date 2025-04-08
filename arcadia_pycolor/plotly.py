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
    pass


def save_figure(
    fig: go.Figure,
    filepath: str,
    filetypes: Union[list[str], None] = None,
    **write_image_kwargs: dict[Any, Any],
) -> None:
    """Saves the current figure to a file using Arcadia's margin and padding settings.

    Args:
        fig (go.Figure): The figure to save.
        filepath (str): Path to save the figure to.
        filetypes (list[str], optional): The file types(s) to save the figure to.
            If None, the original filetype of `filepath` is used.
            If the original filetype is not in `filetypes`, it is appended to the list.
        **write_image_kwargs: Additional keyword arguments to pass to `fig.write_image`.
    """
    valid_filetypes = ["png", "jpg", "jpeg", "webp", "svg", "pdf"]

    filename = Path(filepath).with_suffix("")
    filetype = Path(filepath).suffix[1:]

    # By default, our Plotly template results in a margin of 40 pixels on all sides.
    # We want to reduce this to 20 pixels on all sides, and update the dimensions to
    # account for the reduced margin.
    updated_margins = {key: (value - 20) for key, value in get_arcadia_styles("margin").items()}
    updated_width = fig.layout.width - 20  # type: ignore
    updated_height = fig.layout.height - 20  # type: ignore

    fig_export = go.Figure(fig)
    fig_export.update_layout(margin=updated_margins, width=updated_width, height=updated_height)

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

        fig.write_image(f"{filename}.{ftype}", **write_image_kwargs)

        if ftype == "svg":
            _fix_svg_fonts_for_illustrator(f"{filename}.svg")


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
    """Sets the font of the x-axis ticklabels to a monospace font.

    Args:
        fig (go.Figure): The Plotly figure to modify.
        row (int, optional): The row index of the subplot to modify.
        col (int, optional): The column index of the subplot to modify.
    """
    set_xticklabel_font(fig, MONOSPACE_FONT_PLOTLY, font_size=MONOSPACE_FONT_SIZE, row=row, col=col)


def set_yticklabel_monospaced(
    fig: go.Figure, row: Union[int, None] = None, col: Union[int, None] = None
) -> None:
    """Sets the font of the y-axis ticklabels to a monospace font.

    Args:
        fig (go.Figure): The Plotly figure to modify.
        row (int, optional): The row index of the subplot to modify.
        col (int, optional): The column index of the subplot to modify.
    """
    set_yticklabel_font(fig, MONOSPACE_FONT_PLOTLY, font_size=MONOSPACE_FONT_SIZE, row=row, col=col)


def set_colorbar_ticklabel_monospaced(
    fig: go.Figure, row: Union[int, None] = None, col: Union[int, None] = None
) -> None:
    """Sets the font of the colorbar ticklabels to a monospace font.

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
    """Sets the font of both the x- and y-axis ticklabels to a monospace font.

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
    """Sets the style of the x-axis to a categorical axis, removing ticks and adjusting padding.

    Args:
        fig (go.Figure): The Plotly figure to modify.
        row (int, optional): The row index of the subplot to modify.
        col (int, optional): The column index of the subplot to modify.
    """
    fig.update_xaxes(ticks="", row=row, col=col)


def set_yaxis_categorical(
    fig: go.Figure, row: Union[int, None] = None, col: Union[int, None] = None
) -> None:
    """Sets the style of the y-axis to a categorical axis, removing ticks and adjusting padding.

    Args:
        fig (go.Figure): The Plotly figure to modify.
        row (int, optional): The row index of the subplot to modify.
        col (int, optional): The column index of the subplot to modify.
    """
    fig.update_yaxes(ticks="", row=row, col=col)


def set_axes_categorical(
    fig: go.Figure, row: Union[int, None] = None, col: Union[int, None] = None
) -> None:
    """Sets both the x- and y-axes to categorical axes, removing ticks and adjusting padding.

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


def hide_xaxis_ticks(
    fig: go.Figure, row: Union[int, None] = None, col: Union[int, None] = None
) -> None:
    """Hides the ticks on the x-axis.

    Args:
        fig (go.Figure): The Plotly figure to modify.
        row (int, optional): The row index of the subplot to modify.
        col (int, optional): The column index of the subplot to modify.
    """
    fig.update_xaxes(ticks="", showticklabels=False, row=row, col=col)


def hide_yaxis_ticks(
    fig: go.Figure, row: Union[int, None] = None, col: Union[int, None] = None
) -> None:
    """Hides the ticks on the y-axis.

    Args:
        fig (go.Figure): The Plotly figure to modify.
        row (int, optional): The row index of the subplot to modify.
        col (int, optional): The column index of the subplot to modify.
    """
    fig.update_yaxes(ticks="", showticklabels=False, row=row, col=col)


def hide_ticks(fig: go.Figure, row: Union[int, None] = None, col: Union[int, None] = None) -> None:
    """Hides the ticks on both the x- and y-axes.

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
    """Hides the line on the y-axis.

    Args:
        fig (go.Figure): The Plotly figure to modify.
        row (int, optional): The row index of the subplot to modify.
        col (int, optional): The column index of the subplot to modify.
    """
    fig.update_yaxes(showline=False, row=row, col=col)


def hide_xaxis_line(
    fig: go.Figure, row: Union[int, None] = None, col: Union[int, None] = None
) -> None:
    """Hides the line on the x-axis.

    Args:
        fig (go.Figure): The Plotly figure to modify.
        row (int, optional): The row index of the subplot to modify.
        col (int, optional): The column index of the subplot to modify.
    """
    fig.update_xaxes(showline=False, row=row, col=col)


def hide_axis_lines(
    fig: go.Figure, row: Union[int, None] = None, col: Union[int, None] = None
) -> None:
    """Hides the lines on both the x- and y-axes.

    Args:
        fig (go.Figure): The Plotly figure to modify.
        row (int, optional): The row index of the subplot to modify.
        col (int, optional): The column index of the subplot to modify.
    """
    hide_yaxis_line(fig, row, col)
    hide_xaxis_line(fig, row, col)


def capitalize_legend_title(fig: go.Figure) -> None:
    """Capitalizes the legend title."""
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


def capitalize_legend_text(fig: go.Figure) -> None:
    """Capitalize the legend title and entries."""
    capitalize_legend_title(fig)
    capitalize_legend_entries(fig)


def get_arcadia_styles(key: Union[str, None] = None) -> Union[dict[str, Any], Any]:
    """Returns the styles for the given key from the Arcadia Plotly template.

    Args:
        key (str, optional): The key (or nested keys separated by dots) to access the styles.
            If None, returns the entire Arcadia Plotly template.

    Returns:
        dict[str, Any] | Any: The styles for the given key.
    """
    value = ARCADIA_PLOTLY_TEMPLATE_LAYOUT.to_plotly_json()
    if key is None:
        return value

    keys = key.split(".")

    for key in keys:
        value = value.get(key)
        if value is None:
            raise ValueError(f"Key {key} not found in Arcadia Plotly template.")

    return value


def get_colorbar_styles() -> Union[dict[str, Any], Any]:
    """Returns the colorbar styles from the Arcadia Plotly template."""
    return get_arcadia_styles("coloraxis.colorbar")


def style_legend(fig: go.Figure) -> None:
    """Styles the legend according to Arcadia's style guide."""
    capitalize_legend_text(fig)


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


def set_figure_dimensions(fig: go.Figure, size: FigureSize) -> None:
    """Sets the width and height of a figure.

    Args:
        fig (go.Figure): The figure to modify.
        size (PanelSize): The size of the figure, which must be one of the following:
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
    """Loads all Arcadia colors, fonts, styles, and colormaps into Plotly."""
    arcadia_template = go.layout.Template(layout=ARCADIA_PLOTLY_TEMPLATE_LAYOUT)
    pio.templates["arcadia"] = arcadia_template
    pio.templates.default = "arcadia"
