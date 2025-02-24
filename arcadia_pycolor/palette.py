from __future__ import annotations
from typing import overload

import matplotlib.colors as mcolors

from arcadia_pycolor.display import colorize
from arcadia_pycolor.hexcode import HexCode


class Palette:
    """
    A Palette is a discrete ordered sequence of HexCode objects.
    """

    def __init__(self, name: str, colors: list[HexCode]):
        """
        Initialize a Palette with a name and a list of colors.

        Args:
            name (str): the name of the palette
            colors (list): a list of HexCode objects
        """
        self.name = name

        if not all(isinstance(color, HexCode) for color in colors):
            raise ValueError("All colors must be HexCode objects.")

        self.colors = colors

    @classmethod
    def from_dict(cls, name: str, colors: dict[str, str]) -> Palette:
        """
        Create a Palette from a dictionary of color names and hex codes.

        Args:
            name (str): the name of the palette.
            colors (dict): a dictionary mapping color names to hex codes.
        """
        hex_codes = [HexCode(name, hex_code) for name, hex_code in colors.items()]
        return cls(name, hex_codes)

    def swatch(self) -> str:
        """
        Returns a color swatch showing all colors in the palette.
        """
        swatches = [colorize("  ", bg_color=color) for color in self.colors]
        return "".join(swatches)

    def reverse(self) -> Palette:
        """
        Returns a new palette with the colors in reverse order.
        """
        return Palette(
            name=f"{self.name}_r",
            colors=self.colors[::-1],
        )

    def _get_longest_name_length(self) -> int:
        """Convenience function to get the length of the longest color name in the palette."""
        return max(len(color.name) for color in self.colors)

    def __len__(self) -> int:
        """Returns the number of colors in the palette."""
        return len(self.colors)

    def __iter__(self):
        """Returns an iterator over the colors in the palette."""
        return iter(self.colors)

    @overload
    def __getitem__(self, index: int) -> HexCode: ...

    @overload
    def __getitem__(self, index: slice) -> Palette: ...

    def __getitem__(self, index: int | slice) -> HexCode | Palette:
        """Returns the color at the given index, or a new palette if a slice is provided.

        Args:
            index: An integer index or slice.

        Returns:
            A HexCode if an integer index was provided, or a new Palette if
            a slice was provided.
        """
        if isinstance(index, slice):
            return Palette(name=f"{self.name}_slice", colors=self.colors[index])
        else:
            return self.colors[index]

    def __repr__(self) -> str:
        """Returns a string representation of the palette."""
        longest_name_length = self._get_longest_name_length()

        return "\n".join(
            [self.swatch()]
            + [color.swatch(min_name_width=longest_name_length) for color in self.colors]
        )

    def __add__(self, other: Palette) -> Palette:
        """Returns a new palette that is the concatenation of this palette and another."""
        return Palette(
            name=f"{self.name}+{other.name}",
            colors=self.colors + other.colors,
        )

    def to_mpl_cmap(self) -> mcolors.ListedColormap:
        """
        Convert the palette to a Matplotlib colormap.
        """
        return mcolors.ListedColormap([color.hex_code for color in self.colors], self.name)
