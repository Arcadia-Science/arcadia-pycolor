from typing import Sequence, Union

import numpy as np
from PIL import Image, ImageOps

NumericSequence = Union[Sequence[int], Sequence[float]]


def distribute_values(num_points: int, min_val: float = 0.0, max_val: float = 1.0) -> list[float]:
    """Returns a list of `num_points` values evenly distributed between `min_val` and `max_val`.

    Args:
        num_points (int): The number of points to distribute.
        min_val (float): The minimum value.
        max_val (float): The maximum value.
    """
    if num_points <= 1:
        return [(max_val - min_val) / 2] * num_points
    return np.linspace(min_val, max_val, num_points).tolist()


def interpolate_x_values(y_values: list[float], round_digits: int = 3) -> list[float]:
    """Returns a list of x-values that are linearly interpolated between 0 and 1.

    The first and last y-values correspond to x-values of 0 and 1, respectively.

    Args:
        y_values (list[float]): The list of y-values.
        round_digits (int): The number of digits to round the x-values to.
    """
    # Retrieve first and last values.
    x0 = 0
    y0 = y_values[0]

    x1 = 1
    y1 = y_values[-1]

    # Calculate the slope (m) of the line through the two points.
    m = (y1 - y0) / (x1 - x0)

    # y0 is the y-intercept of the line.
    # Find x-values corresponding to each y-value.
    x_values = [np.round((y - y0) / m, round_digits) for y in y_values]

    return x_values


def is_non_decreasing(values: NumericSequence) -> bool:
    """Returns True if the numbers in `values` are in strictly non-decreasing order.

    Copied from https://stackoverflow.com/questions/4983258.
    """
    return all(x <= y for x, y in zip(values, values[1:]))


def is_non_increasing(values: NumericSequence) -> bool:
    """Returns True if the numbers in `values` are in strictly non-increasing order.

    Copied from https://stackoverflow.com/questions/4983258.
    """
    return all(x >= y for x, y in zip(values, values[1:]))


def is_monotonic(values: NumericSequence) -> bool:
    """Returns True if the numbers in `values` are in strictly monotonic order."""
    return is_non_decreasing(values) or is_non_increasing(values)


def rescale_and_concatenate_values(list1: list[float], list2: list[float]) -> list[float]:
    """Rescale and concatenate two lists of values.

    Rescales `list1` to the range [0, 0.5] and `list2` to the range [0.5, 1].
    """
    rescaled_list1 = [0.5 * x for x in list1]
    rescaled_list2 = [0.5 * x + 0.5 for x in list2]
    return rescaled_list1 + rescaled_list2


def add_margin(
    input_image_path: str,
    output_image_path: str,
    margin_size: Union[int, tuple[int, int, int, int]],
    margin_color: tuple[int, int, int, int] = (0, 0, 0, 255),
):
    """Adds margins to an image.

    Args:
        input_image_path (str):
            Path to the input image.
        output_image_path (str):
            Path to save the image with margin.
        margin_size (int | tuple[int, int, int, int]):
            Size of the margin in pixels.
            Can be an integer for equal margins or a tuple (left, top, right, bottom).
        margin_color (tuple[int, int, int, int]):
            Color of the margin in RGBA format.
    """
    img = Image.open(input_image_path)
    img_with_margin = ImageOps.expand(img, border=margin_size, fill=margin_color)
    img_with_margin.save(output_image_path)
