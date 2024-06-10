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
