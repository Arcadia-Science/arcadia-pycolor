import abc
from typing import Any, Generic, TypeVar

import matplotlib.colors as mcolors

from arcadia_pycolor.display import colorize
from arcadia_pycolor.hexcode import HexCode

T = TypeVar("T", bound="ColorSequence")


class ColorSequence(abc.ABC, Generic[T]):
    def __init__(self, name: str, colors: list[Any]):
        """
        A color sequence is an ordered sequence of HexCode objects.

        Args:
            name (str): the name of the sequence.
            colors (list): a list of HexCode objects.
        """
        self.name = name

        if not all(isinstance(color, HexCode) for color in colors):
            raise ValueError("All colors must be HexCode objects.")

        self.colors = colors

    def _get_longest_name_length(self) -> int:
        """
        Convenience function to get the length of the longest color name in the sequence.
        """
        return max(len(color.name) for color in self.colors)

    @abc.abstractmethod
    def swatch(self) -> str:
        pass

    @abc.abstractmethod
    def reverse(self) -> T:
        pass

    @abc.abstractmethod
    def __add__(self, other: T) -> T:
        pass

    @abc.abstractmethod
    def __repr__(self) -> str:
        pass

    @abc.abstractmethod
    def to_mpl_cmap(self) -> Any:
        pass


class Palette(ColorSequence["Palette"]):
    """
    A Palette is a discrete ordered sequence of HexCode objects.
    """

    def __init__(self, name: str, colors: list[Any]):
        super().__init__(name, colors)

    @classmethod
    def from_dict(cls, name: str, colors: dict[str, str]):
        hex_codes = [HexCode(name, hex_code) for name, hex_code in colors.items()]
        return cls(name, hex_codes)

    def swatch(self):
        swatches = [colorize("  ", bg_color=color) for color in self.colors]

        return "".join(swatches)

    def reverse(self) -> "Palette":
        return Palette(
            name=f"{self.name}_r",
            colors=self.colors[::-1],
        )

    def __repr__(self) -> str:
        longest_name_length = self._get_longest_name_length()

        return "\n".join(
            [self.swatch()]
            + [color.swatch(min_name_width=longest_name_length) for color in self.colors]
        )

    def __add__(self, other: "Palette") -> "Palette":
        return Palette(
            name=f"{self.name}+{other.name}",
            colors=self.colors + other.colors,
        )

    def to_mpl_cmap(self):
        return mcolors.ListedColormap([color.hex_code for color in self.colors], self.name)
