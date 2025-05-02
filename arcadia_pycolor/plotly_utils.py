from pathlib import Path
from typing import Any, Literal, Union, get_args

import plotly.graph_objects as go
import plotly.io as pio
from bs4 import BeautifulSoup

from arcadia_pycolor.style_defaults import (
    ARCADIA_PLOTLY_TEMPLATE_LAYOUT,
    DEFAULT_FONT_PLOTLY,
    FIGURE_SIZES_IN_PIXELS,
    MONOSPACE_FONT_PLOTLY,
    MONOSPACE_FONT_SIZE,
    PLOTLY_HTML_EXPORT_CSS,
    FigureSize,
)

# Reference: https://plotly.com/python/3d-charts/.
PLOTLY_3D_TRACE_TYPES = (
    go.Mesh3d,
    go.Scatter3d,
    go.Cone,
    go.Isosurface,
    go.Surface,
    go.Volume,
    go.Contour,
    go.Parcoords,
    go.Streamtube,
)

AxisSelector = Literal["x", "y", "z", "xy", "yz", "xz", "xyz", "all"]


def _has_subplots(fig: go.Figure) -> bool:
    layout_keys = fig.layout.to_plotly_json().keys()  # type: ignore
    xaxes = [key for key in layout_keys if key.startswith("xaxis")]
    yaxes = [key for key in layout_keys if key.startswith("yaxis")]
    return len(xaxes) > 1 or len(yaxes) > 1


def _is_3d_plot(fig: go.Figure, row: Union[int, None] = None, col: Union[int, None] = None) -> bool:
    """Returns True if the figure data only contains 3D traces."""
    if _has_subplots(fig) and row is not None and col is not None:
        return isinstance(fig.get_subplot(row, col), go.layout.Scene)
    return isinstance(fig.data[0], PLOTLY_3D_TRACE_TYPES)


def _is_plot_with_3d_traces(fig: go.Figure) -> bool:
    """Returns True if the figure data contains any 3D traces."""
    return any(isinstance(trace, PLOTLY_3D_TRACE_TYPES) for trace in fig.data)


def _is_plot_with_3d_traces_only(fig: go.Figure) -> bool:
    """Returns True if the figure data only contains 3D traces."""
    return all(isinstance(trace, PLOTLY_3D_TRACE_TYPES) for trace in fig.data)


def _is_plot_with_colorbar(fig: go.Figure) -> bool:
    """Returns True if the figure layout contains a non-emptycolorbar."""
    return len(fig.layout.coloraxis.colorbar.to_plotly_json()) > 0  # type: ignore


def _is_plot_with_legend(fig: go.Figure) -> bool:
    """Returns True if the figure layout contains a non-empty legend."""
    return len(fig.layout.legend.to_plotly_json()) > 0  # type: ignore


