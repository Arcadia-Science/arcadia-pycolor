import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.colors as mc
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from IPython.display import Markdown, display
import colorsys
from colorspacious import cspace_converter, cspace_convert

__all__ = [
    "print_color",
    "slice_dict",
    "reverse_gradient",
    "adjust_lightness",
    "extend_colors",
    "display_palette",
    "display_palette_interactive",
    "plot_color_gradients",
    "plot_color_lightness",
    "simulate_cvd",
    "simulate_cvd_image",
]


def print_color(colors):
    """
    Prints colors to output in an interactive session using HTML formatting.

    Args:
        colors (str, list, or dict)
    """

    # detect what format the input colors are provided as and plot appropriately.
    if type(colors) == str:
        display(
            Markdown(
                "<br>".join(
                    f'<span style="font-family: monospace">{colors} <span style="color: {colors}">██████</span></span>'
                )
            )
        )
    if type(colors) == list:
        display(
            Markdown(
                "<br>".join(
                    f'<span style="font-family: monospace">{color} <span style="color: {color}">██████</span></span>'
                    for color in colors
                )
            )
        )
    elif type(colors) == dict:
        display(
            Markdown(
                "<br>".join(
                    f'<span style="font-family: monospace"> {color} <span style="color: {color}">██████</span> {name}</span>'
                    for name, color in colors.items()
                )
            )
        )
    else:
        print("failed")


def slice_dict(dictionary: dict, lst: list):
    """
    Slices a dictionary using a list of keys.

    Args:
        dictionary (dict): dictionary to slice.
        lst (list): list of keys to use for slicing.
    """
    return {i: dictionary[i] for i in lst if i in dictionary}


def reverse_gradient(grad_dictionary: dict):
    """
    Takes in a gradient dictionary containing a 'color_dict' entry and a 'values' entry and reverses it.

    Args:
        grad_dictionary (dict): a dictionary containing a 'color_dict' where keys are color names and values are color HEX codes, and a 'values' list that contains the value of colors positioned from 0 to 1.
    """

    if "color_dict" not in grad_dictionary or "values" not in grad_dictionary:
        raise TypeError(
            'Gradient dictionary should have both a "color_dict" and a "values" entry.'
        )

    if len(grad_dictionary["color_dict"]) != len(grad_dictionary["values"]):
        raise ValueError(
            "Number of values must be equal to number of color_dict entries."
        )

    keys = [i for i in grad_dictionary["color_dict"]].copy()
    keys.reverse()

    color_dict = {key: grad_dictionary["color_dict"][key] for key in keys}

    values = grad_dictionary["values"].copy()
    values.reverse()
    values = [1 - value for value in values]

    return {"color_dict": color_dict, "values": values}


def adjust_lightness(color: str, amount=0.5) -> str:
    """
    Takes a HEX code or matplotlib color name and adjusts the lightness.
    Values < 1 result in a darker color, whereas values > 1 result in a lighter color.

    Args:
        color (str): hex value (e.g. "#FEACAF") or a valid matplotlib color name (e.g. "tab:blue").
        amount (float): values < 1 produce a darker color and values > 1 produce a lighter color.
    Returns:
        resulting color as HEX string.
    """
    try:
        color_string = mc.cnames[color]
    except:
        color_string = color
    # convert rgb to hls
    color_string = colorsys.rgb_to_hls(*mc.to_rgb(color_string))
    # adjust the lightness in hls space and convert back to rgb
    color_string2 = colorsys.hls_to_rgb(
        color_string[0], max(0, min(1, amount * color_string[1])), color_string[2]
    )
    # return the new rgb as a hex value
    return mc.to_hex(color_string2)


def extend_colors(color_order: list, total_colors: int, how="darken", steps=[]) -> list:
    """
    Checks a list of keys and colors and extends the colors list as needed.

    Args:
        color_keys (list): list of color keys
        color_order (list): list of HEX colors
        steps (list): float list of potential lightness adjustments to make
    Returns:
        extended list of colors, including original colors
    """
    num_cycles = int(np.ceil(total_colors / len(color_order)))

    if len(steps) > 0:
        steps_used = steps
    elif how == "lighten":
        steps_used = [1.1, 1.25, 1.4]
    elif how == "darken":
        steps_used = [0.7, 0.5, 0.3]

    # collector for additional colors
    more_colors = []

    # if there aren't enough cycles, die
    if num_cycles > len(steps_used):
        raise Exception(
            f"Can create up to {len(steps_used) * len(color_order)} colors to use.\nNeeded {total_colors} colors."
        )

    # create additional colors and add to collector
    for n in range(num_cycles - 1):
        color_order_duplicated = [adjust_lightness(color) for color in color_order]
        more_colors.extend(color_order_duplicated)

    output_colors = color_order + more_colors

    return output_colors[:total_colors]


