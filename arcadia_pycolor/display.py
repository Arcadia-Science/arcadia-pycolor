import arcadia_pycolor.classes_new


def swatch(color: arcadia_pycolor.classes_new.Color, width: int = 2, name_width: int = None):
    """
    Returns a color swatch with the specified width and color name.

    Args:
        color (Color): the Color object to display
        width (int): the width of the color swatch
        name_width (int): the desired width of the color name;
            pads the name with spaces if necessary

    Based on colorir's swatch function:
    https://github.com/aleferna12/colorir/blob/master/colorir/utils.py#L59
    """
    # Add padding to the color name if necessary.
    # Used when displaying multiple colors in a palette.
    if name_width:
        color_name = color.name.ljust(name_width)
    else:
        color_name = color.name

    # Creates a block of color with the specified width in monospace characters.
    swatch_text = " " * width
    output = colorize(swatch_text, bg_color=color)

    output += colorize(f" {color_name} {color.hex_code}", fg_color=color)

    return output


def gradient_swatch(gradient: arcadia_pycolor.classes_new.Gradient, steps=21):
    """
    Returns a gradient swatch with the specified number of steps.

    Args:
        gradient (Gradient): the Gradient object to display
        steps (int): the number of steps in the gradient

    """
    # Calculate the color for each step in the gradient
    cmap = gradient.to_mpl_cmap_linear()

    # Get the color for each step in the gradient
    colors = [arcadia_pycolor.classes_new.Color(i, cmap(i / steps)) for i in range(steps)]

    swatches = [colorize(" ", bg_color=c) for c in colors]

    return "".join(swatches)


def colorize(
    string: str,
    fg_color: arcadia_pycolor.classes_new.Color = None,
    bg_color: arcadia_pycolor.classes_new.Color = None,
):
    """
    Colorizes a string with the specified foreground and background colors.

    Args:
        string (str): the string to colorize
        fg_color (Color): the foreground color
        bg_color (Color): the background color

    Based on colorir's color_str function:
    https://github.com/aleferna12/colorir/blob/master/colorir/utils.py#L370

    Relies on ANSI escape codes for colorization.
    See https://gist.github.com/fnky/458719343aabd01cfb17a3a4f7296797
    """
    if fg_color:
        rgb = fg_color._rgb
        string = f"\033[38;2;{rgb[0]};{rgb[1]};{rgb[2]}m" + string + "\33[0m"

    if bg_color:
        bg_rgb = bg_color._rgb
        string = f"\033[48;2;{bg_rgb[0]};{bg_rgb[1]};{bg_rgb[2]}m" + string + "\33[0m"

    return string