def _revert_to_default_fonts(fig: go.Figure) -> None:
    """Reverts the fonts in a Plotly figure to the default Plotly fonts."""
    template_without_fonts = go.Layout(**ARCADIA_PLOTLY_TEMPLATE_LAYOUT.to_plotly_json())

    template_without_fonts.update(
        font_family=None,
        title_font_family=None,
        legend_title_font_family=None,
        legend_font_family=None,
        hoverlabel_font_family=None,
        coloraxis_colorbar_title_font_family=None,
        coloraxis_colorbar_tickfont_family="monospace",
        xaxis_title_font_family=None,
        yaxis_title_font_family=None,
        scene_xaxis_title_font_family=None,
        scene_yaxis_title_font_family=None,
        scene_zaxis_title_font_family=None,
    )

    is_monospaced_xaxis = fig.layout.xaxis.tickfont.family == MONOSPACE_FONT_PLOTLY  # type: ignore
    is_monospaced_yaxis = fig.layout.yaxis.tickfont.family == MONOSPACE_FONT_PLOTLY  # type: ignore

    fig.update_layout(
        xaxis_tickfont_family="monospace" if is_monospaced_xaxis else None,
        yaxis_tickfont_family="monospace" if is_monospaced_yaxis else None,
        xaxis_tickfont_size=13.5 if is_monospaced_xaxis else None,
        yaxis_tickfont_size=13.5 if is_monospaced_yaxis else None,
    )

    is_monospaced_xaxis = fig.layout.scene.xaxis.tickfont.family == MONOSPACE_FONT_PLOTLY  # type: ignore
    is_monospaced_yaxis = fig.layout.scene.yaxis.tickfont.family == MONOSPACE_FONT_PLOTLY  # type: ignore
    is_monospaced_zaxis = fig.layout.scene.zaxis.tickfont.family == MONOSPACE_FONT_PLOTLY  # type: ignore

    fig.update_scenes(
        xaxis_title_font_family=None,
        yaxis_title_font_family=None,
        zaxis_title_font_family=None,
        xaxis_tickfont_family="monospace" if is_monospaced_xaxis else None,
        yaxis_tickfont_family="monospace" if is_monospaced_yaxis else None,
        zaxis_tickfont_family="monospace" if is_monospaced_zaxis else None,
        xaxis_tickfont_size=13.5 if is_monospaced_xaxis else None,
        yaxis_tickfont_size=13.5 if is_monospaced_yaxis else None,
        zaxis_tickfont_size=13.5 if is_monospaced_zaxis else None,
    )

    fig.update_layout(template=dict(layout=template_without_fonts))


def _add_fonts_to_plotly_html_export(filepath: str) -> None:
    """Adds a style tag with fonts loaded from arcadiascience.com to an HTML file's head section.

    This is necessary for embeds of Plotly HTML exports to use the Suisse fonts.

    Args:
        filepath (str): Path to the HTML file to modify.
    """
    with open(filepath) as f:
        content = f.read()

    soup = BeautifulSoup(content, "html.parser")

    style_tag = soup.new_tag("style")
    style_tag.string = PLOTLY_HTML_EXPORT_CSS

    if soup.head is None:
        raise ValueError("Could not find <head> tag in HTML file.")
    soup.head.append(style_tag)

    with open(filepath, "w") as f:
        f.write(str(soup))


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


def export_to_html(fig: go.Figure, filepath: str) -> None:
    """
    Exports the current figure to an HTML file and adds fonts loaded from arcadiascience.com,
    allowing the figure to be embedded on webpages without requiring fonts to be installed.

    If the figure contains 3D traces, all fonts are reverted to default Plotly fonts.
    This is because HTML exports of 3D plots do not apply remotely loaded fonts correctly.
    See this issue for more details: https://github.com/plotly/plotly.js/issues/7413.

    Args:
        fig (go.Figure): The figure to export.
        filepath (str): The path to save the figure to.
    """

    if _is_plot_with_3d_traces(fig):
        _revert_to_default_fonts(fig)
        fig.write_html(filepath)
    else:
        fig.write_html(filepath)
        _add_fonts_to_plotly_html_export(filepath)


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
    if _is_3d_plot(fig, row, col):
        fig.update_scenes(yaxis_tickfont_family=font, row=row, col=col)
        if font_size is not None:
            fig.update_scenes(yaxis_tickfont_size=font_size, row=row, col=col)
    else:
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
    if _is_3d_plot(fig, row, col):
        fig.update_scenes(xaxis_tickfont_family=font, row=row, col=col)
        if font_size is not None:
            fig.update_scenes(xaxis_tickfont_size=font_size, row=row, col=col)
    else:
        fig.update_xaxes(tickfont_family=font, row=row, col=col)
        if font_size is not None:
            fig.update_xaxes(tickfont_size=font_size, row=row, col=col)


