import matplotlib.colors as mcolors

from arcadia_pycolor.display import colorize
from arcadia_pycolor.hexcode import HexCode


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

    def swatch(self):
        swatches = [colorize("  ", bg_color=color) for color in self.colors]

        return "".join(swatches)

    def reverse(self):
        return Palette(
            name=f"{self.name}_r",
            colors=self.colors[::-1],
        )

    def __repr__(self):
        longest_name_length = self._get_longest_name_length()

        return "\n".join(
            [self.swatch()]
            + [color.swatch(min_name_width=longest_name_length) for color in self.colors]
        )

    def __add__(self, other: "Palette"):
        return Palette(
            name=f"{self.name}+{other.name}",
            colors=self.colors + other.colors,
        )

    def _get_longest_name_length(self) -> int:
        "Convenience function to get the length of the longest color name in a palette."
        return max(len(color.name) for color in self.colors)

    def to_mpl_cmap(palette: "Palette"):
        return mcolors.ListedColormap([color.hex_code for color in palette.colors], palette.name)
