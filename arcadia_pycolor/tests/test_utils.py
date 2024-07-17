import pytest

from arcadia_pycolor.utils import distribute_values


@pytest.mark.parametrize(
    "n, min_val, max_val, expected",
    [
        (1, 0.0, 1.0, [0.5]),
        (2, 0.0, 1.0, [0.0, 1.0]),
        (3, 0.0, 1.0, [0.0, 0.5, 1.0]),
        (4, 0.0, 1.0, [0.0, 0.3333333333333333, 0.6666666666666666, 1.0]),
        (5, 0.0, 1.0, [0.0, 0.25, 0.5, 0.75, 1.0]),
        (3, 0.0, 10.0, [0.0, 5.0, 10.0]),
    ],
)
def test_distribute_values(n, min_val, max_val, expected):
    assert distribute_values(n, min_val, max_val) == expected
