import arcadia_pycolor.classes_new


def swatch(color: arcadia_pycolor.classes_new.Color, width: int = 2, name_width: int = None):
    swatch_text = " " * width

    # pad the name to the right
    if name_width:
        color_name = color.name.ljust(name_width)
    else:
        color_name = color.name

    output = colorize(swatch_text, bg_color=color)
    output += colorize(f" {color_name} {color.hex_code}", fg_color=color)
    return output


def colorize(
    string,
    fg_color: arcadia_pycolor.classes_new.Color = None,
    bg_color: arcadia_pycolor.classes_new.Color = None,
):
    if fg_color:
        rgb = fg_color._rgb
        string = f"\033[38;2;{rgb[0]};{rgb[1]};{rgb[2]}m" + string + "\33[0m"

    if bg_color:
        bg_rgb = bg_color._rgb
        string = f"\033[48;2;{bg_rgb[0]};{bg_rgb[1]};{bg_rgb[2]}m" + string + "\33[0m"

    return string