def set_zticklabel_font(
    fig: go.Figure,
    font: str = DEFAULT_FONT_PLOTLY,
    font_size: Union[float, None] = None,
    row: Union[int, None] = None,
    col: Union[int, None] = None,
) -> None:
    """Sets the font and font size of the z-axis tick labels for a Plotly figure.

    Args:
        fig (go.Figure): The Plotly figure to modify.
        font (str): The font family to use for the tick labels.
        font_size (float, optional): The font size to use for the tick labels.
            If None, keeps current size.
        row (int, optional): The row index of the subplot to modify.
        col (int, optional): The column index of the subplot to modify.
    """
    fig.update_scenes(zaxis_tickfont_family=font, row=row, col=col)
    if font_size is not None:
        fig.update_scenes(zaxis_tickfont_size=font_size, row=row, col=col)


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
    if _is_3d_plot(fig, row, col):
        set_zticklabel_font(fig, font, font_size, row, col)


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


def set_zticklabel_monospaced(
    fig: go.Figure, row: Union[int, None] = None, col: Union[int, None] = None
) -> None:
    """Sets the font of the z-axis ticklabels to the default monospace font.

    Args:
        fig (go.Figure): The Plotly figure to modify.
        row (int, optional): The row index of the subplot to modify.
        col (int, optional): The column index of the subplot to modify.
    """
    set_zticklabel_font(fig, MONOSPACE_FONT_PLOTLY, font_size=MONOSPACE_FONT_SIZE, row=row, col=col)


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
        colorbar_tickfont_family=MONOSPACE_FONT_PLOTLY,
        colorbar_tickfont_size=MONOSPACE_FONT_SIZE,
        row=row,
        col=col,
    )


def set_ticklabel_monospaced(
    fig: go.Figure, row: Union[int, None] = None, col: Union[int, None] = None
) -> None:
    """Sets the font of all ticklabels to the default monospace font.

    Args:
        fig (go.Figure): The Plotly figure to modify.
        row (int, optional): The row index of the subplot to modify.
        col (int, optional): The column index of the subplot to modify.
    """
    set_xticklabel_monospaced(fig, row, col)
    set_yticklabel_monospaced(fig, row, col)
    if _is_3d_plot(fig, row, col):
        set_zticklabel_monospaced(fig, row, col)
    if _is_plot_with_colorbar(fig):
        set_colorbar_ticklabel_monospaced(fig, row, col)


def capitalize_xticklabels(
    fig: go.Figure, row: Union[int, None] = None, col: Union[int, None] = None
) -> None:
    """Capitalizes the x-axis ticklabels.

    Args:
        fig (go.Figure): The Plotly figure to modify.
        row (int, optional): The row index of the subplot to modify.
        col (int, optional): The column index of the subplot to modify.
    """
    if _is_3d_plot(fig, row, col):
        ticktext = fig.scenes[0].xaxis_ticktext  # type: ignore
        if ticktext.islower():
            fig.update_scenes(
                xaxis_ticktext=ticktext.capitalize(),
                row=row,
                col=col,
            )
    else:
        capitalized_ticklabels = [
            label.capitalize() if label.islower() else label
            for label in fig.data[0].x  # type: ignore
        ]
        fig.update_xaxes(ticktext=capitalized_ticklabels, row=row, col=col)


def capitalize_yticklabels(
    fig: go.Figure, row: Union[int, None] = None, col: Union[int, None] = None
) -> None:
    """Capitalizes the y-axis ticklabels if all letters are lowercase.

    Args:
        fig (go.Figure): The Plotly figure to modify.
        row (int, optional): The row index of the subplot to modify.
        col (int, optional): The column index of the subplot to modify.
    """
    if _is_3d_plot(fig, row, col):
        ticktext = fig.scenes[0].yaxis_ticktext  # type: ignore
        if ticktext.islower():
            fig.update_scenes(
                yaxis_ticktext=ticktext.capitalize(),
                row=row,
                col=col,
            )
    else:
        capitalized_ticklabels = [
            label.capitalize() if label.islower() else label
            for label in fig.data[0].y  # type: ignore
        ]
        fig.update_yaxes(ticktext=capitalized_ticklabels, row=row, col=col)


