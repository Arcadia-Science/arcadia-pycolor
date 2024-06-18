from typing import Sequence, Union

import numpy as np

NumericSequence = Union[Sequence[int], Sequence[float]]


def distribute_values(num_points: int, min_val: float = 0.0, max_val: float = 1.0) -> list[float]:
    if num_points <= 1:
        return [(max_val - min_val) / 2] * num_points
    return np.linspace(min_val, max_val, num_points).tolist()


def interpolate_x_values(y_values: list[float], round_digits: int = 3) -> list[float]:
    """Takes a list of y-values and returns a list of x-values that are
    linearly interpolated between 0 and 1; the first and last y-values
    correspond to x-values of 0 and 1, respectively."""
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
    """Determine if the numbers in `values` are in strictly non-decreasing order.
    Copied from https://stackoverflow.com/questions/4983258.
    """
    return all(x <= y for x, y in zip(values, values[1:]))


def is_non_increasing(values: NumericSequence) -> bool:
    """Determine if the numbers in `values` are in strictly non-increasing order.
    Copied from https://stackoverflow.com/questions/4983258.
    """
    return all(x >= y for x, y in zip(values, values[1:]))


def is_monotonic(values: NumericSequence) -> bool:
    return is_non_decreasing(values) or is_non_increasing(values)


def rescale_and_concatenate_values(list1: list[float], list2: list[float]) -> list[float]:
    rescaled_list1 = [0.5 * x for x in list1]
    rescaled_list2 = [0.5 * x + 0.5 for x in list2]
    return rescaled_list1 + rescaled_list2
