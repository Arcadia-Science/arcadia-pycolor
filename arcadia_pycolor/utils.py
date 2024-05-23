import numpy as np


def distribute_values(num_points: int, min_val: float = 0.0, max_val: float = 1.0):
    if num_points <= 1:
        return [(min_val - max_val) / 2] * num_points
    return np.linspace(min_val, max_val, num_points).tolist()
