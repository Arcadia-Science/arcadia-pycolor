import pytest

from arcadia_pycolor import Gradient, HexCode, Palette
from arcadia_pycolor.mpl import gradient_to_linear_cmap, palette_to_cmap


@pytest.mark.parametrize(
    "name, input, hex_codes",
    [
        (
            "my_palette",
            [HexCode("white", "#FFFFFF"), HexCode("black", "#000000")],
            [HexCode("white", "#FFFFFF"), HexCode("black", "#000000")],
        )
    ],
)
def test_palette_to_cmap(name, input, hex_codes):
    assert palette_to_cmap(Palette(name, input)).colors == hex_codes


@pytest.mark.parametrize(
    "name, colors, values",
    [
        (
            "my_gradient",
            [HexCode("white", "#FFFFFF"), HexCode("black", "#000000")],
            [0, 1],
        ),
        (
            "my_gradient",
            [HexCode("white", "#FFFFFF"), HexCode("black", "#000000")],
            None,
        ),
    ],
)
def test_gradient_to_linear_cmap(name, colors, values):
    grad = gradient_to_linear_cmap(Gradient(name, colors, values))
    assert grad(0) == (1.0, 1.0, 1.0, 1.0)