def capitalize_zticklabels(
    fig: go.Figure, row: Union[int, None] = None, col: Union[int, None] = None
) -> None:
    """Capitalizes the z-axis ticklabels if all letters are lowercase.

    Args:
        fig (go.Figure): The Plotly figure to modify.
        row (int, optional): The row index of the subplot to modify.
        col (int, optional): The column index of the subplot to modify.
    """
    ticktext = fig.scenes[0].zaxis_ticktext  # type: ignore
    if ticktext.islower():
        fig.update_scenes(
            zaxis_ticktext=ticktext.capitalize(),
            row=row,
            col=col,
        )


def capitalize_ticklabels(
    fig: go.Figure, row: Union[int, None] = None, col: Union[int, None] = None
) -> None:
    """Capitalizes ticklabels for the x- and y-axes, and z-axis if applicable,
    if all letters are lowercase.

    Args:
        fig (go.Figure): The Plotly figure to modify.
        row (int, optional): The row index of the subplot to modify.
        col (int, optional): The column index of the subplot to modify.
    """
    capitalize_xticklabels(fig, row, col)
    capitalize_yticklabels(fig, row, col)
    if _is_3d_plot(fig, row, col):
        capitalize_zticklabels(fig, row, col)


def add_commas_to_xaxis_ticklabels(
    fig: go.Figure, row: Union[int, None] = None, col: Union[int, None] = None
) -> None:
    """Adds commas to the x-axis ticklabels.

    Args:
        fig (go.Figure): The Plotly figure to modify.
        row (int, optional): The row index of the subplot to modify.
        col (int, optional): The column index of the subplot to modify.
    """
    if _is_3d_plot(fig, row, col):
        fig.update_scenes(xaxis_tickformat=",", row=row, col=col)
    else:
        fig.update_xaxes(tickformat=",", row=row, col=col)


def add_commas_to_yaxis_ticklabels(
    fig: go.Figure, row: Union[int, None] = None, col: Union[int, None] = None
) -> None:
    """Adds commas to the y-axis ticklabels.

    Args:
        fig (go.Figure): The Plotly figure to modify.
        row (int, optional): The row index of the subplot to modify.
        col (int, optional): The column index of the subplot to modify.
    """
    if _is_3d_plot(fig, row, col):
        fig.update_scenes(yaxis_tickformat=",", row=row, col=col)
    else:
        fig.update_yaxes(tickformat=",", row=row, col=col)


def add_commas_to_zaxis_ticklabels(
    fig: go.Figure, row: Union[int, None] = None, col: Union[int, None] = None
) -> None:
    """Adds commas to the z-axis ticklabels.

    Args:
        fig (go.Figure): The Plotly figure to modify.
        row (int, optional): The row index of the subplot to modify.
        col (int, optional): The column index of the subplot to modify.
    """
    fig.update_scenes(zaxis_tickformat=",", row=row, col=col)


def add_commas_to_axis_tick_labels(
    fig: go.Figure, row: Union[int, None] = None, col: Union[int, None] = None
) -> None:
    """Adds commas to the numbers used for axis ticklabels.

    For example, transform 1000000 to 1,000,000.

    Args:
        fig (go.Figure): The Plotly figure to modify.
        row (int, optional): The row index of the subplot to modify.
        col (int, optional): The column index of the subplot to modify.
    """
    add_commas_to_xaxis_ticklabels(fig, row, col)
    add_commas_to_yaxis_ticklabels(fig, row, col)
    if _is_3d_plot(fig, row, col):
        add_commas_to_zaxis_ticklabels(fig, row, col)


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
    if _is_3d_plot(fig, row, col):
        fig.update_scenes(xaxis_ticks="", row=row, col=col)
    else:
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
    if _is_3d_plot(fig, row, col):
        fig.update_scenes(yaxis_ticks="", row=row, col=col)
    else:
        fig.update_yaxes(ticks="", row=row, col=col)


