import re

import matplotlib.colors as mcolors

from arcadia_pycolor.display import colorize


def _is_hex_code(hex_string: str) -> bool:
    """Checks if a string is a valid HEX code."""
    if not isinstance(hex_string, str):
        return False

    match = re.search(r"^#(?:[0-9a-fA-F]{3}){1,2}$", hex_string)
    if match:
        return True
    return False


class HexCode(str):
    def __new__(cls, name: str, hex_code: str):
        """
        A HexCode object stores a color's name and HEX code.

        Args:
            name (str): the name of the color
            hex_code (str): the HEX code of the color
        """
        if not _is_hex_code(hex_code):
            raise ValueError(f"Invalid HEX code: {hex_code}")

        obj = str.__new__(cls, hex_code)
        obj.name = name
        obj.hex_code = hex_code
        return obj

    def to_rgb(self):
        """Returns a tuple of RGB values for the color."""
        return [int(c * 255) for c in mcolors.to_rgb(self.hex_code)]

    def swatch(self, width: int = 2, min_name_width: int = None):
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
            color_name = self.name.ljust(min_name_width)
        else:
            color_name = self.name

        # Creates a block of color with the specified width in monospace characters.
        swatch_text = " " * width
        output = colorize(swatch_text, bg_color=self)

        output += colorize(f" {color_name} {self.hex_code}", fg_color=self)

        return output

    def __repr__(self):
        return self.swatch()

    def __str__(self):
        return self.hex_code