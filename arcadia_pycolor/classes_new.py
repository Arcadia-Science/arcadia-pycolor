import matplotlib.colors as mcolors

from .utils import distribute_values


class Color(str):
    def __new__(cls, name: str, hex_code: str):
        """
        A Color object stores a color's name and HEX code.

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

    @property
    def _rgb(self):
        return [int(c * 255) for c in mcolors.to_rgb(self.hex_code)]

    def __repr__(self):
        from arcadia_pycolor.display import swatch  # imported here to avoid circular import

        return swatch(self)

    def __str__(self):
        return self.hex_code


class Palette:
    def __init__(self, name: str, colors: dict[str, str] | list[Color]):
        """
        A Palette object stores a collection of Color objects.

        Args:
            name (str): the name of the color palette
            colors (dict): a dictionary where the key is the color's name as a string
                and the value is the HEX code of the color as a string
            OR
            colors (list): a list of Color objects
        """
        self.name = name

        if isinstance(colors, dict):
            self.colors = {name: Color(name, hex_code) for name, hex_code in colors.items()}
        elif isinstance(colors, list):
            self.colors = {color.name: color for color in colors}
        else:
            raise ValueError(
                "Colors must be either a dictionary of color name and HEX codes",
                "or a list of Color objects.",
            )

    def __repr__(self):
        from arcadia_pycolor.display import swatch  # imported here to avoid circular import

        longest_name = max(len(color.name) for color in self.colors.values())

        return "\n".join([swatch(color, name_width=longest_name) for color in self.colors.values()])

    def __add__(self, other):
        return Palette(
            name=f"{self.name} + {other.name}",
            colors={**self.colors, **other.colors},
        )

    def rename(self, name: str):
        self.name = name


class Gradient(Palette):
    def __init__(self, name: str, colors: dict[str, str] | list[Color], values: list[float] = None):
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
            self.values = values
        else:
            self.values = distribute_values(self.colors)

    def __repr__(self):
        from arcadia_pycolor.display import gradient_swatch, swatch

        longest_name = max(len(color.name) for color in self.colors.values())

        return "\n".join(
            [gradient_swatch(self)]
            + [
                f"{swatch(color, name_width=longest_name)} {value}"
                for color, value in zip(self.colors.values(), self.values)
            ]
        )

    def to_mpl_cmap_linear(self):
        colors = [
            (value, color.hex_code) for value, color in zip(self.values, self.colors.values())
        ]
        return mcolors.LinearSegmentedColormap.from_list(
            self.name,
            colors=colors,
        )
