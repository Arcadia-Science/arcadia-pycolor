from typing import Any, Union

import matplotlib.colors as mcolors

from arcadia_pycolor.display import colorize
from arcadia_pycolor.hexcode import HexCode
from arcadia_pycolor.palette import ColorSequence, Palette
from arcadia_pycolor.utils import (
    NumericSequence,
    distribute_values,
    interpolate_x_values,
    is_monotonic,
    rescale_and_concatenate_values,
)


class Gradient(ColorSequence["Gradient"]):
    def __init__(self, name: str, colors: list[Any], values: Union[list[Any], None] = None):
        """
        A Gradient is a sequence of pairs of HexCode objects and numeric values
        from 0 to 1 that represent the position of each color in the gradient.

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
    def from_dict(
        cls, name: str, colors: dict[str, str], values: Union[list[float], None] = None
    ) -> "Gradient":
        hex_codes = [HexCode(name, hex_code) for name, hex_code in colors.items()]
        return cls(name, hex_codes, values)

    def swatch(self, steps: int = 21) -> str:
        """
        Returns a gradient swatch with the specified number of steps.

        Args:
            gradient (Gradient): the Gradient object to display
            steps (int): the number of swatches to display in the gradient

        """
        # Calculate the color for each step in the gradient
        cmap = self.to_mpl_cmap()

        # Get the color for each step in the gradient
        colors = [
            HexCode(name=str(ind), hex_code=mcolors.to_hex(cmap(ind / steps)))
            for ind in range(steps)
        ]

        swatches = [colorize(" ", bg_color=c) for c in colors]

        return "".join(swatches)

    def reverse(self) -> "Gradient":
        return Gradient(
            name=f"{self.name}_r",
            colors=self.colors[::-1],
            values=[1 - value for value in self.values[::-1]],
        )

    def resample_as_palette(self, steps: int = 5) -> Palette:
        """
        Resamples the gradient, returning a Palette with the specified number of steps.
        """
        gradient = self.to_mpl_cmap()
        values = distribute_values(steps)
        colors = [
            HexCode(name=f"{self.name}_{i}", hex_code=mcolors.to_hex(gradient(value)))
            for i, value in enumerate(values)
        ]

        return Palette(
            name=f"{self.name}_resampled_{steps}",
            colors=colors,
        )

    def map_values(
        self,
        values: NumericSequence,
        min_value: Union[float, None] = None,
        max_value: Union[float, None] = None,
    ) -> list[HexCode]:
        """Map a sequence of values to their corresponding colors from a gradient

        Args:
            min_value:
                Determines which value corresponds to the first color in the spectrum.
                Any values below this minimum are assigned to the first color. If not
                provided, min(values) is chosen.
            max_value:
                Determines which value corresponds to the last color in the spectrum.
                Any values greater than this maximum are assigned to the last color. If
                not provided, max(values) is chosen.

        Returns:
            list[HexCode]: A list of hex codes.
        """

        if not len(values):
            return []

        if min_value is None:
            min_value = min(values)

        if max_value is None:
            max_value = max(values)

        if min_value >= max_value:
            raise ValueError(
                f"max_value ({max_value}) must be greater than min_value ({min_value})."
            )

        cmap = self.to_mpl_cmap()

        normalized_values = [(value - min_value) / (max_value - min_value) for value in values]

        return [HexCode(f"{value}", mcolors.to_hex(cmap(value))) for value in normalized_values]

    def interpolate_lightness(self) -> "Gradient":
        """
        Interpolates the gradient to new values based on lightness.
        """

        if len(self.colors) < 3:
            raise ValueError("Interpolation requires at least three colors.")
        if not is_monotonic(self.values):
            raise ValueError("Lightness must be monotonically increasing or decreasing.")

        lightness_values = [color.to_cam02ucs()[0] for color in self.colors]
        new_values = interpolate_x_values(lightness_values)

        return Gradient(
            name=f"{self.name}_interpolated",
            colors=self.colors,
            values=new_values,
        )

    def __add__(self, other: "Gradient") -> "Gradient":
        """
        Return the sum of two gradients by concatenating their colors and values.
        """
        new_colors = []
        new_values = []

        # If the first gradient ends with the same color as the start of the second gradient,
        # drop the repeated color.
        offset = 1 if self.colors[-1] == other.colors[0] else 0
        new_colors = self.colors + other.colors[offset:]
        new_values = rescale_and_concatenate_values(self.values, other.values[offset:])

        return Gradient(
            name=f"{self.name}_{other.name}",
            colors=new_colors,
            values=new_values,
        )

    def __repr__(self) -> str:
        longest_name_length = self._get_longest_name_length()

        return "\n".join(
            [self.swatch()]
            + [
                f"{color.swatch(min_name_width=longest_name_length)} {value}"
                for color, value in zip(self.colors, self.values)
            ]
        )

    def to_mpl_cmap(self):
        colors = [(value, color.hex_code) for value, color in zip(self.values, self.colors)]
        return mcolors.LinearSegmentedColormap.from_list(
            self.name,
            colors=colors,
        )
