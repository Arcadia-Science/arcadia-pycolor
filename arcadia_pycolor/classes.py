import re

import matplotlib.colors as mcolors

from arcadia_pycolor.display import colorize
from arcadia_pycolor.mpl import gradient_to_linear_cmap
from arcadia_pycolor.utils import distribute_values


def _is_hex_code(hex_string: str) -> bool:
    """Checks if a string is a valid HEX code."""
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


class Palette:
    def __init__(self, name: str, colors: list[HexCode]):
        """
        A Palette object stores a collection of HexCode objects.

        Args:
            name (str): the name of the color palette
            colors (list): a list of HexCode objects.
        """
        self.name = name

        if not all(isinstance(color, HexCode) for color in colors):
            raise ValueError("All colors must be HexCode objects.")

        self.colors = colors

    @classmethod
    def from_dict(cls, name: str, colors: dict[str, str]):
        hex_codes = [HexCode(name, hex_code) for name, hex_code in colors.items()]
        return cls(name, hex_codes)

    def __repr__(self):
        longest_name_length = self._get_longest_name_length()

        return "\n".join(
            [color.swatch(min_name_width=longest_name_length) for color in self.colors]
        )

    def __add__(self, other: "Palette"):
        return Palette(
            name=f"{self.name}+{other.name}",
            colors=self.colors + other.colors,
        )

    def _get_longest_name_length(self) -> int:
        "Convenience function to get the length of the longest color name in a palette."
        return max(len(color.name) for color in self.colors)


class Gradient(Palette):
    def __init__(self, name: str, colors: list[HexCode], values: list[float] = None):
        """
        A Gradient object stores a collection of Color objects and their corresponding values.

        Args:
            name (str): the name of the gradient
            colors (list): a list of HexCode objects
            values (list): a list of float values corresponding
                to the position of colors on a 0 to 1 scale.
        """
        super().__init__(name=name, colors=colors)

        if values:
            if not all(0 <= value <= 1 for value in values):
                raise ValueError("All values must be between 0 and 1.")
            if not values[0] == 0 or not values[-1] == 1:
                raise ValueError("The first value must be 0 and the last value must be 1.")
            if len(colors) != len(values):
                raise ValueError("The number of colors and values must be the same.")
            self.values = values
        else:
            self.values = distribute_values(len(self.colors))

    @classmethod
    def from_dict(cls, name: str, colors: dict[str, str], values: list[float] = None):
        hex_codes = [HexCode(name, hex_code) for name, hex_code in colors.items()]
        return cls(name, hex_codes, values)

    def swatch(self, steps=21):
        """
        Returns a gradient swatch with the specified number of steps.

        Args:
            gradient (Gradient): the Gradient object to display
            steps (int): the number of swatches to display in the gradient

        """
        # Calculate the color for each step in the gradient
        cmap = gradient_to_linear_cmap(self)

        # Get the color for each step in the gradient
        colors = [HexCode(i, mcolors.to_hex(cmap(i / steps))) for i in range(steps)]

        swatches = [colorize(" ", bg_color=c) for c in colors]

        return "".join(swatches)

    def __repr__(self):
        longest_name_length = self._get_longest_name_length()

        return "\n".join(
            [self.swatch()]
            + [
                f"{color.swatch(min_name_width=longest_name_length)} {value}"
                for color, value in zip(self.colors, self.values)
            ]
        )