def display_palette(cmap_dicts: list, ncols=1, show=True, figsize=(0, 0)):
    """
    Displays color palettes using Matplotlib imshow.

    Expects a list of dictionaries, where each dictionary contains the following entries:
        - 'name': the name of the palette
        - 'cmap': a matplotlib ListedColorMap containing the palette's colors
        - 'length': the number of squares of color to show, usually the number of colors in 'cmap'

    Args:
        cmap_dicts (list of dict): list of colormap dictionaries
        ncols (int): number of columns to plot
        show (bool): whether or not to show the plotted colors
    """

    if figsize == (0, 0):
        width = 0.5 * max([cmap_dict["length"] for cmap_dict in cmap_dicts])
        height = 0.5 * len(cmap_dicts)
        fig = plt.figure(figsize=(width, height))
    else:
        fig = plt.figure(figsize=figsize)

    nrows = int(np.ceil(len(cmap_dicts) / ncols))

    for n, cmap_dict in enumerate(cmap_dicts):
        name = cmap_dict["name"]
        cmap = cmap_dict["cmap"]
        length = cmap_dict["length"]

        data = [np.arange(0, length)]
        ax = plt.subplot(nrows, ncols, n + 1)

        ax.imshow(data, cmap=cmap)
        ax.title.set_text(name)
        ax.spines[["right", "top", "left", "bottom"]].set_visible(False)

        plt.xticks([])
        plt.yticks([])

    if len(cmap_dicts) > 1:
        plt.tight_layout()

    if show:
        plt.show()

    return fig


def display_palette_interactive(cmap_dict: dict, ncols=1, show=True):
    """
    Displays interactive color palettes using plotly.

    Expects a dictionary, where each entry has the name of the color palette as the key and the color_dict as the value.

    Args:
        cmap_dict (dict): dict of cmaps
        ncols (int): number of columns to plot
        show (bool): whether or not to show the final figure, if False, returns the figure object
    """

    plot_width = 25 * max([len(cmap_dict) for cmap_dict in cmap_dict])
    plot_height = 35 * len(cmap_dict)

    nrows = int(np.ceil(len(cmap_dict) / ncols))

    fig = make_subplots(
        rows=nrows, cols=ncols, horizontal_spacing=0.02, vertical_spacing=0.02
    )

    for n, cmap in enumerate(cmap_dict):
        name = cmap
        cmap = cmap_dict[cmap]
        length = len(cmap)

        row = 1 + n // ncols
        col = 1 + n % ncols

        data = [[i for i in range(0, length)]]

        hovertext = [
            [f"<b>{colorname}</b><br>{hexcode}" for colorname, hexcode in cmap.items()]
        ]

        fig.add_trace(
            go.Heatmap(
                colorscale=list(cmap.values()),
                x=[color for color in cmap.keys()],
                y=[name],
                z=data,
                showscale=False,
                hoverinfo="text",
                text=hovertext,
            ),
            row=row,
            col=col,
        )

        fig.update_yaxes(scaleanchor="x", row=row, col=col)
        fig.update_xaxes(scaleanchor="y", showticklabels=False, row=row, col=col)

    fig.update_layout(width=plot_width, height=plot_height, plot_bgcolor="white")
    fig.update_layout(
        margin=dict(l=0, r=0, t=0, b=0),
    )

    if show:
        fig.show(config={"displayModeBar": False})
    else:
        return fig


