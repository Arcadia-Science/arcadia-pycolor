from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from arcadia_pycolor.classes import HexCode


def swatch(color: "HexCode", width: int = 2, min_name_width: int = None):
    """
    Returns a color swatch with the specified width and color name.

    Args:
        color (HexCode): the HexCode object to display
        width (int): the width of the color swatch
        min_name_width (int): the desired width of the color name;
            pads the name with spaces if necessary.
            If not specified, text will not display in a fixed width.

    Based on colorir's swatch function:
    https://github.com/aleferna12/colorir/blob/master/colorir/utils.py#L59
    """
    # Add padding to the color name if necessary.
    # Used when displaying multiple colors in a palette.
    if min_name_width:
        color_name = color.name.ljust(min_name_width)
    else:
        color_name = color.name

    # Creates a block of color with the specified width in monospace characters.
    swatch_text = " " * width
    output = colorize(swatch_text, bg_color=color)

    output += colorize(f" {color_name} {color.hex_code}", fg_color=color)

    return output


def colorize(
    string: str,
    fg_color: Optional["HexCode"] = None,
    bg_color: Optional["HexCode"] = None,
):
    """
    Colorizes a string with the specified foreground and background colors.

    Args:
        string (str): the string to colorize
        fg_color (HexCode): the foreground color
        bg_color (HexCode): the background color

    Based on colorir's color_str function:
    https://github.com/aleferna12/colorir/blob/master/colorir/utils.py#L370

    Relies on ANSI escape codes for colorization.
    See https://gist.github.com/fnky/458719343aabd01cfb17a3a4f7296797
    """
    if fg_color:
        rgb = fg_color.to_rgb()
        string = f"\033[38;2;{rgb[0]};{rgb[1]};{rgb[2]}m" + string + "\33[0m"

    if bg_color:
        bg_rgb = bg_color.to_rgb()
        string = f"\033[48;2;{bg_rgb[0]};{bg_rgb[1]};{bg_rgb[2]}m" + string + "\33[0m"

    return string
