from __future__ import annotations
import re
from typing import Any, cast

import matplotlib.colors as mcolors
from colorspacious import cspace_converter  # type: ignore

from arcadia_pycolor.display import colorize


def _is_hex_code(hex_string: Any) -> bool:
    """Checks if a string is a valid HEX code."""
    if not isinstance(hex_string, str):
        return False

    match = re.search(r"^#(?:[0-9a-fA-F]{3}){1,2}$", hex_string)
    if match:
        return True
    return False


class HexCode(str):
    """Represents the HEX code of a color.

    Attributes:
        name (str): The name of the color.
        hex_code (str): The HEX code of the color.
    """

    def __new__(cls, name: str, hex_code: str) -> HexCode:
        """Returns a new HexCode object.

        Args:
            name (str): The name of the color.
            hex_code (str): The HEX code of the color.

        Raises:
            ValueError: If the HEX code is invalid.
        """
        if not _is_hex_code(hex_code):
            raise ValueError(f"Invalid HEX code: {hex_code}")

        obj = str.__new__(cls, hex_code)
        obj.name = name
        obj.hex_code = hex_code
        return obj

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, value: str) -> None:
        self._name = value

    @property
    def hex_code(self) -> str:
        return self._hex_code

    @hex_code.setter
    def hex_code(self, value: str) -> None:
        self._hex_code = value

    def __copy__(self) -> HexCode:
        return HexCode(self.name, self.hex_code)

    def __deepcopy__(self, _: dict) -> HexCode:
        return HexCode(self.name, self.hex_code)

    def to_rgb(self) -> list[int]:
        """Returns a tuple of RGB values for the color."""
        return [int(c * 255) for c in mcolors.to_rgb(self.hex_code)]

    def to_cam02ucs(self) -> list[float]:
        """Returns a tuple of CAM02-UCS values for the color.

        The first value is the lightness (J) and the second and third values are
        the chromaticity coordinates (a: redness-to-greenness, b: blueness-to-yellowness).
        """
        # Convert RGB255 to RGB1.
        rgb = [i / 255 for i in self.to_rgb()]

        # Convert RGB1 to CAM02-UCS.
        cam02ucs = cast(list[float], cspace_converter("sRGB1", "CAM02-UCS")(rgb))

        return cam02ucs

    def swatch(self, width: int = 2, min_name_width: int | None = None) -> str:
        """Returns a color swatch with the specified width and color name width.

        Based on colorir's `swatch` function:
        https://github.com/aleferna12/colorir/blob/2d44e4c/colorir/utils.py#L69.

        Args:
            width (int): The desired width of the color swatch.
            min_name_width (int, optional): The desired width of the color name.
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

    def __repr__(self) -> str:
        return self.swatch()

    def __str__(self) -> str:
        return self.hex_code