def plot_color_gradients(cmap_dict: dict, title=None, return_fig=False, figsize=(5, 3)):
    """
    Displays color gradients in color and grayscale.

    Expects a dictionary, where each entry has the name of the color palette as its key and the value as:
        - the string name of the registered Matplotlib colormap OR
        - a Matplotlib ListedColormap object for the colormap

    Args:
        cmap_dict (list of dict): list of colormap dictionaries
        title (str): a title for the plot if desired
        return_fig (bool): whether or not to return the figure as an object
        figsize (tuple): the width, height tuple of the figure size
    """

    # Indices to step through colormap.
    x = np.linspace(0.0, 1.0, 100)

    gradient = np.linspace(0, 1, 256)
    gradient = np.vstack((gradient, gradient))

    fig, axs = plt.subplots(
        nrows=len(cmap_dict), ncols=2, figsize=figsize, squeeze=False
    )
    fig.subplots_adjust(top=0.90, bottom=0.01, left=0.2, right=0.99, wspace=0.05)

    if title is not None:
        fig.suptitle(title, fontsize=12, y=1.0, x=0.6)

    for ax, (name, cmap) in zip(axs, cmap_dict.items()):
        # Get RGB values for colormap.
        if name in mpl.colormaps:
            rgb = mpl.colormaps[name](x)[np.newaxis, :, :3]
        else:
            rgb = cmap(x)[np.newaxis, :, :3]

        # Get colormap in CAM02-UCS colorspace. We want the lightness.
        lab = cspace_converter("sRGB1", "CAM02-UCS")(rgb)
        L = lab[0, :, 0]
        L = np.float32(np.vstack((L, L, L)))

        ax[0].imshow(gradient, aspect="auto", cmap=cmap)
        ax[1].imshow(L, aspect="auto", cmap="binary_r", vmin=0.0, vmax=100.0)
        pos = list(ax[0].get_position().bounds)
        x_text = pos[0] - 0.01
        y_text = pos[1] + pos[3] / 2.0
        fig.text(x_text, y_text, name, va="center", ha="right", fontsize=10)

    # Turn off *all* ticks & spines, not just the ones with colormaps.
    for ax in axs.flat:
        ax.set_axis_off()

    if return_fig:
        return fig

    plt.show()


def plot_color_lightness(
    cmap_dict: dict,
    title=None,
    horizontal_spacing=1.1,
    steps=100,
    figsize=(7, 4),
    cmap_type="linear",
    tickrotation=50,
    markersize=300,
    return_fig=False,
):
    """
    Displays color gradients as lines based on lightness, for looking at uniformity of lightness.

    Expects a dictionary, where each entry has the name of the color palette as its key and the value as:
        - the string name of the registered Matplotlib colormap OR
        - a Matplotlib ListedColormap object for the colormap

    Args:
        cmap_dict (list of dict): list of colormap dictionaries
        title (str): a title for the plot if desired
        horizontal_spacing (float): the spacing between lines
        steps (int): the number of steps along the gradient to generate
        figsize (tuple): the width, height tuple of the figure size
        cmap_type (str): 'linear' if you want the label for the cmap to be at the end; anything else puts the label in the middle.
        tickrotation (int): rotation of the label for each cmap
        markersize (int): the size of the points that make up the gradient color line
        return_fig (bool): whether or not to return the figure as an object
    """

    # Indices to step through colormap
    x = np.linspace(0.0, 1.0, steps)

    locs = []  # locations for text labels

    fig = plt.figure(figsize=figsize)
    ax = plt.gca()

    for j, (name, cmap) in enumerate(cmap_dict.items()):
        # Get RGB values for colormap and convert the colormap in
        # CAM02-UCS colorspace.  lab[0, :, 0] is the lightness.
        if name in mpl.colormaps:
            rgb = mpl.colormaps[name](x)[np.newaxis, :, :3]
        else:
            rgb = cmap(x)[np.newaxis, :, :3]
        lab = cspace_converter("sRGB1", "CAM02-UCS")(rgb)

        # Plot colormap L values.  Do separately for each category
        # so each plot can be pretty.  To make scatter markers change
        # color along plot:
        # https://stackoverflow.com/q/8202605/

        y_ = lab[0, :, 0]
        c_ = x

        dc = horizontal_spacing  # cmaps horizontal spacing
        ax.scatter(x + j * dc, y_, c=c_, cmap=cmap, s=markersize, linewidths=0.0)

        if cmap_type == "linear":
            # Store locations for colormap labels
            locs.append(x[-1] + j * dc)
        else:
            locs.append(x[int(np.round(steps / 2))] + j * dc)

    # Set up the axis limits:
    #   * the 1st subplot is used as a reference for the x-axis limits
    #   * lightness values goes from 0 to 100 (y-axis limits)
    ax.set_xlim(ax.get_xlim())
    ax.set_ylim(0.0, 100.0)

    # Set up labels for colormaps
    ax.xaxis.set_ticks_position("top")
    ticker = mpl.ticker.FixedLocator(locs)
    ax.xaxis.set_major_locator(ticker)
    ax.xaxis.set_tick_params(rotation=tickrotation)
    ax.set_xticklabels(labels=cmap_dict.keys())
    ax.set_ylabel("Lightness $L^*$", fontsize=12)

    if title is not None:
        ax.set_xlabel(title, fontsize=14)

    fig.tight_layout(h_pad=0.0, pad=0.5)

    if return_fig:
        return fig

    plt.show()


