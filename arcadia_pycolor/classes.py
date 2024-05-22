import matplotlib.colors as mcolors

from arcadia_pycolor.display import gradient_swatch, swatch
from arcadia_pycolor.utils import distribute_values


def _longest_name(palette):
    "Convenience function to get the length of the longest color name in a palette."
    return max(len(color.name) for color in palette.colors)


class HexCode(str):
    def __new__(cls, name: str, hex_code: str):
        """
        A HexCode object stores a color's name and HEX code.

        Args:
            name (str): the name of the color
            hex_code (str): the HEX code of the color
        """
        if not mcolors.is_color_like(hex_code):
            raise ValueError(f"Invalid HEX code: {hex_code}")

        obj = str.__new__(cls, hex_code)
        obj.name = name
        obj.hex_code = hex_code
        return obj

    def to_rgb(self):
        return [int(c * 255) for c in mcolors.to_rgb(self.hex_code)]

    def __repr__(self):
        return swatch(self)

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
        self.colors = colors

    @classmethod
    def from_dict(cls, name: str, colors: dict[str, str]):
        hex_codes = [HexCode(name, hex_code) for name, hex_code in colors.items()]
        return cls(name, hex_codes)

    def __repr__(self):
        longest_name = _longest_name(self)

        return "\n".join([swatch(color, min_name_width=longest_name) for color in self.colors])

    def __add__(self, other):
        return Palette(
            name=f"{self.name}+{other.name}",
            colors=self.colors + other.colors,
        )


class Gradient(Palette):
    def __init__(self, name: str, colors: list[HexCode], values: list[float] = None):
        """
        A Gradient object stores a collection of Color objects and their corresponding values.

        Args:
            name (str): the name of the gradient
            colors (dict): a dictionary where the key is the color's name as a string
                and the value is the HEX code of the color as a string
            OR
            colors (list): a list of Color objects
            values (list): a list of float values corresponding to the colors
        """
        super().__init__(name=name, colors=colors)

        if values:
            if not all(0 <= value <= 1 for value in values):
                raise ValueError("All values must be between 0 and 1.")
            elif len(colors) != len(values):
                raise ValueError("The number of colors and values must be the same.")
            self.values = values
        else:
            self.values = distribute_values(self.colors)

    @classmethod
    def from_dict(cls, name: str, colors: dict[str, str], values: list[float] = None):
        hex_codes = [HexCode(name, hex_code) for name, hex_code in colors.items()]
        return cls(name, hex_codes, values)

    def __repr__(self):
        longest_name = _longest_name(self)

        return "\n".join(
            [gradient_swatch(self)]
            + [
                f"{swatch(color, min_name_width=longest_name)} {value}"
                for color, value in zip(self.colors, self.values)
            ]
        )