def set_zaxis_categorical(
    fig: go.Figure, row: Union[int, None] = None, col: Union[int, None] = None
) -> None:
    """Sets the style of the z-axis to a categorical axis by removing ticks.

    Args:
        fig (go.Figure): The Plotly figure to modify.
        row (int, optional): The row index of the subplot to modify.
        col (int, optional): The column index of the subplot to modify.
    """
    fig.update_scenes(zaxis_ticks="", row=row, col=col)


def set_axes_categorical(
    fig: go.Figure, row: Union[int, None] = None, col: Union[int, None] = None
) -> None:
    """Sets all axes to categorical axes by removing ticks.

    Args:
        fig (go.Figure): The Plotly figure to modify.
        row (int, optional): The row index of the subplot to modify.
        col (int, optional): The column index of the subplot to modify.
    """
    set_xaxis_categorical(fig, row, col)
    set_yaxis_categorical(fig, row, col)
    if _is_3d_plot(fig, row, col):
        set_zaxis_categorical(fig, row, col)


def capitalize_ylabel(
    fig: go.Figure, row: Union[int, None] = None, col: Union[int, None] = None
) -> None:
    """Capitalizes the y-axis label if all letters are lowercase.

    Args:
        fig (go.Figure): The Plotly figure to modify.
        row (int, optional): The row index of the subplot to modify.
        col (int, optional): The column index of the subplot to modify.
    """
    if _is_3d_plot(fig, row, col):
        label = fig.layout.scene.yaxis.title.text  # type: ignore
        if label and label.islower():
            fig.update_scenes(
                yaxis_title_text=label.capitalize(),
                row=row,
                col=col,
            )
    else:
        label = fig.layout.yaxis.title.text  # type: ignore
        if label and label.islower():
            fig.update_yaxes(title_text=label.capitalize(), row=row, col=col)


def capitalize_xlabel(
    fig: go.Figure, row: Union[int, None] = None, col: Union[int, None] = None
) -> None:
    """Capitalizes the x-axis label if all letters are lowercase.

    Args:
        fig (go.Figure): The Plotly figure to modify.
        row (int, optional): The row index of the subplot to modify.
        col (int, optional): The column index of the subplot to modify.
    """
    if _is_3d_plot(fig, row, col):
        label = fig.layout.scene.xaxis.title.text  # type: ignore
        if label and label.islower():
            fig.update_scenes(
                xaxis_title_text=label.capitalize(),
                row=row,
                col=col,
            )
    else:
        label = fig.layout.xaxis.title.text  # type: ignore
        if label and label.islower():
            fig.update_xaxes(title_text=label.capitalize(), row=row, col=col)


def capitalize_zlabel(
    fig: go.Figure, row: Union[int, None] = None, col: Union[int, None] = None
) -> None:
    """Capitalizes the z-axis label if all letters are lowercase.

    Args:
        fig (go.Figure): The Plotly figure to modify.
        row (int, optional): The row index of the subplot to modify.
        col (int, optional): The column index of the subplot to modify.
    """
    label = fig.layout.scene.zaxis.title.text  # type: ignore
    if label and label.islower():
        fig.update_scenes(zaxis_title_text=label.capitalize(), row=row, col=col)


def capitalize_colorbar_label(
    fig: go.Figure, row: Union[int, None] = None, col: Union[int, None] = None
) -> None:
    """Capitalizes the colorbar label if all letters are lowercase.

    Args:
        fig (go.Figure): The Plotly figure to modify.
        row (int, optional): The row index of the subplot to modify.
        col (int, optional): The column index of the subplot to modify.
    """
    label = fig.layout.coloraxis.colorbar.title.text  # type: ignore
    if label and label.islower():
        new_label = label.capitalize()
        fig.update_coloraxes(colorbar_title_text=new_label, row=row, col=col)


