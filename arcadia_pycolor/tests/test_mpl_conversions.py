import pytest

from arcadia_pycolor import Gradient, HexCode, Palette
from arcadia_pycolor.mpl import gradient_to_linear_cmap, palette_to_cmap


def test_palette_to_cmap():
    hex_codes = [HexCode("white", "#FFFFFF"), HexCode("black", "#000000")]
    assert palette_to_cmap(Palette("my_palette", hex_codes)).colors == hex_codes


def test_palette_name():
    hex_codes = [HexCode("white", "#FFFFFF"), HexCode("black", "#000000")]
    assert (
        palette_to_cmap(
            Palette.from_dict("my_palette", {"white": "#FFFFFF", "black": "#000000"})
        ).colors
        == hex_codes
    )


@pytest.mark.parametrize(
    "values",
    [
        [0, 1],
        None,
    ],
)
def test_gradient_to_linear_cmap(values):
    grad = gradient_to_linear_cmap(
        Gradient(
            "my_gradient",
            [HexCode("white", "#FFFFFF"), HexCode("black", "#000000")],
            values,
        )
    )
    assert grad(0) == (1.0, 1.0, 1.0, 1.0)


@pytest.mark.parametrize(
    "values",
    [
        [0, 1],
        None,
    ],
)
def test_gradient_name(values):
    name = "my_gradient"
    grad = gradient_to_linear_cmap(
        Gradient(
            name,
            [HexCode("white", "#FFFFFF"), HexCode("black", "#000000")],
            values,
        )
    )
    assert grad.name == name
