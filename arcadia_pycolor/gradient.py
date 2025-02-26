from __future__ import annotations
from dataclasses import dataclass

import matplotlib.colors as mcolors

from arcadia_pycolor.display import colorize
from arcadia_pycolor.hexcode import HexCode
from arcadia_pycolor.palette import Palette
from arcadia_pycolor.utils import (
    NumericSequence,
    distribute_values,
    interpolate_x_values,
    is_monotonic,
    rescale_and_concatenate_values,
)


@dataclass
class Anchor:
    """
    A paired color and position value for a gradient.

    Args:
        color: A HexCode object representing the color
        value: A numeric value between 0 and 1 representing the position in the gradient
    """

    color: HexCode
    value: float


class Gradient:
    """A sequence of colors and their positions that define a continuous color gradient.

    Each color is paired with a numeric value between 0 and 1 that determines its position
    in the gradient. The first color is always at position 0 and the last color at position 1.
    Colors in between are interpolated based on their position values to create a smooth gradient.

    Attributes:
        name (str): The name of the gradient.
        anchors (list[Anchor]): A list of gradient anchors.

    Properties:
        anchor_colors (list[HexCode]):
            The list of HexCodes corresponding to each anchor.
        anchor_values (list[float]):
            The list of values corresponding to each anchor.
    """

    def __init__(self, name: str, colors: list[HexCode], values: list[float] | None = None):
        """Initializes a Gradient.

        Args:
            name: The name of the gradient.
            colors: A list of HexCodes.
            values: An optional list of float values. See class docstring for details.

        Raises:
            ValueError:
                - If there are less than two values.
                - If the values are not integers or floats.
                - If the values are not between 0 and 1.
                - If the first value is not 0 or the last value is not 1.
                - If the number of values is not the same as the number of colors.
        """
        self.name = name

        if not all(isinstance(color, HexCode) for color in colors):
            raise ValueError("All colors must be HexCode objects.")

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
            anchor_values = values
        else:
            anchor_values = distribute_values(len(colors))

        self.anchors = [Anchor(color, value) for color, value in zip(colors, anchor_values)]

    @property
    def anchor_colors(self) -> list[HexCode]:
        return [anchor.color for anchor in self.anchors]

    @property
    def anchor_values(self) -> list[float]:
        return [anchor.value for anchor in self.anchors]

    @property
    def num_anchors(self) -> int:
        """Returns the number of anchors in the gradient"""
        return len(self.anchors)

    @classmethod
    def from_dict(
        cls, name: str, colors: dict[str, str], values: list[float] | None = None
    ) -> Gradient:
        """Creates a gradient from a dictionary of colors and values."""
        hex_codes = [HexCode(name, hex_code) for name, hex_code in colors.items()]
        return cls(name, hex_codes, values)

    def swatch(self, steps: int = 21) -> str:
        """
        Returns a gradient swatch with the specified number of steps.

        Args:
            steps (int): the number of swatches to display in the gradient
        """
        # Calculate the color for each step in the gradient
        cmap = self.to_mpl_cmap()

        # Get the color for each step in the gradient.
        colors = [
            HexCode(name=str(ind), hex_code=mcolors.to_hex(cmap(ind / steps)))
            for ind in range(steps)
        ]

        swatches = [colorize(" ", bg_color=c) for c in colors]

        return "".join(swatches)

    def reverse(self) -> Gradient:
        """Returns a new gradient with the colors and values in reverse order"""
        return Gradient(
            name=f"{self.name}_r",
            colors=self.anchor_colors[::-1],
            values=[1 - value for value in self.anchor_values[::-1]],
        )

    def resample_as_palette(self, steps: int = 5) -> Palette:
        """Returns a resampled gradient as a Palette with the specified number of steps."""
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
        min_value: float | None = None,
        max_value: float | None = None,
    ) -> list[HexCode]:
        """Maps a sequence of values to their corresponding colors from a gradient.

        Args:
            values (NumericSequence): A sequence of values to map to colors.
            min_value (float, optional):
                Determines which value corresponds to the first color in the spectrum.
                Any values below this minimum are assigned to the first color.
                If not provided, the minimum value of `values` is chosen.
            max_value (float, optional):
                Determines which value corresponds to the last color in the spectrum.
                Any values greater than this maximum are assigned to the last color.
                If not provided, the maximum value of `values` is chosen.

        Returns:
            list[HexCode]: A list of HexCode objects corresponding to the values.
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

    def interpolate_lightness(self) -> Gradient:
        """Interpolates the gradient to new values based on lightness."""

        if self.num_anchors < 3:
            raise ValueError("Interpolation requires at least three colors.")
        if not is_monotonic(self.anchor_values):
            raise ValueError("Lightness must be monotonically increasing or decreasing.")

        lightness_values = [color.to_cam02ucs()[0] for color in self.anchor_colors]
        new_values = interpolate_x_values(lightness_values)

        return Gradient(
            name=f"{self.name}_interpolated",
            colors=self.anchor_colors,
            values=new_values,
        )

    def __add__(self, other: Gradient) -> Gradient:
        """Return the sum of two gradients by concatenating their colors and values."""
        # If the first gradient ends with the same color as the start of the second gradient,
        # drop the repeated color.
        offset = int(self.anchor_colors[-1] == other.anchor_colors[0])
        new_colors = self.anchor_colors + other.anchor_colors[offset:]
        new_values = rescale_and_concatenate_values(
            self.anchor_values, other.anchor_values[offset:]
        )

        return Gradient(
            name=f"{self.name}_{other.name}",
            colors=new_colors,
            values=new_values,
        )

    def __repr__(self) -> str:
        longest_name_length = max(len(anchor.color.name) for anchor in self.anchors)

        return "\n".join(
            [self.swatch()]
            + [
                f"{anchor.color.swatch(min_name_width=longest_name_length)} {anchor.value}"
                for anchor in self.anchors
            ]
        )

    def to_mpl_cmap(self) -> mcolors.LinearSegmentedColormap:
        """Converts the gradient to a matplotlib colormap."""
        colors = [(anchor.value, anchor.color.hex_code) for anchor in self.anchors]
        return mcolors.LinearSegmentedColormap.from_list(
            self.name,
            colors=colors,
        )

    def to_plotly_colorscale(self) -> list[tuple[float, str]]:
        """Converts the gradient to a colorscale acceptable by plotly graph objects.

        Example:
        >>> import plotly.graph_objects as go
        >>> import arcadia_pycolor as apc
        >>> gradient = apc.gradients.reds
        >>> data = np.random.rand(10, 10)
        >>> heatmap = go.Heatmap(z=data, colorscale=gradient.to_plotly_colorscale())
        >>> fig = go.Figure(data=[heatmap])
        >>> fig.show()

        Returns:
            list[tuple[tuple, str]]:
                A 256 (8-bit) color scale. Each element is a two-ple of normalized
                position in the colorscale and the associated hex value.
        """
        return [(i / 255.0, mcolors.rgb2hex(self.to_mpl_cmap()(i / 255.0))) for i in range(256)]
