import matplotlib.colors as mcolors

from arcadia_pycolor.display import colorize
from arcadia_pycolor.hexcode import HexCode
from arcadia_pycolor.palette import Palette
from arcadia_pycolor.utils import distribute_values


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

        if values is not None:
            if len(values) < 2:
                raise ValueError("A gradient must have at least two values.")
            if not all(isinstance(value, (int, float)) for value in values):
                raise ValueError("All values must be integers or floats.")
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
        cmap = self.to_mpl_linear_cmap()

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

    def to_mpl_linear_cmap(self):
        colors = [(value, color.hex_code) for value, color in zip(self.values, self.colors)]
        return mcolors.LinearSegmentedColormap.from_list(
            self.name,
            colors=colors,
        )