def capitalize_axislabels(
    fig: go.Figure, row: Union[int, None] = None, col: Union[int, None] = None
) -> None:
    """Capitalizes all axis labels if all letters are lowercase.

    Args:
        fig (go.Figure): The Plotly figure to modify.
        row (int, optional): The row index of the subplot to modify.
        col (int, optional): The column index of the subplot to modify.
    """
    capitalize_xlabel(fig, row, col)
    capitalize_ylabel(fig, row, col)
    if _is_3d_plot(fig, row, col):
        capitalize_zlabel(fig, row, col)
    if _is_plot_with_colorbar(fig):
        capitalize_colorbar_label(fig, row, col)


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
    if _is_3d_plot(fig, row, col):
        fig.update_scenes(yaxis_ticks="", yaxis_showticklabels=False, row=row, col=col)


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
    if _is_3d_plot(fig, row, col):
        fig.update_scenes(xaxis_ticks="", xaxis_showticklabels=False, row=row, col=col)


def hide_zaxis_ticks(
    fig: go.Figure, row: Union[int, None] = None, col: Union[int, None] = None
) -> None:
    """Hides the ticks and ticklabels on the z-axis.

    Args:
        fig (go.Figure): The Plotly figure to modify.
        row (int, optional): The row index of the subplot to modify.
        col (int, optional): The column index of the subplot to modify.
    """
    fig.update_scenes(zaxis_ticks="", zaxis_showticklabels=False, row=row, col=col)


def hide_ticks(fig: go.Figure, row: Union[int, None] = None, col: Union[int, None] = None) -> None:
    """Hides the ticks and ticklabels on all axes.

    Args:
        fig (go.Figure): The Plotly figure to modify.
        row (int, optional): The row index of the subplot to modify.
        col (int, optional): The column index of the subplot to modify.
    """
    hide_xaxis_ticks(fig, row, col)
    hide_yaxis_ticks(fig, row, col)
    if _is_3d_plot(fig, row, col):
        hide_zaxis_ticks(fig, row, col)


def hide_yaxis_line(
    fig: go.Figure, row: Union[int, None] = None, col: Union[int, None] = None
) -> None:
    """Hides the y-axis line.

    Args:
        fig (go.Figure): The Plotly figure to modify.
        row (int, optional): The row index of the subplot to modify.
        col (int, optional): The column index of the subplot to modify.
    """
    if _is_3d_plot(fig, row, col):
        fig.update_scenes(yaxis_showline=False, row=row, col=col)
    else:
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
    if _is_3d_plot(fig, row, col):
        fig.update_scenes(xaxis_showline=False, row=row, col=col)
    else:
        fig.update_xaxes(showline=False, row=row, col=col)


def hide_zaxis_line(
    fig: go.Figure, row: Union[int, None] = None, col: Union[int, None] = None
) -> None:
    """Hides the z-axis line.

    Args:
        fig (go.Figure): The Plotly figure to modify.
        row (int, optional): The row index of the subplot to modify.
        col (int, optional): The column index of the subplot to modify.
    """
    fig.update_scenes(zaxis_showline=False, row=row, col=col)


def hide_axis_lines(
    fig: go.Figure, row: Union[int, None] = None, col: Union[int, None] = None
) -> None:
    """Hides all axis lines.

    Args:
        fig (go.Figure): The Plotly figure to modify.
        row (int, optional): The row index of the subplot to modify.
        col (int, optional): The column index of the subplot to modify.
    """
    hide_yaxis_line(fig, row, col)
    hide_xaxis_line(fig, row, col)
    if _is_3d_plot(fig, row, col):
        hide_zaxis_line(fig, row, col)