def make_cvd_dict(form: str, severity: int) -> dict:
    """
    Makes a dictionary for colorspacious to simulate color vision deficiency.

    Args:
        form (str): 'd' for deuteranomaly, 'p' for protanomaly, and 't' for tritanomaly.
        severity (int): severity of the color vision deficiency, from 0 to 100.
    """
    forms = {"d": "deuteranomaly", "p": "protanomaly", "t": "tritanomaly"}

    if form not in forms:
        raise ValueError(
            "Choose 'd' for deuteranomaly, 'p' for protanomaly, and 't' for tritanomaly."
        )

    sev = np.clip(severity, 0, 100)

    # define a cvd space
    cvd_space = {"name": "sRGB1+CVD", "cvd_type": forms[form], "severity": sev}

    return cvd_space


def simulate_cvd(colors: list, form="d", severity=100) -> list:
    """
    Simulates color vision deficiency on a list of colors.

    Args:
        colors (list): list of colors to simulate color vision deficiency on.
        form (str): 'd' for deuteranomaly, 'p' for protanomaly, and 't' for tritanomaly.
        severity (int): severity of the color vision deficiency, from 0 to 100.
    """
    cvd_space = make_cvd_dict(form=form, severity=severity)

    # check if it's a hex color, converting to rgb as needed
    if "#" in colors[0] and len(colors[0]) == 7:
        rgb_colors = [mpl.colors.to_rgb(i) for i in colors]
    else:
        rgb_colors = colors

    cvd_rgb_colors = np.clip(cspace_convert(rgb_colors, cvd_space, "sRGB1"), 0, 1)
    cvd_hex_colors = [mpl.colors.to_hex(color) for color in cvd_rgb_colors]

    return cvd_hex_colors


def simulate_cvd_image(file: str, severity=100, fig_width=10, show=True):
    """
    Simulates color vision deficiency on an image.

    Args:
        file (str): path to file of the image to simulate color vision deficiency on.
        severity (int): severity of the color vision deficiency, from 0 to 100.
        fig_width (float): width of the figure in inches.
        show (bool): whether or not to show the figure.
    """
    forms = ["d", "p", "t"]

    fmt = file.split(".")[-1].lower()

    cvd_spaces = {form: make_cvd_dict(form=form, severity=severity) for form in forms}

    if fmt == "png":
        im_sRGB = plt.imread(file)[:, :, :3]
    elif fmt == "tiff":
        im_sRGB255 = plt.imread(file)[:, :, :3]
        im_sRGB = cspace_convert(im_sRGB255, "sRGB255", "sRGB1")
    elif fmt == "jpg" or fmt == "jpeg":
        im_sRGB255 = plt.imread(file)
        im_sRGB = cspace_convert(im_sRGB255, "sRGB255", "sRGB1")

    im_cvds = {
        form: np.clip(cspace_convert(im_sRGB, cvd_spaces[form], "sRGB1"), 0, 1)
        for form in forms
    }

    px_height = im_sRGB.shape[0]
    px_width = im_sRGB.shape[1]

    im_width = fig_width / 2
    px_ratio = px_height / px_width
    im_height = im_width * px_ratio * 1.05

    fig, axs = plt.subplots(2, 2, figsize=(im_width * 2, im_height * 2))

    labels = ["original", "deuteranopia", "protanopia", "tritanopia"]

    for i, im in enumerate([im_sRGB] + list(im_cvds.values())):
        ax = axs.flat[i]

        ax.imshow(im)
        ax.text(0, 0, labels[i])
        ax.axis("off")

    plt.tight_layout()

    if show:
        plt.show()
    else:
        return fig
