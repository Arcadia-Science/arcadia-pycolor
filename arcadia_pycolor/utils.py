import numpy as np


def distribute_values(objects, min_val=0, max_val=1):
    n = len(objects)
    if n <= 1:
        return [(min_val - max_val) / 2] * n
    return np.linspace(min_val, max_val, n).tolist()