def capitalize_legend_title(fig: go.Figure) -> None:
    """Capitalizes the legend title if all letters are lowercase.

    Plotly does have the `legend_font_textcase` attribute, but the CSS styles are not
    applied correctly in SVG exports, so we manually mutate the legend entries instead.
    """
    legend_title_text = fig.layout.legend.title.text  # type: ignore
    if legend_title_text and legend_title_text.islower():
        fig.update_layout(legend_title_text=legend_title_text.capitalize())


def capitalize_legend_entries(fig: go.Figure) -> None:
    """Capitalizes the legend entries if all letters are lowercase.

    Plotly does have the `legend_font_textcase` attribute, but the CSS styles are not
    applied correctly in SVG exports, so we manually mutate the legend entries instead.
    """
    for trace in fig.data:
        if trace.name and trace.name.islower():  # type: ignore
            trace.name = trace.name.capitalize()  # type: ignore


def style_legend(fig: go.Figure) -> None:
    """Styles the legend according to Arcadia's style guide."""
    capitalize_legend_title(fig)
    capitalize_legend_entries(fig)


def get_arcadia_styles() -> dict[str, Any]:
    """Returns the Arcadia Plotly layout template as a dictionary."""
    return ARCADIA_PLOTLY_TEMPLATE_LAYOUT.to_plotly_json()


def style_plot(
    fig: go.Figure,
    monospaced_axes: Union[AxisSelector, None] = None,
    categorical_axes: Union[AxisSelector, None] = None,
    row: Union[int, None] = None,
    col: Union[int, None] = None,
) -> None:
    """Styles the plot according to Arcadia's style guide.

    Args:
        fig (go.Figure): The Plotly figure to modify.
        monospaced_axes (AxisSelector, optional): Which axes to set to the default monospaced font.
        categorical_axes (AxisSelector, optional): Which axes to set to categorical.
        row (int, optional): The row index of the subplot to modify.
        col (int, optional): The column index of the subplot to modify.
    """
    valid_axes = get_args(AxisSelector)

    if monospaced_axes is not None and monospaced_axes not in valid_axes:
        raise ValueError(f"monospaced_axes must be one of {valid_axes}, got {monospaced_axes}")
    if categorical_axes is not None and categorical_axes not in valid_axes:
        raise ValueError(f"categorical_axes must be one of {valid_axes}, got {categorical_axes}")

    capitalize_axislabels(fig, row, col)

    if categorical_axes == "all":
        set_axes_categorical(fig, row, col)
    if categorical_axes in ("x", "xy", "xz"):
        set_xaxis_categorical(fig, row, col)
    if categorical_axes in ("y", "xy", "yz"):
        set_yaxis_categorical(fig, row, col)
    if categorical_axes in ("z", "yz", "xz"):
        set_zaxis_categorical(fig, row, col)

    if monospaced_axes == "all":
        set_ticklabel_monospaced(fig, row, col)
        add_commas_to_axis_tick_labels(fig, row, col)
    if monospaced_axes in ("x", "xy", "xz"):
        set_xticklabel_monospaced(fig, row, col)
        add_commas_to_xaxis_ticklabels(fig, row, col)
    if monospaced_axes in ("y", "xy", "yz"):
        set_yticklabel_monospaced(fig, row, col)
        add_commas_to_yaxis_ticklabels(fig, row, col)
    if monospaced_axes in ("z", "yz", "xz"):
        set_zticklabel_monospaced(fig, row, col)
        add_commas_to_zaxis_ticklabels(fig, row, col)

    if _is_plot_with_legend(fig):
        style_legend(fig)

    if _is_plot_with_colorbar(fig):
        set_colorbar_ticklabel_monospaced(fig, row, col)

    # For 3D plots, we overwrite the default margin from the template.
    if _is_plot_with_3d_traces_only(fig):
        fig.update_layout(margin=dict(l=40, r=40, t=40, b=40))


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
