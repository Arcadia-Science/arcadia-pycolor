import numpy as np


def distribute_values(num_points: int, min_val: float = 0.0, max_val: float = 1.0):
    if num_points <= 1:
        return [(max_val - min_val) / 2] * num_points
    return np.linspace(min_val, max_val, num_points).tolist()


def interpolate_x_values(y_values: list, round_digits=3):
    # Retrieve first and last values.
    x0, y0 = 0, y_values[0]
    x1, y1 = 1, y_values[-1]

    # Calculate the slope (m) of the line through the two points.
    m = (y1 - y0) / (x1 - x0)

    # y0 is the y-intercept of the line.
    # Find x-values corresponding to each y-value.
    x_values = [np.round((y - y0) / m, round_digits) for y in y_values]

    return x_values


# Copied from https://stackoverflow.com/questions/4983258
def is_non_decreasing(L):
    return all(x <= y for x, y in zip(L, L[1:]))


def is_non_increasing(L):
    return all(x >= y for x, y in zip(L, L[1:]))


def is_monotonic(L):
    return is_non_decreasing(L) or is_non_increasing(L)


def rescale_and_concatenate_values(list1: list[float], list2: list[float]):
    rescaled_list1 = [0.5 * x for x in list1]
    rescaled_list2 = [0.5 * x + 0.5 for x in list2]
    return rescaled_list1 + rescaled_list2
